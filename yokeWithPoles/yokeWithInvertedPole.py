#!python
#!python2
import sys
sys.path.append('C:\\Python27\\Lib\\site-packages')
sys.path.append('C:\\Program Files\\Cubit 15.3\\bin')
import cubit
import numpy as np
#
#
# Reset Cubit to default settings
def cubitReset():
    cubit.init([''])
    cubit.reset()
    cubit.cmd('set geometry engine acis')
    cubit.cmd('set duplicate block elements on')
    cubit.cmd('undo off')
#
#
def intList2String(intList):
    intString = ''
    for i in intList:
        intString += '%d ' % i
    return intString
#
#
class Vector2D:
    def __init__(self):
        self._cartesian = np.empty(2)
        self._polar = np.empty(2)
    #
    ###### Hidden Utility Functions
    def _calcPolar(self):
        self._polar = np.array([np.linalg.norm(self._cartesian, 2), np.arctan2(self._cartesian[1],self._cartesian[0])])
    def _calcCartesian(self):
        self._cartesian = np.array([self._polar[0] * np.cos(self._polar[1]), self._polar[0] * np.sin(self._polar[1])])
    #
    ###### Vector operations
    @staticmethod
    def add(vector1, vector2):
        return Vector2D.cartesianMatrix(vector1._cartesian + vector2._cartesian)
    @staticmethod
    def subtract(vector1, vector2):
        return Vector2D.cartesianMatrix(vector1._cartesian - vector2._cartesian)
    @staticmethod
    def scale(vector, scaleFactor):
        return Vector2D.cartesianMatrix(vector._cartesian * scaleFactor)
    @staticmethod
    def dot(vector1, vector2):
        return np.dot(vector1._cartesian, vector2._cartesian)
    @staticmethod
    def unit(vector):
        return Vector2D.cartesianMatrix(vector._cartesian / vector.rho)
    @staticmethod
    def perpendicular(vector):
        return Vector2D.cartesianMatrix(np.array([-vector._cartesian[1], vector._cartesian[0]]))
    @staticmethod
    def findIntersection(p1, v1, p2, v2):
        v1Perp = Vector2D.perpendicular(v1)
        dp1p2 = Vector2D.subtract(p1, p2)
        num = Vector2D.dot(v1Perp, dp1p2)
        denom = Vector2D.dot(v1Perp, v2)
        return Vector2D.add(Vector2D.scale(v2, num/denom), p2)
    #
    ###### Getters, Setters, and Constructors
    @classmethod
    def xy(cls, x, y):
        vector = cls()
        vector._cartesian[0] = x
        vector._cartesian[1] = y
        vector._calcPolar()
        return vector
    @classmethod
    def cartesianMatrix(cls, matrix):
        vector = cls()
        vector._cartesian = matrix
        vector._calcPolar()
        return vector
    @classmethod
    def rhoTheta(cls, rho, theta):
        vector = cls()
        vector._polar[0] = rho
        vector._polar[1] = theta
        vector._calcCartesian()
        return vector
    @classmethod
    def polarMatrix(cls, matrix):
        vector = cls()
        vector._polar = matrix
        vector._calcCartesian()
        return vector
    @property
    def x(self):
        return self._cartesian[0]
    @property
    def y(self):
        return self._cartesian[1]
    @property
    def rho(self):
        return self._polar[0]
    @property
    def theta(self):
        return self._polar[1]
#
def manualNGon(segmentPivotVecList, segmentParallelVecList, zOffset=0.0):
    nGonVertexList = []
    for p1, v1, p2, v2 in zip(segmentPivotVecList, segmentParallelVecList, segmentPivotVecList[1:]+segmentPivotVecList[0:1], segmentParallelVecList[1:]+segmentParallelVecList[0:1]):
        nGonVec = Vector2D.findIntersection(p1, v1, p2, v2)
        nGonVertexList.append(cubit.create_vertex(nGonVec.x, nGonVec.y, zOffset))
    #
    curveList = []
    for vertex1, vertex2 in zip(nGonVertexList[-1:]+nGonVertexList[:-1], nGonVertexList):
        curveList.append(cubit.create_curve(vertex1, vertex2))
    return nGonVertexList, curveList
#
def yokeWithPipe(xRadius, yRadius, cornerRadius, thickness, zThickness, pipeLength, pipeOR, pipeIR, yokeCollarGap, collarThickness, poleLength, poleRad1, poleRad2, poleDepth, yokePipeGap, pipeCoildGap, cellsPerThickness, unvFD=''):
    rhoCycle = [xRadius, cornerRadius, yRadius, cornerRadius]
    #
    # Create outer n-gon
    segmentPivotVecList = []
    segmentParallelVecList = []
    for i in range(8):
        segmentPivotVecList.append(Vector2D.rhoTheta(rho=rhoCycle[i % (len(rhoCycle))], theta=(i/4.0)*np.pi))
        segmentParallelVecList.append(Vector2D.rhoTheta(rho=1.0, theta=((i+2.0)/4.0)*np.pi))
    outerVertexList, outerCurveList = manualNGon(segmentPivotVecList, segmentParallelVecList, zThickness/2.0)
    #
    # Creat inner n-gon
    segmentPivotVecList = []
    segmentParallelVecList = []
    for i in range(8):
        segmentPivotVecList.append(Vector2D.rhoTheta(rho=rhoCycle[i % (len(rhoCycle))] - thickness, theta=(i/4.0)*np.pi))
        segmentParallelVecList.append(Vector2D.rhoTheta(rho=1.0, theta=((i+2.0)/4.0)*np.pi))
    innerVertexList, innerCurveList = manualNGon(segmentPivotVecList, segmentParallelVecList, zThickness/2.0)
    #
    # Create curves connecting both n-gons
    connectingCurveList = []
    for outerVertex, innerVertex in zip(outerVertexList[-1:]+outerVertexList[:-1], innerVertexList[-1:]+innerVertexList[:-1]):
        connectingCurveList.append(cubit.create_curve(outerVertex, innerVertex))
    #
    # Create surfaces from curves
    surfaceIDList = []
    surfaceBodyList = []
    for i in range(len(outerVertexList)):
        surfaceBody = cubit.create_surface([outerCurveList[i], innerCurveList[i], connectingCurveList[i], connectingCurveList[(i+1) % len(connectingCurveList)]])
        surfaceIDList.append(cubit.get_last_id('surface'))
        surfaceBodyList.append(surfaceBody)
    #
    # Sweep surfaces to create yoke
    yokeBlockID = cubit.get_next_block_id()
    for surfaceID, surfaceBody in zip(surfaceIDList, surfaceBodyList):
        cubit.cmd('sweep surface %d vector 0 0 -1 distance %f' % (surfaceID, zThickness))
        cubit.cmd('block %d body %d' % (yokeBlockID, surfaceBody.id()))
    #
    # Cut hole in bottom side of yoke for pipe (no collar)
    holeRadius = pipeOR + yokePipeGap
    cutterBody = cubit.cylinder(pipeLength, holeRadius, holeRadius, holeRadius)
    cubit.cmd('rotate body %d angle 90 about x include_merged' % cutterBody.id())
    cubit.move(cutterBody, (0.0, -pipeLength/2.0, 0.0))
    cubit.subtract([cutterBody], surfaceBodyList)
    #
    # Cut hole in top side of yoke for collar
    holeRadius = pipeOR + yokeCollarGap + collarThickness + yokePipeGap
    cutterBody = cubit.cylinder(pipeLength, holeRadius, holeRadius, holeRadius)
    cubit.cmd('rotate body %d angle 90 about x include_merged' % cutterBody.id())
    cubit.move(cutterBody, (0.0, pipeLength/2.0, 0.0))
    cubit.subtract([cutterBody], surfaceBodyList)
    #
    # Create collar
    collarOR = pipeOR + yokePipeGap + collarThickness
    collarIR = pipeOR + yokePipeGap
    collarLength = thickness
    collarBody = cubit.cylinder(collarLength, collarOR, collarOR, collarOR)
    cutterBody = cubit.cylinder(collarLength, collarIR, collarIR, collarIR)
    cubit.subtract([cutterBody], [collarBody])
    cubit.cmd('rotate body %d angle 90 about x include_merged' % collarBody.id())
    cubit.move(collarBody, (0.0, yRadius-collarLength/2.0, 0.0))
    collarBlockID = cubit.get_next_block_id()
    cubit.cmd('block %d body %d' % (collarBlockID, collarBody.id()))
    #
    # poleLength, poleRad1, poleRad2,
    #
    # create poles
    ######################################################
    #
    poleBody1 = cubit.cylinder(poleLength, poleRad1, poleRad1, poleRad1)
    coneCutterBody1 = cubit.cylinder(poleDepth, collarOR, collarOR, poleRad2)
    cubit.subtract([coneCutterBody1], [poleBody1])
    whatsLeft = (poleLength - poleDepth)/2
    conCutterBody1b = cubit.cylinder(whatsLeft, poleRad2, poleRad2, poleRad2)
    cubit.move(conCutterBody1b, (0.0, 0.0, 0.5*(whatsLeft +  poleDepth)))
    cubit.subtract([conCutterBody1b], [poleBody1])
    cutterBody1 = cubit.cylinder(poleLength, collarIR, collarIR, collarIR)
    cubit.subtract([cutterBody1], [poleBody1])
    cubit.cmd('rotate body %d angle 90 about x include_merged' % poleBody1.id())
    cubit.move(poleBody1, (0.0, yRadius-thickness-poleLength/2.0, 0.0))
    poleBlockID1 = cubit.get_next_block_id()
    cubit.cmd('block %d body %d' % (poleBlockID1, poleBody1.id()))
    ######################################################
    #
    poleBody2 = cubit.cylinder(poleLength, poleRad1, poleRad1, poleRad1)
    coneCutterBody2 = cubit.cylinder(poleDepth, collarOR, collarOR, poleRad2)
    cubit.subtract([coneCutterBody2], [poleBody2])
    whatsLeft = (poleLength - poleDepth)/2
    conCutterBody2b = cubit.cylinder(whatsLeft, poleRad2, poleRad2, poleRad2)
    cubit.move(conCutterBody2b, (0.0, 0.0, 0.5*(whatsLeft +  poleDepth)))
    cubit.subtract([conCutterBody2b], [poleBody2])
    cutterBody2 = cubit.cylinder(poleLength, collarIR, collarIR, collarIR)
    cubit.subtract([cutterBody2], [poleBody2])
    cubit.cmd('rotate body %d angle 270 about x include_merged' % poleBody2.id())
    cubit.move(poleBody2, (0.0, -(yRadius-thickness-poleLength/2.0), 0.0))
    poleBlockID2 = cubit.get_next_block_id()
    cubit.cmd('block %d body %d' % (poleBlockID2, poleBody2.id()))
    #
    # Create pipe
    pipeBody = cubit.cylinder(pipeLength, pipeOR, pipeOR, pipeOR)
    pipeBoreBody = cubit.cylinder(pipeLength, pipeIR, pipeIR, pipeIR)
    cubit.subtract([pipeBoreBody], [pipeBody])
    cubit.cmd('rotate body %d angle 90 about x include_merged' % pipeBody.id())
    pipeBlockID = cubit.get_next_block_id()
    cubit.cmd('block %d body %d' % (pipeBlockID, pipeBody.id()))
    #
    # Cut yoke, collar, and pipe along planes to help meshing
    cubit.cmd('webcut volume all in block %d %d %d %d %d with plane xplane offset %f noimprint nomerge' % (yokeBlockID, pipeBlockID, collarBlockID, poleBlockID1, poleBlockID2, 0.0))
    cubit.cmd('webcut volume all in block %d %d %d %d %d with plane zplane offset %f noimprint nomerge' % (yokeBlockID, pipeBlockID, collarBlockID, poleBlockID1, poleBlockID2, 0.0))
    cubit.cmd('webcut volume all in block %d with plane xplane offset %f noimprint nomerge' % (yokeBlockID, pipeCoilGap))
    cubit.cmd('webcut volume all in block %d with plane xplane offset %f noimprint nomerge' % (yokeBlockID, -pipeCoilGap))
    #
    # Mesh yoke
    meshSize = thickness/cellsPerThickness
    cubit.cmd('imprint volume all in block %d %d %d %d %d' % (yokeBlockID, pipeBlockID, collarBlockID, poleBlockID1, poleBlockID2))
    cubit.cmd('merge volume all in block %d %d %d %d %d' % (yokeBlockID, pipeBlockID, collarBlockID, poleBlockID1, poleBlockID2))
    cubit.cmd('volume in block %d %d %d %d %d size %f' % (yokeBlockID, pipeBlockID, collarBlockID, poleBlockID1, poleBlockID2, meshSize))
    cubit.cmd('volume all in block %d %d %d %d %d scheme auto' % (yokeBlockID, pipeBlockID, collarBlockID, poleBlockID1, poleBlockID2))
    cubit.cmd('mesh volume all in block %d %d ' % (poleBlockID1, poleBlockID2))
    cubit.cmd('mesh volume all in block %d %d %d' % (yokeBlockID, pipeBlockID, collarBlockID))
    #
    # Export mesh
    # cubit.cmd('group "Cline2"  add Hex in volume 19 with  z_coord < 0.19134')
    # cubit.cmd('group "Cline1"  add Hex in volume 19 with  x_coord < 0.19134')
    cubit.cmd('group "%s" add volume all in block %d' % ('yoke', yokeBlockID))
    cubit.cmd('group "%s" add volume all in block %d' % ('pipeSample', pipeBlockID))
    cubit.cmd('group "%s" add volume all in block %d %d %d' % ('collar', collarBlockID, poleBlockID1, poleBlockID2))
    exportBlockID = cubit.get_next_block_id()
    cubit.cmd('block %d %s %s %s' % (exportBlockID, 'yoke', 'pipeSample', 'collar'))
    cubit.cmd('block %d element type HEX27' % exportBlockID)
    cubit.cmd('export ideas "%s" block %d overwrite' % (unvFD + 'yokeCollarPipe.unv', exportBlockID))
#
#
def coilsOctagon(xRadius, yRadius, cornerRadius, thickness, zThickness, coilSegmentIndexList, coilGap, splitCoilOffset, cellsPerThickness, unvFD, resetCubitForEachCoil=False):
    # Create inner n-gon
    segmentPivotVecList = []
    segmentParallelVecList = []
    # Right Side
    segmentPivotVecList.append(Vector2D.rhoTheta(rho=xRadius-thickness-coilGap, theta=0.0))
    segmentParallelVecList.append(Vector2D.rhoTheta(rho=1.0, theta=np.pi/2.0))
    # Top right corner
    segmentPivotVecList.append(Vector2D.rhoTheta(rho=cornerRadius-thickness-coilGap, theta=np.pi/4.0))
    segmentParallelVecList.append(Vector2D.rhoTheta(rho=1.0, theta=3.0*np.pi/4.0))
    # Top right side
    segmentPivotVecList.append(Vector2D.rhoTheta(rho=yRadius-thickness-coilGap, theta=np.pi/2.0))
    segmentParallelVecList.append(Vector2D.rhoTheta(rho=1.0, theta=np.pi))
    # Top right coil edge
    segmentPivotVecList.append(Vector2D.xy(x=splitCoilOffset, y=yRadius-thickness-coilGap))
    segmentParallelVecList.append(Vector2D.rhoTheta(rho=1.0, theta=5.0*np.pi/4.0))
    # Top left coil edge
    segmentPivotVecList.append(Vector2D.xy(x=-splitCoilOffset, y=yRadius-thickness-coilGap))
    segmentParallelVecList.append(Vector2D.rhoTheta(rho=1.0, theta=3.0*np.pi/4.0))
    # Top left side
    segmentPivotVecList.append(Vector2D.rhoTheta(rho=yRadius-thickness-coilGap, theta=np.pi/2.0))
    segmentParallelVecList.append(Vector2D.rhoTheta(rho=1.0, theta=np.pi))
    # Top Left Corner
    segmentPivotVecList.append(Vector2D.rhoTheta(rho=cornerRadius-thickness-coilGap, theta=3.0*np.pi/4.0))
    segmentParallelVecList.append(Vector2D.rhoTheta(rho=1.0, theta=5.0*np.pi/4.0))
    # Left Side
    segmentPivotVecList.append(Vector2D.rhoTheta(rho=xRadius-thickness-coilGap, theta=np.pi))
    segmentParallelVecList.append(Vector2D.rhoTheta(rho=1.0, theta=3.0*np.pi/2.0))
    # Bottom left corner
    segmentPivotVecList.append(Vector2D.rhoTheta(rho=cornerRadius-thickness-coilGap, theta=5.0*np.pi/4.0))
    segmentParallelVecList.append(Vector2D.rhoTheta(rho=1.0, theta=7.0*np.pi/4.0))
    # Bottom left side
    segmentPivotVecList.append(Vector2D.rhoTheta(rho=yRadius-thickness-coilGap, theta=3.0*np.pi/2.0))
    segmentParallelVecList.append(Vector2D.rhoTheta(rho=1.0, theta=0.0))
    # Bottom left coil edge
    segmentPivotVecList.append(Vector2D.xy(x=-splitCoilOffset, y=-yRadius+thickness+coilGap))
    segmentParallelVecList.append(Vector2D.rhoTheta(rho=1.0, theta=np.pi/4.0))
    # Bottom right coil edge
    segmentPivotVecList.append(Vector2D.xy(x=splitCoilOffset, y=-yRadius+thickness+coilGap))
    segmentParallelVecList.append(Vector2D.rhoTheta(rho=1.0, theta=7.0*np.pi/4.0))
    # Bottom right side
    segmentPivotVecList.append(Vector2D.rhoTheta(rho=yRadius-thickness-coilGap, theta=3.0*np.pi/2.0))
    segmentParallelVecList.append(Vector2D.rhoTheta(rho=1.0, theta=0.0))
    # Bottom right corner
    segmentPivotVecList.append(Vector2D.rhoTheta(rho=cornerRadius-thickness-coilGap, theta=7.0*np.pi/4.0))
    segmentParallelVecList.append(Vector2D.rhoTheta(rho=1.0, theta=np.pi/4.0))
    _, curveList = manualNGon(segmentPivotVecList, segmentParallelVecList, zThickness/2.0 + coilGap)
    #
    meshSize = (thickness+2.0*coilGap)/cellsPerThickness
    for coilSegmentIndex in coilSegmentIndexList:
        if resetCubitForEachCoil is True:
            cubitReset()
            _, curveList = manualNGon(segmentPivotVecList, segmentParallelVecList, zThickness/2.0 + coilGap)
        #
        coilBodyList = []
        coilBlockID = cubit.get_next_block_id()
        normVector = Vector2D.unit(Vector2D.scale(Vector2D.perpendicular(segmentParallelVecList[coilSegmentIndex]), -1.0))
        # Create top surfaces of coils
        cubit.cmd('sweep curve %d vector %f %f %f distance %f' % (curveList[coilSegmentIndex].id(), normVector.x, normVector.y, 0.0, thickness+2.0*coilGap))
        coilBodyList.append(cubit.body(cubit.get_owning_body('surface', cubit.get_last_id('surface'))))
        cubit.cmd('block %d body %d' % (coilBlockID, coilBodyList[-1].id()))
        # Create bottom surfaces of coils
        coilBodyList.append(cubit.copy_body(coilBodyList[-1]))
        cubit.move(coilBodyList[-1], (0.0, 0.0, -zThickness-2.0*coilGap))
        cubit.cmd('block %d body %d' % (coilBlockID, coilBodyList[-1].id()))
        # Create inside surfaces of coils
        cubit.cmd('sweep curve %d vector %f %f %f distance %f' % (curveList[coilSegmentIndex].id(), 0.0, 0.0, -1.0, zThickness+2.0*coilGap))
        coilBodyList.append(cubit.body(cubit.get_owning_body('surface', cubit.get_last_id('surface'))))
        cubit.cmd('block %d body %d' % (coilBlockID, coilBodyList[-1].id()))
        # Create outside surfaces of coils
        coilBodyList.append(cubit.copy_body(coilBodyList[-1]))
        cubit.move(coilBodyList[-1], (normVector.x*(thickness+2.0*coilGap), normVector.y*(thickness+2.0*coilGap), 0.0))
        cubit.cmd('block %d body %d' % (coilBlockID, coilBodyList[-1].id()))
        # Create top current terminal
        cubit.cmd('sweep curve %d vector %f %f %f distance %f' % (curveList[coilSegmentIndex].id(), normVector.x, normVector.y, 0.0, meshSize))
        topCurrentTerminalBody = cubit.body(cubit.get_owning_body('surface', cubit.get_last_id('surface')))
        cubit.cmd('block %d body %d' % (coilBlockID, topCurrentTerminalBody.id()))
        # Create inside current terminal
        cubit.cmd('sweep curve %d vector %f %f %f distance %f' % (curveList[coilSegmentIndex].id(), 0.0, 0.0, -1.0, meshSize))
        insideCurrentTerminalBody = cubit.body(cubit.get_owning_body('surface', cubit.get_last_id('surface')))
        cubit.cmd('block %d body %d' % (coilBlockID, insideCurrentTerminalBody.id()))
        #
        # Mesh coil
        cubit.cmd('imprint volume all in block %d' % coilBlockID)
        cubit.cmd('merge volume all in block %d' % coilBlockID)
        cubit.cmd('volume in block %d size %f' % (coilBlockID, meshSize))
        cubit.cmd('volume all in block %d scheme auto' % coilBlockID)
        surfaceIDList = []
        for coilBody in coilBodyList:
            surfaceIDList += cubit.get_relatives('body', coilBody.id(), 'surface')
        cubit.cmd('mesh surface %s' % intList2String(surfaceIDList))
        #
        # Create coil and current terminal groups
        coilNameBase = 'coil%d' % coilSegmentIndex
        cubit.cmd('group "%s" add surface %s' % (coilNameBase+'coil', intList2String(surfaceIDList)))
        cubit.cmd('group "%s" add surface %s' % (coilNameBase+'topTerminal', intList2String(cubit.get_relatives('body', topCurrentTerminalBody.id(), 'surface'))))
        cubit.cmd('group "%s" add surface %s' % (coilNameBase+'insideTerminal', intList2String(cubit.get_relatives('body', insideCurrentTerminalBody.id(), 'surface'))))
        #
        # Export mesh
        exportBlockID = cubit.get_next_block_id()
        cubit.cmd('block %d %s %s %s' % (exportBlockID, coilNameBase+'coil', coilNameBase+'topTerminal', coilNameBase+'insideTerminal'))
        cubit.cmd('export ideas "%s" block %d overwrite' % (unvFD + coilNameBase +'.unv', exportBlockID))
#
cubitReset()
#
xRadius = 7.875
yRadius = 4.0
cornerRadius = 7.875
thickness = 1.0
zThickness = 1.5
pipeLength = 10.0
pipeOR = 0.5
pipeIR = 0.4375
yokeCollarGap = 0.0
collarThickness = 0.0625
poleLength = 1.5
poleRad1 = 0.75
poleRad2 =0.725
poleDepth = 0.5
yokePipeGap = 0.001
coilGap = 0.1
pipeCoilGap = 1.25
resetCubitForEachCoil = False
#
# if len(sys.argv) > 1:
#     print(sys.argv[1:])
#     for command in sys.argv[1:]:
#         exec(command)
#
yokeWithPipe(xRadius, yRadius, cornerRadius, thickness, zThickness, pipeLength, pipeOR, pipeIR, yokeCollarGap, collarThickness, poleLength, poleRad1, poleRad2, poleDepth, yokePipeGap, pipeCoilGap, cellsPerThickness=5, unvFD='')
# coilsOctagon(xRadius, yRadius, cornerRadius, thickness, zThickness, [0,1,2,5,6,7,8,9,12,13], coilGap, splitCoilOffset=pipeCoilGap+pipeOR, cellsPerThickness=5, unvFD='', resetCubitForEachCoil=resetCubitForEachCoil)
#














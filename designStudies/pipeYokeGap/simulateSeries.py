#!python3

from magLabUtilities.parametrictestutilities.parameterspace import Parameter
from magLabUtilities.parametrictestutilities.testmanager import TestGroup, TestCase
from magLabUtilities.cubitutilities.cubitmanager import GeometryGenerator
from magLabUtilities.magstromutilities.magstrommanager import LinearMagstromSimulation

if __name__ == '__main__':
    # Initialize test group
    testGroup = TestGroup()

    # Add parameters to be varied
    testGroup.addParameter(Parameter('yokeCollarGap', [0.00, 0.01]))
    testGroup.addParameter(Parameter('collarThickness', [0.00, 0.121]))
    testGroup.addParameter(Parameter('yokePipeGap', [0.00, 0.005]))
    testGroup.addParameter(Parameter('yokeMur', [160.0]))
    testGroup.addParameter(Parameter('collarMur', [160.0]))
    testGroup.addParameter(Parameter('pipeMur', [68.0]))

    # Supply functions to be evaluated for each test case (each function is evaluated in the order they are supplied here)
    testGroup.addProcessFunction(TestCase.createCaseFD, ['yokeCollarGap', 'collarThickness', 'yokePipeGap'], {'testCaseRootFD':'./simulations/'})
    testGroup.addProcessFunction(GeometryGenerator.fromTestCase, ['yokeCollarGap', 'collarThickness', 'yokePipeGap'], {'scriptFP':'./yokeWithCollar.py'})
    testGroup.addProcessFunction(LinearMagstromSimulation.fromTestCase, ['yokeMur', 'collarMur', 'pipeMur'], {'inputFileTemplateFP':'./inputYoke.txt', 'replacementDict':{'__magstromMaxThreads__':'12'}})
    testGroup.addProcessFunction(LinearMagstromSimulation.runFromTestCase, [], {'magstromExeFP':r'C:\Users\travemar\ONR\magstrom\magstrom_application\x64\Release\magstrom_application.exe'})

    # Execute process functions for each test case
    testGroup.execute()
#!python3

from magLabUtilities.parameterspaceutilities.parameterspace import Parameter
from magLabUtilities.magstromutilities.testcaseutilities import MagstromTestGroup

if __name__ == '__main__':
    testGroup = MagstromTestGroup('', 'D:/BitBucket/yokedesign/testRuns/041621/')
    testGroup.addParameter(Parameter('thickness', [1.0, 1.5]))
    testGroup.addParameter(Parameter('zThickness', [1.5, 2.0]))
    testGroup.addParameter(Parameter('cornerRadius', [6.0, 7.0, 8.0]))
    testGroup.generateTestCases()
    testGroup.createTestCaseDirectories()
    
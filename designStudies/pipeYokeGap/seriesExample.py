#!python3

from magLabUtilities.parametrictestutilities.parameterspace import Parameter
from magLabUtilities.parametrictestutilities.testmanager import TestGroup, TestCase

if __name__ == '__main__':
    # Initialize test group
    testGroup = TestGroup()

    # Add parameters to be varied
    testGroup.addParameter(Parameter('thickness', [1.0, 1.5]))
    testGroup.addParameter(Parameter('zThickness', [1.5, 2.0]))
    testGroup.addParameter(Parameter('cornerRadius', [6.0, 7.0, 8.0]))
    testGroup.addParameter(Parameter('yokeMur', [200.0, 400.0]))

    # Supply functions to be evaluated for each test case (each function is evaluated in the order they are supplied here)
    testGroup.addProcessFunction(TestCase.createCaseFD, ['thickness', 'zThickness', 'cornerRadius', 'yokeMur'], {'testCaseRootFD':'./testRuns/052121/'})
    
    # Execute all functions for each test case
    testGroup.execute()
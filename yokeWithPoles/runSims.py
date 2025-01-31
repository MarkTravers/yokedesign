#!python3

from typing import List, Tuple

import subprocess
from multiprocessing import Pool

def execute(magstromInputFN:str) -> None:
    subprocess.run(['C:/Users/travemar/ONR/magstrom/magstrom_application/x64/Release/magstrom_application.exe', magstromInputFN])

if __name__ == '__main__':
    murList = [2, 101, 1001, 10001]

    # magstromExeFP = 'C:/Users/travemar/ONR/magstrom/magstrom_application/x64/Release/magstrom_application.exe'
    magstromInputTemplateFN = 'magstromInput_template.txt'

    cueArgsList:List[str] = []

    for mur in murList:
        with open(magstromInputTemplateFN, 'rt') as inputTemplate:
            inputStr:str = inputTemplate.read()

        inputStr = inputStr.replace('_pipe_mur_jobname', f'mur{mur:05d}')
        inputStr = inputStr.replace('_pipe_mur', f'{mur:.1f}')

        magstromInputCaseFN:str = f'magstromInput_mur{mur:05d}.txt'

        with open(magstromInputCaseFN, 'tw') as inputCase:
            inputCase.write(inputStr)

        cueArgsList.append(f'./{magstromInputCaseFN}')

    with Pool(processes=len(murList)) as simWorkerPool:
        simWorkerPool.map(execute, cueArgsList)

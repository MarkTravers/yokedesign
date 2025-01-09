#!python
#reset
import sys
import os
import shutil
import glob
import re
from array import *

##################################################################
def main():

    

    
    Xai = array('d',[2, 100, 1000, 10000])

    magsExe = 'magstrom_application.exe'

    for index in range(len(Xai)):
        inputfile = 'input_' + str(index) + '.txt'
        shelcom = magsExe + ' ' + inputfile
        #print shelcom
        os.system(shelcom)

            

main()

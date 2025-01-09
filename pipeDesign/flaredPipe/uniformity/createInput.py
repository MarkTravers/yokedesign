#!python
#reset
import sys
import string

from array import *



Xai = array('d',[2, 100, 1000, 10000])


infilename = 'input.txt'

index = 0
for index in range(len(Xai)):
    infile = open(infilename,'r')
    file_contents = infile.read()
    infile.close()
    mu = Xai[index]+1
    newinfile = 'input_' + str(index) + '.txt'
    jobname = 'pipe_' + str(index)
    mu_val = ' ' + str(mu)
    f1 = file_contents.replace('_jobname',jobname)
    f2 = f1.replace('_mur',mu_val)
    outfile = open(newinfile,'w')
    outfile.write(f2)
    outfile.close()

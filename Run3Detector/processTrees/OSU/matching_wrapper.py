#!/usr/bin/python3

import sys
import os
import shutil
import glob

def getRun():
    fin = open(sys.argv[3], 'r')
    info = fin.readlines()
    runNum = int(info[int(sys.argv[1])])
    return runNum

def initialize():
    print("Running on compute node: {}".format(os.uname()[1]))

    if not len(sys.argv) > 3:
        print("Need to provide run number, data directory, and matching list, exiting")
        sys.exit(1)

    if not os.path.exists(sys.argv[2]):
        print("Data directory {0} does not exist, exiting".format(sys.argv[2]))
        sys.exit(1)
    
    #output directory should be the same as data directory
    '''if not os.path.exists(sys.argv[2]):
        try:
            os.mkdir(sys.argv[2])
        except:
            print("Output directory {0} does not exist and couldn't create it, exiting".format(sys.argv[2]))
            sys.exit(1)
    '''
    
    if not os.path.exists(os.getcwd() + '/MilliDAQ/'):
        os.system('tar -xzf MilliDAQ.tar.gz')
    shutil.copy(sys.argv[3], os.getcwd()+'/MilliDAQ/')
    os.chdir(os.getcwd()+'/MilliDAQ/')

    cmd = 'singularity exec ../offline.sif ./compileAddTriggerNumber.sh'
    os.system(cmd)

def runCombine(runNum):

    cmd = 'singularity exec -B /store/ ../offline.sif python3 test/runCombineFiles.py -r {0} -d {1} --standalone'.format(runNum, sys.argv[2])
    os.system(cmd)

def postJob():

    for file in glob.glob('MatchedEvents*.root'):
        shutil.copy(file, sys.argv[2])

if __name__ == "__main__":

    initialize()
    runNum = getRun()
    runCombine(runNum)
    postJob()

    

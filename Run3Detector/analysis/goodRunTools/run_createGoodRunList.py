import pickle
import os,re
import sys
import time
from decimal import Decimal
import glob
import subprocess
import numpy as np
import datetime
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--runDir', type=str, help='Primary directory to be processed')
    parser.add_argument('-s', '--subDir', type=str, help='Subdirectory to be processed')
    parser.add_argument('-a', '--all', action='store_true', help='Option to run over all directories and sub directories')
    parser.add_argument('-f', '--reprocess', action='store_true', help='Reprocess all files')
    args = parser.parse_args()
    return args

def singleRun(mainDir, subDir, logDir):

    condorFile = 'goodRunCondorSingle.sub'

    f = open(condorFile, 'w')
    submitLines = """
    Universe = vanilla
    +IsLocalJob = true
    +IsSmallJob = true
    Rank = TARGET.IsLocalSlot
    request_disk = 5000MB
    request_memory = 125MB
    request_cpus = 1
    executable              = goodRun_wrapper.sh
    arguments               = $(PROCESS) {0} {1} {2}
    log                     = {2}log_$(PROCESS).log
    output                  = {2}out_$(PROCESS).txt
    error                   = {2}error_$(PROCESS).txt
    should_transfer_files   = Yes
    when_to_transfer_output = ON_EXIT
    transfer_input_files = goodRun_wrapper.sh, checkMatching.py
    getenv = true
    queue 1
    """.format(mainDir,subDir,logDir)

    f.write(submitLines)
    f.close()

    os.system('condor_submit {}'.format(condorFile))

def allRuns():

    size = getDirectories()

    condorFile = 'goodRunCondorAll.sub'

    f = open(condorFile, 'w')
    submitLines = """
    Universe = vanilla
    +IsLocalJob = true
    +IsSmallJob = true
    Rank = TARGET.IsLocalSlot
    request_disk = 5000MB
    request_memory = 125MB
    request_cpus = 1
    executable              = goodRun_wrapper.sh
    arguments               = $(PROCESS) {1}
    log                     = {1}log_$(PROCESS).log
    output                  = {1}out_$(PROCESS).txt
    error                   = {1}error_$(PROCESS).txt
    should_transfer_files   = Yes
    when_to_transfer_output = ON_EXIT
    transfer_input_files = goodRun_wrapper.sh, checkMatching.py, directoryList.txt
    getenv = true
    queue {0}
    """.format(size, logDir)

    f.write(submitLines)
    f.close()

    os.system('condor_submit {}'.format(condorFile))


def getDirectories(dataDir='/store/user/milliqan/run3/bar/'):

    directories = []

    for d in os.listdir(dataDir):
        item_path = os.path.join(dataDir, d)
        if not os.path.isdir(item_path): continue
        for s in os.listdir(item_path):
            if os.path.isdir(os.path.join(item_path, s)): directories.append([d, s])

    print(directories)

    np.savetxt('directoryList.txt', np.array(directories), fmt='%s')

    return len(directories)
if __name__=="__main__":

    args = parse_args()

    d = datetime.datetime.now()

    force = args.reprocess

    mainDir = '1400'
    subDir = '0000'

    if args.runDir: mainDir = args.runDir
    if args.subDir: subDir = args.subDir

    logDir = '/data/users/mcarrigan/log/goodRunLists/' + d.strftime('%m_%d_%H')

    condorFile = 'goodRunCondor.sub'

    if(not os.path.isdir(logDir)): os.mkdir(logDir)
    else:
        index = 2
        newLogDir = logDir + '_v' + str(index) + '/'
        while os.path.isdir(newLogDir):
            index += 1
            newLogDir = logDir + '_v' + str(index) + '/'
        os.mkdir(newLogDir)
        logDir = newLogDir
    if not logDir.endswith('/'): logDir += '/'

    if args.runDir and args.subDir:
        singleRun(args,runDir, args.subDir, logDir)
    elif args.all:
        allRuns()
    else:
        print("Need to specify either one directory/subdirectory combination, or run on all runs")
        sys.exit(1)

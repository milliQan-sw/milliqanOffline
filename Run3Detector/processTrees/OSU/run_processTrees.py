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
    args = parser.parse_args()
    return args


if __name__=="__main__":

    args = parse_args()

    d = datetime.datetime.now()

    swVersion = '31'
    subName = 'v' + swVersion + '_firstPedestals'    
    runNum = '800'
    subRun = '0000'

    if args.runDir: runNum = args.runDir
    if args.subDir: subRun = args.subDir

    milliqanOffline = 'milliqanOffline_v' + swVersion + '.tar.gz'

    dataDir = '/store/user/milliqan/run3/{0}/{1}/'.format(runNum, subRun)
    outDir = '/store/user/milliqan/trees/' + 'v' + swVersion + '/'
    logDir = '/data/users/milliqan/log/trees/v31/logs_v{0}_{1}_{2}/'.format(swVersion, runNum, subRun)
    reprocessAllFiles = False

    if(not os.path.isdir(outDir)): os.mkdir(outDir)
    if(not os.path.isdir(logDir)): os.mkdir(logDir)

    alreadyProcessedFiles = []
    for filename in os.listdir(outDir):
        if('.root' in filename and "MilliQan" in filename):
            index1 = filename.find("_")
            index2 = filename.find(".")
            index3 = filename.find("_", index2+1)
            numRun = int(filename[index1+4:index2])
            numFile = int(filename[index2+1:index3])
            alreadyProcessedFiles.append([numRun,numFile])
    files = []
    for filename in os.listdir(dataDir):
        if('.root' in filename and "MilliQan" in filename):
            index1 = filename.find("_")
            index2 = filename.find(".")
            index3 = filename.find("_", index2+1)
            numRun = int(filename[index1+4:index2])
            numFile = int(filename[index2+1:index3])
            if(not reprocessAllFiles):
                if([numRun,numFile] in alreadyProcessedFiles): continue
            files.append([numRun, numFile]) 
    print("Going to submit {0} jobs".format(len(files)))
    print(files)
    filelist = 'filelist_{0}_{1}.txt'.format(runNum, subRun)
    np.savetxt(filelist,files)

    f = open('run.sub', 'w')
    submitLines = """
    Universe = vanilla
    +IsLocalJob = true
    Rank = TARGET.IsLocalSlot
    request_disk = 2000MB
    request_memory = 250MB
    request_cpus = 1
    executable              = wrapper.sh
    arguments               = $(PROCESS) {1} {2} {3} {5}
    log                     = {6}log_$(PROCESS).log
    output                  = {6}out_$(PROCESS).txt
    error                   = {6}error_$(PROCESS).txt
    should_transfer_files   = Yes
    when_to_transfer_output = ON_EXIT
    transfer_input_files = {2}, wrapper.sh, tree_wrapper.py, MilliDAQ.tar.gz, {4}, offline.sif, compile.sh
    getenv = true
    queue {0}
    """.format(len(files),dataDir,filelist,outDir,milliqanOffline, subName, logDir)

    f.write(submitLines)
    f.close()

    os.system('condor_submit run.sub')

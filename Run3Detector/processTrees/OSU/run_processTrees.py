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
    parser.add_argument('-a', '--all', action='store_true', help='Find all non processed files and create offline trees')
    parser.add_argument('-f', '--reprocess', action='store_true', help='Reprocess all files')
    parser.add_argument('-v', '--version', type=str, default='31', help='Set the version of offline trees')
    parser.add_argument('-S', '--single', type=str, default='-1', help='Single run to be submitted')
    args = parser.parse_args()
    return args

def singleRun():
    subName = 'v' + args.version + '_firstPedestals'

    now = datetime.datetime.now()

    milliqanOffline = 'milliqanOffline_v' + args.version + '.tar.gz'

    dataDir = '/store/user/milliqan/run3/{0}/{1}/'.format(args.runDir, args.subDir)
    outDir = '/store/user/milliqan/trees/' + 'v' + args.version + '/'
    logDir = '/data/users/milliqan/log/trees/v31/logs_v{0}_{1}_{2}-{3}/'.format(args.version, args.runDir, args.subDir, now.strftime("%m-%d"))

    if(not os.path.isdir(outDir)): os.mkdir(outDir)
    if(not os.path.isdir(logDir)): os.mkdir(logDir)

    #placeholder
    filelist = 'durp'
    files = []

    f = open('run.sub', 'w')
    submitLines = """
    Universe = vanilla
    +IsLocalJob = true
    Rank = TARGET.IsLocalSlot
    request_disk = 2000MB
    request_memory = 250MB
    request_cpus = 1
    executable              = wrapper.sh
    arguments               = $(PROCESS) {1} {2} {3} {5} {7}
    log                     = {6}log_$(PROCESS).log
    output                  = {6}out_$(PROCESS).txt
    error                   = {6}error_$(PROCESS).txt
    should_transfer_files   = Yes
    when_to_transfer_output = ON_EXIT
    transfer_input_files = wrapper.sh, tree_wrapper.py, MilliDAQ.tar.gz, {4}, offline.sif, compile.sh
    getenv = true
    priority = 15
    queue 1
    """.format(len(files),dataDir,filelist,outDir,milliqanOffline, subName, logDir, args.single)

    f.write(submitLines)
    f.close()

    os.system('condor_submit run.sub')

def runAll():
    print("Running over all directories")
    dataDir = '/store/user/milliqan/run3/'

    runDirs = []
    subDirs = ['0000', '0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009']

    for dir in os.listdir(dataDir):
        if not os.path.isdir(os.path.join(dataDir, dir)): continue
        runDirs.append(dir)

    for runDir in runDirs:
        if int(runDir) < 800: continue
        for subDir in subDirs:
            if not os.path.exists("{0}/{1}/{2}".format(dataDir, runDir, subDir)): continue
            print("Running main")
            print(runDir, subDir, args.version, args.reprocess)
            main(runDir, subDir, args.version, args.reprocess)

def main(runNum, subRun, swVersion, reprocessAllFiles=False):

    subName = 'v' + swVersion + '_firstPedestals'    
    
    now = datetime.datetime.now()

    milliqanOffline = 'milliqanOffline_v' + swVersion + '.tar.gz'

    dataDir = '/store/user/milliqan/run3/{0}/{1}/'.format(runNum, subRun)
    outDir = '/store/user/milliqan/trees/' + 'v' + swVersion + '/'
    logDir = '/data/users/milliqan/log/trees/v31/logs_v{0}_{1}_{2}-{3}/'.format(swVersion, runNum, subRun, now.strftime("%m-%d-%H-%M-%S"))

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
                if([numRun,numFile] in alreadyProcessedFiles): 
                    continue
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
    priority = 15
    queue {0}
    """.format(len(files),dataDir,filelist,outDir,milliqanOffline, subName, logDir)

    f.write(submitLines)
    f.close()

    #os.system('condor_submit run.sub')

if __name__=="__main__":

    args = parse_args()

    if args.all:
        runAll()
    elif args.single != '-1':
        singleRun()
    elif args.runDir and args.subDir:
        main(args.runDir, args.subDir, args.version, args.reprocess)

    else:
        print("Error need to provide either run and subrun or option '--all'")
        sys.exit(1)

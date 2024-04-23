import pickle
import os,re
import sys
import time
import os 
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
    parser.add_argument('-v', '--version', type=str, default='35', help='Set the version of offline trees')
    parser.add_argument('-S', '--single', type=str, default='-1', help='Single file to be submitted')
    parser.add_argument('-R', '--run', type=str, help='Single run to be submitted')
    parser.add_argument('-o', '--outputDir', type=str, help='Output directory for files')
    parser.add_argument('-l', '--logOutDir', type=str, help='Output directory for logs')
    parser.add_argument('--slab', action='store_true', help='Option to run over slab data (default is bar)')
    parser.add_argument('--formosa', action='store_true', help='Option to run over formosa data (overrides slab)')
    #parser.add_argument('--reprocess', type=str, default='missingOfflineFiles.txt', help='reprocess files in given txt file')
    args = parser.parse_args()
    return args

def singleRun():
    subName = 'v' + args.version

    runOnFORMOSA = 'true' if args.formosa else 'false'
    runOnSlabs = 'true' if args.slab and not args.formosa else 'false'

    now = datetime.datetime.now()

    milliqanOffline = 'milliqanOffline_v' + args.version + '.tar.gz'

    if args.formosa:
        dataDir = '/eos/experiment/formosa/commissioning/data/DAQ/{0}/{1}/'.format(args.runDir, args.subDir)
    else:
        if args.slab:
            dataDir = '/store/user/milliqan/run3/slab/{0}/{1}/'.format(args.runDir, args.subDir)
        else:
            dataDir = '/store/user/milliqan/run3/bar/{0}/{1}/'.format(args.runDir, args.subDir)

    if args.outputDir:
        outDir = args.outputDir
    else:
        if os.getenv("OFFLINESITE") == "eos": 
            outDir = '/eos/experiment/formosa/commissioning/data/offline/v{}/{}/{}/'.format(args.version, args.runDir,args.subDir)
        else:
            outDir = '/store/user/milliqan/trees/v{}/{}/'.format(args.version, args.runDir)
    if args.logOutDir:
        logDir = args.logOutDir
    else:
        if os.getenv("OFFLINESITE") == "eos": 
            logDir = '/afs/cern.ch/work/m/mcitron/batchOutput/log/trees/v{0}/logs_v{0}_{1}_{2}-{3}/'.format(args.version, args.runDir, args.subDir, now.strftime("%m-%d-%H-%M"))
        else:
            logDir = '/data/users/milliqan/log/trees/v{0}/logs_v{0}_{1}_{2}-{3}/'.format(args.version, args.runDir, args.subDir, now.strftime("%m-%d"))

    if(not os.path.isdir(outDir)): os.makedirs(outDir)
    if(not os.path.isdir(logDir)): os.makedirs(logDir)

    #placeholder
    filelist = 'durp'
    files = []

    print('Running on slab', args.slab and not args.formosa)
    print('Running on FORMOSA', args.formosa)

    condor_file = 'subs/run_trees.sub'

    f = open(condor_file, 'w')
    submitLines = """
    Universe = vanilla
    +IsLocalJob = true
    Rank = TARGET.IsLocalSlot
    request_disk = 2000MB
    request_memory = 500MB
    request_cpus = 1
    executable              = wrapper.sh
    arguments               = $(PROCESS) {1} {2} {3} {5} {7} {8} {9}
    log                     = {6}log_$(PROCESS).log
    output                  = {6}out_$(PROCESS).txt
    error                   = {6}error_$(PROCESS).txt
    should_transfer_files   = Yes
    when_to_transfer_output = ON_EXIT
    transfer_input_files = wrapper.sh, tree_wrapper.py, MilliDAQ.tar.gz, {4}, compile.sh
    getenv = true
    priority = 15
    queue 1
    """.format(len(files), dataDir, filelist, outDir, milliqanOffline, subName, logDir, args.single, runOnSlabs,runOnFORMOSA)
    f.write(submitLines)
    f.close()

    os.system('condor_submit subs/run_trees.sub')

def runAll():
    print("Running over all directories")
    dataDir = '/eos/experiment/formosa/commissioning/data/DAQ/'

    runDirs = []
    subDirs = ['0000', '0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009']

    for dir in os.listdir(dataDir):
        typedir = os.path.join(dataDir, dir)
        if not os.path.exists(typedir): continue
        if not os.path.isdir(typedir): continue
        for rundir in os.listdir(typedir):
            if not os.path.isdir(os.path.join(typedir, rundir)): continue
            runDirs.append(os.path.join(dir, rundir))

    for runDir in runDirs:
        for subDir in subDirs:
            if not os.path.exists("{0}/{1}/{2}".format(dataDir, runDir, subDir)): continue
            print("Running main")
            print(runDir, subDir, args.version, args.reprocess)
            main(runDir, subDir, args.version, args.reprocess)

def main(runNum, subRun, swVersion, reprocessAllFiles=False):

    subName = 'v' + swVersion
  
    runOnFORMOSA = 'true' if args.formosa else 'false'
    runOnSlabs = 'true' if args.slab and not args.formosa else 'false'
    
    now = datetime.datetime.now()

    milliqanOffline = 'milliqanOffline_v' + swVersion + '.tar.gz'
    #milliqanOffline = 'milliqanOffline_lumi.tar.gz'

    if args.formosa:
        dataDir = '/eos/experiment/formosa/commissioning/data/DAQ/{0}/{1}/'.format(args.runDir, args.subDir)
    else:
        if args.slab:
            dataDir = '/store/user/milliqan/run3/slab/{0}/{1}/'.format(runNum, subRun)
        else:
            dataDir = '/store/user/milliqan/run3/bar/{0}/{1}/'.format(runNum, subRun)

    if args.outputDir:
        outDir = args.outputDir
    else:
        if os.getenv("OFFLINESITE") == "eos": 
            outDir = '/eos/experiment/formosa/commissioning/data/offline/v{}/{}/{}/'.format(args.version, args.runDir,args.subDir)
        else:
            outDir = '/store/user/milliqan/trees/v{}/{}/'.format(swVersion, runNum)
    if os.getenv("OFFLINESITE") == "eos": 
        logDir = '/afs/cern.ch/work/m/mcitron/batchOutput/log/trees/v{0}/logs_v{0}_{1}_{2}-{3}/'.format(args.version, args.runDir, args.subDir, now.strftime("%m-%d-%H-%M"))
    else:
        logDir = '/data/users/milliqan/log/trees/v{0}/logs_v{0}_{1}_{2}-{3}/'.format(args.version, args.runDir, args.subDir, now.strftime("%m-%d"))

    if(not os.path.isdir(outDir)): os.makedirs(outDir)
    if(not os.path.isdir(logDir)): os.makedirs(logDir)

    alreadyProcessedFiles = []
    print("Looking in output dir", outDir)
    for filename in os.listdir(outDir):
        if('.root' in filename and "MilliQan" in filename):
            index1 = filename.find("_")
            index2 = filename.find(".")
            index3 = filename.find("_", index2+1)
            numRun = int(filename[index1+4:index2])
            numFile = int(filename[index2+1:index3])
            if args.run and numRun != int(args.run): continue
            alreadyProcessedFiles.append([numRun,numFile])
    
    counter = 0
    print("Already processed {0} files".format(len(alreadyProcessedFiles)))
    files = []
    print("Looking for raw files in dataDir", dataDir)
    if not os.path.exists(dataDir):
        print("No such directory: ",dataDir)
        return 
    for filename in os.listdir(dataDir):
        if('.root' in filename and "MilliQan" in filename):
            index1 = filename.find("_")
            index2 = filename.find(".")
            index3 = filename.find("_", index2+1)
            numRun = int(filename[index1+4:index2])
            numFile = int(filename[index2+1:index3])
            if args.run and numRun != int(args.run): continue
            if(not reprocessAllFiles):
                if([numRun,numFile] in alreadyProcessedFiles): 
                    counter+=1
                    continue
            files.append([numRun, numFile]) 
    print("Already processed {0} files".format(counter))
    print("Going to submit {0} jobs".format(len(files)))
    print(files)
    filelist = 'fileLists/filelist_{0}_{1}.txt'.format(runNum, subRun)
    np.savetxt(filelist,files)

    condor_file = 'subs/run_trees.sub'

    f = open(condor_file, 'w')
    submitLines = """
    Universe = vanilla
    +IsLocalJob = true
    Rank = TARGET.IsLocalSlot
    request_disk = 2000MB
    request_memory = 500MB
    request_cpus = 1
    executable              = wrapper.sh
    arguments               = $(PROCESS) {1} {2} {3} {5} {7} {8}
    log                     = {6}log_$(PROCESS).log
    output                  = {6}out_$(PROCESS).txt
    error                   = {6}error_$(PROCESS).txt
    should_transfer_files   = Yes
    when_to_transfer_output = ON_EXIT
    transfer_input_files = {2}, wrapper.sh, tree_wrapper.py, MilliDAQ.tar.gz, {4}, compile.sh
    getenv = true
    priority = 15
    queue {0}
    """.format(len(files), dataDir, filelist, outDir, milliqanOffline, subName, logDir, runOnSlabs,runOnFORMOSA)

    f.write(submitLines)
    f.close()

    os.system('condor_submit {0}'.format(condor_file))

def reprocess(reprocessList):

    runOnFORMOSA = 'true' if args.formosa else 'false'
    runOnSlabs = 'true' if args.slab and not args.formosa else 'false'

    print("Reprocessing files")
    files = []
    fin = open(reprocessList, 'r')
    for line in fin:
        line = line.split()
        files.append([line[0], line[1]])
    filelist = 'fileLists/filelist_reprocess.txt'
    np.savetxt(filelist, files)

    print('Running on slab', args.slab and not args.formosa)
    print('Running on FORMOSA', args.formosa)

    condor_file = 'subs/run_trees.sub'

    f = open(condor_file, 'w')
    submitLines = """
    Universe = vanilla
    Rank = TARGET.IsLocalSlot
    request_disk = 2000MB
    request_memory = 250MB
    request_cpus = 1
    executable              = wrapper.sh
    arguments               = $(PROCESS) {1} {2} {3} {5} {7} {8}
    log                     = {6}log_$(PROCESS).log
    output                  = {6}out_$(PROCESS).txt
    error                   = {6}error_$(PROCESS).txt
    should_transfer_files   = Yes
    when_to_transfer_output = ON_EXIT
    transfer_input_files = {2}, wrapper.sh, tree_wrapper.py, MilliDAQ.tar.gz, {4}, compile.sh
    getenv = true
    priority = 15
    queue {0}
    +JobFlavour = "longlunch"
    """.format(len(files), dataDir, filelist, outDir, milliqanOffline, subName, logDir, runOnSlabs,runOnFORMOSA)

    f.write(submitLines)
    f.close()

    os.system('condor_submit {0}'.format(condor_file)) 

if __name__=="__main__":

    args = parse_args()

    if args.all:
        runAll()
    elif args.single != '-1':
        singleRun()
    #elif args.reprocess:
    
    elif args.runDir and args.subDir:
        main(args.runDir, args.subDir, args.version, args.reprocess)

    else:
        print("Error need to provide either run and subrun or option '--all'")
        sys.exit(1)

    print('Running on slab', args.slab and not args.formosa)
    print('Running on FORMOSA', args.formosa)


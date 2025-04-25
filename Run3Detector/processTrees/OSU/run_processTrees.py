import pickle
import os,re
import sys
import time
from decimal import Decimal
import glob
import subprocess
import numpy as np
import pandas as pd
from datetime import datetime
import argparse
import json

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
    parser.add_argument('--slab', action='store_true', help='Option to run over slab data (default is bar)')
    #parser.add_argument('--reprocess', type=str, default='missingOfflineFiles.txt', help='reprocess files in given txt file')
    args = parser.parse_args()
    return args

def copyFromEOS(slab=False):
    if not slab:
        os.system('cp /eos/experiment/milliqan/Configs/mqLumis.json .')
        os.system('cp /eos/experiment/milliqan/Configs/goodRunsList.json .')
    
    #make datetimes into uint64 to be read by c++
    lumis = pd.read_json('mqLumis.json', orient = 'split', compression = 'infer')
    convert_cols = ['start', 'stop', 'fillStart', 'fillEnd', 'startStableBeam', 'endStableBeam']

    for col in convert_cols:
        lumis[col] = convertTimes(lumis[col])
    lumis.to_json('mqLumis.json', orient = 'split', compression = 'infer', index = 'true')

def convertTimes(input):
    input = input.apply(datetime_to_uint64)
    return input

def datetime_to_uint64(x):
    if isinstance(x, str):  # If x is a string
        dt = datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ')
        return np.uint64(dt.timestamp())
    elif isinstance(x, list):  # If x is a list
        timestamps = [datetime_to_uint64(item) for item in x]
        return timestamps
    return x  # Return unchanged if x is None or some other non-string value

def singleRun():

    subName = 'v' + args.version

    runOnSlabs = 'true' if args.slab else 'false'

    now = datetime.now()

    milliqanOffline = 'milliqanOffline_v' + args.version + '.tar.gz'

    ftype = 'bar'
    if args.slab: ftype = 'slab'

    if args.slab:
        dataDir = '/store/user/milliqan/run3/slab/{0}/{1}/'.format(args.runDir, args.subDir)
    else:
        dataDir = '/store/user/milliqan/run3/bar/{0}/{1}/'.format(args.runDir, args.subDir)

    if args.outputDir:
        outDir = args.outputDir
    else:
        outDir = '/store/user/milliqan/trees/v{}/{}/{}/'.format(args.version, ftype, args.runDir)
    logDir = '/data/users/milliqan/log/trees/v{0}/logs_v{0}_{1}_{2}_{3}_{4}_{5}/'.format(args.version, ftype, args.runDir, args.subDir, now.strftime("%m-%d"), args.single.replace('.', '-'))

    if(not os.path.isdir(outDir)): os.mkdir(outDir)
    if(not os.path.isdir(logDir)): os.mkdir(logDir)

    #placeholder
    filelist = 'durp'
    files = []

    print('Running on slab', args.slab)

    condor_file = 'subs/run_trees.sub'

    f = open(condor_file, 'w')
    submitLines = """
    Universe = vanilla
    +IsLocalJob = true
    +IsSmallJob = true
    Rank = TARGET.IsLocalSlot
    request_disk = 2000MB
    request_memory = 500MB
    request_cpus = 1
    requirements = machine != "compute-0-0.local" && machine != "compute-0-2.local" && machine != "compute-0-4.local" &&  machine != "compute-0-30.local"
    executable              = wrapper.sh
    arguments               = $(PROCESS) {1} {2} {3} {5} {7} {8}
    log                     = {6}log_$(PROCESS).log
    output                  = {6}out_$(PROCESS).txt
    error                   = {6}error_$(PROCESS).txt
    should_transfer_files   = Yes
    when_to_transfer_output = ON_EXIT
    transfer_input_files = wrapper.sh, tree_wrapper.py, MilliDAQ.tar.gz, {4}, mqLumis.json, goodRunsList.json, compile.sh
    getenv = true
    priority = 15
    queue 1
    """.format(len(files), dataDir, filelist, outDir, milliqanOffline, subName, logDir, args.single, runOnSlabs)

    f.write(submitLines)
    f.close()

    os.system('condor_submit subs/run_trees.sub')

def runAll():
    print("Running over all directories")
    dataDir = '/store/user/milliqan/run3/'

    runDirs = []
    subDirs = ['0000', '0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009']

    for dir in os.listdir(dataDir):
        typedir = os.path.join(dataDir, dir)
        if not os.path.isdir(typedir): continue
        for rundir in os.listdir(typedir):
            if not os.path.isdir(os.path.join(typedir, rundir)): continue
            runDirs.append(os.path.join(dir, rundir))

    for runDir in runDirs:
        if int(runDir) < 800: continue
        for subDir in subDirs:
            if not os.path.exists("{0}/{1}/{2}".format(dataDir, runDir, subDir)): continue
            print("Running main")
            print(runDir, subDir, args.version, args.reprocess)
            main(runDir, subDir, args.version, args.reprocess)

def main(runNum, subRun, swVersion, reprocessAllFiles=False):

    subName = 'v' + swVersion
  
    runOnSlabs = 'true' if args.slab else 'false'
    
    now = datetime.now()

    milliqanOffline = 'milliqanOffline_v' + swVersion + '.tar.gz'
    #milliqanOffline = 'milliqanOffline_lumi.tar.gz'

    ftype = 'bar'
    if args.slab: ftype = 'slab'

    if args.slab:
        dataDir = '/store/user/milliqan/run3/slab/{0}/{1}/'.format(runNum, subRun)
    else:
        dataDir = '/store/user/milliqan/run3/bar/{0}/{1}/'.format(runNum, subRun)

    if args.outputDir:
        outDir = args.outputDir
    else:
        outDir = '/store/user/milliqan/trees/v{}/{}/{}/'.format(swVersion, ftype, runNum)
    logDir = '/data/users/milliqan/log/trees/v{0}/logs_v{0}_{1}_{2}_{3}-{4}/'.format(swVersion, ftype, runNum, subRun, now.strftime("%m-%d-%H-%M-%S"))

    if(not os.path.isdir(outDir)): os.mkdir(outDir)
    if(not os.path.isdir(logDir)): os.mkdir(logDir)

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
    njobs = 0
    print("Already processed {0} files".format(len(alreadyProcessedFiles)))
    files = {}
    print("Looking for raw files in dataDir", dataDir)
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
            print("filename", filename)
            if numRun in files.keys():
                files[numRun].append([numRun, numFile])
            else:
                files[numRun] = [[numRun, numFile]]

    print("Already processed {0} files".format(counter))
    print("Going to submit {0} jobs".format(len(files)))
    print(files)
    filelist = 'fileLists/filelist_{0}_{1}.json'.format(runNum, subRun)
    with open(filelist, 'w') as fout:
        json.dump(files, fout)
    #np.savetxt(filelist,files)

    condor_file = 'subs/run_trees.sub'

    f = open(condor_file, 'w')
    submitLines = """
    Universe = vanilla
    +IsLocalJob = true
    Rank = TARGET.IsLocalSlot
    request_disk = 2000MB
    request_memory = 500MB
    request_cpus = 1
    requirements = machine != "compute-0-0.local" && machine != "compute-0-2.local" && machine != "compute-0-4.local" &&  machine != "compute-0-30.local"
    executable              = wrapper.sh
    arguments               = $(PROCESS) {1} {2} {3} {5} {7}
    log                     = {6}log_$(PROCESS).log
    output                  = {6}out_$(PROCESS).txt
    error                   = {6}error_$(PROCESS).txt
    should_transfer_files   = Yes
    when_to_transfer_output = ON_EXIT
    transfer_input_files = {2}, wrapper.sh, tree_wrapper.py, MilliDAQ.tar.gz, {4}, mqLumis.json, goodRunsList.json, compile.sh
    getenv = true
    priority = 15
    queue {0}
    """.format(len(files), dataDir, filelist, outDir, milliqanOffline, subName, logDir, runOnSlabs)

    f.write(submitLines)
    f.close()

    os.system('condor_submit {0}'.format(condor_file))

def reprocess(reprocessList):

    runOnSlabs = 'true' if args.slab else 'false'

    print("Reprocessing files")
    files = []
    fin = open(reprocessList, 'r')
    for line in fin:
        line = line.split()
        files.append([line[0], line[1]])
    filelist = 'fileLists/filelist_reprocess.txt'
    np.savetxt(filelist, files)

    print('Running on slab', args.slab)

    condor_file = 'subs/run_trees.sub'

    f = open(condor_file, 'w')
    submitLines = """
    Universe = vanilla
    +IsLocalJob = true
    Rank = TARGET.IsLocalSlot
    request_disk = 2000MB
    request_memory = 250MB
    request_cpus = 1
    requirements = machine != "compute-0-0.local" && machine != "compute-0-2.local" && machine != "compute-0-4.local" &&  machine != "compute-0-30.local"
    executable              = wrapper.sh
    arguments               = $(PROCESS) {1} {2} {3} {5} {7}
    log                     = {6}log_$(PROCESS).log
    output                  = {6}out_$(PROCESS).txt
    error                   = {6}error_$(PROCESS).txt
    should_transfer_files   = Yes
    when_to_transfer_output = ON_EXIT
    transfer_input_files = {2}, wrapper.sh, tree_wrapper.py, MilliDAQ.tar.gz, {4}, mqLumis.json, goodRunsList.json, compile.sh
    getenv = true
    priority = 15
    queue {0}
    """.format(len(files), dataDir, filelist, outDir, milliqanOffline, subName, logDir, runOnSlabs)

    f.write(submitLines)
    f.close()

    #os.system('condor_submit {0}'.format(condor_file)) 

if __name__=="__main__":

    args = parse_args()

    copyFromEOS()

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


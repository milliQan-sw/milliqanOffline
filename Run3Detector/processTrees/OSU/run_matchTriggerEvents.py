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
    parser.add_argument('-v', '--version', type=str, default='33', help='Set the version of offline trees')
    parser.add_argument('-S', '--single', type=str, default='-1', help='Single file to be submitted')
    parser.add_argument('-R', '--run', type=str, help='Single run to be submitted')
    parser.add_argument('-o', '--outputDir', type=str, help='Output directory for files')
    parser.add_argument('--slab', action='store_true', help='Option to run on slab data')
    parser.add_argument('--site', type=str, default='OSU', help='Site that you are running on, will be used when adding to mongoDB')
    #parser.add_argument('--reprocess', type=str, default='missingOfflineFiles.txt', help='reprocess files in given txt file')
    args = parser.parse_args()
    return args

def makeRunList(directory, force):

    runList = []
    for filename in os.listdir(directory):
        if not filename.startswith('MilliQan') or not filename.endswith('.root'): continue
        runNum = int(filename.split("Run")[1].split(".")[0])
        subNum = int(filename.split(".")[1].split("_")[0])
        matchedFile = "MatchedEvents_Run{0}.{1}_rematch.root".format(runNum, subNum)
        if not os.path.exists(directory+matchedFile) or force:
            if runNum in runList: continue
            runList.append(runNum)

    return np.array(runList)

if __name__=="__main__":

    args = parse_args()

    d = datetime.datetime.now()

    force = args.reprocess

    milliDAQ = 'MilliDAQ.tar.gz'
    site = args.site
    mainDir = '1100'
    subDir = '0007'

    if args.runDir: mainDir = args.runDir
    if args.subDir: subDir = args.subDir

    if args.slab: 
        dataDir = '/store/user/milliqan/run3/slab/{0}/{1}/'.format(mainDir, subDir)
    else:
        dataDir = '/store/user/milliqan/run3/bar/{0}/{1}/'.format(mainDir, subDir)

    logDir = '/data/users/milliqan/log/triggerMatching/' + d.strftime('%m_%d_%H')

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

    runsToProcess = makeRunList(dataDir, force)
    #runsToProcess = np.array([1172])
    #print("Going to submit {0} jobs".format(len(runsToProcess)))
    print(runsToProcess)
    if not os.path.exists(os.getcwd() + '/matchLists'):
        print("Making directory {} to save match lists".format(os.getcwd() + '/matchLists'))
        os.mkdir(os.getcwd() + '/matchLists')
    filelist = '{0}/matchLists/matchlist_{1}_{2}.txt'.format(os.getcwd(), mainDir, subDir)
    print("Filelist", filelist)
    np.savetxt(filelist,runsToProcess.astype(int), fmt='%i')
    if not os.path.exists(os.getcwd() + '/subs'):
        print("Making directory {} to save condor sub files".format(os.getcwd() + '/subs'))
        os.mkdir(os.getcwd() + '/subs')
    condorFile = 'subs/run_{0}_{1}.sub'.format(mainDir, subDir)


    f = open(condorFile, 'w')
    submitLines = """
    Universe = vanilla
    +IsLocalJob = true
    Rank = TARGET.IsLocalSlot
    request_disk = 5000MB
    request_memory = 500MB
    request_cpus = 1
    requirements = machine != "compute-0-0.local" && machine != "compute-0-2.local" && machine != "compute-0-4.local" &&  machine != "compute-0-30.local"
    executable              = matching_wrapper.py
    arguments               = $(PROCESS) {1} {2} {5}
    log                     = {3}log_$(PROCESS).log
    output                  = {3}out_$(PROCESS).txt
    error                   = {3}error_$(PROCESS).txt
    should_transfer_files   = Yes
    when_to_transfer_output = ON_EXIT
    transfer_input_files = {2}, {4}, matching_wrapper.py
    getenv = true
    queue {0}
    """.format(len(runsToProcess),dataDir,filelist,logDir,milliDAQ,site)

    f.write(submitLines)
    f.close()

    os.system('condor_submit {}'.format(condorFile))

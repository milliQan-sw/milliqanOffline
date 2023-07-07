import pickle
import os,re
import sys
import time
from decimal import Decimal
import glob
import subprocess
import numpy as np
import datetime

def makeRunList(directory, force):

    runList = []
    for filename in os.listdir(directory):
        if not filename.startswith('MilliQan') or not filename.endswith('.root'): continue
        runNum = int(filename.split("Run")[1].split(".")[0])
        subNum = int(filename.split(".")[1].split("_")[0])
        matchedFile = "MatchedEvents_Run{0}.{1}.root".format(runNum, subNum)
        if not os.path.exists(directory+matchedFile) or force:
            if runNum in runList: continue
            runList.append(runNum)

    return np.array(runList)

if __name__=="__main__":

    d = datetime.datetime.now()

    force = False

    milliDAQ = 'MilliDAQ.tar.gz'

    dataDir = '/store/user/milliqan/run3/700/0000/'
    logDir = '/data/users/milliqan/log/triggerMatching/' + d.strftime('%m_%d_%H/')

    if(not os.path.isdir(logDir)): os.mkdir(logDir)

    runsToProcess = makeRunList(dataDir, force)
    #runsToProcess = np.array([700])
    print("Going to submit {0} jobs".format(len(runsToProcess)))
    print(runsToProcess)
    filelist = 'matchlist.txt'
    np.savetxt(filelist,runsToProcess.astype(int), fmt='%i')

    f = open('run.sub', 'w')
    submitLines = """
    Universe = vanilla
    +IsLocalJob = true
    Rank = TARGET.IsLocalSlot
    request_disk = 500MB
    request_memory = 125MB
    request_cpus = 1
    executable              = matching_wrapper.py
    arguments               = $(PROCESS) {1} {1}
    log                     = {3}log_$(PROCESS).log
    output                  = {3}out_$(PROCESS).txt
    error                   = {3}error_$(PROCESS).txt
    should_transfer_files   = Yes
    when_to_transfer_output = ON_EXIT
    transfer_input_files = {2}, {4}, offline.sif, matching_wrapper.py
    getenv = true
    queue {0}
    """.format(len(runsToProcess),dataDir,filelist,logDir,milliDAQ)

    f.write(submitLines)
    f.close()

    os.system('condor_submit run.sub')

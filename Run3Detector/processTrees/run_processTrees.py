import pickle
import os,re
import sys
import time
from decimal import Decimal
import glob
import subprocess
import numpy as np

if __name__=="__main__":

    dataDir = '/store/user/milliqan/run3/'
    #dataDir = '/store/user/mcarrigan/milliqan/test/'
    #outDir = '/store/user/mcarrigan/milliqan/run3/trees/'
    outDir = '/store/user/mcarrigan/trees/'
    logDir = '/data/users/mcarrigan/log/trees/'
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
            #if "Run592" not in filename: continue
            index1 = filename.find("_")
            index2 = filename.find(".")
            index3 = filename.find("_", index2+1)
            numRun = int(filename[index1+4:index2])
            numFile = int(filename[index2+1:index3])
            if(not reprocessAllFiles):
                if([numRun,numFile] in alreadyProcessedFiles): continue
            files.append([numRun, numFile]) 
    filelist = 'filelist.txt'
    np.savetxt(filelist,files)

    f = open('run.sub', 'w')
    submitLines = """
    Universe = vanilla
    +IsLocalJob = true
    Rank = TARGET.IsLocalSlot
    request_disk = 500MB
    request_memory = 1024MB
    request_cpus = 1
    executable              = wrapper.sh
    arguments               = $(PROCESS) {1} {2} {3}
    log                     = {4}log_$(PROCESS).log
    output                  = {4}out_$(PROCESS).txt
    error                   = {4}error_$(PROCESS).txt
    should_transfer_files   = Yes
    when_to_transfer_output = ON_EXIT
    transfer_input_files = {2}, wrapper.sh, tree_wrapper.py, MilliDAQ.tar.gz, milliqanOffline.tar.gz, offline.sif, compile.sh
    getenv = true
    queue {0}
    """.format(len(files),dataDir,filelist,outDir,logDir)

    f.write(submitLines)
    f.close()

    os.system('condor_submit run.sub')

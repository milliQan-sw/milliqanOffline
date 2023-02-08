import pickle
import os,re
import sys
import time
from decimal import Decimal
import glob
import subprocess
import numpy as np
import datetime

if __name__=="__main__":

    d = datetime.datetime.now()

    swVersion = '29'
    subName = 'v' + swVersion + '_firstPedestals'    

    milliqanOffline = 'milliqanOffline_v' + swVersion + '.tar.gz'

    dataDir = '/store/user/milliqan/run3/500/'
    outDir = '/store/user/mcarrigan/trees/' + 'v' + swVersion + '/'
    logDir = d.strftime('/data/users/mcarrigan/log/trees/%m_%d_%H/')
    reprocessAllFiles = True

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
    filelist = 'filelist.txt'
    np.savetxt(filelist,files)

    f = open('run.sub', 'w')
    submitLines = """
    Universe = vanilla
    +IsLocalJob = true
    Rank = TARGET.IsLocalSlot
    request_disk = 4000MB
    request_memory = 250MB
    request_cpus = 1
    executable              = wrapper.sh
    arguments               = $(PROCESS) {1} {2} {3} {6}
    log                     = {4}log_$(PROCESS).log
    output                  = {4}out_$(PROCESS).txt
    error                   = {4}error_$(PROCESS).txt
    should_transfer_files   = Yes
    when_to_transfer_output = ON_EXIT
    transfer_input_files = {2}, wrapper.sh, tree_wrapper.py, MilliDAQ.tar.gz, {5}, offline.sif, compile.sh
    getenv = true
    queue {0}
    """.format(len(files),dataDir,filelist,outDir,logDir,milliqanOffline, subName)

    f.write(submitLines)
    f.close()

    os.system('condor_submit run.sub')

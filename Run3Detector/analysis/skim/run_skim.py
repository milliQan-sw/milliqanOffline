import pickle
import os,re
import sys
import time
from decimal import Decimal
import glob
import subprocess
import numpy as np
from ROOT import TFile
import json

if __name__=="__main__":

    dataDir = '/store/user/mcarrigan/trees/v29/'
    outDir = '/store/user/mcarrigan/skim/muon/v29/'
    logDir = '/data/users/mcarrigan/log/skim/muon/v29/'
    reprocessAllFiles = True
    checkFiles = False

    if(not os.path.isdir(outDir)): os.mkdir(outDir)
    if(not os.path.isdir(logDir)): os.mkdir(logDir)

    alreadyProcessedFiles = []
    for filename in os.listdir(outDir):
        if('.root' in filename and 'MilliQan' in filename):
            numRun = filename.split('_')[1].split('.')[0].replace('Run', '')
            numFile = filename.split('_')[1].split('.')[1]
            alreadyProcessedFiles.append([numRun, numFile])
    files = []
    for filename in os.listdir(dataDir):
        if('.root' in filename and 'MilliQan_Run' in filename):
            numRun = filename.split('_')[1].split('.')[0].replace('Run', '')
            numFile = filename.split('_')[1].split('.')[1]
            if int(numRun) < 583: continue
            if(not reprocessAllFiles):
                if([numRun, numFile] in alreadyProcessedFiles): continue
            if checkFiles:
                myfile = TFile.Open(dataDir+filename)
                if myfile.IsZombie(): continue
            files.append(dataDir + filename) 
    print(files)
    filelist = 'filelist.json'
    file_dict = {'filelist':files}
    fout = open(filelist, 'w')
    json.dump(file_dict, fout)

    f = open('run.sub', 'w')
    submitLines = """
    Universe = vanilla
    +IsLocalJob = true
    Rank = TARGET.IsLocalSlot
    request_disk = 500MB
    request_memory = 2048MB
    request_cpus = 1
    executable              = skim_wrapper.sh
    arguments               = $(PROCESS) {1} {2}
    log                     = {3}log_$(PROCESS).log
    output                  = {3}out_$(PROCESS).txt
    error                   = {3}error_$(PROCESS).txt
    should_transfer_files   = Yes
    when_to_transfer_output = ON_EXIT
    transfer_input_files = {1}, skim_wrapper.sh, muonSkim.py
    getenv = true
    queue {0}
    """.format(len(files),filelist,outDir,logDir)

    f.write(submitLines)
    f.close()

    os.system('condor_submit run.sub')
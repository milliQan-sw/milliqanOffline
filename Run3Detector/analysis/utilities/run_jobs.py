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
import argparse

def checkProcessedFiles(outputDir):
    alreadyProcessedFiles = []
    for filename in os.listdir(outputDir):
        if('.root' in filename and 'MilliQan' in filename):
            numRun = filename.split('_')[1].split('.')[0].replace('Run', '')
            numFile = filename.split('_')[1].split('.')[1]
            alreadyProcessedFiles.append([numRun, numFile])
    return alreadyProcessedFiles

def getFilesToProcess(dataDir, alreadyProcessedFiles, reprocessAllFiles=False, checkFiles=False):
    files = []
    for filename in os.listdir(dataDir):
        if('.root' in filename and 'MilliQan_Run' in filename):
            numRun = filename.split('_')[1].split('.')[0].replace('Run', '')
            numFile = filename.split('_')[1].split('.')[1]
            if(not reprocessAllFiles):
                if([numRun, numFile] in alreadyProcessedFiles): continue
            if checkFiles:
                myfile = TFile.Open(dataDir+filename)
                if myfile.IsZombie(): continue
            files.append(dataDir + filename) 
    return files

def createJson(files, listName):
    filelist = listName
    file_dict = {'filelist':files}
    fout = open(filelist, 'w')
    json.dump(file_dict, fout)

def writeCondorSub(files, pythonFile, filelist, outDir, requirements):
    f = open('run.sub', 'w')
    submitLines = """
    Universe = vanilla
    +IsLocalJob = true
    Rank = TARGET.IsLocalSlot
    request_disk = {6}
    request_memory = {5}
    request_cpus = {4}
    executable              = condor_wrapper.sh
    arguments               = {1} $(PROCESS) {2} {3}
    log                     = {3}/log_$(PROCESS).log
    output                  = {3}/out_$(PROCESS).out
    error                   = {3}/error_$(PROCESS).err
    should_transfer_files   = Yes
    when_to_transfer_output = ON_EXIT
    transfer_input_files = {1}, {2}, condor_wrapper.sh
    getenv = true
    queue {0}
    """.format(len(files),pythonFile,filelist,outDir,requirements[0],requirements[1],requirements[2])

    f.write(submitLines)
    f.close()


if __name__=="__main__":

    parser=argparse.ArgumentParser()
    parser.add_argument("-i", "--inputDirectory", type=str, help="Input dataset directory", required=True)
    parser.add_argument("-o", "--outputDirectory", type=str, help="Output file directory", required=True)
    parser.add_argument("-s", "--script", type=str, help="Python script to run over", required=True)
    parser.add_argument("-r", "--reprocessAll", action='store_true', help="Reprocess all files if argument is given")
    parser.add_argument("-c", "--checkFiles", action='store_true', help="Checks that input files are valid")
    parser.add_argument("-j", "--jsonFile", type=str, default="filelist.json", help="Name of json file containing files dictionary")
    parser.add_argument("-C", "--cpu", type=str, default='1', help="Request number of cpus per job")
    parser.add_argument("-M", "--memory", type=str, default="1024MB", help="Request amount of memory per job (in MB)")
    parser.add_argument("-D", "--disk", type=str, default="500MB", help="Request amount of disk space per job (in MB)")
    parser.add_argument("-t", "--test", action='store_true', help="Runs without submitting condor job")
    parser.add_argument("-d", "--debug", action='store_true', help="Debug flag to help debugging")

    args = parser.parse_args()

    if(not os.path.isdir(args.outputDirectory)): os.mkdir(args.outputDirectory)

    alreadyProcessedFiles = checkProcessedFiles(args.outputDirectory)

    files = getFilesToProcess(args.inputDirectory, alreadyProcessedFiles, args.reprocessAll, args.checkFiles)
    if args.debug: print(files)

    createJson(files, args.jsonFile)

    if 'MB' not in args.memory: args.memory += 'MB'
    if 'MB' not in args.disk: args.disk += 'MB'
    computer_requirements = [args.cpu, args.memory, args.disk]

    writeCondorSub(files, args.script, args.jsonFile, args.outputDirectory, computer_requirements)

    if not args.test: os.system('condor_submit run.sub')

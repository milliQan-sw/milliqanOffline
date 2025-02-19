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
    parser.add_argument('-d', '--dataDir', type=str, help='Primary directory to be processed')
    parser.add_argument('-o', '--outputDir', type=str, help='Output directory for files and logs')
    parser.add_argument('--debug', action='store_true', help="Option to debug, won't submit condor job")

    args = parser.parse_args()
    return args


def createCondorFile(numFiles, dataDir, filelist, outputDir, milliqanOffline, logDir):

    if not os.path.exists('subs'):
        os.mkdir('subs')

    condor_file = 'subs/run_trees.sub'

    f = open(condor_file, 'w')
    submitLines = """
    Universe = vanilla
    +IsLocalJob = true
    Rank = TARGET.IsLocalSlot
    request_disk = 10000MB
    request_memory = 5000MB
    request_cpus = 1
    requirements = machine != "compute-0-0.local" && machine != "compute-0-2.local" && machine != "compute-0-4.local" &&  machine != "compute-0-30.local"
    executable              = pulseInjectionWrapper.sh
    arguments               = $(PROCESS) {2} {3}
    log                     = {5}log_$(PROCESS).log
    output                  = {5}out_$(PROCESS).txt
    error                   = {5}error_$(PROCESS).txt
    should_transfer_files   = Yes
    when_to_transfer_output = ON_EXIT
    transfer_input_files = {2}, pulseInjectionWrapper.sh, processSimFiles.py, MilliDAQ.tar.gz, {4}, milliQanSim.tar.gz, 
    getenv = true
    priority = 15
    queue {0}
    """.format(numFiles, dataDir, filelist, outputDir, milliqanOffline, logDir)

    f.write(submitLines)
    f.close()

def createFileList(dataDir, jsonFile):

    fileDict = {}

    ifile = 0
    for filename in os.listdir(dataDir):
        if not filename.endswith('.root'): continue

        inputFile = '/'.join([dataDir, filename])
        outputFile = filename.replace('_sim', '')
        fileDict[ifile] = [inputFile, outputFile]

        ifile += 1

    with open(jsonFile, 'w') as json_file:
        json.dump(fileDict, json_file)

    return ifile


def main():

    filelist = 'pulseInjectionFileList.json'
    milliqanOffline = 'milliqanOffline.tar.gz'
    logDir = args.outputDir + '/logs/'

    if not os.path.exists(args.outputDir):
        os.mkdir(args.outputDir)
    if not os.path.exists(logDir):
        os.mkdir(logDir)
    if not os.path.exists(args.outputDir+'/pulseInjected'):
        os.mkdir(args.outputDir+'/pulseInjected')
    if not os.path.exists(args.outputDir+'/globalEvent'):
        os.mkdir(args.outputDir+'/globalEvent')
    if not os.path.exists(args.outputDir+'/trees'):
        os.mkdir(args.outputDir+'/trees')

    os.system(f'chmod -R a+rwx {args.outputDir}')

    numFiles = createFileList(args.dataDir, jsonFile=filelist)
    createCondorFile(numFiles, args.dataDir, filelist, args.outputDir, milliqanOffline, logDir)

    if not args.debug:
        cmd = 'condor_submit subs/run_trees.sub'
        os.system(cmd)


if __name__=="__main__":

    args = parse_args()

    if not args.dataDir:
        print("Need to provide data directory")
        sys.exit(0)
    if not args.outputDir:
        print("Need to provide output directory")
        sys.exit(0)

    main()



#!/usr/bin/python3

import sys
import os
import shutil
import glob
from datetime import datetime
import subprocess
import ROOT as r
sys.path.append(os.getcwd()+'/../../scripts/')
print("System path \n\t", sys.path)

from mongoConnect import *


def getRun():
    fin = open(sys.argv[2], 'r')
    info = fin.readlines()
    runNum = int(info[int(sys.argv[1])].split()[0])
    dataDir = str(info[int(sys.argv[1])].split()[1])
    if not dataDir.endswith('/'): dataDir += '/'
    return runNum, dataDir

def initialize():

    print("Running on compute node: {}".format(os.uname()[1]))

    if not len(sys.argv) > 3:
        print("Need to provide run number, matching list, and site exiting")
        sys.exit(1)

    if not os.path.exists(os.getcwd() + '/milliqanOffline/'):
        os.system('tar -xzf milliqanOffline*.tar.gz')
    
    if not os.path.exists(os.getcwd() + '/MilliDAQ/'):
        os.system('tar -xzf MilliDAQ.tar.gz')
    shutil.copy(sys.argv[2], os.getcwd()+'/MilliDAQ/')
    os.chdir(os.getcwd()+'/MilliDAQ/')

    cmd = 'singularity exec ../offline.sif ./compileAddTriggerNumber.sh'
    os.system(cmd)

def runCombine(runNum, dataDir):

    if not os.path.exists(dataDir):
        print("Data directory {0} does not exist, exiting".format(dataDir))
        sys.exit(1)

    cmd = 'singularity exec -B /store/,/data /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline\:x86/ python3 test/runCombineFiles.py -r {0} -d {1} --standalone'.format(runNum, dataDir)
    os.system(cmd)

def postJob():

    db = mongoConnect()

    for file in glob.glob('MatchedEvents*.root'):
        runNum = file.split('Run')[1].split('.')[0]
        fileNum = file.split('.')[1].split('_')[0]
        site = sys.argv[3]
        ctime = datetime.fromtimestamp(os.path.getctime(file))
        fin = r.TFile.Open(file)
        mytree = fin.Get('matchedTrigEvents')
        selected_entries = mytree.Draw(">>selList", "trigger>0", "entrylist")
        selected_entries = r.gDirectory.Get("selList").GetN()
        total = mytree.GetEntries()
        match_rate = selected_entries / total
        fin.Close()
        _id = '{}_{}_MatchedEvents_{}'.format(runNum, fileNum, site)
        query = {'_id' : _id}
        update = {'run' : int(runNum),
                  'file' : int(fileNum),
                  'site': site, 
                  'location' : dataDir,
                  'type' : 'MatchedEvents',
                  'time' : ctime,
                  'trigMatchFrac' : match_rate}
        db.milliQanRawDatasets.update_one(query, {'$set': update}, upsert=True)
        shutil.copy(file, dataDir)

if __name__ == "__main__":

    initialize()
    runNum, dataDir = getRun()
    runCombine(runNum, dataDir)
    postJob()

    

#!/usr/bin/python3

import sys
import os
import shutil
import glob
from datetime import datetime
#import ROOT as r
#from pymongo import MongoClient

def getRun():
    fin = open(sys.argv[3], 'r')
    info = fin.readlines()
    runNum = int(info[int(sys.argv[1])])
    return runNum

def initialize():

    print("Running on compute node: {}".format(os.uname()[1]))

    if not len(sys.argv) > 4:
        print("Need to provide run number, data directory, matching list, and site exiting")
        sys.exit(1)

    if not os.path.exists(sys.argv[2]):
        print("Data directory {0} does not exist, exiting".format(sys.argv[2]))
        sys.exit(1)
    
    if not os.path.exists(os.getcwd() + '/MilliDAQ/'):
        os.system('tar -xzf MilliDAQ.tar.gz')
    shutil.copy(sys.argv[3], os.getcwd()+'/MilliDAQ/')
    os.chdir(os.getcwd()+'/MilliDAQ/')

    cmd = 'singularity exec /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline\:x86/  ./compileAddTriggerNumber.sh'
    os.system(cmd)

def runCombine(runNum):

    cmd = 'singularity exec -B /store/ /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline\:x86/ python3 test/runCombineFiles.py -r {0} -d {1} --standalone --site {2}'.format(runNum, sys.argv[2], sys.argv[4])
    os.system(cmd)

def postJob():

    db = mongoConnect()

    for file in glob.glob('MatchedEvents*.root'):
        runNum = file.split('Run')[1].split('.')[0]
        fileNum = file.split('.')[1].split('_')[0]
        site = sys.argv[4]
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
                  'location' : sys.argv[2],
                  'type' : 'MatchedEvents',
                  'time' : ctime,
                  'trigMatchFrac' : match_rate}
        db.milliQanRawDatasets.update_one(query, {'$set': update}, upsert=True)
        shutil.copy(file, sys.argv[2])

if __name__ == "__main__":

    initialize()
    runNum = getRun()
    runCombine(runNum)
    #postJob()

    

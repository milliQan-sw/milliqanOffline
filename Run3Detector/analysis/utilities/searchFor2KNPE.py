#the goal is to locate the files that have 2k pulse npe. Base on previous study when muon hit the bar detector  pulse npe should be at least 2k.


import ROOT as r
import os 
import sys
import time
import uproot 
import awkward as ak
from array import array
import numpy as np



#filelist =['/mnt/hadoop/se/store/user/milliqan/trees/v34/MilliQan_Run1190.4_v34.root:t']


#"""
startFile = 1111
endFile = 1131

filelist = []

def appendRun(filelist,run):
    #directory = "/mnt/hadoop/se/store/user/milliqan/trees/v34/1000/"
    directory = "/mnt/hadoop/se/store/user/milliqan/trees/v34/"
    for filename in os.listdir(directory):
        if filename.startswith(f"MilliQan_Run{run}") and filename.endswith(".root"):
            filelist.append(directory+filename+":t")

cosmicGoodRun = [f"{i}" for i in range(startFile, endFile)]


for run in cosmicGoodRun:
    appendRun(filelist,run)
#"""




branches = ["runNumber","event","fileNumber",'boardsMatched', 'pickupFlag','nPE','type']

pulseBasedBranches = ['pickupFlag','nPE','type']




total_events = 0

for events in uproot.iterate(
    filelist,
    branches,
    step_size=1000,
    num_workers=8,
    ):

    total_events += len(events)

    events['boardsMatched'], junk = ak.broadcast_arrays(events.boardsMatched, events.pickupFlag)
    
    for branch in pulseBasedBranches:
        events[branch] = events[branch][events.boardsMatched]

    for branch in pulseBasedBranches:
        events[branch] = events[branch][events.pickupFlag]

    for branch in pulseBasedBranches:
        events[branch] = events[branch][events['type']==0]
    
    #print(ak.to_pandas(events))

    #get the list of pulse npe(bar)
    #pulseNPE = ak.drop_none(events.nPE)
    pulseNPE = ak.flatten(events.nPE,axis=None)
    #print(pulseNPE)
    pulseNPEarray = array('d', pulseNPE)
    #print(pulseNPEarray)
    try:
        if max(pulseNPEarray) >=2000:
            print("cosmic muon ?")
            print(max(pulseNPEarray))
            print(set(events.runNumber))
            print(set(events.fileNumber))
            #print(events.event)
    except Exception as error:
        print(error)
        print(set(events.runNumber))
        print(set(events.fileNumber))



print("Number of processed events", total_events)

    


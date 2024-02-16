"""
what is the pulse with large duration (>1000) and large height (> 1000mV)
"""


import ROOT as r
import os 
import sys
import time
import uproot 
import awkward as ak
from array import array
import numpy as np


filelist =['/mnt/hadoop/se/store/user/milliqan/trees/v34/1100/MilliQan_Run1190.4_v34.root:t']

pulseBasedBranches = ["pickupFlag","chan","layer","nPE","type","row","duration","height"]
branches = ["chan","runNumber","event","fileNumber",'boardsMatched',"pickupFlag","layer","nPE","type","row","duration","height"]

for events in uproot.iterate(
    filelist,
    branches,
    step_size=1000,
    num_workers=8,
    ):
    #total_events += len(events)
    for branch in pulseBasedBranches:
        events[branch] = events[branch][events.boardsMatched]
    for branch in pulseBasedBranches:
        events[branch] = events[branch][events.pickupFlag]

    #barCut=events['type']==0
    #for branch in pulseBasedBranches:
    #    events[branch] = events[branch][barCut]

    
    durationCuts = ak.any(events.duration >= 1000,axis=1)
    """
    print(durationCuts)
    for branch in pulseBasedBranches:
        events[branch] = events[branch][durationCuts]
    """

    heightCuts = ak.any(events.height >= 1000,axis=1)
    """
    print(heightCuts)
    for branch in pulseBasedBranches:
        events[branch] = events[branch][heightCuts]
    """
    
    print(set(ak.to_list(events.fileNumber[heightCuts & durationCuts])))
    print(set(ak.to_list(events.runNumber[heightCuts & durationCuts])))
    print(set(ak.to_list(events.event[heightCuts & durationCuts])))
    

    



    
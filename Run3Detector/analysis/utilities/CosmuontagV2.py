#use pulse area to determine nPE and then there is no need to separate bar and panel pulses

import ROOT as r
import os 
import sys
import time
import uproot 
import awkward as ak
from array import array
import numpy as np

filelist =['/mnt/hadoop/se/store/user/milliqan/trees/v34/MilliQan_Run1190.4_v34.root:t']


branches = ["runNumber","event","fileNumber",'boardsMatched',"pickupFlag","layer","type","row","chan","area"]

pulseBasedBranches = ["pickupFlag","layer","area","type","row","chan"]

NPECut = 20


for events in uproot.iterate(
    filelist,
    pulseBasedBranches,
    step_size=1000,
    num_workers=8,
    ):


    events['boardsMatched'], junk = ak.broadcast_arrays(events.boardsMatched, events.pickupFlag)
    
    for branch in pulseBasedBranches:
        events[branch] = events[branch][events.boardsMatched]

    for branch in pulseBasedBranches:
        events[branch] = events[branch][events.pickupFlag]

    
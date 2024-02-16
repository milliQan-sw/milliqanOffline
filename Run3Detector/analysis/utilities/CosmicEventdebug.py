#this file is to check the event 

import ROOT as r
import os 
import sys
import time
import uproot 
import awkward as ak
from array import array
import numpy as np


def EventCheck(RunNum,filenum,eventNum):

    pulseBasedBranches = ["pickupFlag","layer","nPE","type","area","chan"]
    branches = ["runNumber","event","fileNumber",'boardsMatched',"pickupFlag","layer","nPE","type","area","chan","row"]
    filelist =[f'/mnt/hadoop/se/store/user/milliqan/trees/v34/MilliQan_Run{RunNum}.{filenum}_v34.root:t']
    
    for events in uproot.iterate(
                filelist,
                branches,
                step_size=1000,
                num_workers=8,
                ):
                """
                for branch in pulseBasedBranches:
                    events[branch] = events[branch][events.boardsMatched]
                for branch in pulseBasedBranches:
                    events[branch] = events[branch][events.pickupFlag]
                """
                #extract the intersting events
                events =  events[events.event == eventNum]
                
                print(ak.to_pandas(events))
if __name__ == "__main__":

    EventCheck(1190,4,47)

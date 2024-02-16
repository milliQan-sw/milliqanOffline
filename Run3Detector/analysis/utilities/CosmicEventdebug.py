#this file is to check the event 

import ROOT as r
import os 
import sys
import time
import uproot 
import awkward as ak
from array import array
import numpy as np


def EventCheck(RunNum=1190,filenum=4,eventNum=47):

    pulseBasedBranches = ["pickupFlag","layer","nPE","type","area","chan","row"]
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
                print("before doing the cut")
                print(ak.to_pandas(events))
                NPECut = events.nPE >= 20
                print(NPECut)
                for branch in pulseBasedBranches:
                    print(f"doing {branch} cut")
                    events[branch] = events[branch][NPECut]
                    
                    print(ak.to_pandas(events))
if __name__ == "__main__":

    EventCheck(1190,4,2)

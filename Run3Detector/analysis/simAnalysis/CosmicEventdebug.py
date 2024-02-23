#this file is to check the event 

import ROOT as r
import os 
import sys
import time
import uproot 
import awkward as ak
from array import array
import numpy as np


def EventCheck(RunNum=1190,eventNum=47):

    branches = ['pmt_nPE','pmt_layer','pmt_chan','pmt_time','pmt_type','event','runNumber']

    filelist =[f'/mnt/hadoop/se/store/user/czheng/SimFlattree/withPhoton/output_{RunNum}.root:t']
    
    for events in uproot.iterate(
                filelist,
                branches,
                step_size=10000,
                num_workers=8,
                ):

                #extract the intersting events
                events =  events[events.event == eventNum]

                print(ak.to_pandas(events))

if __name__ == "__main__":

    EventCheck(23,5980)

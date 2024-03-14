import ROOT as r
import os 
import sys
import time
import uproot 
import awkward as ak
from array import array
import numpy as np


numRun = 1
filelist =[f'/home/czheng/SimCosmicFlatTree/withPhotonMuontag/output_{numRun}.root:t']

branches = ["chan","runNumber","event","layer","nPE","type","row","muonHit"]

for events in uproot.iterate(
    filelist,
    branches,
    step_size=1000,
    num_workers=8,
    ):

    #create a event based branches
    events['None_empty_event'] = ak.num(events['layer']) > 0
    print(ak.to_list(events))
    events=events[events["None_empty_event"]]
    print(ak.to_list(events))
    print(ak.to_list(events.layer))

    break



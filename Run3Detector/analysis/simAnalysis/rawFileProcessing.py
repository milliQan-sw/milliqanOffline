#the goal of this file is to process the raw flat files that come with particle ID.


import ROOT as r
import os 
import sys
import time
import uproot 
import awkward as ak
from array import array
import numpy as np

run = 1
filelist = [f"/mnt/hadoop/se/store/user/czheng/SimFlattree/withPhotonRaw/output_{run}.root:Events"]

pulseBasedBranches = ["scint_particleName","scint_copyNo","scint_EDep_MeV"]
branches = ["scint_particleName","eventID","NbOfPMTHits","scint_copyNo","scint_EDep_MeV"]


for events in uproot.iterate(
    filelist,
    branches,
    step_size=10000,
    num_workers=8,
    ):

    MuonDirectHit=ak.any(events["scint_particleName"]==13, axis = 1) | ak.any(events["scint_particleName"]==-13, axis = 1)
    #MuonDirectHit= ak.any(events["scint_particleName"]==-13, axis = 1)
    events=events[MuonDirectHit]
    #print(ak.to_list(events.eventID))
    #print(len(events.NbOfPMTHits))
    #print(ak.to_list(events.scint_copyNo))
    NPECut = events.NbOfPMTHits >= 2500
    events = events[NPECut]
    #print(ak.to_list(ak.Array([np.unique(x) for x in events.scint_copyNo])))
    print(ak.to_list(events.scint_copyNo))
    print(ak.to_list(events.scint_EDep_MeV))



    
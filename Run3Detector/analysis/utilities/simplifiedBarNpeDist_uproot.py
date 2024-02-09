import ROOT as r
import os 
import sys
import time
import uproot 
import awkward as ak
from array import array
import numpy as np


filelist = ["/mnt/hadoop/se/store/user/czheng/SimFlattree/withPhoton/output_592.root"]
"""
filelist = []

def appendRun(filelist):
    directory = "/mnt/hadoop/se/store/user/czheng/SimFlattree/withPhoton/"
    for filename in os.listdir(directory):
        if filename.startswith("output") and filename.endswith(".root"):
            filelist.append(directory+filename+":t")

appendRun(filelist)
"""

Npedist=r.TH1F("Npedist","Npedist;barNpe",500,0,100000)

def NpedistPlot(events):
    #remove empty events
    events['None_empty_event'] = ak.num(events.pmt_chan) > 0
    events=events[events.None_empty_event]
    #remove the non-bar channel
    for branch in ["pmt_chan","pmt_nPE"]:

        events[branch] = events[branch][events.pmt_chan <= 64]
    output = ak.flatten(events.pmt_nPE,axis=None)
    myarray = array('d', output)
    Npedist.FillN(len(myarray), myarray, np.ones(len(myarray)))






branches = ["pmt_chan","pmt_nPE"]
total_events = 0
for events in uproot.iterate(
    filelist,
    branches,
    step_size=1000,
    num_workers=8,
    ):

    total_events += len(events)
    NpedistPlot(events)



print("Number of processed events:", total_events)

output_file = r.TFile("NPEtest.root", "RECREATE")
Npedist.Write()
output_file.Close()
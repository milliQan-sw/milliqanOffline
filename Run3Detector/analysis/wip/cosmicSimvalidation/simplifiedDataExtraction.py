"""
run into some new bug ValueError: cannot broadcast RegularArray of size 988 with RegularArray of size 1000
1039,1038,1035 has this issue
find the event and file number

1031 & 1190 is fine
"""


import os
import sys

import numpy as np
import pandas as pd
import ROOT as r
import os 
import sys
import time
import uproot 
import awkward as ak


#filelist =['/mnt/hadoop/se/store/user/milliqan/trees/v34/MilliQan_Run1190.155_v34.root:t','/mnt/hadoop/se/store/user/milliqan/trees/v34/MilliQan_Run1190.154_v34.root:t']
#filelist = ['/mnt/hadoop/se/store/user/milliqan/trees/v34/1000/MilliQan_Run1039.1_v34.root:t']

#"""
filelist = []

def appendRun(filelist,run):
    #directory = "/mnt/hadoop/se/store/user/milliqan/trees/v34/1000/"
    directory = "/mnt/hadoop/se/store/user/milliqan/trees/v34/"
    for filename in os.listdir(directory):
        if filename.startswith(f"MilliQan_Run{run}") and filename.endswith(".root"):
            filelist.append(directory+filename+":t")

#hand pick the cosmic runs with good matching rate. The run with green color in "Matching MilliQan Files"
#cosmicGoodRun = [1039,1038,1035,1034,1031]
cosmicGoodRun = [1364]
#print(filelist)

for run in cosmicGoodRun:
    appendRun(filelist,run)
#"""
nbars = r.TH1F("nbars", "n_BARS", 32, 0, 32)


branches = ['boardsMatched', 'height', 'layer','type','chan','pickupFlag']

total_events = 0

for events in uproot.iterate(

            #files
            filelist,

            #branches
            branches,
            step_size=1000
    
            ):
    
    #if smax_events and total_events >= max_events: break
    

    #boardMatched  check
    for branch in branches:
        if branch == 'boardsMatched': continue
        events[branch] = events[branch][events.boardsMatched]

    
    #loose pickup check
    for branch in branches:
        if branch == 'boardsMatched': continue
        events[branch] = events[branch][events.pickupFlag]

    total_events += len(events)
    
    #type cut for bar
    barCut = events['type'] == 0 # create pulse base T/F table
    for branch in branches:
        if branch == 'boardsMatched': continue   #this is needed to avoid too many jacked slice in array.(dont know the meaing)
        events[branch] = events[branch][barCut]
    


    #height cut
    h_threashold = 36
    #h_threashold = 100
    heightcut = events.height > h_threashold   
    for branch in branches:
        if branch == 'boardsMatched': continue
        events[branch] = events[branch][heightcut]
    
    heightCutdf = ak.to_pandas(events)

    
    
    #1 hit + per layer
    #broadcast the array based t/f table to the event based variable
    events['fourLayerCut'] = ak.any(events.layer==0, axis=1) & ak.any(events.layer==1, axis=1) & ak.any(events.layer==2, axis=1) & ak.any(events.layer==3, axis=1)
    events = events[events['fourLayerCut']]
    #print("final result")
    #print(ak.to_pandas(events))


    

    if len(events) == 0: continue
    #fill the histogram
    for eventIndex in range(len(events)):
        NbarHit=len(set(events[eventIndex]["chan"]))
        nbars.Fill(NbarHit)


    #break #use for single file debug
    
output_file = r.TFile("test.root", "RECREATE")
nbars.Write()
output_file.Close()
print(f"total event(board matched only):{total_events}")

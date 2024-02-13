import ROOT as r
import os 
import sys
import time
import uproot 
import awkward as ak
from array import array
import numpy as np


#there is layer that each row got a big hit
#currently. it can't do the event based analysis
"""
def Cosmuontag1(events,NpeCut=20):
    nPEList = events.nPE
    typeList = events.type
    rowList = events.row
    layerList = events.layer
    layDict = {}

    #FIXME:need to do event based manipulation
    for nPE,type,row,layer in zip(nPEList,typeList,rowList,layerList):
        if type >= 1:
            # for panels, the data inside nPE branch is the same as the data inside area branch.
            nPE = nPE/1320
            #Since the calibration is unfinished for panels. I use the average spe area from bar channels to find estimated pulse NPE value for panels.
        
        elif type == 0:
            #for bars, the  value inside nPE branch is equal to pulse area/ spe area(channel based).
            npe = nPE
        
        if layer not in layDict:
            layDict[layer]={row:[nPE]}
        elif row not in layDict[layer]:
            layDict[layer][row] = npe
        else:
            layDict[layer][row].append(nPE)
        
    print(layDict)
"""
#def bartrim


filelist =['/mnt/hadoop/se/store/user/milliqan/trees/v34/MilliQan_Run1190.4_v34.root:t']

pulseBasedBranches = ["pickupFlag","layer","nPE","type","row"]

branches = ["runNumber","event","fileNumber",'boardsMatched',"pickupFlag","layer","nPE","type","row"]


NPECut = 20

for events in uproot.iterate(
    filelist,
    branches,
    step_size=1000,
    num_workers=8,
    ):

    #total_events += len(events)

    events['boardsMatched'], junk = ak.broadcast_arrays(events.boardsMatched, events.pickupFlag)
    
    for branch in pulseBasedBranches:
        events[branch] = events[branch][events.boardsMatched]

    for branch in pulseBasedBranches:
        events[branch] = events[branch][events.pickupFlag]

    for branch in pulseBasedBranches:
        events[branch] = events[branch][events['type']==0]
    
    for branch in pulseBasedBranches:
        events[branch] = events[branch][events.nPE >= NPECut]

    
    for r in range(4):
        for l in range(4):
            events[f"l{l}R{r}"] = (events.layer == l) & (events.row == r)
    


    
    events["fourRowBigHits"] = (ak.any(events.l0R0==True, axis=1) & 
                                ak.any(events.l0R1==True, axis=1) & 
                                ak.any(events.l0R2==True, axis=1) & 
                                ak.any(events.l0R3==True, axis=1)) | (ak.any(events.l1R0==True, axis=1) & 
                                ak.any(events.l1R1==True, axis=1) & 
                                ak.any(events.l1R2==True, axis=1) & 
                                ak.any(events.l1R3==True, axis=1)) | (ak.any(events.l2R0==True, axis=1) & 
                                ak.any(events.l2R1==True, axis=1) & 
                                ak.any(events.l2R2==True, axis=1) & 
                                ak.any(events.l2R3==True, axis=1)) | (ak.any(events.l3R0==True, axis=1) & 
                                ak.any(events.l3R1==True, axis=1) & 
                                ak.any(events.l3R2==True, axis=1) & 
                                ak.any(events.l3R3==True, axis=1)) 
    


PossibleMuonEvent = events[events.fourRowBigHits == True]
print(ak.to_list(PossibleMuonEvent["event"][PossibleMuonEvent.fourRowBigHits == True]))
print(ak.to_list(PossibleMuonEvent["runNumber"][PossibleMuonEvent.fourRowBigHits == True]))
print(ak.to_list(PossibleMuonEvent["fileNumber"][PossibleMuonEvent.fourRowBigHits == True]))
    
--------------------------------------


    

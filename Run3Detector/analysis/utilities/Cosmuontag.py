"""
when I apply bartrim & 4 rows got big hit in a layer
The pulse NPE measurement is accurate under 20NPE
I saw some channel reach 300-400NPE(saturated value), Can I use those saturated value check cosmic muon?



    events["panelBighit"] = ak.any(events.type == 2,axis = 1) & ak.any(events.nPE >= NPECut,axis = 1)
TypeError: __eq__(): incompatible function arguments. The following argument types are supported:
    1. (self: awkward._ext.Type, arg0: awkward._ext.Type) -> bool



"""
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

pulseBasedBranches = ["pickupFlag","layer","nPE","type","row","chan"]

#branches = ["runNumber","event","fileNumber",'boardsMatched',"pickupFlag","layer","nPE","type","row","chan"]

fakebranches = ["runNumber","pickupFlag","layer","nPE","type","row","chan"]

NPECut = 20



for events in uproot.iterate(
    filelist,
    pulseBasedBranches,
    step_size=1000,
    num_workers=8,
    ):

    #total_events += len(events)
    """
    events['boardsMatched'], junk = ak.broadcast_arrays(events.boardsMatched, events.pickupFlag)
    
    for branch in pulseBasedBranches:
        events[branch] = events[branch][events.boardsMatched]

    for branch in pulseBasedBranches:
        events[branch] = events[branch][events.pickupFlag]
    """

    #create dummy arrays
    dummyDict={'runNumber': [0]}
    barEvents = ak.Array(dummyDict)
    PanelEvents = ak.Array(dummyDict)
    

    #for branch in pulseBasedBranches:
    #trimevent[branch] = events[branch][events['type']>=0] # get rid of the ev
    barEvents = events[events['type']==0] #FIXME: ValueError: too many jagged slice dimensions for array when using branches in interate()
    PanelEvents = events[events['type']>=1]
    

    #currently the panel NPE is the same of pulse area. 1320 is the average spe pulse area from bars. 
    PanelEvents["panelNPE"] = PanelEvents["nPE"]/1320

    #unifinished TBD
    #when cosmic muon hit the panel(5cm thickness) and bar, it will generate at least 2k NPE
    
    for branch in pulseBasedBranches:
        barEvents[branch] = barEvents[branch][barEvents.nPE >= NPECut]
        PanelEvents[branch] = PanelEvents[branch][PanelEvents.panelNPE >= NPECut]

    #event based, NPE trim is applied at above.(I need to think about this again. it seems redundant)
    #PanelEvents["panelBigHit"] = ak.any(PanelEvents.type == 2,axis = 1)

    
    for l in range(4):
        for r in range(4):
            barEvents[f"l{l}R{r}"] = (barEvents.layer == l) & (barEvents.row == r)
    


    
    barEvents["fourRowBigHits"] = (ak.any(barEvents.l0R0==True, axis=1) & 
                                ak.any(barEvents.l0R1==True, axis=1) & 
                                ak.any(barEvents.l0R2==True, axis=1) & 
                                ak.any(barEvents.l0R3==True, axis=1)) | (ak.any(barEvents.l1R0==True, axis=1) & 
                                ak.any(barEvents.l1R1==True, axis=1) & 
                                ak.any(barEvents.l1R2==True, axis=1) & 
                                ak.any(barEvents.l1R3==True, axis=1)) | (ak.any(barEvents.l2R0==True, axis=1) & 
                                ak.any(barEvents.l2R1==True, axis=1) & 
                                ak.any(barEvents.l2R2==True, axis=1) & 
                                ak.any(barEvents.l2R3==True, axis=1)) | (ak.any(barEvents.l3R0==True, axis=1) & 
                                ak.any(barEvents.l3R1==True, axis=1) & 
                                ak.any(barEvents.l3R2==True, axis=1) & 
                                ak.any(barEvents.l3R3==True, axis=1)) 
    
    #top and bottom row has big hit
    barEvents["TBBigHit"] = (ak.any(barEvents.l0R0==True, axis=1) & 
                                ak.any(barEvents.l0R3==True, axis=1)) | (ak.any(barEvents.l1R0==True, axis=1) &  
                                ak.any(barEvents.l1R3==True, axis=1)) | (ak.any(barEvents.l2R0==True, axis=1) & 
                                ak.any(barEvents.l2R3==True, axis=1)) | (ak.any(barEvents.l3R0==True, axis=1) & 
                                ak.any(barEvents.l3R3==True, axis=1)) 


print(ak.to_pandas(PanelEvents))
#print(ak.to_list(PanelEvents["event"][PanelEvents.panelNPE >= NPECut]))
#print(ak.to_list(barEvents.TBBigHit))
#print(ak.to_list(events["event"][events.TBBigHit == True]))
"""
PossibleMuonEvent = events[events.fourRowBigHits == True]
print(ak.to_list(PossibleMuonEvent["event"][PossibleMuonEvent.fourRowBigHits == True]))
print(ak.to_list(PossibleMuonEvent["runNumber"][PossibleMuonEvent.fourRowBigHits == True]))
print(ak.to_list(PossibleMuonEvent["fileNumber"][PossibleMuonEvent.fourRowBigHits == True]))
print(ak.to_pandas(PossibleMuonEvent))
"""
#--------------------------------------


    

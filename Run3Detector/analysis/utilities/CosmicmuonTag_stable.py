"""
2-14-24 This file only check the bar channel when try to tag cosmic muon evnet.


"""



import ROOT as r
import os 
import sys
import time
import uproot 
import awkward as ak
from array import array
import numpy as np

from CosmicTagPlots import plots

filelist =['/mnt/hadoop/se/store/user/milliqan/trees/v34/MilliQan_Run1190.4_v34.root:t']
runN = 1190
"""
runN = 1163
filelist = []

def appendRun(filelist,run):
    #directory = "/mnt/hadoop/se/store/user/milliqan/trees/v34/1000/"
    directory = "/mnt/hadoop/se/store/user/milliqan/trees/v34/"
    for filename in os.listdir(directory):
        if filename.startswith(f"MilliQan_Run{run}") and filename.endswith(".root"):
            filelist.append(directory+filename+":t")
cosmicGoodRun = [runN]

for run in cosmicGoodRun:
    appendRun(filelist,run)
"""
pulseBasedBranches = ["pickupFlag","chan","layer","nPE","type","row"]
branches = ["chan","runNumber","event","fileNumber",'boardsMatched',"pickupFlag","layer","nPE","type","row"]
NPECut = 20
ChanVsbarNpeBTag1 = r.TH2F("B ChanvsNPE tag 1","bar chanvsmpe tag1;chan; pulse NPE", 80,0,80,200,0,1000)
ChanVsbarNpePTag1 = r.TH2F("P ChanvsNPE tag 1","panel chanvsmpe tag1;chan; pulse NPE", 80,0,80,200,0,1000)
ChanVsbarNpeBTag2 = r.TH2F("B ChanvsNPE tag 2","bar chanvsmpe tag2;chan; pulse NPE", 80,0,80,200,0,1000)
ChanVsbarNpePTag2 = r.TH2F("P ChanvsNPE tag 2","panel chanvsmpe tag2;chan; pulse NPE", 80,0,80,200,0,1000)


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
    
    for R in range(4):
        for l in range(4):
            events[f"l{l}R{R}"] = (events.layer == l) & (events.row == R)
    
    
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

    #top and bottom row has big hit
    events["TBBigHit"] = (ak.any(events.l0R0==True, axis=1) & 
                                ak.any(events.l0R3==True, axis=1)) | (ak.any(events.l1R0==True, axis=1) &  
                                ak.any(events.l1R3==True, axis=1)) | (ak.any(events.l2R0==True, axis=1) & 
                                ak.any(events.l2R3==True, axis=1)) | (ak.any(events.l3R0==True, axis=1) & 
                                ak.any(events.l3R3==True, axis=1)) 
    

    #debug
    print(ak.to_pandas(events[events.TBBigHit]))
    
    print(ak.to_pandas(events[events.fourRowBigHits]))
    
    #the script at below is commented out for debugging.
    """
    FileNumberList=(ak.to_list(events["fileNumber"][events.TBBigHit == True]))
    runNumberList=(ak.to_list(events["runNumber"][events.TBBigHit == True]))
    EventIDlist=(ak.to_list(events["event"][events.TBBigHit == True]))
    #collect the range of NPE for event that is tagged & channel that has hit above 20 NPE(plot chan vs NPE).
    #The head(max) of NPE distribution is for cosmic muon and the tail is for low energy photon 
    #there is need to get the origianl event since I used bar & NPE trim
    for RN,FN,EV in zip(runNumberList,FileNumberList,EventIDlist):
        print(RN)
        print(FN)
        print(EV)
        plots(RN,FN,EV,ChanVsbarNpeBTag1,ChanVsbarNpePTag1)
    

    #print("-----")
    FileNumberList2=(ak.to_list(events["fileNumber"][events.fourRowBigHits == True]))
    runNumberList2=(ak.to_list(events["runNumber"][events.fourRowBigHits == True]))
    EventIDlist2 = (ak.to_list(events["event"][events.fourRowBigHits == True]))
    for RN,FN,EV in zip(runNumberList2,FileNumberList2,EventIDlist2):
        plots(RN,FN,EV,ChanVsbarNpeBTag2,ChanVsbarNpePTag2)
    #print("next")
    """


output_file = r.TFile(f"Run{runN}chanvsNPEtest_debug.root", "RECREATE")
ChanVsbarNpeBTag1.Write()
ChanVsbarNpePTag1.Write()
ChanVsbarNpeBTag2.Write()
ChanVsbarNpePTag2.Write()
output_file.Close()

#print(ak.to_list(events["event"][events.TBBigHit == True]))
"""
PossibleMuonEvent = events[events.fourRowBigHits == True]
print(ak.to_list(PossibleMuonEvent["event"][PossibleMuonEvent.fourRowBigHits == True]))
print(ak.to_list(PossibleMuonEvent["runNumber"][PossibleMuonEvent.fourRowBigHits == True]))
print(ak.to_list(PossibleMuonEvent["fileNumber"][PossibleMuonEvent.fourRowBigHits == True]))
print(ak.to_pandas(PossibleMuonEvent))
    
"""
#--------------------------------------

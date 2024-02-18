"""
2-14-24 This file is for All four rows hit & top row hit, bottom row hit cosmic muon tag


"""



import ROOT as r
import os 
import sys
import time
import uproot 
import awkward as ak
from array import array
import numpy as np

from muonTagPlot import plots

run = 20
filelist = [f"/mnt/hadoop/se/store/user/czheng/SimFlattree/withPhoton/output_{run}.root:t"]
"""
filelist = []

def appendRun(filelist):
    directory = "/mnt/hadoop/se/store/user/czheng/SimFlattree/withPhoton/"
    for filename in os.listdir(directory):
        if filename.startswith("output") and filename.endswith(".root"):
            filelist.append(directory+filename+":t")


appendRun(filelist)
#print(filelist)
"""
#filelist = filelist[:20]
pulseBasedBranches = ["chan","layer","nPE","type","row"]
branches = ["chan","runNumber","event","layer","nPE","type","row"]
NPECut = 2000
ChanVsbarNpeBTag1 = r.TH2F("B ChanvsNPE tag 1","bar chanvsmpe tag1;chan; bar NPE", 80,0,80,200,0,100000)
ChanVsbarNpePTag1 = r.TH2F("P ChanvsNPE tag 1","panel chanvsmpe tag1;chan; bar NPE", 80,0,80,200,0,100000)
ChanVsbarNpeBTag2 = r.TH2F("B ChanvsNPE tag 2","bar chanvsmpe tag2;chan; bar NPE", 80,0,80,200,0,100000)
ChanVsbarNpePTag2 = r.TH2F("P ChanvsNPE tag 2","panel chanvsmpe tag2;chan; bar NPE", 80,0,80,200,0,100000)


for events in uproot.iterate(
    filelist,
    branches,
    step_size=10000,
    num_workers=8,
    ):
    #print(ak.to_pandas(events))
    #print(ak.to_list(events)) #event branches is indeed event based. Jagged slide might come the way of using cuts
    events['None_empty_event'] = ak.num(events.chan) > 0
    events=events[events.None_empty_event]


    #total_events += len(events)
    barCut=events['type']==0
    for branch in pulseBasedBranches:
        events[branch] = events[branch][barCut]
    
    NPECuts = events.nPE >= NPECut
    for branch in pulseBasedBranches:
        events[branch] = events[branch][NPECuts]
    
    #print(ak.to_pandas(events))

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
    #print(ak.to_pandas(events[events.TBBigHit]))
    
    #print(ak.to_pandas(events[events.fourRowBigHits]))
    #print(ak.to_list(events[events.TBBigHit]))
    
    #the script at below is commented out for debugging.

    runNumberList=(ak.to_list(events["runNumber"][events.TBBigHit == True]))
    EventIDlist=(ak.to_list(events["event"][events.TBBigHit == True]))
    #print(events)
    #"""
    #collect the range of NPE for event that is tagged & channel that has hit above 20 NPE(plot chan vs NPE).
    #The head(max) of NPE distribution is for cosmic muon and the tail is for low energy photon 
    #there is need to get the origianl event since I used bar & NPE trim
    for RN,EV in zip(runNumberList,EventIDlist):
       
        plots(RN,EV,ChanVsbarNpeBTag1,ChanVsbarNpePTag1)
    

    runNumberList2=(ak.to_list(events["runNumber"][events.fourRowBigHits == True]))
    EventIDlist2 = (ak.to_list(events["event"][events.fourRowBigHits == True]))
    for RN,EV in zip(runNumberList2,EventIDlist2):
        plots(RN,EV,ChanVsbarNpeBTag2,ChanVsbarNpePTag2)

    #"""
    
    

#"""
output_file = r.TFile(f"Run{run}SIMchanvsNPE_2KNPE.root", "RECREATE")
ChanVsbarNpeBTag1.Write()
ChanVsbarNpePTag1.Write()
ChanVsbarNpeBTag2.Write()
ChanVsbarNpePTag2.Write()
output_file.Close()
#"""
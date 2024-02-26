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

from CosmicTagPlots import plots

#filelist =['/mnt/hadoop/se/store/user/milliqan/trees/v34/1100/MilliQan_Run1190.4_v34.root:t']
#runN = 1190
#"""
runN = 1190
filelist = []

def appendRun(filelist,run):
    #directory = "/mnt/hadoop/se/store/user/milliqan/trees/v34/1000/"
    directory = "/mnt/hadoop/se/store/user/milliqan/trees/v34/1100/"
    for filename in os.listdir(directory):
        if filename.startswith(f"MilliQan_Run{run}") and filename.endswith(".root"):
            filelist.append(directory+filename+":t")
cosmicGoodRun = [runN]

for run in cosmicGoodRun:
    appendRun(filelist,run)
#"""

branches = ["chan","runNumber","event","fileNumber",'boardsMatched',"pickupFlag","layer","nPE","type","row","area"]
NPECut = 20
ChanVsbarNpeBTag1 = r.TH2F("B ChanvsNPE tag 1","bar chanvsmpe tag1;chan; pulse NPE", 80,0,80,200,0,1000)
ChanVsbarNpePTag1 = r.TH2F("P ChanvsNPE tag 1","panel chanvsmpe tag1;chan; pulse NPE", 80,0,80,200,0,1000)
ChanVsbarNpeBTag2 = r.TH2F("B ChanvsNPE tag 2","bar chanvsmpe tag2;chan; pulse NPE", 80,0,80,200,0,1000)
ChanVsbarNpePTag2 = r.TH2F("P ChanvsNPE tag 2","panel chanvsmpe tag2;chan; pulse NPE", 80,0,80,200,0,1000)
ChanVsbarNpeBTag3 = r.TH2F("B ChanvsNPE tag 3","bar chanvsmpe tag3;chan; pulse NPE", 80,0,80,200,0,1000)
ChanVsbarNpePTag3 = r.TH2F("P ChanvsNPE tag 3","panel chanvsmpe tag3;chan; pulse NPE", 80,0,80,200,0,1000)
ChanVsbarNpeBTag4 = r.TH2F("B ChanvsNPE tag 4","bar chanvsmpe tag4;chan; pulse NPE", 80,0,80,200,0,1000)
ChanVsbarNpePTag4 = r.TH2F("P ChanvsNPE tag 4","panel chanvsmpe tag4;chan; pulse NPE", 80,0,80,200,0,1000)


for events in uproot.iterate(
    filelist,
    branches,
    step_size=1000,
    num_workers=8,
    ):
    #total_events += len(events)
    events['boardsMatched'], junk = ak.broadcast_arrays(events.boardsMatched, events.pickupFlag)
    pulseBasedBranches = ["pickupFlag","chan","layer","nPE","type","row","area"] 
    #"""
    for branch in pulseBasedBranches:
        events[branch] = events[branch][events.boardsMatched]
    for branch in pulseBasedBranches:
        events[branch] = events[branch][~events.pickupFlag]
    #"""
    events["barCut"]=events['type']==0
    pulseBasedBranches.append("barCut")

    #for branch in pulseBasedBranches:
    #    events[branch] = events[branch][barCut]
    
    NPECuts = events.nPE >= NPECut
    for branch in pulseBasedBranches:
        events[branch] = events[branch][NPECuts]
    
    for R in range(4):
        for l in range(4):
            events[f"l{l}R{R}"] = (events.layer == l) & (events.row == R) & events.barCut
    
    
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

    #top and bottom row has big hits
    events["TBBigHit"] = (ak.any(events.l0R0==True, axis=1) & 
                                ak.any(events.l0R3==True, axis=1)) | (ak.any(events.l1R0==True, axis=1) &  
                                ak.any(events.l1R3==True, axis=1)) | (ak.any(events.l2R0==True, axis=1) & 
                                ak.any(events.l2R3==True, axis=1)) | (ak.any(events.l3R0==True, axis=1) & 
                                ak.any(events.l3R3==True, axis=1)) 
    #Top cosmic panel + row 0 bar channel have big hits
    events["panel"]=events['row']==4
    events["estimatedNPE"] = events.area / 1320
    events["panelHit"] = ak.any((events.estimatedNPE >= 20) & (events.panel), axis = 1)
    #strict cosmic muon with panel tag 
    events["StPanelTag"] = events["panelHit"] & events["TBBigHit"]
    #sufficienc cosmic muon with panel tag 
    events["SuPanelTag"] = events["panelHit"] & ak.any((events["row"] == 0) & (events["type"] == 0),axis =1)




    #debug
    #print(ak.to_pandas(events[events.TBBigHit]))
    
    #print(ak.to_pandas(events[events.fourRowBigHits]))
    
    #the script at below is commented out for debugging.
   
    FileNumberList=(ak.to_list(events["fileNumber"][events.TBBigHit == True]))
    runNumberList=(ak.to_list(events["runNumber"][events.TBBigHit == True]))
    EventIDlist=(ak.to_list(events["event"][events.TBBigHit == True]))
    #collect the range of NPE for event that is tagged & channel that has hit above 20 NPE(plot chan vs NPE).
    #The head(max) of NPE distribution is for cosmic muon and the tail is for low energy photon 
    #there is need to get the origianl event since I used bar & NPE trim
    for RN,FN,EV in zip(runNumberList,FileNumberList,EventIDlist):
        plots(RN,FN,EV,ChanVsbarNpeBTag1,ChanVsbarNpePTag1)
    

    
    FileNumberList2=(ak.to_list(events["fileNumber"][events.fourRowBigHits == True]))
    runNumberList2=(ak.to_list(events["runNumber"][events.fourRowBigHits == True]))
    EventIDlist2 = (ak.to_list(events["event"][events.fourRowBigHits == True]))
    for RN,FN,EV in zip(runNumberList2,FileNumberList2,EventIDlist2):
        plots(RN,FN,EV,ChanVsbarNpeBTag2,ChanVsbarNpePTag2)


    FileNumberList3=(ak.to_list(events["fileNumber"][events.StPanelTag == True]))
    runNumberList3=(ak.to_list(events["runNumber"][events.StPanelTag == True]))
    EventIDlist3 = (ak.to_list(events["event"][events.StPanelTag == True]))
    for RN,FN,EV in zip(runNumberList3,FileNumberList3,EventIDlist3):
        plots(RN,FN,EV,ChanVsbarNpeBTag3,ChanVsbarNpePTag3)


    FileNumberList4=(ak.to_list(events["fileNumber"][events.SuPanelTag == True]))
    runNumberList4=(ak.to_list(events["runNumber"][events.SuPanelTag == True]))
    EventIDlist4 = (ak.to_list(events["event"][events.SuPanelTag == True]))
    for RN,FN,EV in zip(runNumberList4,FileNumberList4,EventIDlist4):
        plots(RN,FN,EV,ChanVsbarNpeBTag4,ChanVsbarNpePTag4)
    
    


#output_file = r.TFile(f"Run{runN}chanvsNPE_NoPickUPboardmaChecked.root", "RECREATE")
output_file = r.TFile(f"Run{runN}chanvsNPE.root", "RECREATE")
ChanVsbarNpeBTag1.Write()
ChanVsbarNpePTag1.Write()
ChanVsbarNpeBTag2.Write()
ChanVsbarNpePTag2.Write()
ChanVsbarNpeBTag3.Write()
ChanVsbarNpePTag3.Write()
ChanVsbarNpeBTag4.Write()
ChanVsbarNpePTag4.Write()
output_file.Close()


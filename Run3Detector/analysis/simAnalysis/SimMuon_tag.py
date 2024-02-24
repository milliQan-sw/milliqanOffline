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

run = 21
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
NPECut = 20
ChanVsbarNpeBTag1 = r.TH2F("B ChanvsNPE tag 1","bar chanvsmpe tag1;chan; bar NPE", 80,0,80,200,0,100000)
ChanVsbarNpePTag1 = r.TH2F("P ChanvsNPE tag 1","panel chanvsmpe tag1;chan; bar NPE", 80,0,80,200,0,100000)
NBarsHitTag1 =  r.TH1F("NBarsHitTag1" , "number of bars get hit;number of bars; Events",30,0,30)
CorrectTimeDtTag1 =  r.TH1F("CorrectTimeDtTag1" , "D_t Max with correction w;D_t Max; Events",40,-15,25)
NPERatioTag1 = r.TH1F("NPEratioTag1","NPE ratio;max NPE/min NPE;Events",150,0,150)

ChanVsbarNpeBTag2 = r.TH2F("B ChanvsNPE tag 2","bar chanvsmpe tag2;chan; bar NPE", 80,0,80,200,0,100000)
ChanVsbarNpePTag2 = r.TH2F("P ChanvsNPE tag 2","panel chanvsmpe tag2;chan; bar NPE", 80,0,80,200,0,100000)
NBarsHitTag2 =  r.TH1F("NBarsHitTag2" , "number of bars get hit;number of bars; Events",30,0,30)
CorrectTimeDtTag2 =  r.TH1F("CorrectTimeDtTag2" , "D_t Max with correction w;D_t Max; Events",40,-15,25)
NPERatioTag2 = r.TH1F("NPEratioTag2","NPE ratio;max NPE/min NPE;Events",150,0,150)

ChanVsbarNpeBTag3 = r.TH2F("B ChanvsNPE tag 3","bar chanvsmpe tag3;chan; bar NPE", 80,0,80,200,0,1000)
ChanVsbarNpePTag3 = r.TH2F("P ChanvsNPE tag 3","panel chanvsmpe tag3;chan; bar NPE", 80,0,80,200,0,1000)
NBarsHitTag3 =  r.TH1F("NBarsHitTag3" , "number of bars get hit;number of bars; Events",30,0,30)
CorrectTimeDtTag3 =  r.TH1F("CorrectTimeDtTag3" , "D_t Max with correction w;D_t Max; Events",40,-15,25)
NPERatioTag3 = r.TH1F("NPEratioTag3","NPE ratio;max NPE/min NPE;Events",150,0,150)

ChanVsbarNpeBTag4 = r.TH2F("B ChanvsNPE tag 4","bar chanvsmpe tag4;chan; bar NPE", 80,0,80,200,0,1000)
ChanVsbarNpePTag4 = r.TH2F("P ChanvsNPE tag 4","panel chanvsmpe tag4;chan; bar NPE", 80,0,80,200,0,1000)
NBarsHitTag4 =  r.TH1F("NBarsHitTag4" , "number of bars get hit;number of bars; Events",30,0,30)
CorrectTimeDtTag4 =  r.TH1F("CorrectTimeDtTag4" , "D_t Max with correction w;D_t Max; Events",40,-15,25)
NPERatioTag4 = r.TH1F("NPEratioTag4","NPE ratio;max NPE/min NPE;Events",150,0,150)


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
    events["bar"]=events['type']==0
    events["barHits"] = (events['type']==0) & (events.nPE >= NPECut)
    #for branch in pulseBasedBranches:
    #    events[branch] = events[branch][barCut]
    
    #NPECuts = events.nPE >= NPECut
    #for branch in pulseBasedBranches:
    #    events[branch] = events[branch][NPECuts]
    
    #print(ak.to_pandas(events))

    for R in range(4):
        for l in range(4):
            events[f"l{l}R{R}"] = (events.layer == l) & (events.row == R) & events["barHits"]
    
    
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
    
    #Top cosmic panel + row 0 bar channel have big hits
    events["panel"]=events['type']==1
    events["panelHit"] = ak.any((events.nPE >= NPECut) & (events.panel), axis = 1)


    
    #strict cosmic muon with panel tag 
    events["StPanelTag"] = events["panelHit"] & events["TBBigHit"]
    #sufficienc cosmic muon with panel tag 
    events["SuPanelTag"] = events["panelHit"] & ak.any((events["row"] == 0) & (events["type"] == 0),axis =1)
    
    #collect the range of NPE for event that is tagged & channel that has hit above 20 NPE(plot chan vs NPE).
    #The head(max) of NPE distribution is for cosmic muon and the tail is for low energy photon 
    #there is need to get the origianl event since I used bar & NPE trim
    runNumberList=(ak.to_list(events["runNumber"][events.TBBigHit == True]))
    EventIDlist=(ak.to_list(events["event"][events.TBBigHit == True]))
    for RN,EV in zip(runNumberList,EventIDlist):
       
        plots(RN,EV,ChanVsbarNpeBTag1,ChanVsbarNpePTag1,NBarsHitTag1,CorrectTimeDtTag1,NPERatioTag1)
    

    runNumberList2=(ak.to_list(events["runNumber"][events.fourRowBigHits == True]))
    EventIDlist2 = (ak.to_list(events["event"][events.fourRowBigHits == True]))
    for RN,EV in zip(runNumberList2,EventIDlist2):
        plots(RN,EV,ChanVsbarNpeBTag2,ChanVsbarNpePTag2,NBarsHitTag2,CorrectTimeDtTag2,NPERatioTag2)

    runNumberList3 =(ak.to_list(events["runNumber"][events.StPanelTag == True]))
    EventIDlist3 = (ak.to_list(events["event"][events.StPanelTag == True]))
    for RN,EV in zip(runNumberList3,EventIDlist3):
        plots(RN,EV,ChanVsbarNpeBTag3,ChanVsbarNpePTag3,NBarsHitTag3,CorrectTimeDtTag3,NPERatioTag3)


    runNumberList4=(ak.to_list(events["runNumber"][events.SuPanelTag == True]))
    EventIDlist4 = (ak.to_list(events["event"][events.SuPanelTag == True]))
    for RN,EV in zip(runNumberList4,EventIDlist4):
        plots(RN,EV,ChanVsbarNpeBTag4,ChanVsbarNpePTag4,NBarsHitTag4,CorrectTimeDtTag4,NPERatioTag4)

    #"""
    
    

#"""
output_file = r.TFile(f"SIMchanvsNPE_{NPECut}NPE.root", "RECREATE")
ChanVsbarNpeBTag1.Write()
ChanVsbarNpePTag1.Write()
NBarsHitTag1.Write()
CorrectTimeDtTag1.Write()
NPERatioTag1.Write()
ChanVsbarNpeBTag2.Write()
ChanVsbarNpePTag2.Write()
NBarsHitTag2.Write()
CorrectTimeDtTag2.Write()
NPERatioTag2.Write()
ChanVsbarNpeBTag3.Write()
ChanVsbarNpePTag3.Write()
NBarsHitTag3.Write()
CorrectTimeDtTag3.Write()
NPERatioTag3.Write()
ChanVsbarNpeBTag4.Write()
ChanVsbarNpePTag4.Write()
NBarsHitTag4.Write()
CorrectTimeDtTag4.Write()
NPERatioTag4.Write()
output_file.Close()
#"""
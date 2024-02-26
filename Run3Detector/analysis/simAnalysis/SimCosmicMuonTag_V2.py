#this file is created based on SimMuon_tag.py & muonTagPlot.py. But it can work with offline offline utilies
#TBD add pulse based plot & event based plot with MilliqanPlotter & Check TBD

import math


import os
import sys

sys.path.append("/share/scratch0/czheng/sim_uproot/milliqanOffline/Run3Detector/analysis/utilities/")

from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *


filelist = []

def appendRun(filelist):
    directory = "/mnt/hadoop/se/store/user/czheng/SimFlattree/withPhoton/"
    for filename in os.listdir(directory):
        if filename.startswith("output") and filename.endswith(".root"):
            filelist.append(directory+filename+":t")


appendRun(filelist)


branches = ['pmt_nPE','pmt_layer','pmt_chan','pmt_time','pmt_type','event','runNumber']

barbranches = ['pmt_nPE','pmt_layer','pmt_chan','pmt_time','pmt_type']

mycuts = milliqanCuts()

myplotter = milliqanPlotter()


#histograms for different cosmic muon tags

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




#----------------------------plotting preparation script----------------------
#the plots requires extra manipulation, so I merge the plotting script with milliqanCut.
#If you try to compare the effects of different cosmic muon tagging algorism, then don't use the "cut".

#bar trim should be used prior using this one
def NbarsHitsCount(self,cut = None):

    if cut:
        cutMask, junk = ak.broadcast_arrays(self.events.cut, self.events.layer)

        uniqueBarArr = ak.Array([np.unique(x) for x in self.event.chan[cutMask]])
        self.events["NBarsHits"] = ak.count(uniqueBarArr,axis = 1)
    else:
        uniqueBarArr = ak.Array([np.unique(x) for x in self.event.chan])
        self.events["NBarsHits"] = ak.count(uniqueBarArr, axis = 1)

#bar trim should be used prior using this function
def BarNPERatioCalculate(self,cut = None):
    if cut:
        cutMask, junk = ak.broadcast_arrays(self.events.cut, self.events.layer)
        self.events['BarNPERatio'] = ((ak.max(self.events.pmt_nPE[cutMask],axis=1)/ak.min(self.events.pmt_nPE[cutMask],axis=1)))
    else:
        self.events['BarNPERatio'] = ((ak.max(self.events.pmt_nPE,axis=1)/ak.min(self.events.pmt_nPE,axis=1)))

#bar trim should be used prior using this function
#introduce correction factor such that time for paricle travel from IP to bar channel is same for time at different layer
def findCorrectTime(self,cut = None):
    if cut:
        cutMask, junk = ak.broadcast_arrays(self.events.cut, self.events.layer)
        TimeArrayL0 = slef.events["time"][cutMask & self.events.layer==0]
        TimeArrayL1 = slef.events["time"][cutMask & self.events.layer==1]
        TimeArrayL2 = slef.events["time"][cutMask & self.events.layer==2]
        TimeArrayL3 = slef.events["time"][cutMask & self.events.layer==3]
        
        
    else:
        TimeArrayL0 = slef.events["time"][self.events.layer==0]
        TimeArrayL1 = slef.events["time"][self.events.layer==1]
        TimeArrayL2 = slef.events["time"][self.events.layer==2]
        TimeArrayL3 = slef.events["time"][self.events.layer==3]
        
    
    CorretTimeArray = np.concatenate((Lay0Time, Lay1Time,Lay2Time,Lay3Time), axis=1)
    self.events["CorrectTime"] = (np.max(CorretTimeArray,axis=1)-np.min(CorretTimeArray,axis=1)).tolist()



#----------------------------------cosmic muon tagging script-------------------------------------------


def CosmuonTagIntialization(self, NPEcut = 0, offline = None):
    for R in range(4):
        for l in range(4):
            self.events[f"l{l}R{R}"] = (self.events.layer == l) & (self.events.row == R) & self.events["barCut"] & self.events["nPE"] >= NPEcut
    
    if offline:
        #1320 is the average spe pulse area from bar channel. Since the calibration on panel is not being done, so NPE need to be recalculated from (pulse area / spe pulse area).
        self.events["TopPanelHit"] = ak.any(self.events["row"]==4 & (self.events["area"]/1320) >= NPEcut ,axis =1)
    else:
        self.events["TopPanelHit"] = ak.any(self.events["row"]==4 & self.events["nPE"] >= NPEcut, axis = 1)

def fourRowBigHits(self):
    self.events["fourRowBigHits"] = (ak.any(self.events.l0R0==True, axis=1) & 
                                ak.any(self.events.l0R1==True, axis=1) & 
                                ak.any(self.events.l0R2==True, axis=1) & 
                                ak.any(self.events.l0R3==True, axis=1)) | (ak.any(self.events.l1R0==True, axis=1) & 
                                ak.any(self.events.l1R1==True, axis=1) & 
                                ak.any(self.events.l1R2==True, axis=1) & 
                                ak.any(self.events.l1R3==True, axis=1)) | (self.ak.any(events.l2R0==True, axis=1) & 
                                ak.any(self.events.l2R1==True, axis=1) & 
                                ak.any(self.events.l2R2==True, axis=1) & 
                                ak.any(self.events.l2R3==True, axis=1)) | (ak.any(self.events.l3R0==True, axis=1) & 
                                ak.any(self.events.l3R1==True, axis=1) & 
                                ak.any(self.events.l3R2==True, axis=1) & 
                                ak.any(self.events.l3R3==True, axis=1)) 
#top and bottom row have big hit
def TBBigHit(self):
    self.events["TBBigHit"] = (ak.any(self.events.l0R0==True, axis=1) & 
                                ak.any(self.events.l0R3==True, axis=1)) | (ak.any(self.events.l1R0==True, axis=1) &  
                                ak.any(self.events.l1R3==True, axis=1)) | (ak.any(self.events.l2R0==True, axis=1) & 
                                ak.any(self.events.l2R3==True, axis=1)) | (ak.any(self.events.l3R0==True, axis=1) & 
                                ak.any(self.events.l3R3==True, axis=1)) 
#cosmic panel , top and bottom row have big hit.
def P_TBBigHit(self):
    self.events["P_TBBigHit"] = self.events["TBBigHit"] & self.events["TopPanelHit"]

#cosmic panel & bottom row have big hits.

def P_BBigHit(self):
    self.events["P_BBigHit"] = ak.any(self.events["row"]==0 & self.events["barCut"], axis=1) & self.events["TopPanelHit"]


#remove the empty events
def EmptyListFilter(self,cutName=None):

    self.events['None_empty_event'] = ak.num(self.events['pmt_layer']) > 0
    self.events=self.events[self.events.None_empty_event]


setattr(milliqanCuts, 'CosmuonTagIntialization', CosmuonTagIntialization)

setattr(milliqanCuts, 'EmptyListFilter', EmptyListFilter)

setattr(milliqanCuts, 'fourRowBigHits', fourRowBigHits)

setattr(milliqanCuts, 'TBBigHit', TBBigHit)

setattr(milliqanCuts, 'P_TBBigHit', P_TBBigHit)

setattr(milliqanCuts, 'P_BBigHit', P_BBigHit)

setattr(milliqanCuts, 'NbarsHitsCount',NbarsHitsCount)

setattr(milliqanCuts, 'BarNPERatioCalculate',BarNPERatioCalculate)

setattr(milliqanCuts, 'findCorrectTime',findCorrectTime)




#pulse based plot



#event based plot




cutflow = [mycuts.EmptyListFilter,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,mycuts.fourRowBigHits,mycuts.TBBigHit,mycuts.P_TBBigHit,mycut.P_BBigHit]





myschedule = milliQanScheduler(cutflow, mycuts)
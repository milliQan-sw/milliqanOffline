#this file is created based on SimMuon_tag.py & muonTagPlot.py. But it can work with offline offline utilies
#TBD add pulse based plot & event based plot with MilliqanPlotter & Check TBD
#get the muon hit after the empty check.
#The row constrain for making plots is not implement yet

import math


import os
import sys

sys.path.append("/home/czheng/scratch0/SIManalysisDEV/milliqanOffline/Run3Detector/analysis/utilities")

from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *
import awkward as ak


filelist =['/mnt/hadoop/se/store/user/czheng/SimFlattree/withPhotonMuontag/output_1.root:t']

"""
filelist = []

def appendRun(filelist):
    directory = "/mnt/hadoop/se/store/user/czheng/SimFlattree/withPhoton/"
    for filename in os.listdir(directory):
        if filename.startswith("output") and filename.endswith(".root"):
            filelist.append(directory+filename+":t")


appendRun(filelist)
"""


branches = ["chan","runNumber","event","layer","nPE","type","row","muonHit"]

barbranches = ["chan","layer","nPE","type","row","muonHit"]

mycuts = milliqanCuts()

myplotter = milliqanPlotter()


#histograms for different cosmic muon tags

ChanVsbarNpeBTag1 = r.TH2F("ChanVsbarNpeBTag1","bar chanvsmpe tag1;chan; bar NPE", 80,0,80,200,0,100000)
ChanVsbarNpePTag1 = r.TH2F("P ChanvsNPE tag 1","panel chanvsmpe tag1;chan; bar NPE", 80,0,80,200,0,100000)
NBarsHitTag1 =  r.TH1F("NBarsHitTag1" , "number of bars get hit;number of bars; Events",60,0,60)
CorrectTimeDtTag1 =  r.TH1F("CorrectTimeDtTag1" , "D_t Max with correction w;D_t Max; Events",40,-15,25)
NPERatioTag1 = r.TH1F("NPEratioTag1","NPE ratio;max NPE/min NPE;Events",150,0,150)

ChanVsbarNpeBTag2 = r.TH2F("B ChanvsNPE tag 2","bar chanvsmpe tag2;chan; bar NPE", 80,0,80,200,0,100000)
ChanVsbarNpePTag2 = r.TH2F("P ChanvsNPE tag 2","panel chanvsmpe tag2;chan; bar NPE", 80,0,80,200,0,100000)
NBarsHitTag2 =  r.TH1F("NBarsHitTag2" , "number of bars get hit;number of bars; Events",60,0,60)
CorrectTimeDtTag2 =  r.TH1F("CorrectTimeDtTag2" , "D_t Max with correction w;D_t Max; Events",40,-15,25)
NPERatioTag2 = r.TH1F("NPEratioTag2","NPE ratio;max NPE/min NPE;Events",150,0,150)

ChanVsbarNpeBTag3 = r.TH2F("B ChanvsNPE tag 3","bar chanvsmpe tag3;chan; bar NPE", 80,0,80,200,0,1000)
ChanVsbarNpePTag3 = r.TH2F("P ChanvsNPE tag 3","panel chanvsmpe tag3;chan; bar NPE", 80,0,80,200,0,1000)
NBarsHitTag3 =  r.TH1F("NBarsHitTag3" , "number of bars get hit;number of bars; Events",60,0,60)
CorrectTimeDtTag3 =  r.TH1F("CorrectTimeDtTag3" , "D_t Max with correction w;D_t Max; Events",40,-15,25)
NPERatioTag3 = r.TH1F("NPEratioTag3","NPE ratio;max NPE/min NPE;Events",150,0,150)

ChanVsbarNpeBTag4 = r.TH2F("B ChanvsNPE tag 4","bar chanvsmpe tag4;chan; bar NPE", 80,0,80,200,0,1000)
ChanVsbarNpePTag4 = r.TH2F("P ChanvsNPE tag 4","panel chanvsmpe tag4;chan; bar NPE", 80,0,80,200,0,1000)
NBarsHitTag4 =  r.TH1F("NBarsHitTag4" , "number of bars get hit;number of bars; Events",60,0,60)
CorrectTimeDtTag4 =  r.TH1F("CorrectTimeDtTag4" , "D_t Max with correction w;D_t Max; Events",40,-15,25)
NPERatioTag4 = r.TH1F("NPEratioTag4","NPE ratio;max NPE/min NPE;Events",150,0,150)




#----------------------------plotting preparation script----------------------

"""
#row constraint plotting script FIXME: non finished yet
def RowbasedPlot(self,ROWs,cut):
    interestEvents =ak.copy(self.events[self.events[cut]])
    rowCuts = ak.Array([])
    for ROW in ROWs:
        rowCuts = rowCuts | sinterestEvents.row == ROW

    interestEvents = interestEvents[rowCuts]

    #plots
    self.

"""


#the plots requires extra manipulation, so I merge the plotting script with milliqanCut.


#bar NPE


#num of unique bar(if possible also think about offline)

myplotter.addHistograms(NBarsHitTag1, 'NBarsHits', 'fourRowBigHits')

myplotter.addHistograms(NBarsHitTag2, 'NBarsHits', 'TBBigHit')

myplotter.addHistograms(NBarsHitTag3, 'NBarsHits', 'P_TBBigHit')

myplotter.addHistograms(NBarsHitTag4, 'NBarsHits', 'P_BBigHit')


myplotter.addHistograms(NPERatioTag1, 'BarNPERatio', 'fourRowBigHits')

myplotter.addHistograms(NPERatioTag2, 'BarNPERatio', 'TBBigHit')

myplotter.addHistograms(NPERatioTag3, 'BarNPERatio', 'P_TBBigHit')

myplotter.addHistograms(NPERatioTag4, 'BarNPERatio', 'P_BBigHit')


myplotter.addHistograms(CorrectTimeDtTag1, 'DT_CorrectTime', 'fourRowBigHits')

myplotter.addHistograms(CorrectTimeDtTag2, 'DT_CorrectTime', 'TBBigHit')

myplotter.addHistograms(CorrectTimeDtTag3, 'DT_CorrectTime', 'P_TBBigHit')

myplotter.addHistograms(CorrectTimeDtTag4, 'DT_CorrectTime', 'P_BBigHit')




#-------plot that work with milliqanplot -------
#Nbars(require extra in milliqancut)

# num of unque bars
#If you try to compare the effects of different cosmic muon tagging algorism, then don't use the "cut".


def ChannelNPEDist(self,cutName = None, cut = None, hist=None):
    if cut:
        interestArrays = ak.copy(self.events[self.events[cut]])
    else:
        interestArrays = ak.copy(self.events)
    
    npeList = ak.flatten(interestArrays.nPE,axis=None)
    chanList = ak.flatten(interestArrays.chan,axis=None)
    nPEarray = array('d', npeList)
    Chanarray = array('d', chanList)

    if len(nPEarray) == 0: return

    if (hist != None) & (len(nPEarray) == len(Chanarray)):
        hist.FillN(len(nPEarray), Chanarray, nPEarray, np.ones(len(nPEarray)))


#bar trim should be used prior using this one
#FIXME: remove the hist arguemtn if I can't make the histogram with milliqanCut
def NbarsHitsCount(self,cutName = "NBarsHits",cut = None, hist = None):

    if cut:
        cutMask, junk = ak.broadcast_arrays(self.events.cut, self.events.layer)

        uniqueBarArr = ak.Array([np.unique(x) for x in self.events.chan[cutMask]])
        self.events[cutName] = ak.count(uniqueBarArr,axis = 1)
    else:
        uniqueBarArr = ak.Array([np.unique(x) for x in self.events.chan])
        self.events[cutName] = ak.count(uniqueBarArr, axis = 1)
        print(self.events[cutName])
        print(self.events.fields)
    
    if hist:
        bararr = ak.flatten(self.events[cutName],axis=None)
        hist.FillN(len(bararr), bararr, np.ones(len(bararr)))


#bar trim should be used prior using this function
def BarNPERatioCalculate(self,cutName = "BarNPERatio",cut = None):
    if cut:
        cutMask, junk = ak.broadcast_arrays(self.events.cut, self.events.layer)
        self.events[cutName] = ((ak.max(self.events.pmt_nPE[cutMask],axis=1)/ak.min(self.events.pmt_nPE[cutMask],axis=1)))
    else:
        self.events[cutName] = ((ak.max(self.events.pmt_nPE,axis=1)/ak.min(self.events.pmt_nPE,axis=1)))

#bar trim should be used prior using this function
#introduce correction factor such that time for paricle travel from IP to bar channel is same for time at different layer
def findCorrectTime(self,cutName = "DT_CorrectTime",cut = None):
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
    self.events[cutName] = (np.max(CorretTimeArray,axis=1)-np.min(CorretTimeArray,axis=1)).tolist()



#----------------------------------cosmic muon tagging script-------------------------------------------


def CosmuonTagIntialization(self, NPEcut = 0, offline = None):
    for R in range(4):
        for l in range(4):
            self.events[f"l{l}R{R}"] = (self.events.layer == l) & (self.events.row == R) & (self.events.barCut) & (self.events.nPE >= NPEcut)

    
    if offline:
        #1320 is the average spe pulse area from bar channel. Since the calibration on panel is not being done, so NPE need to be recalculated from (pulse area / spe pulse area).
        self.events["TopPanelHit"] = ak.any(self.events["row"]==4 & (self.events["area"]/1320) >= NPEcut ,axis =1)
    else:
        self.events["TopPanelHit"] = ak.any((self.events["row"]==4) & (self.events["nPE"] >= NPEcut), axis = 1)

def fourRowBigHits(self,cutName = None, cut = None):
    self.events["fourRowBigHits"] = (ak.any(self.events.l0R0==True, axis=1) & 
                                ak.any(self.events.l0R1==True, axis=1) & 
                                ak.any(self.events.l0R2==True, axis=1) & 
                                ak.any(self.events.l0R3==True, axis=1)) | (ak.any(self.events.l1R0==True, axis=1) & 
                                ak.any(self.events.l1R1==True, axis=1) & 
                                ak.any(self.events.l1R2==True, axis=1) & 
                                ak.any(self.events.l1R3==True, axis=1)) | (ak.any(self.events.l2R0==True, axis=1) & 
                                ak.any(self.events.l2R1==True, axis=1) & 
                                ak.any(self.events.l2R2==True, axis=1) & 
                                ak.any(self.events.l2R3==True, axis=1)) | (ak.any(self.events.l3R0==True, axis=1) & 
                                ak.any(self.events.l3R1==True, axis=1) & 
                                ak.any(self.events.l3R2==True, axis=1) & 
                                ak.any(self.events.l3R3==True, axis=1)) 

    if cut:
        self.events = self.events[self.events["fourRowBigHits"]]
#top and bottom row have big hit
def TBBigHit(self,cutName = None,cut = None):
    self.events["TBBigHit"] = (ak.any(self.events.l0R0==True, axis=1) & 
                                ak.any(self.events.l0R3==True, axis=1)) | (ak.any(self.events.l1R0==True, axis=1) &  
                                ak.any(self.events.l1R3==True, axis=1)) | (ak.any(self.events.l2R0==True, axis=1) & 
                                ak.any(self.events.l2R3==True, axis=1)) | (ak.any(self.events.l3R0==True, axis=1) & 
                                ak.any(self.events.l3R3==True, axis=1)) 
    
    if cut: self.events = self.events[self.events["TBBigHit"]]

#cosmic panel , top and bottom row have big hit.
def P_TBBigHit(self,cutName = None,cut = None):
    self.events["P_TBBigHit"] = self.events["TBBigHit"] & self.events["TopPanelHit"]
    
    if cut: self.events = self.events[self.events["P_TBBigHit"]]

#cosmic panel & bottom row have big hits.

def P_BBigHit(self, cutName = None,cut = None):
    self.events["P_BBigHit"] = ak.any(self.events["row"]==0 & self.events["barCut"], axis=1) & self.events["TopPanelHit"]
    
    if cut:
        self.events=self.events[self.events["P_BBigHit"]]

#remove the empty events
def EmptyListFilter(self,cutName=None):

    self.events['None_empty_event'] = ak.num(self.events['layer']) > 0
    self.events=self.events[self.events.None_empty_event]


#tag muon event (sim only)
def MuonEvent(self, cutName = None, CutonBars = True):

    if CutonBars:
        for branch in barbranches:
            self.events[branch] = self.events[branch][self.events.muonHit == 1]

    else:
        self.events = self.events[ak.any(self.events.muonHit == 1, axis = 1)]

def countEvent(self, cut=None):
    if cut:
        print(f"{cut} event: {len(self.events[self.events[cut]])}")
    else:
        print(f"current available events {len(self.events['event'])}")



setattr(milliqanCuts, 'countEvent', countEvent)

setattr(milliqanCuts, 'MuonEvent', MuonEvent)

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





#test cut flow. Check if the mask can be made
#cutflow = [mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,mycuts.fourRowBigHits,mycuts.TBBigHit,mycuts.P_TBBigHit,mycuts.P_BBigHit]

fourRowBigHitsCut = mycuts.getCut(mycuts.fourRowBigHits, "fourRowBigHitsCut",cut=True)
TBBigHitCut = mycuts.getCut(mycuts.TBBigHit,"TBBigHitCut", cut = True)
P_TBBigHitCut= mycuts.getCut(mycuts.P_TBBigHit, "P_TBBigHitCut",cut = True)
P_BBigHitCut= mycuts.getCut(mycuts.P_BBigHit, "P_BBigHitCut",cut = True)
#NbarsHitsCount1= mycuts.getCut(mycuts.P_BBigHit, "NBarsHits",cut = None,hist = NBarsHitTag1)#FIXME: getCut can't take hist as argument. Maybe I should remove it
cutflow = [mycuts.MuonEvent,mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,TBBigHitCut,mycuts.NbarsHitsCount ,myplotter.dict['NBarsHitTag1']]

myschedule = milliQanScheduler(cutflow, mycuts)

myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts)

myiterator.run()
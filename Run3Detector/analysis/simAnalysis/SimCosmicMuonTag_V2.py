#this file is created based on SimMuon_tag.py & muonTagPlot.py. But it can work with offline offline utilies
#TBD add pulse based plot & event based plot with MilliqanPlotter & Check TBD
#get the muon hit after the empty check.
#The row constrain for making plots is not implement yet

import math


import os
import sys
import time
import json

sys.path.append("../utilities")

from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *
import awkward as ak




mycuts = milliqanCuts()

myplotter = milliqanPlotter()


#histograms for different cosmic muon tags





#----------------------------plotting preparation script----------------------




#collect the data from adjacient layer
#FIXME:unfinished
def adjLayerData(self,layer0Cut,layer1Cut,layer2Cut,layer3Cut):

    #keep the array size 
    arrSize = ak.copy(layer0Cut)


    layer0Cut = ak.any(layer0Cut,axis =1)
    layer1Cut = ak.any(layer1Cut,axis =1)
    layer2Cut = ak.any(layer2Cut,axis =1)
    layer3Cut = ak.any(layer3Cut,axis =1)
    adjLayArrL0= []
    adjLayArrL1= []
    adjLayArrL2= []
    adjLayArrL3= []
    for L0, L1, L2, L3 in zip(layer0Cut,layer1Cut,layer2Cut,layer3Cut):
        innerArr = []
        adjLay = []
        if L0:
            innerArr.append(0)
        if L1:
            innerArr.append(1)
        if L2:
            innerArr.append(2)
        if L3:
            innerArr.append(3)
        
        if len(innerArr) == 1:
            if innerArr[0] == 4:
                adjLay.append(3) 
            else:
                adjLay.append(innerArr[0] + 1)
        elif len(innerArr) == 2:
            if 1 in innerArr and 0 in innerArr:
                adjLay.append(3) 
                adjLay.append(2) 
            elif 3 in innerArr and 2 in innerArr:
                adjLay.append(0) 
                adjLay.append(1)
            else:
                for num in [0,1,2,3]:
                    if num not in innerArr:
                        adjLay.append(num)
        elif len(innerArr) == 3:
            for num in [0,1,2,3]:
                if num not in innerArr:
                        adjLay.append(num)
        
        #check what is in the adjLay
        if 0 in adjLay:
            adjLayArrL0.append(True)
        else:
            adjLayArrL0.append(False)
        if 1 in adjLay:
            adjLayArrL1.append(True)
        else:
            adjLayArrL1.append(False)
        
        if 2 in adjLay:
            adjLayArrL2.append(True)
        else:
            adjLayArrL2.append(False)
        
        if 3 in adjLay:
            adjLayArrL3.append(True)
        else:
            adjLayArrL3.append(False)

    #convert the 
    adjLayArrL0, junk=ak.broadcast_arrays(adjLayArrL0, arrSize)
    adjLayArrL1, junk=ak.broadcast_arrays(adjLayArrL1, arrSize)
    adjLayArrL2, junk=ak.broadcast_arrays(adjLayArrL2, arrSize)
    adjLayArrL3, junk=ak.broadcast_arrays(adjLayArrL3, arrSize)

    return adjLayArrL0,adjLayArrL1,adjLayArrL2,adjLayArrL3




#need to use getCut to make it work
#barbraches in sim is bar-based variable. In offline you should choose the pulse based variable
# I want to extract the data with layer constaint but without changing the original array
#To do: get the adjacent array
def LayerContraint(self,layer0Cut,layer1Cut,layer2Cut,layer3Cut, layerConstraintEnable = None,branches = None,CutomizedEvents=None):

    if CutomizedEvents:
        SpecialArr = ak.copy(CutomizedEvents)

        

        if layerConstraintEnable == False:
            return SpecialArr
        
    
    else:
        specialArr = ak.copy(self.events)
        if layerConstraintEnable == "adjacent":
            layer0Cut,layer1Cut,layer2Cut,layer3Cut=adjLayerData (layer0Cut,layer1Cut,layer2Cut,layer3Cut)

        elif layerConstraintEnable  == False:
            return SpecialArr
    
    if layerConstraintEnable == "adjacent":
        layer0Cut,layer1Cut,layer2Cut,layer3Cut=adjLayerData (layer0Cut,layer1Cut,layer2Cut,layer3Cut)
        #think hard did I do it right? adjcuts?
        for b in branches:
            if branch == 'boardsMatched' or branch == "runNumber" or branch == "fileNumber" or branch == "event": continue
            specialArr[b] = specialArr[b][((specialArr["layer"] ==0) & (layer0Cut)) | ((specialArr["layer"] ==1)  & (layer1Cut))  | ((specialArr["layer"] == 2) & (layer2Cut)) | ((specialArr["layer"] == 3) & (layer3Cut))]
        return specialArr
    

    specialArrCut = ((specialArr["layer"] ==0) & (layer0Cut)) | ((specialArr["layer"] ==1)  & (layer1Cut))  | ((specialArr["layer"] == 2) & (layer2Cut)) | ((specialArr["layer"] == 3) & (layer3Cut))

    for branch in branches:
      
        if branch == 'boardsMatched' or branch == "runNumber" or branch == "fileNumber" or branch == "event" : continue
        
        specialArr[branch] = specialArr[branch][specialArrCut]

    return specialArr

    
    



#the plots requires extra manipulation, so I merge the plotting script with milliqanCut.


#bar NPE


#num of unique bar(if possible also think about offline)








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

def ChannelNPEDistV2(self,arr, hist, branches = None):
    npeList = ak.flatten(arr.nPE,axis=None)
    chanList = ak.flatten(arr.chan,axis=None)
    nPEarray = array('d', npeList)
    Chanarray = array('d', chanList)

    if len(nPEarray) == 0: return

    if (hist != None) & (len(nPEarray) == len(Chanarray)):
        hist.FillN(len(nPEarray), Chanarray, nPEarray, np.ones(len(nPEarray)))



#bar trim should be used prior using this one
#FIXME: remove the hist arguemtn if I can't make the histogram with milliqanCut
def NbarsHitsCount(self,cutName = "NBarsHits",cut = None, hist = None):

    bararr = ak.copy(self.events)

    bararr["chan"] = bararr["chan"][(bararr["type"]==0) & (bararr["nPE"]>=20)]

    if cut:
        cutMask, junk = ak.broadcast_arrays(bararr.cut, bararr.layer)

        uniqueBarArr = ak.Array([np.unique(x) for x in bararr.chan[cutMask]])
        self.events[cutName] = ak.count(uniqueBarArr,axis = 1)
    else:
        uniqueBarArr = ak.Array([np.unique(x) for x in bararr["chan"]])
        self.events[cutName] = ak.count(uniqueBarArr, axis = 1)
        
    
    if hist:
        bararr = ak.flatten(self.events[cutName],axis=None)
        hist.FillN(len(bararr), bararr, np.ones(len(bararr)))

def NbarsHitsCountV2(self,arr, hist, branches = None):

    for branch in branches:
        if branch == 'boardsMatched' or branch == "runNumber" or branch == "fileNumber" or branch == "event": continue
        arr[branch] = arr[branch][arr["type"] == 0]

    uniqueBarArr = ak.Array([np.unique(x) for x in arr.chan])
    NumberOfBarHits = ak.count(uniqueBarArr, axis = 1)
    
    for num in NumberOfBarHits:
        hist.Fill(num)



#bar trim should be used prior using this function
#this is used for finding NPE ratio from pulse at any layer.
#the "cut" here is the event based cut/tag.
def BarNPERatioCalculate(self,cutName = "BarNPERatio",cut = None):
    if cut:
        cutMask, junk = ak.broadcast_arrays(self.events[cut], self.events.layer)
        self.events[cutName] = ((ak.max(self.events.nPE[(cutMask) & (self.events.barCut)],axis=1)/ak.min(self.events.nPE[(cutMask) & (self.events.barCut)],axis=1)))
    else:
        self.events[cutName] = ((ak.max(self.events.nPE[self.events.barCut],axis=1)/ak.min(self.events.nPE[self.events.barCut],axis=1)))

#NPERatio V2. Layer constraint is applied. The layer constraint need to be converted into pulse based
def BarNPERatioCalculateV2(self,cutName = "BarNPERatio_P",cut = None):

    self.events[cutName] = ((ak.max(self.events.nPE[self.events[cut]],axis=1)/ak.min(self.events.nPE[self.events[cut]],axis=1)))



#bar trim should be used prior using this function
#introduce correction factor such that time for paricle travel from IP to bar channel is same for time at different layer

#original method for finding the Max Dt
"""
def findCorrectTime(self,cutName = "DT_CorrectTime",cut = None,timeData = "time", NPECut = 0):
    if cut:
        cutMask, junk = ak.broadcast_arrays(self.events.cut, self.events.layer)
        TimeArrayL0 = slef.events[timeData][cutMask & self.events.layer==0]
        TimeArrayL1 = slef.events[timeData][cutMask & self.events.layer==1]
        TimeArrayL2 = slef.events[timeData][cutMask & self.events.layer==2]
        TimeArrayL3 = slef.events[timeData][cutMask & self.events.layer==3]
        
        
    else:
        TimeArrayL0 = self.events[timeData][(self.events.layer==0) & (self.events["nPE"] >= NPECut) & (self.events[timeData] > 0)] 
        TimeArrayL1 = self.events[timeData][(self.events.layer==1) & (self.events["nPE"] >= NPECut) & (self.events[timeData] > 0)] - (3.96 * 1)
        TimeArrayL2 = self.events[timeData][(self.events.layer==2) & (self.events["nPE"] >= NPECut) & (self.events[timeData] > 0)] - (3.96 * 2)
        TimeArrayL3 = self.events[timeData][(self.events.layer==3) & (self.events["nPE"] >= NPECut) & (self.events[timeData] > 0)] - (3.96 * 3)
        
    
    #TimeArrayL2 and TimeArrayL1 will be used in the later case
    TimeArrayL0 = TimeArrayL0 [(TimeArrayL0 <= 2500)]
    TimeArrayL3 = TimeArrayL3[TimeArrayL3 <= 2500]
    TimeArrayL0_max = ak.max(TimeArrayL0,axis=1)
    TimeArrayL0_min = ak.min(TimeArrayL0,axis=1)
    TimeArrayL3_max = ak.max(TimeArrayL3,axis=1)
    TimeArrayL3_min = ak.min(TimeArrayL3,axis=1)
    diff1 = TimeArrayL3_max - TimeArrayL0_min
    diff2 = TimeArrayL3_min - TimeArrayL0_max
    
    #change array strturn for np concatination
    diff1 = [[x] for x in diff1]
    diff1=ak.fill_none(diff1,-6000.0)
    diff2 = [[x] for x in diff2]
    diff2=ak.fill_none(diff2,-6000.0)
    TimeDiff = np.concatenate((diff1,diff2),axis = 1)
    
    abs_max_index = np.argmax(np.abs(TimeDiff),axis = 1) #get the index for abs max value
    #find the max abs Dt with value in abs_max_index
    TimeDiff = [TimeDiff[index][value] for index,value in enumerate(abs_max_index)]

    self.events["maxTimeDTL0L3"] = TimeDiff
"""

#new method Dt is calculated by first hit at each layer
def findCorrectTime(self,cutName = "DT_CorrectTime",cut = None,timeData = "time", NPECut = 0):
    if cut:
        cutMask, junk = ak.broadcast_arrays(self.events.cut, self.events.layer)
        TimeArrayL0 = self.events[timeData][cutMask & self.events.layer==0]
        TimeArrayL1 = self.events[timeData][cutMask & self.events.layer==1]
        TimeArrayL2 = self.events[timeData][cutMask & self.events.layer==2]
        TimeArrayL3 = self.events[timeData][cutMask & self.events.layer==3]
        
        
    else:
        

        TimeArrayL0 = self.events[timeData][(self.events.layer==0) & (self.events["nPE"] >= NPECut) & (self.events[timeData] > 0)] 
        TimeArrayL1 = self.events[timeData][(self.events.layer==1) & (self.events["nPE"] >= NPECut) & (self.events[timeData] > 0)] - (3.96 * 1)
        TimeArrayL2 = self.events[timeData][(self.events.layer==2) & (self.events["nPE"] >= NPECut) & (self.events[timeData] > 0)] - (3.96 * 2)
        TimeArrayL3 = self.events[timeData][(self.events.layer==3) & (self.events["nPE"] >= NPECut) & (self.events[timeData] > 0)] - (3.96 * 3)
        
    
    #TimeArrayL2 and TimeArrayL1 will be used in the later case
    TimeArrayL0 = TimeArrayL0 [(TimeArrayL0 <= 2500)]
    TimeArrayL3 = TimeArrayL3[TimeArrayL3 <= 2500]
    TimeArrayL0_min = ak.min(TimeArrayL0,axis=1)
    TimeArrayL3_min = ak.min(TimeArrayL3,axis=1)
    diff1 = TimeArrayL3_min - TimeArrayL0_min

    
    #change array strturn for np concatination
    diff1 = [[x] for x in diff1]
    diff1=ak.fill_none(diff1,-6000.0)

    self.events["DTL0L3"] = diff1

    

    

#----------------------------------cosmic muon tagging script-------------------------------------------


def CosmuonTagIntialization(self, cutName = None, cut = None, NPEcut = 20, offline = None):
    for R in range(4):
        for l in range(4):
            self.events[f"l{l}R{R}"] = (self.events.layer == l) & (self.events.row == R) & (self.events.barCut) & (self.events.nPE >= NPEcut)

    
    if offline:
        #1320 is the average spe pulse area from bar channel. Since the calibration on panel is not being done, so NPE need to be recalculated from (pulse area / spe pulse area).
        self.events["TopPanelHit"] = ak.any((self.events["row"]==4) & ((self.events["area"]/(1320)) >= (NPEcut/12))  ,axis =1)
    else:
        self.events["TopPanelHit"] = ak.any((self.events["row"]==4) & (self.events["nPE"]>= (NPEcut/12) ), axis = 1)

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
def TBBigHit(self,cutName = None,cut = None, LayerContraint = False, adjLayer = False):
    
    TBBigHit_lay0 =  (ak.any(self.events.l0R0==True, axis=1) & ak.any(self.events.l0R3==True, axis=1)) #data at layer 0 should be kept
    TBBigHit_lay1 =  (ak.any(self.events.l1R0==True, axis=1) & ak.any(self.events.l1R3==True, axis=1))
    TBBigHit_lay2 =  (ak.any(self.events.l2R0==True, axis=1) & ak.any(self.events.l2R3==True, axis=1))
    TBBigHit_lay3 =  (ak.any(self.events.l3R0==True, axis=1) & ak.any(self.events.l3R3==True, axis=1))
    

    #this mask is only useful when doing the counting
    self.events["TBBigHit"] = (TBBigHit_lay0 | TBBigHit_lay1 | TBBigHit_lay2 | TBBigHit_lay3) 
    

    #apply the cut and pick out which layer should be kept when using layer contraint
    # if the event cut is applied then milliqan plotter unable to work properly.
    if cut: 
        
        TBBigHit_lay0, junk=ak.broadcast_arrays(TBBigHit_lay0, self.events.layer)
        TBBigHit_lay1, junk=ak.broadcast_arrays(TBBigHit_lay1, self.events.layer)
        TBBigHit_lay2, junk=ak.broadcast_arrays(TBBigHit_lay2, self.events.layer)
        TBBigHit_lay3, junk=ak.broadcast_arrays(TBBigHit_lay3, self.events.layer)
        
        TBBigHit_lay0 = TBBigHit_lay0[self.events["TBBigHit"]]
        TBBigHit_lay1 = TBBigHit_lay1[self.events["TBBigHit"]]
        TBBigHit_lay2 = TBBigHit_lay2[self.events["TBBigHit"]]
        TBBigHit_lay3 = TBBigHit_lay3[self.events["TBBigHit"]]


        self.events = self.events[self.events["TBBigHit"]]



    #LayerContraint
    #there is need to create special array when doing the layer constaint to avoid changing array significantly
    #to get those containt data I need to edit the plotter directly. instead of here
    # create combine cut
        
    #combine cut 
        

    if LayerContraint:
        self.events["layerContraint"] = ((self.events["layer"] ==0) & (TBBigHit_lay0)) | ((self.events["layer"] ==1)  & (TBBigHit_lay1))  | ((self.events["layer"] == 2) & (TBBigHit_lay2)) | ((self.events["layer"] == 3) & (TBBigHit_lay3))

    if adjLayer:
        adjLayArrL0,adjLayArrL1,adjLayArrL2,adjLayArrL3 = self.adjLayerData(TBBigHit_lay0,TBBigHit_lay1,TBBigHit_lay2,TBBigHit_lay3)
        self.events["layerContraint"] = ((self.events["layer"] ==0) & (adjLayArrL0)) | ((self.events["layer"] ==1)  & (adjLayArrL1))  | ((self.events["layer"] == 2) & (adjLayArrL2)) | ((self.events["layer"] == 3) & (adjLayArrL3))


#cosmic panel , top and bottom row have big hit.
def P_TBBigHit(self,cutName = None,cut = None):
    self.events["P_TBBigHit"] = self.events["TBBigHit"] & self.events["TopPanelHit"]
    
    if cut: self.events = self.events[self.events["P_TBBigHit"]]

#cosmic panel & bottom row have big hits.

def P_BBigHit(self, cutName = None,cut = None):
    self.events["P_BBigHit"] = ak.any(self.events.l0R0 | self.events.l0R1 | self.events.l0R2 | self.events.l0R3) & self.events["TopPanelHit"]
    
    if cut:
        self.events=self.events[self.events["P_BBigHit"]]

#remove the empty events
def EmptyListFilter(self,cutName=None):

    self.events['None_empty_event'] = ak.num(self.events['layer']) > 0 #create a event-based mask that check if the event is empty
    #


#tag muon event (sim only)
def MuonEvent(self, cutName = None, CutonBars = True, branches = None):
    
    #create a mask for each hit anc check whether it is hit by muon
    if CutonBars:
        for branch in branches:
            if branch == 'boardsMatched' or branch == "runNumber" or branch == "fileNumber" or branch == "event": continue
            self.events[branch] = self.events[branch][self.events.muonHit == 1]

    #create a mask for event that contain muon hit
    else:
        self.events["muonEvent"] = ak.any(self.events.muonHit == 1, axis = 1) 

#the default behaviour is to count the number of events that has data.
def countEvent(self, cutName = None, Countobject='None_empty_event', debug = False):
    if debug: 
        print(ak.to_pandas(self.events))
    if cutName:
        print(f"{Countobject} event: {len(self.events[self.events[Countobject]])}")
    else:
        print(f"current available events : {ak.count_nonzero(self.events['None_empty_event'])}")


#the EmptyListFilter() has a weird bug that can cause the milliqanplotter unable to work. So the current solution for doing analysis without looping over the empty 
#FIXME: check does it work? if not then use the milliqancut
def SimPanelCut(self):
    PanelDefault=self.events['type'] == 2
    self.events['barCut'] = PanelDefault & self.events["None_empty_event"]

def SimBarCut(self):
    barCutdefault=self.events['type'] == 0
    self.events['barCut'] = barCutdefault & self.events["None_empty_event"]


def CheckFieldName(self):
    print(self.events.fields)


def MiddleRow(self):
    self.events["MiddleRow"] = ( (self.events["row"]== 1) | (self.events["row"]== 2) )


def sudo_straight(self, cutName = "StraghtCosmic",NPEcut = 20):
    
    #new script:
    lxArr = ak.copy(self.events)
    
    eventList = []

    #FIXME: move this section to initialization?
    for layer in range(4):
        for row in range(4):
            for column in range(4):
                lxArr[f"L{layer}_r{row}_c{column}"]=(lxArr["nPE"] >= NPEcut) & (lxArr["layer"] == layer) & (lxArr["column"] == column) & (lxArr["row"] == row) & (lxArr["barCut"])
    

    for layer in range(4):

        #case 1: for muon passing straight across the detector and leave the hits along same column but different rows.
        for c in range(4):
            eventList.append(ak.any(lxArr[f"L{layer}_r0_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c}"], axis = 1))
        

        #case 2-1: for the  first three hits(count from the layer 3 to layer 0) are at the same column
        for c in range(3):
            eventList.append(ak.any(lxArr[f"L{layer}_r0_c{c+1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c}"], axis = 1))
            eventList.append(ak.any(lxArr[f"L{layer}_r0_c{c+1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c+1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c}"], axis = 1))
            eventList.append(ak.any(lxArr[f"L{layer}_r0_c{c+1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c+1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c+1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c}"], axis = 1))
        

        #case 2-2: similar to case 2-1 but the hit at row 0 shift by -1
        for c in [1,2,3]:
            eventList.append(ak.any(lxArr[f"L{layer}_r0_c{c-1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c}"], axis = 1))
            eventList.append(ak.any(lxArr[f"L{layer}_r0_c{c-1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c-1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c}"], axis = 1))
            eventList.append(ak.any(lxArr[f"L{layer}_r0_c{c-1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c-1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c-1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c}"], axis = 1))

        #path that cross three columns
        for c in [0,1]:
            eventList.append(ak.any(lxArr[f"L{layer}_r0_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c+1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c+2}"], axis = 1))
            eventList.append(ak.any(lxArr[f"L{layer}_r0_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c+1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c+2}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c+2}"], axis = 1))
            eventList.append(ak.any(lxArr[f"L{layer}_r0_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c+1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c+1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c+2}"], axis = 1))
    
        for c in [2,3]:
            eventList.append(ak.any(lxArr[f"L{layer}_r0_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c-1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c-2}"], axis = 1))
            eventList.append(ak.any(lxArr[f"L{layer}_r0_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c-1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c-2}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c-2}"], axis = 1))
            eventList.append(ak.any(lxArr[f"L{layer}_r0_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c-1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c-1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c-2}"], axis = 1))
            

        #diaganal path
        eventList.append(ak.any(lxArr[f"L{layer}_r0_c0"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c1"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c2"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c3"], axis = 1))
        eventList.append(ak.any(lxArr[f"L{layer}_r3_c0"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c1"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c2"], axis = 1) & ak.any(lxArr[f"L{layer}_r0_c3"], axis = 1))
   

    lay0Muon = []
    lay1Muon = []
    lay2Muon = []
    lay3Muon = []

    
    


    for index, path in enumerate(eventList):

        #section for checking wether a event passes the muon cut
        if index == 0: passArr = path # create an intial array
        else: passArr = passArr | path #the events that have interesting path will be saved

        #section for checking which layer passes the muon cut

        #there are 36 muon paths. So the size(outtermost) of array eventList is 36 * 4. index / 36 = layer number
        if (index // 36) == 0: #// : division with round down
            if index == 0:
                lay0Muon = path
            else: lay0Muon = lay0Muon | path
        elif (index // 36) == 1:
            if index == 36:
                lay1Muon = path
            else: lay1Muon = lay1Muon | path
        elif (index // 36) == 2:
            if index == 72:
                lay2Muon = path
            else: lay2Muon = lay2Muon | path
        elif (index // 36) == 3:
            if index == 108:
                lay3Muon = path
            else: lay3Muon = lay3Muon | path
            
    
    #tag the pulses that has is in the layer where muon event can be found
    l0Arr = (lay0Muon) & ((self.events["layer"]==0) & (self.events["barCut"]))
    l1Arr = (lay1Muon) & ((self.events["layer"]==1)  & (self.events["barCut"]))
    l2Arr = (lay2Muon) & ((self.events["layer"]==2)  & (self.events["barCut"]))
    l3Arr = (lay3Muon) & ((self.events["layer"]==3)  & (self.events["barCut"]))
    



    #try to find the event that only one layer has the muon events. This is an Event based tag.
    #print(len(lay0Muon)) #10K should be event based
    #print(ak.to_list(lay0Muon))
    lay0Muon_T =  [[x] for x in lay0Muon]
    lay1Muon_T =  [[x] for x in lay1Muon]
    lay2Muon_T =  [[x] for x in lay2Muon]
    lay3Muon_T =  [[x] for x in lay3Muon]
    CleanEventTags = np.concatenate((lay0Muon_T,lay1Muon_T,lay2Muon_T,lay3Muon_T),axis = 1) 
    self.events["Clean_MuonEvent"] = ak.count_nonzero(CleanEventTags,axis = 1) == 1
    #print(ak.to_list(self.events["event"][self.events["Clean_MuonEvent"]])) #used for debug only

   
    #tag the pulses that is at the adjacent layers where muon event can be found
    adj0,adj1,adj2,adj3=self.adjLayerData(l0Arr,l1Arr,l2Arr,l3Arr) 

    #put the layer constraint tags back to the array
    self.events["MuonL0"] = l0Arr
    self.events["MuonL1"] = l1Arr      
    self.events["MuonL2"] = l2Arr      
    self.events["MuonL3"] = l3Arr
    self.events["MuonLayers"] = l0Arr | l1Arr | l2Arr | l3Arr   #pulse based tag.
    self.events["otherlayer"] = ~self.events["MuonLayers"] #layers that can't find the muon event.
    self.events["MuonADJL0"] = (self.events["layer"]==0) & (adj0)
    self.events["MuonADJL1"] = (self.events["layer"]==1) & (adj1)      
    self.events["MuonADJL2"] = (self.events["layer"]==2) & (adj2)      
    self.events["MuonADJL3"] = (self.events["layer"]==3) & (adj3)
    self.events["MuonADJLayers"] = self.events["MuonADJL0"] | self.events["MuonADJL1"] | self.events["MuonADJL2"] | self.events["MuonADJL3"]

    #put the new straight muon tag back to arrays
    self.events[cutName] = passArr
    #check the number of events that can pass the cosmic straight cut
    print(f"cosmic straight : {len(self.events['event'][self.events[cutName]])}")
      
setattr(milliqanCuts, 'BarNPERatioCalculateV2' ,BarNPERatioCalculateV2)
setattr(milliqanCuts, 'sudo_straight',sudo_straight)    

setattr(milliqanCuts, 'adjLayerData' , adjLayerData)
setattr(milliqanCuts, 'MiddleRow', MiddleRow)

setattr(milliqanCuts, 'CheckFieldName' , CheckFieldName)

setattr(milliqanCuts, 'SimPanelCut', SimPanelCut)

setattr(milliqanCuts, 'SimBarCut', SimBarCut)

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

setattr(milliqanCuts,'LayerContraint',LayerContraint)

setattr(milliqanCuts, 'NbarsHitsCountV2', NbarsHitsCountV2)


if __name__ == "__main__":


    #---------------------------------------condor job section(get the file that needs to be processed)---------------------------------
    """
    def getFile(processNum, fileList):

        filelist = open(fileList)
        files = json.load(filelist)['filelist']
        filelist.close()

        return files[processNum]

    #run number, filelist
    processNum = int(sys.argv[1])
    fileList = sys.argv[2]


    #get the filename to run over
    filename = getFile(processNum, fileList)

    if('.root' in filename and 'output' in filename):
        numRun = filename.split('_')[1].split('.')[0].replace('Run', '')

    filelist =['/mnt/hadoop/se/store/user/czheng/SimFlattree/withPhotonMuontag/output_1.root:t']
    filelist =[f'{filename}:t']
    #"""

    #----------------------------------------------------------------------------------------------------------------------------------- OSU T3
    #signle file test
    #numRun = 1
    #numRun = str(sys.argv[1])
    #filelist =[f'/mnt/hadoop/se/store/user/czheng/SimFlattree/withPhotonMuontag/output_{numRun}.root:t']
    #outputPath = str(sys.argv[2]) # the path is used at the very end for the output txt file

    #------------------------------------------------------------------------------------------------
    #path for the milliqan machine

    #print("this is numRun" + str(sys.argv[1]) )
    
    #"""

    numRun = str(sys.argv[1])
    filelist =[f'/home/czheng/SimCosmicFlatTree/withPhotonMuontag/output_{numRun}.root:t']
    print(filelist)

    outputPath = str(sys.argv[2]) # the path is used at the very end for the output txt file
    print(outputPath)
    
    #"""

    #-----------------------------------OSU T3--------------------------------------------------------

    #multiple file test(non recommend to use due to time consuming)
    """
    filelist = []

    def appendRun(filelist):
        directory = "/mnt/hadoop/se/store/user/czheng/SimFlattree/withPhoton/"
        for filename in os.listdir(directory):
            if filename.startswith("output") and filename.endswith(".root"):
                filelist.append(directory+filename+":t")


    appendRun(filelist)
    """
    #---------------------------------------------------------------------------------------------
    #branch for data analysis
    branches = ["column","time","chan","runNumber","event","layer","nPE","type","row","muonHit"]
    
    #test cut flow. Check if the mask can be made
    #cutflow = [mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,mycuts.fourRowBigHits,mycuts.TBBigHit,mycuts.P_TBBigHit,mycuts.P_BBigHit]


    """
    #"placeholder" is use in cutName argument. This argument is useless in some of the methods but to make the "getCut" work I need to use the  
    fourRowBigHitsCut = mycuts.getCut(mycuts.fourRowBigHits, "fourRowBigHitsCut",cut=False)
    TBBigHitCut = mycuts.getCut(mycuts.TBBigHit,"placeholder", cut = False)
    P_TBBigHitCut= mycuts.getCut(mycuts.P_TBBigHit, "P_TBBigHitCut",cut = False)
    P_BBigHitCut= mycuts.getCut(mycuts.P_BBigHit, "P_BBigHitCut",cut = False)
    MuonCut = mycuts.getCut(mycuts.MuonEvent, "placeholder", CutonBars =True, branches=branches)
    MuonEventCut = mycuts.getCut(mycuts.MuonEvent, "placeholder", CutonBars =False, branches=branches)
    

    TBBigHitCutCount= mycuts.getCut(mycuts.countEvent, "placeholder" ,Countobject = "TBBigHit")
    fourRowBigHitsCutCount= mycuts.getCut(mycuts.countEvent, "placeholder" ,Countobject = "fourRowBigHits")
    P_TBBigHitCutCount= mycuts.getCut(mycuts.countEvent,"placeholder"  ,Countobject = "P_TBBigHit")
    P_BBigHitCutCount= mycuts.getCut(mycuts.countEvent, "placeholder" ,Countobject = "P_BBigHit")
    #NbarsHitsCount1= mycuts.getCut(mycuts.P_BBigHit, "NBarsHits",cut = None,hist = NBarsHitTag1)#FIXME: getCut can't take hist as argument. Maybe I should remove it
    #cutflowSTD = [mycuts.MuonEvent,mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,TBBigHitCut,mycuts.NbarsHitsCount ,myplotter.dict['NBarsHitTag2']] #default analysis cutflow
    
    #-------------------------section for making histograms---------------------------------------
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

    nPEPlot = r.TH1F("nPEPlot", "nPE", 4000, 0, 40000)
    middleRowNPE = r.TH1F("middleRowNPE", "nPE", 4000, 0, 40000)
    ChanVsbarNpeB = r.TH2F("ChanVsbarNpeB","bar chanvsmpe tag1;chan; bar NPE", 80,0,80,200,0,100000)
    CorrectTimeDist =  r.TH1F("CorrectTimeDist" , "D_t Max with correction w;D_t Max; Events",40,-15,25)
    #NuniqueBar = r.TH1F("NuniqueBar" , "NuniqueBar;number of unique bar;events",50,0,50)  
    #NPERatio = r.TH1F("NPERatio","NPE ratio;max NPE/min NPE;Events",150,0,150)

    #eventCuts at below is used while making plot
    eventCutsD = mycuts.getCut(mycuts.combineCuts, 'eventCuts', ["None_empty_event","TBBigHit", "barCut"])
    eventCuts = mycuts.getCut(mycuts.combineCuts, 'eventCuts', ["layerContraint","None_empty_event","TBBigHit", "barCut"])
    eventCuts2 = mycuts.getCut(mycuts.combineCuts, 'eventCuts2', ["layerContraint","None_empty_event","TBBigHit", "MiddleRow", "barCut"])
    eventCuts3 = mycuts.getCut(mycuts.combineCuts, 'eventCuts3', ["layerContraint","None_empty_event","TBBigHit"]) #debug only. I use this one on NPE vs chan distribution to check if the layer contraints is applied corretly
    eventCuts4 = mycuts.getCut(mycuts.combineCuts, 'eventCuts4', ["TBBigHit"]) #debug only. same like above
    eventCuts5 = mycuts.getCut(mycuts.combineCuts, 'eventCuts5', ["None_empty_event","TBBigHit","barCut"]) #for the time distribution

    #add histogram
    myplotter.addHistograms(nPEPlot, 'nPE', 'eventCuts')
    myplotter.addHistograms(middleRowNPE, 'nPE', 'eventCuts2') #bar NPE
    myplotter.addHistograms(ChanVsbarNpeB, ['chan','nPE'], 'eventCuts4') #general NPE vs chan distribution
    myplotter.addHistograms(CorrectTimeDist, 'DT_CorrectTime', 'eventCuts5') #FIXME: this is not being used now. general NPE vs chan distribution.
    #myplotter.addHistograms(NuniqueBar, 'NBarsHits', 'eventCuts4')
    #myplotter.addHistograms(NPERatio, 'BarNPERatio', 'eventCuts4')
    


    #------------new plots for straight muon events--------------------------------
    #The direct comparision for sim and offline is only meaningful before pulse reach saturation value(20 Npe). I use the range 0-100 nPE just like the deomonstrator.
    M_NPE = r.TH1F("M_NPE", "nPE muon event layer", 100, 0, 100)
    M_adj_NPE = r.TH1F("M_adj_NPE", "nPE muon event adjacnet layer", 100, 0, 100)
    myplotter.addHistograms(M_NPE, 'nPE', 'MuonLayers')
    myplotter.addHistograms(M_adj_NPE, 'nPE', 'MuonADJLayers')
    NuniqueBar = r.TH1F("NuniqueBar" , "NuniqueBar;number of unique bar;events",50,0,50)
    myplotter.addHistograms(NuniqueBar, 'NBarsHits', 'StraghtCosmic')
    CorrectTime =  r.TH1F("CorrectTime" , "D_t Max with correction w;D_t Max; Events",5000,0,5000)
    myplotter.addHistograms(CorrectTime, 'DT_CorrectTime', 'StraghtCosmic')
    NPERatio = r.TH1F("NPERatio","NPE ratio;max NPE/min NPE;Events",5000,0,5000)
    myplotter.addHistograms(NPERatio, 'BarNPERatio', 'StraghtCosmic')
    

    
    #------------------------plot for "clean" muon event. Cut flow 7------------------------------------
    M_NPE_C = r.TH1F("M_NPE_C", "nPE muon event layer", 100, 0, 100)
    M_adj_NPE_C = r.TH1F("M_adj_NPE_C", "nPE muon event adjacnet layer", 100, 0, 100)
    myplotter.addHistograms(M_NPE_C, 'nPE', 'clean_Muon_layer')
    myplotter.addHistograms(M_adj_NPE_C	, 'nPE', 'clean_Muon_adj_layer')
    NuniqueBar_C = r.TH1F("NuniqueBar_C" , "NuniqueBar;number of unique bar;events",50,0,50)
    myplotter.addHistograms(NuniqueBar_C, 'NBarsHits', 'Clean_MuonEvent')
    CorrectTime_C =  r.TH1F("CorrectTime_C" , "D_t Max with correction w;D_t Max; Events",6000,-3000,3000)
    myplotter.addHistograms(CorrectTime_C, 'maxTimeDTL0L3', 'Clean_MuonEvent')
    NPERatio_C = r.TH1F("NPERatio_C","NPE ratio;max NPE/min NPE;Events",5000,0,5000)
    myplotter.addHistograms(NPERatio_C, 'BarNPERatio', 'Clean_MuonEvent')
    CorrectTime_default =  r.TH1F("CorrectTime_default" , "D_t Max with correction w;D_t Max; Events",6000,-3000,3000)
    myplotter.addHistograms(CorrectTime_default, 'maxTimeDTL0L3', 'None_empty_event') 
   



    #-------------------------start of cut efficiency analysis cutflows-----------------------------------------------------------

    #Cut flow 1. This one is for testing the cut efficiency of different tags. TB big hits - > TB + panel big hits 
    cutflow1 = [MuonCut,mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,TBBigHitCut,TBBigHitCutCount,P_TBBigHitCut,P_TBBigHitCutCount] #FIXME: stop applying the cut to remove events in the array
    #FIXME: I need to bring back MuonCut and put it into combined cut after checking the NPE cutefficiency plot
    #cutflow1 = [mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,TBBigHitCut,TBBigHitCutCount,P_TBBigHitCut,P_TBBigHitCutCount]
    



    #Cut flow 1. but the the muon cut change the muon event cut
    cutflow1A = [MuonEventCut,mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,TBBigHitCut,TBBigHitCutCount,P_TBBigHitCut,P_TBBigHitCutCount]
   
    #cut flow 1. but the muon event cut are removed

    cutflow1B = [mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,TBBigHitCut,TBBigHitCutCount,P_TBBigHitCut,P_TBBigHitCutCount]


    #Cut flow 2. This one is for testing the cut efficiency of different tags. TB big hits - > 4 rows big hits
    cutflow2 = [MuonCut,mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,TBBigHitCut,TBBigHitCutCount,fourRowBigHitsCut,fourRowBigHitsCutCount]

    #cut flow2. but the the muon cut change the muon event cut
    cutflow2A = [MuonEventCut,mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,TBBigHitCut,TBBigHitCutCount,fourRowBigHitsCut,fourRowBigHitsCutCount]

    #cut flow 2. but the muon event cut are removed
    cutflow2B = [mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,TBBigHitCut,TBBigHitCutCount,fourRowBigHitsCut,fourRowBigHitsCutCount]

    #cut flow 3. This one is for testing the cut efficiency of different tags. B + panel big hits  - > TB + panel big hits 
    cutflow3 = [MuonCut,mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,P_BBigHitCut,P_BBigHitCutCount,TBBigHitCut,P_TBBigHitCut,P_TBBigHitCutCount]

    #Cut flow 3. but the the muon cut change the muon event cut
    cutflow3A = [MuonEventCut,mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,P_BBigHitCut,P_BBigHitCutCount,TBBigHitCut,P_TBBigHitCut,P_TBBigHitCutCount]

    #cut flow 3. but the muon event cut are removed
    cutflow3B = [mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,P_BBigHitCut,P_BBigHitCutCount,TBBigHitCut,P_TBBigHitCut,P_TBBigHitCutCount]


    #--------------------end of cut efficiency analysis cutflows----------------------
    

    #-------------------cut flows for study the NPE distribution and plotting---------
    TBBigHitCutPlot = mycuts.getCut(mycuts.TBBigHit,"placeholder", cut = True,Hist1 = NBarsHitTag1,branches= branches)
    cutflow4 = [mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,TBBigHitCutPlot]

    #------------------cut flow5 for new  sudo_straight ----------------------
    
    #make sure the NPE cut in sudo_straight is the same as CosmuonTagIntialization, so I can make the comparision
    cutflow5 =[MuonCut,MuonEventCut,mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,TBBigHitCut,TBBigHitCutCount,P_TBBigHitCut,P_TBBigHitCutCount,mycuts.sudo_straight]

    cutflow5A =[MuonEventCut,MuonEventCut,mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,TBBigHitCut,TBBigHitCutCount,P_TBBigHitCut,P_TBBigHitCutCount,mycuts.sudo_straight]

    cutflow5B =[mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,TBBigHitCut,TBBigHitCutCount,P_TBBigHitCut,P_TBBigHitCutCount,mycuts.sudo_straight]


    #---------------------workflow for only using the muon straight line cut------------
    #based on prior research, we concluded that we should use the muon straight line to tag muon event.
    #cutflow6 = [mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.sudo_straight,myplotter.dict['M_NPE'], myplotter.dict['M_adj_NPE']]


    

    cutflow6 = [mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.BarNPERatioCalculate,mycuts.NbarsHitsCount,mycuts.findCorrectTime,mycuts.sudo_straight,myplotter.dict['CorrectTime'],myplotter.dict['M_NPE'],myplotter.dict['M_adj_NPE'],myplotter.dict["NuniqueBar"],myplotter.dict["NPERatio"]]

    #------------------cut flow 7: finding the event that only one layer pass the cosmic muon straight tag------------

    cleanMuon_count = mycuts.getCut(mycuts.countEvent,'placeholder', Countobject= 'Clean_MuonEvent')
    clean_Muon_layer = mycuts.getCut(mycuts.combineCuts, 'clean_Muon_layer', ["MuonLayers","Clean_MuonEvent"])
    clean_Muon_adj_layer = mycuts.getCut(mycuts.combineCuts, 'clean_Muon_adj_layer', ["MuonADJLayers","Clean_MuonEvent"])
    
    cutflow7 = [mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.BarNPERatioCalculate,mycuts.NbarsHitsCount,mycuts.sudo_straight,clean_Muon_layer,clean_Muon_adj_layer,cleanMuon_count,mycuts.findCorrectTime,myplotter.dict['M_NPE_C'],myplotter.dict['M_adj_NPE_C'],myplotter.dict["NuniqueBar_C"],myplotter.dict["NPERatio_C"],myplotter.dict["CorrectTime_C"],myplotter.dict["CorrectTime_default"]]
    """

    #FIXME: I juse copy the script from Offline analysis to here. I need to clean up the code layer. 
    #FIXME: cutflow 7 from offline analysis
    cleanMuon_count = mycuts.getCut(mycuts.countEvent,'placeholder', Countobject= 'Clean_MuonEvent')
    clean_Muon_layer = mycuts.getCut(mycuts.combineCuts, 'clean_Muon_layer', ["MuonLayers","Clean_MuonEvent"])
    clean_Muon_adj_layer = mycuts.getCut(mycuts.combineCuts, 'clean_Muon_adj_layer', ["MuonADJLayers","Clean_MuonEvent"])
    clean_Muon_Dt = mycuts.getCut(mycuts.findCorrectTime, 'placeholder',cut = None,timeData = "time")
    M_NPE_C = r.TH1F("M_NPE_C", "nPE muon event layer", 100, 0, 100)
    M_adj_NPE_C = r.TH1F("M_adj_NPE_C", "nPE muon event adjacnet layer", 100, 0, 100)
    myplotter.addHistograms(M_NPE_C, 'nPE', 'clean_Muon_layer')
    myplotter.addHistograms(M_adj_NPE_C	, 'nPE', 'clean_Muon_adj_layer')
    NuniqueBar_C = r.TH1F("NuniqueBar_C" , "NuniqueBar;number of unique bar;events",50,0,50)
    myplotter.addHistograms(NuniqueBar_C, 'NBarsHits', 'Clean_MuonEvent')

    #npe ratio with hits from adjacent layers 
    #
    NpeRatio_adj = r.TH1F("NpeRatio_adj","NPE ratio;max NPE/min NPE;Events",5000,0,5000)
    NpeRatio_adj_tag= mycuts.getCut(mycuts.BarNPERatioCalculateV2, "NpeRatio_adj_tag",cut = "MuonADJLayers") 
    myplotter.addHistograms(NpeRatio_adj, 'NpeRatio_adj_tag', 'Clean_MuonEvent')

    #non- muon layer
    NpeRatio_ot_tag= mycuts.getCut(mycuts.BarNPERatioCalculateV2, "NpeRatio_ot_tag",cut = "MuonADJLayers")
    NpeRatio_ot = r.TH1F("NpeRatio_ot","NPE ratio;max NPE/min NPE;Events",5000,0,5000)
    myplotter.addHistograms(NpeRatio_ot, 'NpeRatio_ot_tag', 'Clean_MuonEvent')


    
    #extra histogram for Offline data
    CorrectTime_OL =  r.TH1F("CorrectTime_OL" , "D_t Max with correction w;D_t Max; Events",6000,-3000,3000)
    myplotter.addHistograms(CorrectTime_OL, 'DTL0L3', 'Clean_MuonEvent') 
    #CorrectTime_default_OL is to check what does CorrectTime should look like without the Clean muon cut
    CorrectTime_default_OL =  r.TH1F("CorrectTime_default_OL" , "D_t Max with correction w;D_t Max; Events",6000,-3000,3000)
    myplotter.addHistograms(CorrectTime_default_OL, 'DTL0L3', 'None_empty_event') 



    NPERatio_C = r.TH1F("NPERatio_C","NPE ratio;max NPE/min NPE;Events",5000,0,5000)
    myplotter.addHistograms(NPERatio_C, 'BarNPERatio', 'Clean_MuonEvent')
    #FIXME:mycuts.offlinePreProcess   this method cause the find correctTime crash 
    cutflow7 = [mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.BarNPERatioCalculate,mycuts.NbarsHitsCount,mycuts.sudo_straight,NpeRatio_adj_tag,NpeRatio_ot_tag,clean_Muon_layer,clean_Muon_adj_layer,cleanMuon_count,clean_Muon_Dt,myplotter.dict['M_NPE_C'],myplotter.dict['M_adj_NPE_C'],myplotter.dict["NuniqueBar_C"],myplotter.dict["NPERatio_C"],myplotter.dict["CorrectTime_OL"],myplotter.dict["CorrectTime_default_OL"],myplotter.dict["NpeRatio_adj"],myplotter.dict["NpeRatio_ot"]]    
    



    
    #-----------------------start of analysis---------------------------------------

    #-----------------------CustomFunction in MQprocessor---------------------------
    #CEhist = r.TH1F("hist", "CutEfficiency", 10, 0, 10) #histogram for making the cutefficiency
    
    """
    def makeCuteffPlot(events):
        Non_empty = ak.count_nonzero(events['None_empty_event'])
        NumTBBigHit=ak.count_nonzero(events["TBBigHit"])
        NumP_TBBigHit=ak.count_nonzero(events["P_TBBigHit"])
        
        
        for i in range(Non_empty):
            CEhist.Fill(0)

        for i in range(NumTBBigHit):
            CEhist.Fill(1)
        
        for i in range(NumP_TBBigHit):
            CEhist.Fill(2)

        CEhist.GetXaxis().SetBinLabel(1, "None_empty_event")
        CEhist.GetXaxis().SetBinLabel(2, "TBBigHit")
        CEhist.GetXaxis().SetBinLabel(3, "P_TBBigHit")
    """
        



    
    #note cutflow 1-3 are checked
    
    cutflow = cutflow7

    myschedule = milliQanScheduler(cutflow, mycuts)

    myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts)

    #myiterator.setCustomFunction(makeCuteffPlot) #I don't want to make the cut efficiency plot for now

    #myiterator.run() #use this one in condor job
    
    #f_out = r.TFile("test.root", "RECREATE") #FIXME: this is use for test only!
    #CEhist.Write()
    #f_out.Close()
    #--------------section for using to check cut efficiency(please use this one by default)-----------------------------
    #"""
    if outputPath == '':
        myiterator.run()

    #output result to txt file
    else:
        with open(f'{outputPath}/Run{numRun}CutFlow7.txt', 'w') as cfFile:
            sys.stdout = cfFile  # Change the standard output to the file
            myiterator.run() #output from counting function will be saved in the txt file above.



        # After the block, stdout will return to its default (usually the console)
        # reset stdout to its original state
        sys.stdout = sys.__stdout__
        #"""
        f_out = r.TFile(f"{outputPath}/Run{numRun}CutFlow7.root", "RECREATE")
        M_adj_NPE_C.Write()
        M_NPE_C.Write()
        NPERatio_C.Write()
        CorrectTime_C.Write()
        NuniqueBar_C.Write()
        CorrectTime_default.Write()
        f_out.Close()
        
        #"""
   
        #-------------------------------------output histograms and save in root file. Please comment it out if you dont need it------------------------------------------------

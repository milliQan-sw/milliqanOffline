#this file is created based on SimMuon_tag.py & muonTagPlot.py. But it can work with offline offline utilies
#TBD add pulse based plot & event based plot with MilliqanPlotter & Check TBD
#get the muon hit after the empty check.
#The row constrain for making plots is not implement yet

import math


import os
import sys
import time
import json

sys.path.append("/home/czheng/milliqanOffline/Run3Detector/analysis/utilities/")

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
        adjlay = []
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
            specialArr[b] = specialArr[b][(specialArr.layer ==0 & layer0Cut)|(specialArr.layer ==1  & layer1Cut)  | ( specialArr.layer == 2 & layer2Cut) | (specialArr.layer == 3 & layer3Cut)]
        return specialArr
    
    for b in branches:
        if branch == 'boardsMatched' or branch == "runNumber" or branch == "fileNumber" or branch == "event": continue
        #ideally, layer0Cut should be = spcialArr.LayX == X(current layer0Cut if true for an event)


        specialArr[b] = specialArr[b][(specialArr.layer ==0 & layer0Cut)|(specialArr.layer ==1  & layer1Cut)  | ( specialArr.layer == 2 & layer2Cut) | (specialArr.layer == 3 & layer3Cut)]
    
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


#bar trim should be used prior using this one
#FIXME: remove the hist arguemtn if I can't make the histogram with milliqanCut
def NbarsHitsCount(self,cutName = "NBarsHits",cut = None, hist = None):

    bararr = ak.copy(self.events)



    if cut:
        cutMask, junk = ak.broadcast_arrays(bararr.cut, bararr.layer)

        uniqueBarArr = ak.Array([np.unique(x) for x in bararr.chan[cutMask]])
        self.events[cutName] = ak.count(uniqueBarArr,axis = 1)
    else:
        uniqueBarArr = ak.Array([np.unique(x) for x in bararr.chan])
        self.events[cutName] = ak.count(uniqueBarArr, axis = 1)
        print(self.events[cutName])
        print(self.events.fields)
    
    if hist:
        bararr = ak.flatten(self.events[cutName],axis=None)
        hist.FillN(len(bararr), bararr, np.ones(len(bararr)))

def NbarsHitsCountV2(self,arr, hist):
    for b in barbraches:
        arr[b] = arr[b][arr.type == 0]

    uniqueBarArr = ak.Array([np.unique(x) for x in arr.chan])
    uniqueBarArr = ak.drop_none[uniqueBarArr]
    uniqueBarArr = ak.flatten(uniqueBarArr,axis=None)
    hist.FillN(len(uniqueBarArr), uniqueBarArr, np.ones(len(uniqueBarArr)))



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
        self.events["TopPanelHit"] = ak.any(self.events["row"]==4 & (self.events["area"]/(1320*12)) >= NPEcut ,axis =1)
    else:
        self.events["TopPanelHit"] = ak.any((self.events["row"]==4) & (self.events["nPE"]/12 >= NPEcut), axis = 1)

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
def TBBigHit(self,cutName = None,cut = None, Hist1 = None):
    
    TBBigHit_lay0 =  (ak.any(self.events.l0R0==True, axis=1) & ak.any(self.events.l0R3==True, axis=1)) #data at layer 0 should be kept
    TBBigHit_lay1 =  (ak.any(self.events.l1R0==True, axis=1) & ak.any(self.events.l1R3==True, axis=1))
    TBBigHit_lay2 =  (ak.any(self.events.l2R0==True, axis=1) & ak.any(self.events.l2R3==True, axis=1))
    TBBigHit_lay3 =  (ak.any(self.events.l3R0==True, axis=1) & ak.any(self.events.l3R3==True, axis=1))
    


    self.events["TBBigHit"] = (TBBigHit_lay0 | TBBigHit_lay1 | TBBigHit_lay2 | TBBigHit_lay3) 

    
    if cut: self.events = self.events[self.events["TBBigHit"]]

    #plot section
    if Hist1:
        #convert the events based tag to pulse(bar based in sim) based
        #FIXME:this steps seems has bugs. It can't tell which data to keep. Intead it it keep all data as long as one of the layer get hit. 

        TBBigHit_lay0, junk=ak.broadcast_arrays(TBBigHit_lay0, self.events.layer)
        TBBigHit_lay1, junk=ak.broadcast_arrays(TBBigHit_lay1, self.events.layer)
        TBBigHit_lay2, junk=ak.broadcast_arrays(TBBigHit_lay2, self.events.layer)
        TBBigHit_lay3, junk=ak.broadcast_arrays(TBBigHit_lay3, self.events.layer)





        #constraintArray is to save the data from the layer where pass the cosmic muon tag or the data from the ajacent array. Or you could use layerConstraintEnable = False which return the copy array without changing anything
        constraintArray=self.LayerContraint(TBBigHit_lay0,TBBigHit_lay1,TBBigHit_lay2,TBBigHit_lay3)
        self.NbarsHitsCountV2(arr=constraintArray,hist=Hist1)


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
    self.events=self.events[self.events.None_empty_event]#this one can cause milliqanplotter unable to work. I haven't figure out the cuase yet.


#tag muon event (sim only)
def MuonEvent(self, cutName = None, CutonBars = True, branches = None):

    if CutonBars:
        for branch in branches:
            if branch == 'boardsMatched' or branch == "runNumber" or branch == "fileNumber" or branch == "event": continue
            self.events[branch] = self.events[branch][self.events.muonHit == 1]

    #cut on events
    else:
        self.events = self.events[ak.any(self.events.muonHit == 1, axis = 1)]

#the default behaviour is to count the number of events that has data.
def countEvent(self, cutName = None, Countobject='None_empty_event', debug = False):
    if debug: 
        print(ak.to_pandas(self.events))
    if cutName:
        print(f"{Countobject} event: {len(self.events[self.events[Countobject]])}")
    else:
        print(f"current available events : {len(self.events['event'])}")


#the EmptyListFilter() has a weird bug that can cause the milliqanplotter unable to work. So the current solution for doing analysis without looping over the empty 
#FIXME: check does it work? if not then use the milliqancut
def SimPanelCut(self):
    PanelDefault=self.events['type'] == 2
    self.events['barCut'] = PanelDefault & self.events["None_empty_event"]

def SimBarCut(self):
    barCutdefault=self.events['type'] == 0
    self.events['barCut'] = barCutdefault & self.events["None_empty_event"]


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

    #filelist =['/mnt/hadoop/se/store/user/czheng/SimFlattree/withPhotonMuontag/output_1.root:t']
    filelist =[f'{filename}:t']
    """

    #----------------------------------------------------------------------------------------------------------------------------------- OSU T3
    #signle file test
    #numRun = 1
    #filelist =[f'/mnt/hadoop/se/store/user/czheng/SimFlattree/withPhotonMuontag/output_{numRun}.root:t']


    #------------------------------------------------------------------------------------------------
    #path for the milliqan machine

    #print("this is numRun" + str(sys.argv[1]) )


    numRun = str(sys.argv[1])
    filelist =[f'/home/czheng/SimCosmicFlatTree/withPhotonMuontag/output_{numRun}.root:t']
    print(filelist)

    outputPath = str(sys.argv[2]) # the path is used at the very end for the output txt file
    print(outputPath)
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
    branches = ["chan","runNumber","event","layer","nPE","type","row","muonHit"]

    #test cut flow. Check if the mask can be made
    #cutflow = [mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,mycuts.fourRowBigHits,mycuts.TBBigHit,mycuts.P_TBBigHit,mycuts.P_BBigHit]



    #"placeholder" is use in cutName argument. This argument is useless in some of the methods but to make the "getCut" work I need to use the  
    fourRowBigHitsCut = mycuts.getCut(mycuts.fourRowBigHits, "fourRowBigHitsCut",cut=True)
    TBBigHitCut = mycuts.getCut(mycuts.TBBigHit,"placeholder", cut = True)
    P_TBBigHitCut= mycuts.getCut(mycuts.P_TBBigHit, "P_TBBigHitCut",cut = True)
    P_BBigHitCut= mycuts.getCut(mycuts.P_BBigHit, "P_BBigHitCut",cut = True)
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

    #FIXME: for some unknow reason the code at below unable to work, since the mask I created can't be accessed by milliqan for some unknown reason. If I can't figure out the solution, then they should be deleted.
    """
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
    """
    #it seems currently creating a combined mask can retrieve the data
    mask0 = mycuts.getCut(mycuts.combineCuts, 'mask0', ['fourRowBigHits'])
    mask1 = mycuts.getCut(mycuts.combineCuts, 'mask1', ['TBBigHit'])
    mask2 = mycuts.getCut(mycuts.combineCuts, 'mask2', ['P_TBBigHit'])
    mask3 = mycuts.getCut(mycuts.combineCuts, 'mask3', ['P_BBigHit'])
    

    #-------------------------cutflows-----------------------------------------------------------

    #Cut flow 1. This one is for testing the cut efficiency of different tags. TB big hits - > TB + panel big hits 
    cutflow1 = [MuonCut,mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,TBBigHitCut,TBBigHitCutCount,P_TBBigHitCut,P_TBBigHitCutCount]
    
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

    cutflow = cutflow1

    myschedule = milliQanScheduler(cutflow, mycuts,myplotter)

    myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts)

    

    #--------------section for using to check cut efficiency-----------------------------

    if outputPath == '':
        myiterator.run()

    #output result to txt file
    else:
        with open(f'{outputPath}/Run{numRun}CutFlow3A.txt', 'w') as cfFile:
            sys.stdout = cfFile  # Change the standard output to the file
            myiterator.run() #output from counting function will be saved in the txt file above.



        # After the block, stdout will return to its default (usually the console)
        # reset stdout to its original state
        sys.stdout = sys.__stdout__



    #-------------------------------------output histograms and save in root file. Please comment it out if you dont need it------------------------------------------------

    """
    #f_out = r.TFile(f"Run{numRun}TagV2_condorJob.root", "RECREATE")
    #f_out = r.TFile(f"Run{numRun}TagV2_testOnly.root", "RECREATE")
    #f_out.cd()
    """

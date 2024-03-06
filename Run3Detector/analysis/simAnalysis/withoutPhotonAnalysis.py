#data used for this analysis are from scintillator branch

import math
import os
import sys

sys.path.append("/share/scratch0/czheng/sim_uproot/milliqanOffline/Run3Detector/analysis/utilities/")

from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *

#filelist =['/mnt/hadoop/se/store/user/czheng/SimFlattree/withoutPhoton/output_226.root:t']
filelist =['/mnt/hadoop/se/store/user/czheng/SimFlattree/withPhoton/output_810.root:t']
"""
filelist = []

def appendRun(filelist):
    directory = "/mnt/hadoop/se/store/user/czheng/SimFlattree/withoutPhoton/"
    for filename in os.listdir(directory):
        if filename.startswith("output") and filename.endswith(".root"):
            filelist.append(directory+filename+":t")


appendRun(filelist)
"""



branches = ['nPE','layer','chan','time','type','event','runNumber']

barbranches = ['nPE','layer','chan','time','type']

mycuts = milliqanCuts()

myplotter = milliqanPlotter()

#create root histogram 
h_NPE = r.TH1F("nPE", "nPE", 500, 0, 1000)

#add root histogram to plotter
myplotter.addHistograms(h_NPE, 'nPE', 'eventCuts')




#-------------------------extra functions for doing analysis on "NPE" branch-------------------------------------
def LayerCut(self, cutName=None):
    self.events['layer0'] = self.events['layer'] == 0
    self.events['layer1'] = self.events['layer'] == 1
    self.events['layer2'] = self.events['layer'] == 2
    self.events['layer3'] = self.events['layer'] == 3




def geometricCutSIM(self, cutName=None, cut=False):

    self.events['layer0_bar'] = self.events['layer0']  & self.events['barCut']
    self.events['layer1_bar'] = self.events['layer1']  & self.events['barCut']
    self.events['layer2_bar'] = self.events['layer2']  & self.events['barCut']
    self.events['layer3_bar'] = self.events['layer3']  & self.events['barCut']
    
    

    self.events['fourLayerCutSIM'] =(ak.any(self.events.layer0_bar==True, axis=1) & 
                                    ak.any(self.events.layer1_bar==True, axis=1) & 
                                    ak.any(self.events.layer2_bar==True, axis=1) & 
                                    ak.any(self.events.layer3_bar==True, axis=1))
    
    self.events.layer0_bar = self.events['layer0_bar'][self.events.barCut]
    #After applying the mask at above, for each event, the size of layer0_bar is equal the number of unique bars channels get hit.
    self.events['oneHitPerLayerCutSIM'] =((ak.count(self.events.layer0_bar, axis=1)==4) & 
                                    self.events['fourLayerCutSIM'])




    if cut:
        self.events=self.events[self.events['oneHitPerLayerCutSIM']]







def CosmicVetoSIM(self, cutName=None, cut=False):
    self.events['CosmicVetoSIM'] =~((ak.any(self.events.type==2, axis=1))) 

    if cut:
        self.events=self.events[self.events['CosmicVetoSIM']]




#if the summing bar NPE of two beam panels is larger than 50Npe, then return false
def BeamVeto (self,cutName=None,cut=False,heightCut = 50):
    self.events['BeamVeto'] = ~(ak.sum(self.events.nPE[self.events.type==1], axis=1) >= heightCut)

    if cut:
        self.events=self.events[self.events['BeamVeto']]

def NPERatioCut(self,cutName = None,cut = False):

    #remove the none-bar data, so Nan will not exist inside BarNPERatio.
    for branch in barbranches:
        self.events[branch] = self.events[branch][self.events.barCut]

    EmptyCuts= ak.num(self.events['type']) > 0
    self.events = self.events[EmptyCuts]

    self.events['BarNPERatio'] = ((ak.max(self.events.nPE[self.events.type==0],axis=1)/ak.min(self.events.nPE[self.events.type==0],axis=1)) <= 10) & self.events['oneHitPerLayerCutSIM']

    if cut:
        self.events=self.events[self.events['BarNPERatio']]

def timeCutManipulation(Lay0Time,Lay1Time,Lay2Time,Lay3Time):
    if len(Lay0Time) == 0 or len(Lay1Time) == 0 or len(Lay2Time) == 0 or len(Lay3Time) == 0:
        return False
    dT = 3.96 #The shortest time for photon travel 1 bar scitillator + 1 air gap between two bars.
    Time = []
    for time0 in Lay0Time:
        Time.append(time0)
    for time1 in Lay1Time:
        Time.append(time1-dT)
    for time2 in Lay2Time:
        Time.append(time2-2*dT)
    for time3 in Lay3Time:
        Time.append(time3-3*dT)
    if any(num < 0 for num in Time):
        return False 
    print(f"correct time diff {max(Time)-min(Time)}")
    return max(Time)-min(Time) <= 15.09

#
def CorrectTimeCut(self,cutName = None):
    if len(self.events) == 0: return
    Timelist = ak.to_list(self.events.time)
    Layerlist = ak.to_list(self.events.layer)
    typelist = ak.to_list(self.events.type)
    nPElist = ak.to_list(self.events.nPE)
    eventIDlist = ak.to_list(self.events.event)
    runNumberlist = ak.to_list(self.events.runNumber)
    

    NumEvents = len(Layerlist)
    #things inside the sublist are the data within a single event
    i = 0
    for Timesublist,Layersublist in zip(Timelist,Layerlist):
        
        if len(Timesublist) == len(Layersublist):
            NPECut = True
            TimeCut = False 
            Lay0time = list()
            Lay1time = list()
            Lay2time = list()
            Lay3time = list()
            for j,time in enumerate(Timesublist):
                if (typelist[i][j] == 0) and (nPElist[i][j] >=1):

                    if Layersublist[j] == 0:
                        Lay0time.append(time)
                    if Layersublist[j] == 1:
                        Lay1time.append(time)
                    if Layersublist[j] == 2:
                        Lay2time.append(time)
                    if Layersublist[j] == 3:
                        Lay3time.append(time)

            TimeCut=timeCutManipulation(Lay0time,Lay1time,Lay2time,Lay3time)

            if TimeCut:

                print(f"signal like event is found! run number: {runNumberlist[i]} event: {eventIDlist[i]}")

        
        else:
            print(f"issue occur at run {self.events.runNumber[i]} event {self.events.event[i]}" )

        i +=1
        


    

def NPEcut(self, cutName=None, nPECutT=1):
    NPEcuts = self.events.nPE>=nPECutT
    for branch in barbranches:
        self.events[branch] = self.events[branch][NPEcuts]


#create a mask for bar channels
def barCutSim(self, cutName=None, cut=False):
    self.events['barCut'] = self.events.type==0


#remove the empty events
def EmptyListFilter(self,cutName=None):

    self.events['None_empty_event'] = ak.num(self.events['layer']) > 0
    self.events=self.events[self.events.None_empty_event]
    


def begin(self,cutName = None):
    print(f"analysis on file {set(self.events.runNumber)} starts")

#check how many events can pass geometric cuts
def printEvents(self, cutName=None):

    print("four layers cut :" + str(len(self.events[self.events.fourLayerCutSIM])))    
    Num1HITPL=self.events[self.events.oneHitPerLayerCutSIM]
    print("one hit per layer cut :" + str(len(Num1HITPL)))
    if len(Num1HITPL) >= 1:
        print(f"found it at EventID {Num1HITPL.event}  file {set(Num1HITPL.runNumber)}")



#reduce the size of the array and check how many events can pass NPE ratio cut
def furtherTrim(self,cutName=None):
    self.events = self.events[self.events.BarNPERatio]
    print("NPE ratio cut :" + str(len(self.events)))

def selectEvent(self,cutName =None, evenNum=6800):
    self.events = self.events[self.events.event == evenNum]

def applyCut(self,cutName):
    self.events = self.events[self.events[cutName]]

def countEvent(self, cutName = None, Countobject=None, debug = False):
    if debug: 
        print(ak.to_pandas(self.events))
    if cutName:
        print(f"{Countobject} event: {len(self.events[self.events[Countobject]])}")
    else:
        print(f"current available events : {len(self.events)}")


#-----------------------------------------------------------------------------------------------------------------
setattr(milliqanCuts, 'selectEvent', selectEvent)

setattr(milliqanCuts, 'EmptyListFilter', EmptyListFilter)

setattr(milliqanCuts, 'CosmicVetoSIM', CosmicVetoSIM)

setattr(milliqanCuts, 'BeamVeto', BeamVeto)

setattr(milliqanCuts, 'geometricCutSIM', geometricCutSIM)

setattr(milliqanCuts, 'LayerCut', LayerCut)

setattr(milliqanCuts, 'barCutSim', barCutSim)

setattr(milliqanCuts, 'NPERatioCut',NPERatioCut)

setattr(milliqanCuts, 'CorrectTimeCut' ,CorrectTimeCut)

setattr(milliqanCuts,'printEvents',printEvents)

setattr(milliqanCuts,'NPEcut',NPEcut)

setattr(milliqanCuts,'furtherTrim',furtherTrim)

setattr(milliqanCuts,'begin',begin)

setattr(milliqanCuts,'countEvent',countEvent)

setattr(milliqanCuts,'applyCut',applyCut)


fourRowBigHitsCut = mycuts.getCut(mycuts.geometricCutSIM, "placeholder",cut=False) #After using one hit per layer cut, majority of events that pass four layer will be removed. So, to count the four layer events I can't apply the one hit per layer cut at here. 
ApplyoneHitperlayerCut =mycuts.getCut(mycuts.applyCut,"oneHitPerLayerCutSIM")
CosmicPanelsCut = mycuts.getCut(mycuts.CosmicVetoSIM,"placeholder",cut=False)
BeamVetoCut = mycuts.getCut(mycuts.BeamVeto,"placeholder",cut=True)
NPERatioCut = mycuts.getCut(mycuts.NPERatioCut,"placeholder",cut=True)








FourLayersCount= mycuts.getCut(mycuts.countEvent, "placeholder" ,Countobject = "fourLayerCutSIM")
OneHitperLayerCutCount= mycuts.getCut(mycuts.countEvent, "placeholder" ,Countobject = "oneHitPerLayerCutSIM")
CosmicVetoSIMCutCount= mycuts.getCut(mycuts.countEvent,"placeholder"  ,Countobject = "CosmicVetoSIM")
BeamVetoCutCount= mycuts.getCut(mycuts.countEvent, "placeholder" ,Countobject = "BeamVeto")
BarNPERatioCutCount= mycuts.getCut(mycuts.countEvent, "placeholder" ,Countobject = "BarNPERatio")




# withoutphoton sim analysis cutflow

#the NPEcut is used to determine how many nPE can be treated as a hit. data from pulse(offline) or bar(sim) nPE lower the the threashold nPECutT will be removed.
#printEvents is to find the number of event that pass first two geometric cuts.

#furtherTrim: reduce the size of the array and check how many events can pass NPE ratio cut

#FIXME: fix cutflow, for some unknow reason things after "begin" stop working
cutflow = [mycuts.begin,mycuts.countEvent,mycuts.EmptyListFilter,mycuts.NPEcut,mycuts.barCutSim,mycuts.LayerCut, fourRowBigHitsCut,FourLayersCount,OneHitperLayerCutCount,ApplyoneHitperlayerCut,CosmicPanelsCut,CosmicVetoSIMCutCount,BeamVetoCut,BeamVetoCutCount,NPERatioCut,BarNPERatioCutCount,mycuts.furtherTrim,mycuts.CorrectTimeCut]

myschedule = milliQanScheduler(cutflow, mycuts)


myschedule.printSchedule()


myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts)

myiterator.run()

print("test")





"""
2-5 it seems the counter in milliqan Cut is not finished, so I make one for myself
How does it going to work?
1. check if a event pass multiple cuts, it should work like 


def Counter(self, NumEvents, cuts):
    for cut in cuts:
        self.events = self.events[cut]

eg how can I count the cosveto?

passEvents = len(self.events["cosveto"])


milliqanCut.py require a new init variable with {BranchName for checking the event: Eventpass}

+ extra result print result in dict 


issue two: it will be great to let geometric cuts to change into NPE_branch when doing sim analysis

#creating cosmic cut to

create the branch name corrected, copy the data from time branch

event["correctTime"] = even["time"][event["layer"]==1] -ndT


how to include "event" inside th branch and apply the pulse based cut?
I need to event & file number to trace the interesting event. I can use them to do further exploration with the raw root file.
for branch in ["height", "area","layer","time"]:
    branches[branch]=branches[branch][lay0Cut]



File "/share/scratch0/czheng/sim_uproot/milliqanOffline/Run3Detector/analysis/utilities/simDemo.py", line 223, in probabilityTrim
self.events.pmt_nPE_p=1-math.exp(-1* self.events.pmt_nPE)
TypeError: must be real number, not Array

def probabilityTrim(self,cutName = None):

self.events.pmt_nPE_p=1-math.exp(-1* self.events.pmt_nPE)




"""
import math


import os
import sys

sys.path.append("/share/scratch0/czheng/sim_uproot/milliqanOffline/Run3Detector/analysis/utilities/")

from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *

filelist =['/mnt/hadoop/se/store/user/czheng/SimFlattree/withPhoton/output_1.root:t']

branches = ['pmt_nPE','pmt_layer','pmt_chan','pmt_time','pmt_type','event','runNumber']

barbranches = ['pmt_nPE','pmt_layer','pmt_chan','pmt_time','pmt_type']

mycuts = milliqanCuts()

myplotter = milliqanPlotter()

#create root histogram 
h_NPE = r.TH1F("nPE", "nPE", 500, 0, 1000)

#add root histogram to plotter
myplotter.addHistograms(h_NPE, 'pmt_nPE', 'eventCuts')




#-------------------------extra functions for doing analysis on "NPE" branch-------------------------------------
def LayerCut(self, cutName=None, cut=False, branches=None):
    self.events['layer0'] = self.events['pmt_layer'] == 0
    self.events['layer1'] = self.events['pmt_layer'] == 1
    self.events['layer2'] = self.events['pmt_layer'] == 2
    self.events['layer3'] = self.events['pmt_layer'] == 3

    if cut:
        branches.append('layer1')
        for branch in branches:
            self.events[branch] = self.events[branch][LayerCuts]

"""
def geometricCut_count(self,cutName = None):

    print(ak.to_list(self.events[self.events.fourLayerCutSIM])
"""



def geometricCutSIM(self, cutName=None, cut=False):
    #"""
    self.events['layer0_bar'] = self.events['layer0']  & self.events['barCut']
    self.events['layer1_bar'] = self.events['layer1']  & self.events['barCut']
    self.events['layer2_bar'] = self.events['layer2']  & self.events['barCut']
    self.events['layer3_bar'] = self.events['layer3']  & self.events['barCut']
    
    

    self.events['fourLayerCutSIM'] =(ak.any(self.events.layer0_bar==True, axis=1) & 
                                    ak.any(self.events.layer1_bar==True, axis=1) & 
                                    ak.any(self.events.layer2_bar==True, axis=1) & 
                                    ak.any(self.events.layer3_bar==True, axis=1))

    self.events['oneHitPerLayerCutSIM'] =((ak.count(self.events.layer0_bar, axis=1)==4) & 
                                    self.events['fourLayerCutSIM'])
    #"""
    """
    self.events['fourLayerCutSIM'] =(ak.any(self.events.pmt_layer==0, axis=1) & 
                                      ak.any(self.events.pmt_layer==1, axis=1) & 
                                      ak.any(self.events.pmt_layer==2, axis=1) & 
                                      ak.any(self.events.pmt_layer==3, axis=1))


    self.events['oneHitPerLayerCutSIM'] =((ak.count(self.events.pmt_layer, axis=1)==4) & self.events['fourLayerCutSIM'])
    """


    if cut:
        self.events=self.events[self.events['oneHitPerLayerCutSIM']]







def CosmicVetoSIM(self, cutName=None, cut=False):
    self.events['CosmicVetoSIM'] =not((ak.count(self.events.pmt_chan==68, axis=1)>=1) | 
                                (ak.count(self.events.pmt_chan==72, axis=1)>=1) |
                                (ak.count(self.events.pmt_chan == 70, axis=1)>=1) |
                                (ak.count(self.events.pmt_chan == 69, axis=1)>=1) |
                                (ak.count(self.events.pmt_chan == 74, axis=1)>=1) |
                                (ak.count(self.events.pmt_chan == 73, axis=1)>=1))






#if the summing bar NPE of two beam panels is larger than 50Npe, then return false
def BeamVeto (self,cutName=None,heightCut = 50):
    self.events['BeamVeto'] = not (ak.sum(self.events.pmt_nPE[self.events.pmt_type==1], axis=1) >= heightCut)

def NPERatioCut(self,cutName = None):

    #remove the none-bar data, so Nan will not exist inside BarNPERatio
    for branch in barbranches:
        self.events[branch] = self.events[branch][self.events.barCut]
    print(ak.to_list(self.events['oneHitPerLayerCutSIM']))
    #remove the empty event
    EmptyCuts= ak.num(self.events['pmt_type']) > 0
    self.events = self.events[EmptyCuts]

    self.events['BarNPERatio'] = ((ak.max(self.events.pmt_nPE[self.events.pmt_type==0],axis=1)/ak.min(self.events.pmt_nPE[self.events.pmt_type==0],axis=1)) <= 10) & self.events['oneHitPerLayerCutSIM']
    print("BarNPERatio tag:" + str(ak.to_list(self.events['BarNPERatio'])))
    #print(ak.to_list(((ak.max(self.events.pmt_nPE[self.events.pmt_type==0],axis=1)/ak.min(self.events.pmt_nPE[self.events.pmt_type==0],axis=1)) <= 10)))
    #print("event number" + str(ak.to_list(self.events.event)))
    #print("npe list:"+ str(ak.to_list(self.events.pmt_nPE)))
    #print(ak.to_pandas(self.events))
    #print(ak.to_list(self.events['BarNPERatio']))   

#reprocess the tree such that it come with correct time.
#Don't recreate the tree. wait until I finish the the cut validation for cuts at above.

#correct time cut should be used only after apply one hit per layer cut(reduced the size of array)


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
    return max(Time)-min(Time) <= 15.09

#
def CorrectTimeCut(self,cutName = None):
    if len(self.events) == 0: return
    print(self.events)
    Timelist = ak.to_list(self.events.pmt_time)
    Layerlist = ak.to_list(self.events.pmt_layer)
    typelist = ak.to_list(self.events.pmt_type)
    nPElist = ak.to_list(self.events.pmt_nPE)
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
                #pass
                print(f"found it! run number: {runNumberlist[i]} event: {eventIDlist[i]}")
                #save the runNumber and event to txt file

            
            
        else:
            print(f"issue occur at run {self.events.runNumber[i]} event {self.events.event[i]}" )

        i +=1
        


    

def NPEcut(self, cutName=None, cut=False):
    NPEcuts = self.events.pmt_nPE>=1
    for branch in barbranches:
        self.events[branch] = self.events[branch][NPEcuts]


def barCutSim(self, cutName=None, cut=False):

    self.events['barCut'] = self.events.pmt_type==0



#We want to remove the empty empty event and the empty instance inside an event
def EmptyListFilter(self,cutName=None):
    #remove empty events
    self.events['None_empty_event'] = ak.num(self.events['pmt_layer']) > 0
    #print(ak.to_list(self.events.None_empty_event))
    #print(ak.to_list(self.events.pmt_layer))
    #print(ak.to_pandas(self.events))
    self.events=self.events[self.events.None_empty_event]
    
    #print(ak.to_pandas(self.events))
    #check if empty instance exist
    #print(ak.to_list(self.events))
    #print(ak.to_list(self.events.layer))
    """
    condition = self.events['layer'] ==1
    #self.events = self.events[condition]
    for branch in ak.fields(self.events):
        self.events[branch] = self.events[branch][condition]
    """
    #return self.events

def printEvents(self, cutName=None):
    print(len(self.events))
    #print(ak.to_pandas(self.events[self.events.fourLayerCutSIM]))
    #print(ak.to_list(self.events[self.events.fourLayerCutSIM]))
    #print(ak.to_list(self.events))
    
    print(len(self.events[self.events.fourLayerCutSIM]))#the way to count the event
    print(len(self.events[self.events.oneHitPerLayerCutSIM]))
    
    #print(ak.count(self.events[self.events.fourLayerCutSIM]))


def furtherTrim(self,cutName=None):
    print(ak.to_pandas(self.events))
    #print(ak.to_list(self.events.BarNPERatio)) #FIXME: it has None. 
    self.events = self.events[self.events.BarNPERatio]
    #print(ak.to_list(self.events.event))
    #print(ak.to_list(self.events.BarNPERatio))
    #print(ak.to_pandas(self.events))


#-----------------------------------------------------------------------------------------------------------------
setattr(milliqanCuts, 'EmptyListFilter', EmptyListFilter)

setattr(milliqanCuts, 'CosmicVetoSIM', CosmicVetoSIM)

setattr(milliqanCuts, 'geometricCutSIM', geometricCutSIM)

setattr(milliqanCuts, 'LayerCut', LayerCut)

setattr(milliqanCuts, 'barCutSim', barCutSim)

setattr(milliqanCuts, 'NPERatioCut',NPERatioCut)

setattr(milliqanCuts, 'CorrectTimeCut' ,CorrectTimeCut)

setattr(milliqanCuts,'printEvents',printEvents)

setattr(milliqanCuts,'NPEcut',NPEcut)

setattr(milliqanCuts,'furtherTrim',furtherTrim)

#setattr(milliqanCuts, 'probabilityTrim' ,probabilityTrim)

#setattr(milliqanCuts, 'geometricCut_count' , geometricCut_count)

#R_fourlayer = mycuts.getCut(mycuts.combineCuts, 'R_fourlayer', ['barCut','fourLayerCutSIM'])
#R_OneHitperLayer = mycuts.getCut(mycuts.combineCuts, 'R_OneHitperLayer', ['barCut','oneHitPerLayerCutSIM'])


#print(myplotter.dict)
#things inside dict are the name of histogram not the the histogram variable. eg here the name of histogram is nPE


#cutflow = [mycuts.LayerCut,eventCuts,myplotter.dict['nPE']]
#cutflow = [mycuts.barCutSim, mycuts.fourLayerCutSIM,mycuts.oneHitPerLayerCutSIM,R_fourlayer,R_OneHitperLayer]

#sample of withphoton sim analysis cutflow
#I applied the geometric & NPE cut at 
cutflow = [mycuts.EmptyListFilter,mycuts.NPEcut,mycuts.barCutSim,mycuts.LayerCut, mycuts.geometricCutSIM,mycuts.NPERatioCut,mycuts.printEvents,mycuts.furtherTrim,mycuts.CorrectTimeCut]


#debug cutflow. 
#cutflow = [mycuts.EmptyListFilter,mycuts.barCutSim,mycuts.LayerCut ,mycuts.geometricCutSIM,mycuts.printEvents]

#cutflow = [mycuts.EmptyListFilter]
myschedule = milliQanScheduler(cutflow, mycuts)


myschedule.printSchedule()


#in the demo mycuts, myplotter arguements are useless now
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts)

myiterator.run()






#output_file = r.TFile("run99_NPEL1.root", "RECREATE")
#h_NPE.Write()
#output_file.Close()

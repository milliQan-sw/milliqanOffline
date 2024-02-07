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

"""



import os
import sys

sys.path.append("/share/scratch0/czheng/sim_uproot/milliqanOffline/Run3Detector/analysis/utilities/")

from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *

filelist =['/share/scratch0/czheng/cosmicSimFlatTree/output_2.root:t']

branches = ['pmt_nPE','pmt_layer','pmt_chan','layer']

mycuts = milliqanCuts()

myplotter = milliqanPlotter()

#create root histogram 
h_NPE = r.TH1F("nPE", "nPE", 500, 0, 1000)

#add root histogram to plotter
myplotter.addHistograms(h_NPE, 'pmt_nPE', 'eventCuts')




#-------------------------extra functions for doing analysis on "NPE" branch-------------------------------------
def LayerCut(self, cutName=None, cut=False, branches=None):
    self.events['layer1'] = self.events['pmt_layer'] == 1

    if cut:
        branches.append('layer1')
        for branch in branches:
            self.events[branch] = self.events[branch][LayerCuts]


def fourLayerCutSIM(self, cutName=None, cut=False):
    self.events['fourLayerCutSIM'] =(ak.any(self.events.pmt_layer==0, axis=1) & 
                                    ak.any(self.events.pmt_layer==1, axis=1) & 
                                    ak.any(self.events.pmt_layer==2, axis=1) & 
                                    ak.any(self.events.pmt_layer==3, axis=1))

def oneHitPerLayerCutSIM(self, cutName=None, cut=False):
    self.events['oneHitPerLayerCutSIM'] =((ak.count(self.events.pmt_layer==0, axis=1)==1) & 
                                        (ak.count(self.events.pmt_layer==1, axis=1)==1) & 
                                        (ak.count(self.events.pmt_layer==2, axis=1)==1) &
                                        (ak.count(self.events.pmt_layer==3, axis=1)==1))


def CosmicVetoSIM(self, cutName=None, cut=False):
    self.events['CosmicVetoSIM'] =not((ak.count(self.events.pmt_chan==68, axis=1)>=1) | 
                                (ak.count(self.events.pmt_chan==72, axis=1)>=1) |
                                (ak.count(self.events.pmt_chan == 70, axis=1)>=1) |
                                (ak.count(self.events.pmt_chan == 69, axis=1)>=1) |
                                (ak.count(self.events.pmt_chan == 74, axis=1)>=1) |
                                (ak.count(self.events.pmt_chan == 73, axis=1)>=1))

#if the summing bar NPE of two beam panels is larger than 50Npe, then return false
def BeamVeto (self,cutName=None,heightCut = 50):
    self.events['BeamVeto'] = not (ak.sum(self.events.pmt_nPE[self.events.pmt_chan==75 | self.events.pmt_chan==71], axis=1) >= heightCut)

def NPECut(self,cutName = None):
    self.events['BarNPERatio'] = (ak.max(self.events.pmt_nPE[self.events.pmt_chan<=64],axis=1)/ak.min(self.events.pmt_nPE[self.events.pmt_chan<=64],axis=1)) <= 10

#reprocess the tree such that it come with correct time.
#Don't recreate the tree. wait until I finish the the cut validation for cuts at above.
def correctTimeCut(self,cutName = None):
    self.events['time'] = (ak.max(self.events.pmt_time[self.events.pmt_chan<=64],axis=1)-ak.min(self.events.pmt_time[self.events.pmt_chan<=64],axis=1))




def barCutSim(self, cutName=None, cut=False):
    self.events['barCut'] = self.events.pmt_chan <= 64


def EmptyListFilter(self,cutName=None):
    self.events['None_empty_event'] = ak.num(self.events['layer']) > 0
    self.events=self.events[self.events.None_empty_event]

    #for some unknown reason, the script at below can't remove the empty event.
    #to get this done I make some changes inside makeBranches()
    #for branch in ak.fields(self.events):
    #    self.events[branch] = self.events[branch][condition]
    return self.events



#-----------------------------------------------------------------------------------------------------------------
setattr(milliqanCuts, 'EmptyListFilter', EmptyListFilter)

setattr(milliqanCuts, 'oneHitPerLayerCutSIM', oneHitPerLayerCutSIM)

setattr(milliqanCuts, 'CosmicVetoSIM', CosmicVetoSIM)

setattr(milliqanCuts, 'fourLayerCutSIM', fourLayerCutSIM)

setattr(milliqanCuts, 'LayerCut', LayerCut)

setattr(milliqanCuts, 'barCutSim', barCutSim)

R_fourlayer = mycuts.getCut(mycuts.combineCuts, 'R_fourlayer', ['barCut','fourLayerCutSIM'])
R_OneHitperLayer = mycuts.getCut(mycuts.combineCuts, 'R_OneHitperLayer', ['barCut','oneHitPerLayerCutSIM'])


#print(myplotter.dict)
#things inside dict are the name of histogram not the the histogram variable. eg here the name of histogram is nPE


#cutflow = [mycuts.LayerCut,eventCuts,myplotter.dict['nPE']]
#cutflow = [mycuts.barCutSim, mycuts.fourLayerCutSIM,mycuts.oneHitPerLayerCutSIM,R_fourlayer,R_OneHitperLayer]

cutflow = [mycuts.EmptyListFilter,mycuts.barCutSim, mycuts.fourLayerCutSIM,R_fourlayer]
#cutflow = [mycuts.EmptyListFilter]
myschedule = milliQanScheduler(cutflow, mycuts)


myschedule.printSchedule()


#in the demo mycuts, myplotter arguements are useless now
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts)

myiterator.run()

#output_file = r.TFile("run99_NPEL1.root", "RECREATE")
#h_NPE.Write()
#output_file.Close()

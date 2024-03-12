import math


import os
import sys


from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *
import awkward as ak



filelist =['/mnt/hadoop/se/store/user/czheng/SimFlattree/withPhotonMuontag/output_1.root:t']


branches = ["chan","runNumber","event","layer","nPE","type","row","muonHit"]

barbranches = ["chan","layer","nPE","type","row","muonHit"]

mycuts = milliqanCuts()

#histograms for different cosmic muon tags

myplotter = milliqanPlotter()

NBarsHitTag1 =  r.TH1F("NBarsHitTag1" , "number of bars get hit;number of bars; Events",60,0,60)


def EmptyListFilter(self,cutName=None):

    self.events['None_empty_event'] = ak.num(self.events['layer']) > 0
    self.events=self.events[self.events.None_empty_event]


def layerMask(self):
        
    #self.events["lay0"] = (self.events.layer == 0) & (self.events.type == 0) #FIXME:TypeError: __eq__(): incompatible function arguments. The following argument types are supported:(self: awkward._ext.Type, arg0: awkward._ext.Type) -> bool
    self.events["lay0"] = (self.events.layer == 0)
    #self.events["lay1"] = (self.events.layer == 1) & (self.events.type == 0)
    self.events["lay1"] = (self.events.layer == 1)
    #self.events["lay2"] = (self.events.layer == 2) & (self.events.type == 0)
    self.events["lay2"] = (self.events.layer == 2)
    #self.events["lay3"] = (self.events.layer == 3) & (self.events.type == 0)
    self.events["lay3"] = (self.events.layer == 3)


#create root histogram 
h_nPEL0 = r.TH1F("h_nPEL0", "bar nPE distribution at layer 0", 10000, 0, 100000)
#create root histogram 
h_nPEL1 = r.TH1F("h_nPEL1", "bar nPE distribution at layer 1", 10000, 0, 100000)
h_nPEL2 = r.TH1F("h_nPEL2", "bar nPE distribution at layer 2", 10000, 0, 100000)
h_nPEL3 = r.TH1F("h_nPEL3", "bar nPE distribution at layer 3", 10000, 0, 100000)

#add root histogram to plotter
myplotter.addHistograms(h_nPEL0, 'nPE', 'lay0')
myplotter.addHistograms(h_nPEL1, 'nPE', 'lay1')
myplotter.addHistograms(h_nPEL2, 'nPE', 'lay2')
myplotter.addHistograms(h_nPEL3, 'nPE', 'lay3')



setattr(milliqanCuts, 'layerMask', layerMask)

setattr(milliqanCuts, 'EmptyListFilter', EmptyListFilter)

cutflow = [mycuts.EmptyListFilter,mycuts.layerMask,myplotter.dict['h_nPEL0'],myplotter.dict['h_nPEL1'],myplotter.dict['h_nPEL2'],myplotter.dict['h_nPEL3']]

myschedule = milliQanScheduler(cutflow, mycuts,myplotter)

myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts,myplotter)

myiterator.run()

output_file = r.TFile(f"PlotWithCutNPE.root", "RECREATE")

h_nPEL0.Write()
h_nPEL1.Write()
h_nPEL2.Write()
h_nPEL3.Write()

output_file.Close()
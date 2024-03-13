import math


import os
import sys

sys.path.append('../utilities/')

from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *
import awkward as ak



filelist =['/store/user/czheng/SimFlattree/withPhotonMuontag/output_1.root:t']


branches = ["chan","runNumber","event","layer","nPE","type","row","muonHit"]

barbranches = ["chan","layer","nPE","type","row","muonHit"]

mycuts = milliqanCuts()

#histograms for different cosmic muon tags

myplotter = milliqanPlotter()

NBarsHitTag1 =  r.TH1F("NBarsHitTag1" , "number of bars get hit;number of bars; Events",60,0,60)


def EmptyListFilter(self,cutName=None):

    #-----solution 1---
    self.events['None_empty_event'] = ak.num(self.events['layer']) > 0
    #self.events=self.events[self.events.None_empty_event] #Mike notice this can cause a crash(can't find the mask) while while using the mask to extract data with plotter. I suspect there is some issue in the current analysis framework. Applying the cuts directly on the events should not cause this issue, since this is how my version script work. 
    #print(self.events.fields)

    #None_empty_event = ak.num(self.events['layer']) > 0
    #self.events=self.events[None_empty_event]#trigger the same bug.
    print(ak.to_pandas(self.events['None_empty_event']))
    print(ak.to_pandas(self.events))


def layerMask(self):
    self.events["lay0"] = (self.events.layer == 0)
    self.events["lay1"] = (self.events.layer == 1)
    self.events["lay2"] = (self.events.layer == 2)
    self.events["lay3"] = (self.events.layer == 3)

    print(self.events.fields)



#create root histogram 
h_nPEL0 = r.TH1F("h_nPEL0", "bar nPE distribution at layer 0", 1000, 0, 1000)
h_nPEL1 = r.TH1F("h_nPEL1", "bar nPE distribution at layer 1", 1000, 0, 1000)
h_nPEL2 = r.TH1F("h_nPEL2", "bar nPE distribution at layer 2", 1000, 0, 1000)
h_nPEL3 = r.TH1F("h_nPEL3", "bar nPE distribution at layer 3", 1000, 0, 1000)

mask0 = mycuts.getCut(mycuts.combineCuts, 'mask0', ['None_empty_event', 'lay0'])
mask1 = mycuts.getCut(mycuts.combineCuts, 'mask1', ['None_empty_event', 'lay1'])
mask2 = mycuts.getCut(mycuts.combineCuts, 'mask2', ['None_empty_event', 'lay2'])
mask3 = mycuts.getCut(mycuts.combineCuts, 'mask3', ['None_empty_event', 'lay3'])


#add root histogram to plotter
myplotter.addHistograms(h_nPEL0, 'nPE', 'mask0')
myplotter.addHistograms(h_nPEL1, 'nPE', 'mask1')
myplotter.addHistograms(h_nPEL2, 'nPE', 'mask2')
myplotter.addHistograms(h_nPEL3, 'nPE', 'mask3')


setattr(milliqanCuts, 'layerMask', layerMask)

setattr(milliqanCuts, 'EmptyListFilter', EmptyListFilter)

cutflow = [mycuts.EmptyListFilter, mycuts.layerMask, mask0, mask1, mask2, mask3, myplotter.dict['h_nPEL0'],myplotter.dict['h_nPEL1'],myplotter.dict['h_nPEL2'],myplotter.dict['h_nPEL3']]

myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

myiterator.run()

output_file = r.TFile(f"PlotWithCutNPE.root", "RECREATE")

h_nPEL0.Write()
h_nPEL1.Write()
h_nPEL2.Write()
h_nPEL3.Write()

output_file.Close()
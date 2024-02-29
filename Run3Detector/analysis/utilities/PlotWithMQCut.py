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


NBarsHitTag1 =  r.TH1F("NBarsHitTag1" , "number of bars get hit;number of bars; Events",60,0,60)


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
        #bararr = ak.flatten(self.events[cutName],axis=None)
        #print(ak.to_list(self.events[cutName]))
        #print(bararr)
        bararr = self.events[cutName]
        for data in bararr:
            hist.Fill(data)
        
        #hist.FillN(len(bararr), bararr, np.ones(len(bararr))) #FIXME: TypeError: could not convert argument 2 (could not convert argument to buffer or nullptr)


def EmptyListFilter(self,cutName=None):

    self.events['None_empty_event'] = ak.num(self.events['layer']) > 0
    self.events=self.events[self.events.None_empty_event]


setattr(milliqanCuts, 'NbarsHitsCount',NbarsHitsCount)
setattr(milliqanCuts, 'EmptyListFilter', EmptyListFilter)

NbarsHitsCount1= mycuts.getCut(mycuts.NbarsHitsCount, "NBarsHits",cut = None,hist = NBarsHitTag1)

cutflow = [mycuts.EmptyListFilter,NbarsHitsCount1]

myschedule = milliQanScheduler(cutflow, mycuts)

myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts)

myiterator.run()

output_file = r.TFile(f"PlotWithCut.root", "RECREATE")

NBarsHitTag1.Write()
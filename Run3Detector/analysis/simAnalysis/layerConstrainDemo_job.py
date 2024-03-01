import math


import os
import sys
import time
import json

sys.path.append("/home/czheng/scratch0/SIManalysisDEV/milliqanOffline/Run3Detector/analysis/utilities")
from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *
import awkward as ak


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

branches = ["chan","runNumber","event","layer","nPE","type","row","muonHit"]

barbranches = ["chan","layer","nPE","type","row","muonHit"]

mycuts = milliqanCuts()

#histograms for different cosmic muon tags


NBarsHitTag1 =  r.TH1F("NBarsHitTag1" , "number of bars get hit;number of bars; Events",60,0,60)



def CosmuonTagIntialization(self, NPEcut = 2500, offline = None):
    for R in range(4):
        for l in range(4):
            self.events[f"l{l}R{R}"] = (self.events.layer == l) & (self.events.row == R) & (self.events.barCut) & (self.events.nPE >= NPEcut)

    
    if offline:
        #1320 is the average spe pulse area from bar channel. Since the calibration on panel is not being done, so NPE need to be recalculated from (pulse area / spe pulse area).
        self.events["TopPanelHit"] = ak.any(self.events["row"]==4 & (self.events["area"]/1320) >= NPEcut ,axis =1)
    else:
        self.events["TopPanelHit"] = ak.any((self.events["row"]==4) & (self.events["nPE"] >= NPEcut), axis = 1)


#top and bottom row have big hit
def TBBigHit(self,cutName = None,cut = None, constraint = True):


    TBBigHit_lay0 =  (ak.any(self.events.l0R0==True, axis=1) & ak.any(self.events.l0R3==True, axis=1))
    TBBigHit_lay1 =  (ak.any(self.events.l1R0==True, axis=1) & ak.any(self.events.l1R3==True, axis=1))
    TBBigHit_lay2 =  (ak.any(self.events.l2R0==True, axis=1) & ak.any(self.events.l2R3==True, axis=1))
    TBBigHit_lay3 =  (ak.any(self.events.l3R0==True, axis=1) & ak.any(self.events.l3R3==True, axis=1))

    self.events["TBBigHit"] = (TBBigHit_lay0 | TBBigHit_lay1 | TBBigHit_lay2 | TBBigHit_lay3) 

    #convert the events based tag to pulse(bar based in sim) based
    TBBigHit_lay0, junk=ak.broadcast_arrays(TBBigHit_lay0, self.events.layer)
    TBBigHit_lay1, junk=ak.broadcast_arrays(TBBigHit_lay1, self.events.layer)
    TBBigHit_lay2, junk=ak.broadcast_arrays(TBBigHit_lay2, self.events.layer)
    TBBigHit_lay3, junk=ak.broadcast_arrays(TBBigHit_lay3, self.events.layer)


    #only keep the data in layer that pass the cosmic muon tag.
    if constraint:
        for b in barbranches:
            self.events[b] = self.events[b][TBBigHit_lay0 | TBBigHit_lay1 | TBBigHit_lay2 | TBBigHit_lay3]

    #print(ak.to_pandas(self.events))







def NbarsHitsCount(self,cutName = "NBarsHits",cut = None, hist = None):

    bararr = ak.copy(self.events)
    
    print(ak.to_pandas(bararr))

    for b in barbranches:    
        bararr[b] = bararr[b][bararr["type"]==0] #get bar only data

    print(ak.to_pandas(bararr)) #non-bar datas are all removed
    #FIXME: it only has 6 events??????? need double check

    if cut:
        cutMask, junk = ak.broadcast_arrays(bararr.cut, bararr.layer)

        uniqueBarArr = ak.Array([np.unique(x) for x in bararr.chan[cutMask]])
        self.events[cutName] = ak.count(uniqueBarArr,axis = 1) #create a extra tag. in case you want to count the number of bar got hit with specific cut
        
    else:
        uniqueBarArr = ak.Array([np.unique(x) for x in bararr.chan])
        self.events[cutName] = ak.count(uniqueBarArr, axis = 1) #FIXME: it stuck at zero, the minimun amount of unique bar should be 2 when a event pass TBBigHit
        print(ak.count(uniqueBarArr, axis = 1))  #majority are zero. 
        #print(self.events[cutName])
        #print(self.events.fields)
    
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

setattr(milliqanCuts, 'CosmuonTagIntialization',CosmuonTagIntialization)
setattr(milliqanCuts, 'NbarsHitsCount',NbarsHitsCount)
setattr(milliqanCuts, 'EmptyListFilter', EmptyListFilter)
setattr(milliqanCuts, 'TBBigHit', TBBigHit)

NbarsHitsCount1= mycuts.getCut(mycuts.NbarsHitsCount, "NBarsHits",cut = None,hist = NBarsHitTag1)

cutflow = [mycuts.EmptyListFilter,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,mycuts.TBBigHit,NbarsHitsCount1]



myschedule = milliQanScheduler(cutflow, mycuts)

myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts)

myiterator.run()

f_out = r.TFile(f"Run{numRun}PlotWithCut_withConstraint_condorJob.root", "RECREATE")


f_out.cd()

NBarsHitTag1.Write()

f_out.Close()
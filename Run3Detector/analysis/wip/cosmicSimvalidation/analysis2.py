import os
import sys

sys.path.append("/share/scratch0/czheng/eventmissing/milliqanWorking/milliqanOffline/Run3Detector/analysis/utilities/")

from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *


#filelist =['/mnt/hadoop/se/store/user/milliqan/trees/v34/MilliQan_Run1190.155_v34.root:t']


#"""
filelist = []

def appendRun(filelist,run):
    #directory = "/mnt/hadoop/se/store/user/milliqan/trees/v34/1000/"
    directory = "/mnt/hadoop/se/store/user/milliqan/trees/v34/"
    for filename in os.listdir(directory):
        if filename.startswith(f"MilliQan_Run{run}") and filename.endswith(".root"):
            filelist.append(directory+filename+":t")
cosmicGoodRun = [1190]


for run in cosmicGoodRun:
    appendRun(filelist,run)
#"""



branches = ['boardsMatched', 'height', 'layer','type','chan','pickupFlag']



def barCutV2(self, cutName=None, cut=False, branches=None):
    barCut = self.events['type'] == 0
    if cut:
        for branch in branches:
            if branch == 'boardsMatched': continue   #this is needed to avoid too many jacked slice in array.(dont know the meaing)
            self.events[branch] = self.events[branch][barCut]




mycuts = milliqanCuts()

pickupCut = mycuts.getCut(mycuts.pickupCut, 'pickupCut', cut=True, branches=branches)

boardMatchCut = mycuts.getCut(mycuts.boardsMatched, 'boardMatchCut', cut=True, branches=branches)

setattr(milliqanCuts, 'barCutV2', barCutV2)

barCutV2 = mycuts.getCut(mycuts.barCutV2, 'barCutV2', cut=True,branches=branches)

heightCut = mycuts.getCut(mycuts.heightCut, 'heightCut', cut=36,branches=branches)

fourLayerCut = mycuts.getCut(mycuts.fourLayerCut, 'fourLayerCut', cut=True)

#define the milliqan


myplotter = milliqanPlotter()

nbars = r.TH1F("nbars", "n_BARS", 32, 0, 32)
myplotter.addHistograms(nbars, 'nbars')

#things start to looking weird after heightCut, cut is working but the tag is weird
cutflow = [boardMatchCut,pickupCut,barCutV2,heightCut,fourLayerCut, myplotter.dict['nbars']]

myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

#print out the schedule
myschedule.printSchedule()

#create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

myiterator.run()

output_file = r.TFile("test1190.root", "RECREATE")
nbars.Write()
output_file.Close()

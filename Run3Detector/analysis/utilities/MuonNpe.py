"""
I attempt the find the muon npe distribution.
Base on previous analysis with sim, I notice that the first hit of each channel is created by muon. 


To collect the information from muon and minimize the signal from other particle, I use the following tag to collect signal.

1. Collect the first pulse with ipulse = 0   done in offlinePreProcess
2. remove the pulse ouside of 1100-1500 ns  done in offlinePreProcess
The threasholds I used are identicle to the one in similfied anlysis script at /net/cms26/cms26r0/zheng/barsim/ExtraValidationR/AnalyzeHitsStrict.C
3. Collect the pulse npe distribution when event pass the tag of number of Bar = 4 and ST geometric tag. Bit hit Threashold set to be 10, bar counting set to be 10
"""


import math


import os
import sys
import time
import json

from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *
import awkward as ak

branches = ["height","timeFit_module_calibrated","chan","runNumber","column","event","fileNumber",'boardsMatched',"pickupFlag","layer","nPE","type","row","area","ipulse"]

filelist = [f'/home/czheng/SimCosmicFlatTree/offlinefile/MilliQan_RunFile.root:t']

mycuts = milliqanCuts()

myplotter = milliqanPlotter()


OL_sudo_straight = mycuts.getCut(mycuts.sudo_straight,'StraghtCosmic', NPEcut = 10,time = "timeFit_module_calibrated")
Fourbars = mycuts.getCut(mycuts.NbarsHitsCount,cutName ='FourBars', cut = None, NPECut = 10)

#adding combine cuts for downwardPath
CLFourbar = mycuts.getCut(mycuts.combineCuts, 'CLFourbar', ["FourBars", "StraghtCosmic","barCut"])


NPE_4Bar = r.TH1F("Bar_NPE_DW", "nPE bar; nPE ; pulse", 500, 0, 1000)


#add hists with tags
myplotter.addHistograms(NPE_4Bar, 'nPE', 'CLFourbar')


cutflow = [mycuts.offlinePreProcess,mycuts.boardsMatched,mycuts.pickupCut,mycuts.EmptyListFilter,mycuts.barCut,mycuts.panelCut,OL_sudo_straight,Fourbars,CLFourbar,NPE_4Bar]

myschedule = milliQanScheduler(cutflow, mycuts,myplotter)

myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts,fileCheckerEnable=False)

myiterator.run()


NPE_4Bar.Draw()

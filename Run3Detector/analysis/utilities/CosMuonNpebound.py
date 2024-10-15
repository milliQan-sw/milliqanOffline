"""
10-14
The goal of this file is used to determine the lower bound of cosmic muon Npe

to do
get cut NbarsHitsCountLay to change NPE

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

#filelist = [f'/home/czheng/SimCosmicFlatTree/MilliQan_Run1176.root:t']  #change this into smaller file to do the test
filelist = [f'/Users/haoliangzheng/CERN_ana/EventDisplay/MilliQan_Run1176.406_v34.root:t'] #local debug
mycuts = milliqanCuts()

myplotter = milliqanPlotter()

OL_sudo_straight = mycuts.getCut(mycuts.sudo_straight,'StraghtCosmic', NPEcut = 100,time = "timeFit_module_calibrated")

NbarsHitsCountLay = mycuts.getCut(mycuts.NbarsHitsCountLay,'placeholder', NPECut = 100)

cutflow = [mycuts.offlinePreProcess,mycuts.boardsMatched,mycuts.pickupCut,mycuts.EmptyListFilter,mycuts.barCut,mycuts.panelCut,OL_sudo_straight,mycuts.bigHitLayer,NbarsHitsCountLay]

myschedule = milliQanScheduler(cutflow, mycuts,myplotter)

myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts,fileCheckerEnable=False)

myiterator.run()
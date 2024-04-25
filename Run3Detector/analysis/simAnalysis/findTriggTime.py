"""
the goal of this file is to find the trigger time with data from timeFit_module_calibrated

"""
import math
import os
import sys
import time
import json

sys.path.append("../utilities")

from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *
import awkward as ak


branches = ["timeFit_module_calibrated","type","boardsMatched","pickupFlag"]


numRun = str(sys.argv[1])
fileNum = str(sys.argv[2])
filelist =[f'/home/czheng/SimCosmicFlatTree/offlinefile/MilliQan_Run{numRun}.{fileNum}_v34.root:t']
print(filelist)

outputPath = str(sys.argv[3]) # the path is used at the very end for the output txt file
print(outputPath)

mycuts = milliqanCuts()

myplotter = milliqanPlotter()


T_h = r.TH1F("T_h", "timeFit_module_calibrated;ns; # of pulses", 250, 0, 2500)
myplotter.addHistograms(T_h, 'timeFit_module_calibrated', 'barCut')

cutflow = [mycuts.boardsMatched,mycuts.pickupCut,mycuts.barCut,myplotter.dict['T_h']]


#create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

#print out the schedule
myschedule.printSchedule()

#create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

#run the milliqan processor
myiterator.run()


f_out = r.TFile(f"{outputPath}/Run{numRun}_file{fileNum}_findTrigger.root", "RECREATE")
T_h.Write()
f_out.Close()

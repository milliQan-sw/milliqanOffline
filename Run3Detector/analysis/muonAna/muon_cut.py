#importing packages
import os
import ROOT as r
import uproot
import hist
import matplotlib.pyplot as plt
import awkward as ak
import numpy as np
import pandas as pd
import array as arr
import sys
sys.path.append('../utilities')
from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *

#define a file list to run over
filelist = ['/mnt/hadoop/se/store/user/milliqan/trees/v34/1000/MilliQan_Run1006.4_v34.root:t']

#define the necessary branches to run over
branches = ['pickupFlag', 'boardsMatched', 'height', 'area', 'column', 'row', 'layer', 'chan', 'ipulse', 'type']

#define the milliqan cuts object
mycuts = milliqanCuts()

#require pulses are not pickup
pickupCut = mycuts.getCut(mycuts.pickupCut, 'pickupCut', cut=True, branches=branches)

#require that all digitizer boards are matched
boardMatchCut = mycuts.getCut(mycuts.boardsMatched, 'boardMatchCut', cut=True, branches=branches)

#Add four layer cut
fourLayerCut = mycuts.getCut(mycuts.fourLayerCut, 'fourLayerCut', cut=False)

#defining the cutflow
cutflow = [boardMatchCut, pickupCut, mycuts.layerCut, mycuts.fourLayerCut, mycuts.straightLineCut]

#create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts)

#print out the schedule
myschedule.printSchedule()

#create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts)

#run the milliqan processor
myiterator.run()

#check the number of events remaining
num_events_after_cuts = len(mycuts.events[mycuts.events["straightLineCut"]])
print(f"Number of events after cuts: {num_events_after_cuts}")

#print only events with branches that have passed cuts
print("Events with branches that have passed cuts:")
print(mycuts.events[mycuts.events["straightLineCut"]])

#print a boolean list to check if every events has passed cuts
print("A boolean list to check if events have passed cuts:")
print(ak.to_list(mycuts.events["straightLineCut"]))
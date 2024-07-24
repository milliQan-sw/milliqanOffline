# importing packages
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

# define the function to get the number of events that have hits in any 3 layers
def get3LNum(self):
    
    threeLcount = []

    # nPE mask to replace height and area mask
    nPEMask = self.events['nPE'] > 10000

    # develop simulation check: events actually have muons in all 4 layers 
    muonL0Mask = ak.any((abs(self.events['hit_particleName']) == 13) & (self.events['hit_layer'] == 0), axis = 1)
    muonL1Mask = ak.any((abs(self.events['hit_particleName']) == 13) & (self.events['hit_layer'] == 1), axis = 1)
    muonL2Mask = ak.any((abs(self.events['hit_particleName']) == 13) & (self.events['hit_layer'] == 2), axis = 1)
    muonL3Mask = ak.any((abs(self.events['hit_particleName']) == 13) & (self.events['hit_layer'] == 3), axis = 1)
    muonMask = muonL0Mask & muonL1Mask & muonL2Mask & muonL3Mask
    finalPulseMask = nPEMask & muonMask

    # apply the finalPulseMask
    masked_time = self.events['time'][finalPulseMask]
    masked_layer = self.events['layer'][finalPulseMask]

    # masked times per layer
    timeL0 = masked_time[masked_layer == 0]
    timeL1 = masked_time[masked_layer == 1]
    timeL2 = masked_time[masked_layer == 2]
    timeL3 = masked_time[masked_layer == 3]

    # function to get minimum time per event handling None values
    def minTime(pulse_times):
        filtered_times = [time for time in pulse_times if time is not None]
        return min(filtered_times) if filtered_times else None

    # extract minimum times for each layer
    timeL0_min = [minTime(event) for event in ak.to_list(timeL0)]
    timeL1_min = [minTime(event) for event in ak.to_list(timeL1)]
    timeL2_min = [minTime(event) for event in ak.to_list(timeL2)]
    timeL3_min = [minTime(event) for event in ak.to_list(timeL3)]

    for i in range(len(timeL0_min)):
        # require pulses in all 4 layers for one event
        if (timeL0_min[i] is not None and timeL1_min[i] is not None and timeL2_min[i] is not None) or \
           (timeL0_min[i] is not None and timeL1_min[i] is not None and timeL3_min[i] is not None) or \
           (timeL0_min[i] is not None and timeL2_min[i] is not None and timeL3_min[i] is not None) or \
           (timeL1_min[i] is not None and timeL2_min[i] is not None and timeL3_min[i] is not None):
            # count events with valid times in 3 layers
            threeLcount.append(0)
    
    print(len(threeLcount))

# add our custom function to milliqanCuts
setattr(milliqanCuts, 'get3LNum', get3LNum)

filelist = ['/home/bpeng/muonAnalysis/dy_nophoton_flat.root']

# define the necessary branches to run over
branches = ['hit_hitTime_ns', 'hit_nPE', 'hit_layer', 'hit_particleName', 'layer', 'nPE', 'time', 'chan']

# define the milliqan cuts object
mycuts = milliqanCuts()

# define milliqan plotter
myplotter = milliqanPlotter()

# defining the cutflow
cutflow = [mycuts.get3LNum]

# create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

# print out the schedule
myschedule.printSchedule()

# create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

# run the milliqan processor
myiterator.run()
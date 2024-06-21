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

    # make final mask
    finalPulseMask = nPEMask

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
            # calculate time differences only for events with valid times in 3 layers
            threeLcount.append(0)
    
    print(threeLcount)

    # extend the final list to match the size of the current file
    num_events = len(self.events)
    num_nones = num_events - len(threeLcount)
    threeLcount.extend([None] * num_nones)

    # define custom branch
    self.events['threeLcount'] = threeLcount

# add our custom function to milliqanCuts
setattr(milliqanCuts, 'get3LNum', get3LNum)

filelist = ['/home/bpeng/muonAnalysis/dy_nophoton_flat.root']

# define the necessary branches to run over
branches = ['hit_hitTime_ns', 'hit_nPE', 'hit_layer', 'hit_particleName', 'layer', 'nPE', 'time', 'chan']

# define the milliqan cuts object
mycuts = milliqanCuts()

# define milliqan plotter
myplotter = milliqanPlotter()

# create a 1D root histogram
h_1d = r.TH1F("h_1d", "Number of events that have hits in any 3 layers", 10, -5, 5)
h_1d.GetXaxis().SetTitle("number")

# add root histogram to plotter
myplotter.addHistograms(h_1d, 'threeLcount')

# defining the cutflow
cutflow = [mycuts.get3LNum, myplotter.dict['h_1d']]

# create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

# print out the schedule
myschedule.printSchedule()

# create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

# run the milliqan processor
myiterator.run()

# create a new TFile
f = r.TFile("3LayerCount.root", "recreate")

# write the histograms to the file
h_1d.Write()

# close the file
f.Close()
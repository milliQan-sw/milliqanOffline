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

# define the function to get the layer count
def getLayerCount(self):
    
    layerCount = []

    # nPE mask to replace height and area mask
    nPEMask = self.events['hit_nPE'] > 200

    # muon mask
    muonMask = abs(self.events['hit_particleName']) == 13

    # make final mask (to track false negetive)
    finalPulseMask = ~(muonMask & nPEMask)

    # apply the finalPulseMask
    masked_time = self.events['hit_hitTime_ns'][finalPulseMask]
    masked_layer = self.events['hit_layer'][finalPulseMask]

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
    # Check pulses in all 4 layers for one event
    if timeL0_min[i] is not None and timeL1_min[i] is not None and timeL2_min[i] is not None and timeL3_min[i] is not None:
        # All layers have valid times
        layerCount.append(4)
    elif timeL0_min[i] is None and timeL1_min[i] is None and timeL2_min[i] is None and timeL3_min[i] is None:
        # None of the layers have valid times
        layerCount.append(0)
    elif (timeL0_min[i] is not None and timeL1_min[i] is None and timeL2_min[i] is None and timeL3_min[i] is None) or \
         (timeL0_min[i] is None and timeL1_min[i] is not None and timeL2_min[i] is None and timeL3_min[i] is None) or \
         (timeL0_min[i] is None and timeL1_min[i] is None and timeL2_min[i] is not None and timeL3_min[i] is None) or \
         (timeL0_min[i] is None and timeL1_min[i] is None and timeL2_min[i] is None and timeL3_min[i] is not None):
        # Only one layer has a valid time
        layerCount.append(1)
    elif (timeL0_min[i] is not None and timeL1_min[i] is not None and timeL2_min[i] is None and timeL3_min[i] is None) or \
         (timeL0_min[i] is not None and timeL1_min[i] is None and timeL2_min[i] is not None and timeL3_min[i] is None) or \
         (timeL0_min[i] is not None and timeL1_min[i] is None and timeL2_min[i] is None and timeL3_min[i] is not None) or \
         (timeL0_min[i] is None and timeL1_min[i] is not None and timeL2_min[i] is not None and timeL3_min[i] is None) or \
         (timeL0_min[i] is None and timeL1_min[i] is not None and timeL2_min[i] is None and timeL3_min[i] is not None) or \
         (timeL0_min[i] is None and timeL1_min[i] is None and timeL2_min[i] is not None and timeL3_min[i] is not None):
        # Only two layers have valid times
        layerCount.append(2)
    elif (timeL0_min[i] is not None and timeL1_min[i] is not None and timeL2_min[i] is not None and timeL3_min[i] is None) or \
         (timeL0_min[i] is not None and timeL1_min[i] is not None and timeL2_min[i] is None and timeL3_min[i] is not None) or \
         (timeL0_min[i] is not None and timeL1_min[i] is None and timeL2_min[i] is not None and timeL3_min[i] is not None) or \
         (timeL0_min[i] is None and timeL1_min[i] is not None and timeL2_min[i] is not None and timeL3_min[i] is not None):
        # Only three layers have valid times
        layerCount.append(3)

    # extend the final list to match the size of the current file
    num_events = len(self.events)
    num_nones = num_events - len(layerCount)
    layerCount.extend([None] * num_nones)

    # define custom branch
    self.events['FNLayerCount'] = layerCount

# add our custom function to milliqanCuts
setattr(milliqanCuts, 'getLayerCount', getLayerCount)

filelist = ['/home/bpeng/muonAnalysis/dy_nophoton_flat.root']

# define the necessary branches to run over
branches = ['hit_hitTime_ns', 'hit_nPE', 'hit_layer', 'hit_chan', 'hit_particleName']

# define the milliqan cuts object
mycuts = milliqanCuts()

# define milliqan plotter
myplotter = milliqanPlotter()

# create a 1D root histogram
h_1d = r.TH1F("h_1d", "Count of Layers Passed by FN", 5, 0, 5)
h_1d.GetXaxis().SetTitle("count")

# add root histogram to plotter
myplotter.addHistograms(h_1d, 'FNLayerCount')

# defining the cutflow
cutflow = [mycuts.getLayerCount, myplotter.dict['h_1d']]

# create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

# print out the schedule
myschedule.printSchedule()

# create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

# run the milliqan processor
myiterator.run()

# create a new TFile
f = r.TFile("FNLayerCount.root", "recreate")

# write the histograms to the file
h_1d.Write()

# close the file
f.Close()
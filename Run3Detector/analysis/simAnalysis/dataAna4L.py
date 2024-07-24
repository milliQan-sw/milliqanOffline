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

# define the function to get the time differences
def getTimeDiff(self):
    
    time_diffsL30 = []

    # develop simulation check: events actually have muons in 5 layers (simulation check)
    muonL0Mask = ak.any((abs(self.events['hit_particleName']) == 13) & (self.events['hit_layer'] == 0), axis = 1)
    muonL1Mask = ak.any((abs(self.events['hit_particleName']) == 13) & (self.events['hit_layer'] == 1), axis = 1)
    muonL2Mask = ak.any((abs(self.events['hit_particleName']) == 13) & (self.events['hit_layer'] == 2), axis = 1)
    muonL3Mask = ak.any((abs(self.events['hit_particleName']) == 13) & (self.events['hit_layer'] == 3), axis = 1)
    muonL4Mask = ak.any((abs(self.events['hit_particleName']) == 13) & (self.events['hit_layer'] == 4), axis = 1)

    simCheck = muonL0Mask & muonL1Mask & muonL2Mask & muonL3Mask & muonL4Mask

    # nPE mask to replace height and area mask (this is the actual nPE cut being tested) 
    nPEMask = self.events['nPE'] > 10000

    finalPulseMask = nPEMask #& simCheck

    # apply the finalPulseMask
    masked_time = self.events['time'][finalPulseMask]
    masked_layer = self.events['layer'][finalPulseMask]

    # masked times per layer
    timeL0 = masked_time[masked_layer == 0]
    timeL1 = masked_time[masked_layer == 1]
    timeL2 = masked_time[masked_layer == 2]
    timeL3 = masked_time[masked_layer == 3]

    timeL4 = masked_time[masked_layer == 4]
    boolTimeL4 = ak.any(timeL4, axis = 1)

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
        # require an event to have pulses in all 5 layers (this is the actual 5-layer cut being tested) 
        if timeL0_min[i] is not None and timeL1_min[i] is not None and timeL2_min[i] is not None and timeL3_min[i] is not None and boolTimeL4[i] is True:
            # calculate time differences only for events with valid times in all layers
            time_diffsL30.append(timeL3_min[i] - timeL0_min[i])
    
    #print(time_diffsL30)
    #print(len(time_diffsL30))
    
    off = ak.any((self.events['layer'] == 4) & (self.events['nPE'] > 10000), axis = 1)
    sim = ak.any((abs(self.events['hit_particleName']) == 13) & (self.events['hit_layer'] == 4) & (self.events['hit_nPE'] > 10000), axis = 1)

    countoff = 0
    countsim = 0

    for i in range(len(off)):
        if off[i] == True:
            countoff += 1

    for i in range(len(sim)):
        if sim[i] == True:
            countsim += 1

    print(countoff, countsim)

    # extend the final list to match the size of the current file
    num_events = len(self.events)
    num_nones = num_events - len(time_diffsL30)
    time_diffsL30.extend([None] * num_nones)

    # define custom branch
    self.events['timeDiff'] = time_diffsL30

# add our custom function to milliqanCuts
setattr(milliqanCuts, 'getTimeDiff', getTimeDiff)

filelist = ['/home/bpeng/muonAnalysis/dy_nophoton_flat.root']

# define the necessary branches to run over
branches = ['hit_hitTime_ns', 'hit_nPE', 'hit_layer', 'hit_particleName', 'layer', 'nPE', 'time', 'chan']

# define the milliqan cuts object
mycuts = milliqanCuts()

# define milliqan plotter
myplotter = milliqanPlotter()

# create a 1D root histogram
h_1d = r.TH1F("h_1d", "Time Differences between Layer 3 and 0", 100, -50, 50)
h_1d.GetXaxis().SetTitle("Time Differences")

# add root histogram to plotter
myplotter.addHistograms(h_1d, 'timeDiff')

# defining the cutflow
cutflow = [mycuts.getTimeDiff, myplotter.dict['h_1d']]

# create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

# print out the schedule
myschedule.printSchedule()

# create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

# run the milliqan processor
myiterator.run()

# create a new TFile
f = r.TFile("TP_DtL30_4L.root", "recreate")

# write the histograms to the file
h_1d.Write()

# close the file
f.Close()
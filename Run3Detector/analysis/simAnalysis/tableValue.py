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

def createMuonMask(self):
    # Create masks for muons in each layer
    mask_L0 = (abs(self.events['hit_particleName']) == 13) & (self.events['hit_layer'] == 0)
    mask_L1 = (abs(self.events['hit_particleName']) == 13) & (self.events['hit_layer'] == 1)
    mask_L2 = (abs(self.events['hit_particleName']) == 13) & (self.events['hit_layer'] == 2)
    mask_L3 = (abs(self.events['hit_particleName']) == 13) & (self.events['hit_layer'] == 3)
    
    # Apply masks to get muons in each layer
    muons_L0 = self.events[mask_L0]
    muons_L1 = self.events[mask_L1]
    muons_L2 = self.events[mask_L2]
    muons_L3 = self.events[mask_L3]
    
    # Count the number of muons in each layer per event
    num_muons_L0 = ak.num(muons_L0['hit_particleName'], axis=1)
    num_muons_L1 = ak.num(muons_L1['hit_particleName'], axis=1)
    num_muons_L2 = ak.num(muons_L2['hit_particleName'], axis=1)
    num_muons_L3 = ak.num(muons_L3['hit_particleName'], axis=1)
    
    # Create muon mask: events with muons in all 4 layers
    muonMask = (num_muons_L0 > 0) & (num_muons_L1 > 0) & (num_muons_L2 > 0) & (num_muons_L3 > 0)
    
    return muonMask

# define the function to get the time differences
def getTimeDiff(self):
    time_diffsL30 = []

    # nPE mask to replace height and area mask
    nPEMask = self.events['nPE'] > 10000

    # require events to have muons
    muonMask = self.createMuonMask()

    # make final mask
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
        if timeL0_min[i] is not None and timeL1_min[i] is not None and timeL2_min[i] is not None and timeL3_min[i] is not None:
            # calculate time differences only for events with valid times in all layers
            time_diffsL30.append(timeL3_min[i] - timeL0_min[i])
    
    print(time_diffsL30)

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
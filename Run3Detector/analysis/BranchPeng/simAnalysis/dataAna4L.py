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
    missed_chan = []

    # develop simulation check: events actually have muons in 5 layers (simulation check)
    muonL0Mask = ak.any((abs(self.events['hit_particleName']) == 13) & (self.events['hit_layer'] == 0), axis = 1)
    muonL1Mask = ak.any((abs(self.events['hit_particleName']) == 13) & (self.events['hit_layer'] == 1), axis = 1)
    muonL2Mask = ak.any((abs(self.events['hit_particleName']) == 13) & (self.events['hit_layer'] == 2), axis = 1)
    muonL3Mask = ak.any((abs(self.events['hit_particleName']) == 13) & (self.events['hit_layer'] == 3), axis = 1)
    muonL4Mask = ak.any((abs(self.events['hit_particleName']) == 13) & (self.events['hit_layer'] == 4), axis = 1)

    simCheck = ak.any(abs(self.events['hit_particleName']) == 13, axis = 1)
    #simCheck = muonL0Mask & muonL1Mask & muonL2Mask & muonL3Mask & muonL4Mask

    # nPE mask to replace height and area mask (this is the actual nPE cut being tested) 
    bar_nPEMask = self.events['nPE'] > 10000
    backPanel_nPEMask = self.events['nPE'] > 10000 / 12

    bar_finalMask = bar_nPEMask #& simCheck
    backPanel_finalMask = backPanel_nPEMask #& simCheck

    # apply the finalPulseMask
    bar_masked_time = self.events['time'][bar_finalMask]
    bar_masked_layer = self.events['layer'][bar_finalMask]

    backPanel_masked_time = self.events['time']
    backPanel_masked_layer = self.events['layer']

    # masked times per layer
    timeL0 = bar_masked_time[bar_masked_layer == 0]
    timeL1 = bar_masked_time[bar_masked_layer == 1]
    timeL2 = bar_masked_time[bar_masked_layer == 2]
    timeL3 = bar_masked_time[bar_masked_layer == 3]

    timeL4 = backPanel_masked_time[backPanel_masked_layer == 4]
    backPanelBool = ak.any(timeL4, axis = 1)

    # function to get minimum time per event handling None values
    def minTime(pulse_times):
        filtered_times = [time for time in pulse_times if time is not None]
        return min(filtered_times) if filtered_times else None

    # extract minimum times for each layer
    timeL0_min = [minTime(event) for event in ak.to_list(timeL0)]
    timeL1_min = [minTime(event) for event in ak.to_list(timeL1)]
    timeL2_min = [minTime(event) for event in ak.to_list(timeL2)]
    timeL3_min = [minTime(event) for event in ak.to_list(timeL3)]

    chan_L0 = self.events['chan'][self.events['layer'] == 0]

    for i in range(len(timeL0_min)):
        # this is the actual cut being tested
        if timeL0_min[i] is not None and timeL1_min[i] is not None and timeL2_min[i] is not None and timeL3_min[i] is not None:
            # calculate time differences only for events with valid times in all layers
            #time_diffsL30.append(timeL3_min[i] - timeL0_min[i])
            missed_chan.append(chan_L0[i])

    # extend the final list to match the size of the current file
    num_events = len(self.events)
    num_nones = num_events - len(missed_chan)
    missed_chan.extend([None] * num_nones)

    # define custom branch
    self.events['timeDiff'] = missed_chan

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
h_1d = r.TH1F("h_1d", "Chan in Layer 0 of 4 Layer Hit Events", 75, 0, 75)
h_1d.GetXaxis().SetTitle("chan")

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
f = r.TFile("chan.root", "recreate")

# write the histograms to the file
h_1d.Write()

# close the file
f.Close()
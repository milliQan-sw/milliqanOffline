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

# define the function to get the time differences between layer 4 and layer -1
def getTimeDiff(self):

    time_diffs = []

    # keep only events with slab pulses on both layer 4 and -1 whose areas are bigger than the cut value
    mask_layer_4 = (self.events['layer'] == 4) & (self.events['area'] > 80000)
    mask_layer_neg1 = (self.events['layer'] == -1) & (self.events['area'] > 80000)
    events_with_layer_4_pulses = ak.any(mask_layer_4, axis=1)
    events_with_layer_neg1_pulses = ak.any(mask_layer_neg1, axis=1)
    slab_mask = events_with_layer_4_pulses & events_with_layer_neg1_pulses

    # remove events with panel pulses whose heights are bigger than the cut value
    panel_pulse_mask = (self.events['type'] == 2) & (self.events['height'] > 1200)
    events_without_panel_pulses = ~ak.any(panel_pulse_mask, axis=1)

    # central time cut
    timeCut = (self.events['timeFit_module_calibrated'] > 1100) & (self.events['timeFit_module_calibrated'] < 1400)

    # apply the final mask to select the desired events
    final_mask = slab_mask & timeCut & events_without_panel_pulses 
    selected_events = self.events[final_mask]

    # pick out the pulses on layer 4 and -1
    layer_4_pulses = selected_events[(selected_events['layer'] == 4) & (selected_events['area'] > 80000)]
    layer_neg1_pulses = selected_events[(selected_events['layer'] == -1) & (selected_events['area'] > 80000)]

    # loop through each event and calculate the time differences
    for event in range(len(selected_events)):
        event_layer_4_pulses = layer_4_pulses[event]
        event_layer_neg1_pulses = layer_neg1_pulses[event]

        # check if there are pulses in both layers
        if len(event_layer_4_pulses['timeFit_module_calibrated']) > 0 and len(event_layer_neg1_pulses['timeFit_module_calibrated']) > 0:
            timeL4 = min(event_layer_4_pulses['timeFit_module_calibrated'])
            timeLn1 = min(event_layer_neg1_pulses['timeFit_module_calibrated'])
            time_diffs.append(timeL4 - timeLn1)

    print(time_diffs)

# extend the final list to match the size of the current file
    num_events = len(self.events)
    num_nones = num_events - len(time_diffs)
    time_diffs.extend([None] * num_nones)

    # define custom branch
    self.events['timeDiff'] = time_diffs

# add our custom function to milliqanCuts
setattr(milliqanCuts, 'getTimeDiff', getTimeDiff)

# check if command line arguments are provided
if len(sys.argv) != 3:
    print("Usage: python3 [file_name] [start_file_index] [end_file_index]")
    sys.exit(1)

# assign start and end indices from command line
start_index = int(sys.argv[1])
end_index = int(sys.argv[2])

# define a file list to run over
filelist = [
    f"/home/bpeng/muonAnalysis/MilliQan_Run1118.{i}_v34.root"
    for i in range(start_index, end_index + 1)
    if os.path.exists(f"/home/bpeng/muonAnalysis/MilliQan_Run1118.{i}_v34.root")
]

# define the necessary branches to run over
branches = ['pickupFlag', 'boardsMatched', 'timeFit_module_calibrated', 'height', 'area', 'column', 'row', 'layer', 'chan', 'ipulse', 'type']

# define the milliqan cuts object
mycuts = milliqanCuts()

# require pulses are not pickup
pickupCut = mycuts.getCut(mycuts.pickupCut, 'pickupCut', cut=True, branches=branches)

# require that all digitizer boards are matched
boardMatchCut = mycuts.getCut(mycuts.boardsMatched, 'boardMatchCut', cut=True, branches=branches)

# add four layer cut
fourLayerCut = mycuts.getCut(mycuts.fourLayerCut, 'fourLayerCut', cut=False)

# define milliqan plotter
myplotter = milliqanPlotter()

# create a 1D root histogram
h_1d = r.TH1F("h_1d", "Time Differences between Layer 4 and -1", 200, -100, 100)
h_1d.GetXaxis().SetTitle("Time Differences")

# add root histogram to plotter
myplotter.addHistograms(h_1d, 'timeDiff')

# defining the cutflow
cutflow = [boardMatchCut, pickupCut, mycuts.layerCut, mycuts.getTimeDiff, myplotter.dict['h_1d']]

# create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

# print out the schedule
myschedule.printSchedule()

# create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

# run the milliqan processor
myiterator.run()

# create a new TFile
f = r.TFile("1dHistSlabDt.root", "recreate")

# write the histograms to the file
h_1d.Write()

# close the file
f.Close()
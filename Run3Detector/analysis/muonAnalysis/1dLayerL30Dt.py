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

# define the function to get the time differences for the max heights of events in each channel between layer 0 and layer 3
def getTimeDiff(self):
    
    time_diffsL30 = []

    # central time mask
    centralTimeMask = (self.events['timeFit_module_calibrated_corrected'] > 1100) & (self.events['timeFit_module_calibrated_corrected'] < 1400)

    # height and area mask
    heightAreaMask = (self.events['height'] > 1000) & (self.events['area'] > 500000)

    finalPulseMask = centralTimeMask & heightAreaMask & (self.events['ipulse'] == 0)

    # apply the finalPulseMask
    masked_time = self.events['timeFit_module_calibrated_corrected'][finalPulseMask]
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

    # calculate time differences only for events with valid times in all layers
    for i in range(len(timeL0_min)):
        if timeL0_min[i] is not None and timeL1_min[i] is not None and timeL2_min[i] is not None and timeL3_min[i] is not None:
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

'''
# check if command line arguments are provided
if len(sys.argv) != 3:
    print("Usage: python3 [file_name] [start_file_index] [end_file_index]")
    sys.exit(1)

# assign start and end indices from command line
start_index = int(sys.argv[1])
end_index = int(sys.argv[2])

# define a file list to run over
filelist = [
    f"/home/bpeng/muonAnalysis/MilliQan_Run1541.{i}_v34.root"
    for i in range(start_index, end_index + 1)
    if os.path.exists(f"/home/bpeng/muonAnalysis/MilliQan_Run1541.{i}_v34.root")
]
'''
filelist = ['/home/bpeng/muonAnalysis/MilliQan_Run1500_v34_skim_correction.root']

# define the necessary branches to run over
branches = ['pickupFlag', 'boardsMatched', 'timeFit_module_calibrated_corrected', 'height', 'area', 'column', 'row', 'layer', 'chan', 'ipulse', 'type']

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
h_1d = r.TH1F("h_1d", "Time Differences between Layer 3 and 0", 100, -50, 50)
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
f = r.TFile("S1500LayerL30Dt.root", "recreate")

# write the histograms to the file
h_1d.Write()

# close the file
f.Close()

'''
# calculate the finite integral within a certain range
bin_min = h_1d.FindBin(-8)
bin_max = h_1d.FindBin(9)
integral = h_1d.Integral(bin_min, bin_max)

print(f"Integral of the histogram from -8 to 9: {integral}")
'''
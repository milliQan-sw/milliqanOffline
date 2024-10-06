# Importing packages
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
import concurrent.futures
# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# Try to find the utilities directory in the current directory
utilities_dir = os.path.join(script_dir, '..', 'utilities')
if not os.path.exists(utilities_dir):
    # If not found, adjust the path to look one level higher
    utilities_dir = os.path.join(script_dir, '..', '..', 'utilities')
# Add the utilities directory to the Python path
sys.path.append(utilities_dir)
from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *


# Define the function to get the time differences
def getTimeDiff(self):
    time_diffsL30 = []

    # Area mask
    barAreaMask = self.events['nPE'] > 100
    timeWindowMask = (self.events['timeFit_module_calibrated'] > 1000) & (self.events['timeFit_module_calibrated'] < 1500)
    topSideMask = self.events['area'][self.events['type'] == 2] < 100000
    print(self.events['layer'][self.events['type'] == 0])

    # Pick the first pulse
    barFinalPulseMask = barAreaMask & timeWindowMask & topSideMask & (self.events['ipulse'] == 0)

    # Apply the finalPulseMask
    masked_time = self.events['timeFit_module_calibrated'][barFinalPulseMask]
    masked_layer = self.events['layer'][barFinalPulseMask]

    # Masked times per layer
    timeL0 = masked_time[masked_layer == 0]
    timeL1 = masked_time[masked_layer == 1]
    timeL2 = masked_time[masked_layer == 2]
    timeL3 = masked_time[masked_layer == 3]

    timeLn1 = masked_time[masked_layer == -1]

    # Find the minimum time per event (This should be repetitive to ipulse == 0)
    timeL0_min = ak.min(timeL0, axis=1, mask_identity=True)
    timeL1_min = ak.min(timeL1, axis=1, mask_identity=True)
    timeL2_min = ak.min(timeL2, axis=1, mask_identity=True)
    timeL3_min = ak.min(timeL3, axis=1, mask_identity=True)

    timeLn1_min = ak.min(timeLn1, axis=1, mask_identity=True)

    for i in range(len(timeL0_min)):
        # Require pulses in all 4 layers and the front slab for one event
        if timeL0_min[i] is not None and timeL1_min[i] is not None and timeL2_min[i] is not None and timeL3_min[i] is not None and timeLn1_min[i] is not None:
            # Calculate time differences only for events with valid times in all layers
            time_diffsL30.append(timeL3_min[i] - timeL0_min[i])
    
    print(time_diffsL30)

    # Extend the final list to match the size of the current file
    num_events = len(self.events)
    num_nones = num_events - len(time_diffsL30)
    time_diffsL30.extend([None] * num_nones)

    # Define custom branch
    self.events['timeDiff'] = time_diffsL30


# Add our custom function to milliqanCuts
setattr(milliqanCuts, 'getTimeDiff', getTimeDiff)

# Define the range of runs
start_run_number = 1000
end_run_number = 1000

# Define a file list to run over
filelist = []

# To specify the filelist
for run_number in range(start_run_number, end_run_number + 1):
    print(f"Starting processing for run number: {run_number}")
    file_number = 0
    consecutive_missing_files = 0
    while True:
        file_path = f"/home/bpeng/muonAnalysis/1000/MilliQan_Run{run_number}.{file_number}_v34.root" 
        if os.path.exists(file_path):
            print(f"Found file: {file_path}")
            filelist.append(file_path)
            consecutive_missing_files = 0  # Reset counter since file was found
        else:
            print(f"File not found: {file_path}")
            consecutive_missing_files += 1
            if consecutive_missing_files >= 10: # Set the patience as 10
                print(f"No more files found after {file_number} for run {run_number}")
                break
        file_number += 1
print(f"Total files collected: {len(filelist)}")

# Define the necessary branches to run over
branches = ['fileNumber', 'runNumber', 'tTrigger', 'event', 'pickupFlag', 'boardsMatched', 'timeFit_module_calibrated', 'height', 'area', 'column', 'row', 'layer', 'chan', 'ipulse', 'type', 'beamOn']

# Define the milliqan cuts object
mycuts = milliqanCuts()

# require that all digitizer boards are matched
boardMatchCut = mycuts.getCut(mycuts.boardsMatched, 'boardMatchCut', cut=True, branches=branches)

# require pulses are not pickup
pickupCut = mycuts.getCut(mycuts.pickupCut, 'pickupCut', cut=True, branches=branches)

# Define milliqan plotter
myplotter = milliqanPlotter()

# Create a 1D root histogram
h_1d = r.TH1F("h_1d", f"Run {start_run_number} to {end_run_number} time difference", 100, -50, 50)

# Add root histogram to plotter
myplotter.addHistograms(h_1d, 'timeDiff')

# Defining the cutflow 
cutflow = [boardMatchCut, pickupCut, mycuts.getTimeDiff, myplotter.dict['h_1d']]

# Create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

# Print out the schedule
myschedule.printSchedule()

# Create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

# Run the milliqan processor
myiterator.run()

# Draw the histogram
canvas = r.TCanvas("canvas", "canvas", 800, 600)
h_1d.Draw()

# Create a new TFile
f = r.TFile(f"Run{start_run_number}to{end_run_number}Dt.root", "recreate")

# Write the canvas (including histogram and text) to the file
canvas.Write()

# Close the file
f.Close()
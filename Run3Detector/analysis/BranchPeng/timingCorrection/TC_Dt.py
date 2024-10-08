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

    # Event based mask
    panelMask = ak.any(self.events['area'][self.events['type'] == 2] < 100000, axis=1) # type bar = 0, slab = 1, panel = 2

    # Pulse based mask
    firstPulseMask = self.events['ipulse'] == 0
    npeMask = self.events['nPE'] > 100
    timeWindowMask = (self.events['timeFit_module_calibrated'] > 1000) & (self.events['timeFit_module_calibrated'] < 1500)
    
    # Combined mask
    combinedMask = npeMask & timeWindowMask & firstPulseMask & panelMask

    # Initialize mask for straight line events with pulses in all four layers
    straightLine4LMask = ak.ArrayBuilder()

    for col in range(4):
        for row in range(4):
            locationMask = (self.events['col'] == col) & (self.events['row'] == row) & combinedMask

            masked_time = self.events['timeFit_module_calibrated'][locationMask]
            masked_layer = self.events['layer'][locationMask]

            # Masks for individual layers
            timeL0 = masked_time[masked_layer == 0]
            timeL1 = masked_time[masked_layer == 1]
            timeL2 = masked_time[masked_layer == 2]
            timeL3 = masked_time[masked_layer == 3]

            # Flatten and check if all layers are present in each event
            hasL0 = ~ak.is_none(ak.min(timeL0, axis=1, mask_identity=True))
            hasL1 = ~ak.is_none(ak.min(timeL1, axis=1, mask_identity=True))
            hasL2 = ~ak.is_none(ak.min(timeL2, axis=1, mask_identity=True))
            hasL3 = ~ak.is_none(ak.min(timeL3, axis=1, mask_identity=True))

            # Event mask for pulses across all four layers
            eventMask = hasL0 & hasL1 & hasL2 & hasL3

            # Append result to straightLine4LMask
            straightLine4LMask.append(eventMask)

    # Finalize the straightLine4LMask by converting it to an awkward array
    straightLine4LMask = ak.concatenate(straightLine4LMask.snapshot())

            






    self.events['timeDiff'] = time_diffsL30


# Add our custom function to milliqanCuts
setattr(milliqanCuts, 'getTimeDiff', getTimeDiff)

# Define the range of runs
start_run_number = 1541
end_run_number = 1541

# Define a file list to run over
filelist = []

# To specify the filelist
for run_number in range(start_run_number, end_run_number + 1):
    # Determine folder based on run number (using integer division)
    folder_number = (run_number // 100) * 100
    folder_path = f"/home/bpeng/muonAnalysis/{folder_number}"
    
    print(f"Starting processing for run number: {run_number} in folder: {folder_path}")
    file_number = 0
    consecutive_missing_files = 0
    while True:
        file_path = f"{folder_path}/MilliQan_Run{run_number}.{file_number}_v34.root" 
        if os.path.exists(file_path):
            print(f"Found file: {file_path}")
            filelist.append(file_path)
            consecutive_missing_files = 0  # Reset counter since file was found
        else:
            print(f"File not found: {file_path}")
            consecutive_missing_files += 1
            if consecutive_missing_files >= 10:  # Set the patience as 10
                print(f"No more files found after {file_number} for run {run_number}")
                break
        file_number += 1

# Define the necessary branches to run over
branches = ['fileNumber', 'runNumber', 'tTrigger', 'event', 'pickupFlag', 'boardsMatched', 'timeFit_module_calibrated', 'height', 'area', 'column', 'row', 'layer', 'chan', 'ipulse', 'type', 'nPE', 'beamOn']

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
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


# Define the function to get the event count by channel
def getEventbyChan(self):
    accumulatedChan = []

    # Pulse mask
    firstPulseMask = self.events['ipulse'] == 0
    npeMask = self.events['nPE'] > 100
    timeWindowMask = (self.events['timeFit_module_calibrated'] > 1000) & (self.events['timeFit_module_calibrated'] < 1500)

    # Event mask
    panelMask = ak.any(self.events['area'][self.events['type'] == 2] < 100000, axis=1) # type bar = 0, slab = 1, panel = 2
    
    # Pick the first pulse
    finalMask = npeMask & timeWindowMask & panelMask & firstPulseMask

    # Apply the finalPulseMask
    masked_chan = self.events['chan'][finalMask]
    masked_layer = self.events['layer'][finalMask]

    # Divide Masked chan by layer and flatten the 2D lists into 1D
    chanL0 = masked_chan[masked_layer == 0]
    chanL1 = masked_chan[masked_layer == 1]
    chanL2 = masked_chan[masked_layer == 2]
    chanL3 = masked_chan[masked_layer == 3]

    # Flatten the 2D lists into 1D
    chanL0_flat = ak.min(chanL0, axis=1, mask_identity=True)
    chanL1_flat = ak.min(chanL1, axis=1, mask_identity=True)
    chanL2_flat = ak.min(chanL2, axis=1, mask_identity=True)
    chanL3_flat = ak.min(chanL3, axis=1, mask_identity=True)

    for i in range(len(chanL0_flat)):
        if (    chanL0_flat[i] is not None 
            and chanL1_flat[i] is not None  
            and chanL2_flat[i] is not None 
            and chanL3_flat[i] is not None
            ):
            accumulatedChan.append(chanL0_flat[i])
            accumulatedChan.append(chanL1_flat[i])
            accumulatedChan.append(chanL2_flat[i])
            accumulatedChan.append(chanL3_flat[i])

    print('Number of chan with pulse:', len(accumulatedChan))
    
    # Extend the final list to match the size of the current file
    num_events = len(self.events)
    num_nones = num_events - len(accumulatedChan)
    accumulatedChan.extend([None] * num_nones)

    self.events['accumulatedChan'] = accumulatedChan


# Add our custom function to milliqanCuts
setattr(milliqanCuts, 'getEventbyChan', getEventbyChan)

# Define the range of runs
start_run_number = 1540
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
h_1d = r.TH1F("h_1d", f"Run {start_run_number} to {end_run_number} Event Count VS Chan", 80, 0, 80)

# Add root histogram to plotter
myplotter.addHistograms(h_1d, 'timeDiff')

# Defining the cutflow 
cutflow = [boardMatchCut, pickupCut, mycuts.getEventbyChan, myplotter.dict['h_1d']]

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
f = r.TFile(f"Run{start_run_number}to{end_run_number}eventByChan.root", "recreate")

# Write the canvas (including histogram and text) to the file
canvas.Write()

# Close the file
f.Close()
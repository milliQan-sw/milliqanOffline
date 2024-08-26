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


# Initialize a cumulative event count dictionary
cumulativeChanEventCount = {(row, column, layer): 0 for row in range(4) for column in range(4) for layer in range(4)}

def getEventCount(self):
    chanEventCount = {(row, column, layer): 0 for row in range(4) for column in range(4) for layer in range(4)}

    for i in range(len(self.events)):
        for row in range(4):
            for col in range(4):
                chanL0 = self.events[(self.events['layer'] == 0) & (self.events['row'] == row) & (self.events['column'] == col)]
                chanL1 = self.events[(self.events['layer'] == 1) & (self.events['row'] == row) & (self.events['column'] == col)]
                chanL2 = self.events[(self.events['layer'] == 2) & (self.events['row'] == row) & (self.events['column'] == col)]
                chanL3 = self.events[(self.events['layer'] == 3) & (self.events['row'] == row) & (self.events['column'] == col)]

                if chanL0[i] is not None and chanL1[i] is not None and chanL2[i] is not None and chanL3[i] is not None:
                    chanEventCount[(row, col, 0)] += 1
                    chanEventCount[(row, col, 1)] += 1
                    chanEventCount[(row, col, 2)] += 1
                    chanEventCount[(row, col, 3)] += 1

    return chanEventCount

# Add our custom function to milliqanCuts
setattr(milliqanCuts, 'getEventCount', getEventCount)

# Define the range of runs
start_run_number = 1000 
end_run_number = 1009

# Define a file list to run over
filelist = [] 

# this will add all the files that need to be processed into the filelist
for run_number in range(start_run_number, end_run_number + 1):
    print(f"Processing run number: {run_number}")
    file_number = 0
    consecutive_missing_files = 0
    while True:
        file_path = f"/home/bpeng/muonAnalysis/1000/MilliQan_Run{run_number}.{file_number}_v34.root" 
        if os.path.exists(file_path):
            filelist.append(file_path)
            file_number += 1
            consecutive_missing_files = 0
        else:
            consecutive_missing_files += 1
            if consecutive_missing_files >= 10:
                print(f"No more files found after {file_number} for run {run_number}")
                break
            file_number += 1

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

# Defining the cutflow
cutflow = [boardMatchCut, pickupCut, mycuts.getEventCount]

# Create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

# Print out the schedule
myschedule.printSchedule()

# Create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

# Run the milliqan processor and accumulate results
for file in filelist:
    # Process the current file
    myiterator.run()
    
    # Get the event counts from the current file
    fileEventCount = mycuts.getEventCount()
    
    # Update the cumulative event counts
    for key in cumulativeChanEventCount:
        cumulativeChanEventCount[key] += fileEventCount[key]

# Print the cumulative event counts after processing all files
for key, value in cumulativeChanEventCount.items():
    print(f"Channel {key}: {value} events")
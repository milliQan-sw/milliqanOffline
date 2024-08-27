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


# Define the function to get the event count of each channel
def getEventCount(self):
    for row in range(4):
        for col in  range(4):
            for lay in range(4):
                # this branch tells if an event has pulses in current channel (event-based)
                self.events[f"col{col}_row{row}_lay{lay}"] = ak.any((self.events['layer'] == lay & self.events['row'] == row & self.events['column'] == col), axis = 1) 
            # this branch tells if an event has pulses in all 4 layers (event-based)
            self.events[f"col{col}_row{row}"] = self.events[f"col{col}_row{row}_lay{0}"] & self.events[f"col{col}_row{row}_lay{1}"] & self.events[f"col{col}_row{row}_lay{2}"] & self.events[f"col{col}_row{row}_lay{3}"]
            
            for lay in range(4):
                # count straight line path pulses as events for channels
                self.events[f"Count_col{col}_row{row}_lay{lay}"] = ak.count_nonezero(self.events[f"col{col}_row{row}"] & self.events[f"col{col}_row{row}_lay{lay}"] )
    
            

# Add our custom function to milliqanCuts
setattr(milliqanCuts, 'getEventCount', getEventCount)

# Define the range of runs
start_run_number = 1000 
end_run_number = 1009

# Define a file list to run over
filelist = [] 

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

# Run the milliqan processor
myiterator.run()
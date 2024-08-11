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

# Define the function to get the number of events 
def getEventNum(self):
    eventCount = 0

    col = 0
    row = 0
    lay = 0

    locationMask = (self.events['column'] == col) & (self.events['row'] == row) & (self.events['layer'] == lay)

    eventsSL = self.events['straightLineCut']

    eventsFiltered = ak.any(eventsSL[locationMask], axis = 1)

    for i in range(len(eventsFiltered)):
        if eventsFiltered[i] is True:
            eventCount += 1

    print(eventCount)

# Add our custom function to milliqanCuts
setattr(milliqanCuts, 'getEventNum', getEventNum)

# Define the range of runs (from Run1000-1009 to Run1620-1629: 63 histograms)
start_run_number = 1000 ######################################################################################################################################################
end_run_number = 1000 ########################################################################################################################################################

# Define a file list to run over
filelist = []

for run_number in range(start_run_number, end_run_number + 1):
    print(f"Processing run number: {run_number}")
    file_number = 0
    consecutive_missing_files = 0
    while True:
        file_path = f"/home/bpeng/muonAnalysis/1000/MilliQan_Run{run_number}.{file_number}_v34.root" #########################################################################
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
branches = ['timeFit_module_calibrated', 'height', 'area', 'column', 'row', 'layer', 'chan', 'ipulse', 'type', 'beamOn']

# Define the milliqan cuts object
mycuts = milliqanCuts()

# Define milliqan plotter
myplotter = milliqanPlotter()

# Defining the cutflow
cutflow = [mycuts.getEventNum]

# Create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

# Print out the schedule
myschedule.printSchedule()

# Create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

# Run the milliqan processor
myiterator.run()
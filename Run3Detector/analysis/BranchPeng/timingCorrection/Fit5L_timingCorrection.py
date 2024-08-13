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


# Define the function to get the time differences
def getTimeDiff(self):
    time_diffsL30 = []

    # Area mask
    barAreaMask = self.events['area'] > 500000
    slabAreaMask = self.events['area'] > 500000 / 12

    # Pick the first pulse
    barFinalPulseMask = barAreaMask & (self.events['ipulse'] == 0)
    slabFinalPulseMask = slabAreaMask & (self.events['ipulse'] == 0)

    # Apply the finalPulseMask
    masked_time1 = self.events['timeFit_module_calibrated'][barFinalPulseMask]
    masked_layer1 = self.events['layer'][barFinalPulseMask]

    masked_time2 = self.events['timeFit_module_calibrated'][slabFinalPulseMask]
    masked_layer2 = self.events['layer'][slabFinalPulseMask]

    # Masked times per layer
    timeL0 = masked_time1[masked_layer1 == 0]
    timeL1 = masked_time1[masked_layer1 == 1]
    timeL2 = masked_time1[masked_layer1 == 2]
    timeL3 = masked_time1[masked_layer1 == 3]

    timeL4 = masked_time2[masked_layer2 == 4]

    # Function to get minimum time per event handling None values
    def minTime(pulse_times):
        filtered_times = [time for time in pulse_times if time is not None]
        return min(filtered_times) if filtered_times else None

    # Extract minimum times for each layer
    timeL0_min = [minTime(event) for event in ak.to_list(timeL0)]
    timeL1_min = [minTime(event) for event in ak.to_list(timeL1)]
    timeL2_min = [minTime(event) for event in ak.to_list(timeL2)]
    timeL3_min = [minTime(event) for event in ak.to_list(timeL3)]
    timeL4_min = [minTime(event) for event in ak.to_list(timeL4)]

    for i in range(len(timeL0_min)):
        # Require pulses in all 4 layers and the back panel for one event
        if timeL0_min[i] is not None and timeL1_min[i] is not None and timeL2_min[i] is not None and timeL3_min[i] is not None and timeL4_min[i] is not None:
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

# Define the range of runs (from Run1000-1009 to Run1620-1629: 63 histograms)
start_run_number = 1000 ######################################################################################################################################################
end_run_number = 1009 ########################################################################################################################################################

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
branches = ['pickupFlag', 'boardsMatched', 'timeFit_module_calibrated', 'height', 'area', 'column', 'row', 'layer', 'chan', 'ipulse', 'type', 'beamOn']

# Define the milliqan cuts object
mycuts = milliqanCuts()

# require pulses are not pickup
pickupCut = mycuts.getCut(mycuts.pickupCut, 'pickupCut', cut=True, branches=branches)

# require that all digitizer boards are matched
boardMatchCut = mycuts.getCut(mycuts.boardsMatched, 'boardMatchCut', cut=True, branches=branches)

# Define milliqan plotter
myplotter = milliqanPlotter()

# Create a 1D root histogram
h_1d = r.TH1F("h_1d", f"Run {start_run_number} to {end_run_number} time difference", 100, -50, 50)

# Add root histogram to plotter
myplotter.addHistograms(h_1d, 'timeDiff')

# Defining the cutflow
cutflow = [boardMatchCut, pickupCut, mycuts.layerCut, mycuts.getTimeDiff, myplotter.dict['h_1d']]

# Create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

# Print out the schedule
myschedule.printSchedule()

# Create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

# Run the milliqan processor
myiterator.run()


# Fit the histogram with a single Gaussian function for the peak and save the canvas to the ROOT file
def fit_histogram(hist, root_file):
    # Define the Gaussian model for the peak
    gaus1 = r.TF1("gaus1", "gaus", -11, 15)  # Range #####################################################################################################################

    # Initial parameter estimates for the Gaussian function
    gaus1.SetParameters(14, -0.5, 5.145)  # Max Mean Stddev ##############################################################################################################

    # Fit the histogram with the Gaussian model
    hist.Fit(gaus1, "R")

    # Get the mean and stddev of the peak (gaus1)
    mean_peak = gaus1.GetParameter(1)
    stddev_peak = abs(gaus1.GetParameter(2))

    # Draw the histogram and individual fit
    c = r.TCanvas()
    hist.Draw()
    gaus1.SetLineColor(r.kRed) # Red for Beam, Blue for Cosmic ###########################################################################################################
    gaus1.Draw("same")

    # Add the mean and stddev values as text on the plot
    text = r.TText()
    text.SetNDC()
    text.SetTextSize(0.03)
    text.DrawText(0.15, 0.80, f"Mean of the Beam peak: {mean_peak:.2f}") #################################################################################################
    text.DrawText(0.15, 0.75, f"Stddev of the Cosmic peak: {stddev_peak:.2f}") ###########################################################################################

    # Save the canvas to the ROOT file
    root_file.cd()
    c.Write("TimeDiffs_Fit_Canvas")

    return mean_peak, stddev_peak


# Create a new TFile for the fitted histogram and canvas
f_fit = r.TFile(f"FitRun{start_run_number}to{end_run_number}TC.root", "recreate")

# Fit the histogram and get the mean and stddev of the peak
mean_peak, stddev_peak = fit_histogram(h_1d, f_fit)
print("Mean of the peak:", mean_peak)
print("Stddev of the peak:", stddev_peak)

# Close the fit file
f_fit.Close()
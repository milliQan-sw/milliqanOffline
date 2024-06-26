# Run this scirpt on milliqan-pc
# The ###### comments are only for easier locating parameters as I need to change them frequently
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

# Define the function to get the time differences
def getTimeDiff(self):

    time_diffsL30 = []

    # Height and area mask
    areaMask = self.events['area'] > 100000

    # Pick the first pulse
    finalPulseMask = areaMask & (self.events['ipulse'] == 0)

    # Apply the finalPulseMask
    masked_time = self.events['timeFit_module_calibrated'][finalPulseMask]
    masked_layer = self.events['layer'][finalPulseMask]

    # Masked times per layer
    timeL0 = masked_time[masked_layer == 0]
    timeL1 = masked_time[masked_layer == 1]
    timeL2 = masked_time[masked_layer == 2]
    timeL3 = masked_time[masked_layer == 3]

    # Function to get minimum time per event handling None values
    def minTime(pulse_times):
        filtered_times = [time for time in pulse_times if time is not None]
        return min(filtered_times) if filtered_times else None

    # Extract minimum times for each layer
    timeL0_min = [minTime(event) for event in ak.to_list(timeL0)]
    timeL1_min = [minTime(event) for event in ak.to_list(timeL1)]
    timeL2_min = [minTime(event) for event in ak.to_list(timeL2)]
    timeL3_min = [minTime(event) for event in ak.to_list(timeL3)]

    for i in range(len(timeL0_min)):
        # Require pulses in all 4 layers for one event
        if timeL0_min[i] is not None and timeL1_min[i] is not None and timeL2_min[i] is not None and timeL3_min[i] is not None:
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

# Define the range of runs (from Run1000-1009 to Run1620-1629: 62 histograms) 
start_run_number = 1120 ######################################################################################################################################################
end_run_number = 1129 ########################################################################################################################################################

# Define a file list to run over
filelist = []
for run_number in range(start_run_number, end_run_number + 1):
    file_number = 0
    consecutive_missing_files = 0
    while True:
        file_path = f"/home/bpeng/muonAnalysis/1100/MilliQan_Run{run_number}.{file_number}_v34.root" #########################################################################
        if os.path.exists(file_path):
            filelist.append(file_path)
            file_number += 1
            consecutive_missing_files = 0
        else:
            consecutive_missing_files += 1
            if consecutive_missing_files >= 10:
                break
            file_number += 1

# Define the necessary branches to run over
branches = ['pickupFlag', 'boardsMatched', 'timeFit_module_calibrated', 'height', 'area', 'column', 'row', 'layer', 'chan', 'ipulse', 'type']

# Define the milliqan cuts object
mycuts = milliqanCuts()

# Require pulses are not pickup
pickupCut = mycuts.getCut(mycuts.pickupCut, 'pickupCut', cut=True, branches=branches)

# Require that all digitizer boards are matched
boardMatchCut = mycuts.getCut(mycuts.boardsMatched, 'boardMatchCut', cut=True, branches=branches)

# Add four layer cut
fourLayerCut = mycuts.getCut(mycuts.fourLayerCut, 'fourLayerCut', cut=False)

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

# Create a new TFile
f = r.TFile(f"Run{start_run_number}to{end_run_number}timingCorrection.root", "recreate")

# Write the histograms to the file
h_1d.Write()

# Close the file
f.Close()
'''
# Fit the histogram with a combined model of two Gaussian functions and save the canvas to the ROOT file
def fit_histogram(hist, root_file):
    if not isinstance(hist, r.TH1):
        print("Error: The provided object is not a histogram.")
        return None, None

    # Define the combined Gaussian model
    combined_gaus = r.TF1("combined_gaus", "gaus(0) + gaus(3)", -50, 50)
    
    # Initial parameter estimates for the two Gaussian functions
    combined_gaus.SetParameters(6, -28.5, 5.145, 115, -5.5, 4.165)  # Max Mean Stddev ##################################################################################################

    # Fit the histogram with the combined model
    hist.Fit(combined_gaus, "R")

    # Extract the individual Gaussian functions from the combined model
    gaus1 = r.TF1("gaus1", "gaus", -40, -18)  # Range ##################################################################################################################################
    gaus2 = r.TF1("gaus2", "gaus", -12, 3)  # Range ####################################################################################################################################
    for i in range(3):
        gaus1.SetParameter(i, combined_gaus.GetParameter(i))
        gaus2.SetParameter(i, combined_gaus.GetParameter(i + 3))

    # Get the mean and stddev of the right peak (gaus2)
    mean_right_peak = gaus2.GetParameter(1)
    stddev_right_peak = abs(gaus2.GetParameter(2))

    # Draw the histogram and individual fits
    c = r.TCanvas()
    hist.Draw()
    gaus1.SetLineColor(r.kRed)
    gaus1.Draw("same")
    gaus2.SetLineColor(r.kBlue)
    gaus2.Draw("same")

    # Add the mean value as text on the plot
    text = r.TText()
    text.SetNDC()
    text.SetTextSize(0.03)
    text.DrawText(0.15, 0.85, f"Mean of the right peak: {mean_right_peak:.2f}")
    text.DrawText(0.15, 0.80, f"Stddev of the right peak: {stddev_right_peak:.2f}")

    # Save the canvas to the ROOT file
    root_file.cd()
    c.Write("TimeDiffs_Fit_Canvas")

    return mean_right_peak, stddev_right_peak

# Create a new TFile for the fitted histogram and canvas
f_fit = r.TFile(f"FitRun{start_run}to{end_run}timingCorrection.root", "recreate")

# Open the original ROOT file and retrieve the histogram
f_orig = r.TFile(f"Run{start_run}to{end_run}timingCorrection.root")
h_timeDiff = f_orig.Get("h_timeDiff")

# Fit the histogram and get the mean of the right peak
mean_right_peak, stddev_right_peak = fit_histogram(h_timeDiff, f_fit)
print("Mean of the right peak:", mean_right_peak)
print("Stddev of the right peak:", stddev_right_peak)

# Close the files
f_fit.Close()
f_orig.Close()
'''
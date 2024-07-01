# Run this scirpt on milliqan-pc
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
    areaMask = self.events['area'] > 500000

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
    timeL4 = masked_time[masked_layer == 4]

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
end_run_number = 1002 ########################################################################################################################################################

# Define a file list to run over
filelist = []
beamOn_true_count = 0
total_files_count = 0

for run_number in range(start_run_number, end_run_number + 1):
    print(f"Processing run number: {run_number}")
    file_number = 0
    consecutive_missing_files = 0
    while True:
        file_path = f"/home/bpeng/muonAnalysis/1000/MilliQan_Run{run_number}.{file_number}_v34.root" ##########################################################################
        if os.path.exists(file_path):
            filelist.append(file_path)
            try:
                with uproot.open(file_path) as file:
                    tree = file["t"]
                    beamOn = tree["beamOn"].array(library="np")
                    if np.any(beamOn):
                        beamOn_true_count += 1
                    total_files_count += 1
                print(f"Processed file: {file_path}")
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
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

# Create a 1D root histogram
h_1d = r.TH1F("h_1d", f"Run {start_run_number} to {end_run_number} time difference", 100, -50, 50)

# Add root histogram to plotter
myplotter.addHistograms(h_1d, 'timeDiff')

# Defining the cutflow
cutflow = [mycuts.getTimeDiff, myplotter.dict['h_1d']]

# Create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

# Print out the schedule
myschedule.printSchedule()

# Create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

# Run the milliqan processor
myiterator.run()

# Calculate the percentage of beamOn == True files
beamOn_true_percentage = (beamOn_true_count / total_files_count) * 100
print(f"Percentage of beam on files: {beamOn_true_percentage:.2f}%")

# Fit the histogram with a combined model of two Gaussian functions and save the canvas to the ROOT file
def fit_histogram(hist, beamOn_true_percentage, root_file):
    if not isinstance(hist, r.TH1):
        print("Error: The provided object is not a histogram.")
        return None, None

    # Define the combined Gaussian model
    combined_gaus = r.TF1("combined_gaus", "gaus(0) + gaus(3)", -50, 50)
    
    # Initial parameter estimates for the two Gaussian functions
    combined_gaus.SetParameters(27, -16.5, 3.48, 18, -1.5, 8.575)  # Max Mean Stddev ######################################################################################################################

    # Fit the histogram with the combined model
    hist.Fit(combined_gaus, "R")

    # Extract the individual Gaussian functions from the combined model
    gaus1 = r.TF1("gaus1", "gaus", -31, -2)  # Range ######################################################################################################################################################
    gaus2 = r.TF1("gaus2", "gaus", -19, 16)  # Range ######################################################################################################################################################
    for i in range(3):
        gaus1.SetParameter(i, combined_gaus.GetParameter(i))
        gaus2.SetParameter(i, combined_gaus.GetParameter(i + 3))

    # Get the mean and stddev of the left peak (gaus1)
    mean_left_peak = gaus1.GetParameter(1)
    stddev_left_peak = abs(gaus1.GetParameter(2))

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

    # Add the mean and stddev values as text on the plot
    text = r.TText()
    text.SetNDC()
    text.SetTextSize(0.03)
    text.DrawText(0.15, 0.85, f"Mean of the cosmic peak: {mean_left_peak:.2f}")
    text.DrawText(0.15, 0.80, f"Stddev of the cosmic peak: {stddev_left_peak:.2f}")
    text.DrawText(0.15, 0.75, f"Mean of the beam peak: {mean_right_peak:.2f}")
    text.DrawText(0.15, 0.70, f"Stddev of the beam peak: {stddev_right_peak:.2f}")
    text.DrawText(0.15, 0.65, f"Beam on files percentage: {beamOn_true_percentage:.2f}%")

    # Save the canvas to the ROOT file
    root_file.cd()
    c.Write("TimeDiffs_Fit_Canvas")

    return mean_left_peak, stddev_left_peak, mean_right_peak, stddev_right_peak

# Create a new TFile for the fitted histogram and canvas
f_fit = r.TFile(f"FitRun{start_run_number}to{end_run_number}timingCorrection.root", "recreate")

# Fit the histogram and get the mean of the left and right peaks
mean_left_peak, stddev_left_peak, mean_right_peak, stddev_right_peak = fit_histogram(h_1d, beamOn_true_percentage, f_fit)
print("Mean of the left peak:", mean_left_peak)
print("Stddev of the left peak:", stddev_left_peak)
print("Mean of the right peak:", mean_right_peak)
print("Stddev of the right peak:", stddev_right_peak)

# Close the fit file
f_fit.Close()
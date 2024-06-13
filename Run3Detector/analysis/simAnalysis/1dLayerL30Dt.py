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

    # nPE mask to replace height and area mask
    nPEMask = self.events['hit_nPE'] > 200

    # muon mask
    muonMask = self.events['hit_particleName'] == 13

    # make final cut
    finalPulseMask = nPEMask & muonMask

    # apply the finalPulseMask
    masked_time = self.events['hit_hitTime_ns'][finalPulseMask]
    masked_layer = self.events['hit_layer'][finalPulseMask]

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

    for i in range(len(timeL0_min)):
        # require pulses in all 4 layers for one event
        if timeL0_min[i] is not None and timeL1_min[i] is not None and timeL2_min[i] is not None and timeL3_min[i] is not None:
            # calculate time differences only for events with valid times in all layers
            time_diffsL30.append(timeL1_min[i] - timeL0_min[i])
    
    print(time_diffsL30)

    # extend the final list to match the size of the current file
    num_events = len(self.events)
    num_nones = num_events - len(time_diffsL30)
    time_diffsL30.extend([None] * num_nones)

    # define custom branch
    self.events['timeDiff'] = time_diffsL30

# add our custom function to milliqanCuts
setattr(milliqanCuts, 'getTimeDiff', getTimeDiff)

filelist = ['/home/bpeng/muonAnalysis/dy_nophoton_flat.root']

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

# define the necessary branches to run over
branches = ['hit_hitTime_ns', 'hit_nPE', 'hit_layer', 'hit_chan', 'hit_particleName']

# define the milliqan cuts object
mycuts = milliqanCuts()

# define milliqan plotter
myplotter = milliqanPlotter()

# create a 1D root histogram
h_1d = r.TH1F("h_1d", "Time Differences between Layer 1 and 0", 100, -50, 50)
h_1d.GetXaxis().SetTitle("Time Differences")

# add root histogram to plotter
myplotter.addHistograms(h_1d, 'timeDiff')

# defining the cutflow
cutflow = [mycuts.getTimeDiff, myplotter.dict['h_1d']]

# create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

# print out the schedule
myschedule.printSchedule()

# create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

# run the milliqan processor
myiterator.run()

# create a new TFile
f = r.TFile("SimLayerL10Dt.root", "recreate")

# write the histograms to the file
h_1d.Write()

# close the file
f.Close()

'''
# fit the histogram with a combined model of two Gaussian functions and save the canvas to the ROOT file
def fit_histogram(hist, root_file):
    # define the combined Gaussian model
    combined_gaus = r.TF1("combined_gaus", "gaus(0) + gaus(3)", -50, 50)
    
    # initial parameter estimates for the two Gaussian functions
    combined_gaus.SetParameters(45, -17, 6, 140, 0, 6)

    # fit the histogram with the combined model
    hist.Fit(combined_gaus, "R")

    # extract the individual Gaussian functions from the combined model
    gaus1 = r.TF1("gaus1", "gaus", -31, -3)
    gaus2 = r.TF1("gaus2", "gaus", -14, 14)
    for i in range(3):
        gaus1.SetParameter(i, combined_gaus.GetParameter(i))
        gaus2.SetParameter(i, combined_gaus.GetParameter(i + 3))

    # integrate the right peak
    integral_right_peak = gaus2.Integral(-14, 14)

    # draw the histogram and individual fits
    c = r.TCanvas()
    hist.Draw()
    # do not draw the combined Gaussian
    gaus1.SetLineColor(r.kRed)
    gaus1.Draw("same")
    gaus2.SetLineColor(r.kBlue)
    gaus2.Draw("same")

    # add the integrated number as text on the plot
    text = r.TText()
    text.SetNDC()
    text.SetTextSize(0.03)
    text.DrawText(0.15, 0.85, f"Integral of the right peak: {integral_right_peak:.2f}")

    # save the canvas to the ROOT file
    root_file.cd()
    c.Write("TimeDiffs_Fit_Canvas")

    return integral_right_peak

# create a new TFile for the fitted histogram and canvas
f_fit = r.TFile("S1500LayerL30DtFit.root", "recreate")

# open the original ROOT file and retrieve the histogram
f_orig = r.TFile("S1500LayerL30Dt.root")
h_1d = f_orig.Get("h_1d")

# fit the histogram and get the integral of the right peak
integral_right_peak = fit_histogram(h_1d, f_fit)
print("Integral of the right peak:", integral_right_peak)

# close the files
f_fit.Close()
f_orig.Close()
'''
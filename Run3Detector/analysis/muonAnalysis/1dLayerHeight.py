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

# define the function to get the height
def getHeight(self):
    iheight = self.events['height'][self.events['ipulse'] == 0]
    self.events['iheight'] = iheight

# add our custom function to milliqanCuts
setattr(milliqanCuts, 'getHeight', getHeight)

filelist = ['/home/bpeng/muonAnalysis/MilliQan_Run1000_v34_skim_correction.root']

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
branches = ['pickupFlag', 'boardsMatched', 'timeFit_module_calibrated_corrected', 'height', 'area', 'column', 'row', 'layer', 'chan', 'ipulse', 'type']

# define the milliqan cuts object
mycuts = milliqanCuts()

# require pulses are not pickup
pickupCut = mycuts.getCut(mycuts.pickupCut, 'pickupCut', cut=True, branches=branches)

# require that all digitizer boards are matched
boardMatchCut = mycuts.getCut(mycuts.boardsMatched, 'boardMatchCut', cut=True, branches=branches)

# add four layer cut
fourLayerCut = mycuts.getCut(mycuts.fourLayerCut, 'fourLayerCut', cut=False)

# define milliqan plotter
myplotter = milliqanPlotter()

# create a 1D root histogram
h_1d = r.TH1F("h_1d", "Height(ipulse == 0)", 300, 0, 3000)
h_1d.GetXaxis().SetTitle("Height")

# add root histogram to plotter
myplotter.addHistograms(h_1d, 'iheight')

# defining the cutflow
cutflow = [boardMatchCut, pickupCut, mycuts.layerCut, mycuts.getHeight, myplotter.dict['h_1d']]

# create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

# print out the schedule
myschedule.printSchedule()

# create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

# run the milliqan processor
myiterator.run()

# create a new TFile
f = r.TFile("S1000LayerHeight.root", "recreate")

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
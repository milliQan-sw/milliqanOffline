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

# define the function to get the row and column
def getRowCol(self):
    
    rowL0_Tmin = []
    colL0_Tmin = []

    rowL1_Tmin = []
    colL1_Tmin = []

    rowL2_Tmin = []
    colL2_Tmin = []

    rowL3_Tmin = []
    colL3_Tmin = []

    # central time mask
    centralTimeMask = (self.events['timeFit_module_calibrated_corrected'] > 1100) & (self.events['timeFit_module_calibrated_corrected'] < 1400)

    # height and area mask
    heightAreaMask = (self.events['height'] > 1000) & (self.events['area'] > 500000)

    # require ipulse == 0
    finalPulseMask = centralTimeMask & heightAreaMask & (self.events['ipulse'] == 0)

    # apply the finalPulseMask
    masked_time = self.events['timeFit_module_calibrated_corrected'][finalPulseMask]
    masked_layer = self.events['layer'][finalPulseMask]
    masked_row = self.events['row'][finalPulseMask]
    masked_col = self.events['column'][finalPulseMask]

    # masked times/rows/columns per layer
    timeL0 = masked_time[masked_layer == 0]
    rowL0 = masked_row[masked_layer == 0]
    colL0 = masked_col[masked_layer == 0]

    timeL1 = masked_time[masked_layer == 1]
    rowL1 = masked_row[masked_layer == 1]
    colL1 = masked_col[masked_layer == 1]

    timeL2 = masked_time[masked_layer == 2]
    rowL2 = masked_row[masked_layer == 2]
    colL2 = masked_col[masked_layer == 2]

    timeL3 = masked_time[masked_layer == 3]
    rowL3 = masked_row[masked_layer == 3]
    colL3 = masked_col[masked_layer == 3]

    # function to get minimum time per event
    def minTime(pulse_times):
        filtered_times = [time for time in pulse_times if time is not None]
        return min(filtered_times) if filtered_times else None

    # extract minimum time of each event, make a mask to get the row and column of corresponding pulse
    timeL0_min = [minTime(event) for event in ak.to_list(timeL0)]
    maskL0_min = (timeL0_min == ak.broadcast_arrays(timeL0, timeL0_min)[0])
    raw_rowL0 = ak.mask(rowL0, maskL0_min)
    rowL0_min = ak.Array([next((item for item in sublist if item is not None), None) if sublist else None for sublist in ak.to_list(raw_rowL0)])
    raw_colL0 = ak.mask(colL0, maskL0_min)
    colL0_min = ak.Array([next((item for item in sublist if item is not None), None) if sublist else None for sublist in ak.to_list(raw_colL0)])

    timeL1_min = [minTime(event) for event in ak.to_list(timeL1)]
    maskL1_min = (timeL1_min == ak.broadcast_arrays(timeL1, timeL1_min)[0])
    raw_rowL1 = ak.mask(rowL1, maskL1_min)
    rowL1_min = ak.Array([next((item for item in sublist if item is not None), None) if sublist else None for sublist in ak.to_list(raw_rowL1)])
    raw_colL1 = ak.mask(colL1, maskL1_min)
    colL1_min = ak.Array([next((item for item in sublist if item is not None), None) if sublist else None for sublist in ak.to_list(raw_colL1)])

    timeL2_min = [minTime(event) for event in ak.to_list(timeL2)]
    maskL2_min = (timeL2_min == ak.broadcast_arrays(timeL2, timeL2_min)[0])
    raw_rowL2 = ak.mask(rowL2, maskL2_min)
    rowL2_min = ak.Array([next((item for item in sublist if item is not None), None) if sublist else None for sublist in ak.to_list(raw_rowL2)])
    raw_colL2 = ak.mask(colL2, maskL2_min)
    colL2_min = ak.Array([next((item for item in sublist if item is not None), None) if sublist else None for sublist in ak.to_list(raw_colL2)])

    timeL3_min = [minTime(event) for event in ak.to_list(timeL3)]
    maskL3_min = (timeL3_min == ak.broadcast_arrays(timeL3, timeL3_min)[0])
    raw_rowL3 = ak.mask(rowL3, maskL3_min)
    rowL3_min = ak.Array([next((item for item in sublist if item is not None), None) if sublist else None for sublist in ak.to_list(raw_rowL3)])
    raw_colL3 = ak.mask(colL3, maskL3_min)
    colL3_min = ak.Array([next((item for item in sublist if item is not None), None) if sublist else None for sublist in ak.to_list(raw_colL3)])

    for i in range(len(timeL0_min)):
        # require pulses in all 4 layers for one event
        if timeL0_min[i] is not None and timeL1_min[i] is not None and timeL2_min[i] is not None and timeL3_min[i] is not None:

            rowL0_Tmin.append(rowL0_min[i])
            colL0_Tmin.append(colL0_min[i])

            rowL1_Tmin.append(rowL1_min[i])
            colL1_Tmin.append(colL1_min[i])

            rowL2_Tmin.append(rowL2_min[i])
            colL2_Tmin.append(colL2_min[i])

            rowL3_Tmin.append(rowL3_min[i])
            colL3_Tmin.append(colL3_min[i])
    
    for i in range(len(rowL0_Tmin)):
        print(rowL0_Tmin[i], colL0_Tmin[i])

    # extend the final list to match the size of the current file
    num_events = len(self.events)
    num_nones = num_events - len(rowL0_Tmin)

    rowL0_Tmin.extend([None] * num_nones)
    colL0_Tmin.extend([None] * num_nones)

    self.events['rowL0'] = rowL0_Tmin
    self.events['colL0'] = colL0_Tmin

# add our custom function to milliqanCuts
setattr(milliqanCuts, 'getRowCol', getRowCol)

filelist = ['/home/bpeng/muonAnalysis/MilliQan_Run1300_v34_skim_correction.root']

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

# create a 2D root histogram
h_2d = r.TH2F("h_2d", "Rows VS Columns", 4, 0, 4, 4, 0, 4)
h_2d.GetXaxis().SetTitle("Column")
h_2d.GetYaxis().SetTitle("Row")

# add root histogram to plotter
myplotter.addHistograms(h_2d, ['colL0', 'rowL0'], cut=None)

# defining the cutflow
cutflow = [boardMatchCut, pickupCut, mycuts.layerCut, mycuts.getRowCol, myplotter.dict['h_2d']]

# create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

# print out the schedule
myschedule.printSchedule()

# create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

# run the milliqan processor
myiterator.run()

'''
# create a new TFile
f = r.TFile("S1500LayerL30Dt.root", "recreate")

# write the histograms to the file
h_1d.Write()

# close the file
f.Close()

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
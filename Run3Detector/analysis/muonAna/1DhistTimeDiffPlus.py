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

# define the function to get the 16 (or less) time difference between pulses in layer0 and layer1
import awkward as ak

def getTimeDiff(self):
    # get the branches after cuts 
    rows = self.events['row'][self.events['straightLineCut']]
    columns = self.events['column'][self.events['straightLineCut']]
    layers = self.events['layer'][self.events['straightLineCut']]
    heights = self.events['height'][self.events['straightLineCut']]
    times = self.events['timeFit_module_calibrated'][self.events['straightLineCut']]

    # initialize dictionary to hold max heights and corresponding times for each sensor for each event
    max_heights = {}
    min_times = {}

    # iterate over each channel (here using row/column/layer)
    for row in range(4):
        for column in range(4):
            for layer in range(2):
                # generate key for dictionary
                key = (row, column, layer)
                # define the mask for the current channel
                condition = (rows == row) & (columns == column) & (layers == layer)
                # get sublist heights under the condition
                channel_heights = heights[condition]
                channel_times = times[condition]

                # find the max height of each sublist and its corresponding time
                if ak.any(ak.num(channel_heights) > 0):  # check if there are non-empty sublists
                    max_heights[key] = ak.max(channel_heights, axis=-1)
                    # boolean mask for where each sublist achieves its max height
                    max_mask = channel_heights == ak.broadcast_arrays(max_heights[key], channel_heights)[0]
                    # use the mask to select the minimum times corresponding to the max heights
                    masked_times = ak.mask(channel_times, max_mask)
                    # select the first occurrence of the time where the max height is found
                    min_times[key] = ak.min(masked_times, axis=-1)

    # calculate time differences between layer 1 and layer 0 for each channel for each event
    time_diffs = []
    for row in range(4):
        for column in range(4):
            key0 = (row, column, 0)
            key1 = (row, column, 1)
            if key0 in min_times and key1 in min_times:
                # compute time difference for each event in the channel
                channel_diffs = min_times[key1] - min_times[key0]
                time_diffs.append(channel_diffs)

    print(time_diffs)

    # fit the list data into timeDiff branch to make plots
    self.events['timeDiff'] = time_diffs

# add our custom function to milliqanCuts
setattr(milliqanCuts, 'getTimeDiff', getTimeDiff)

# define a file list to run over
filelist = ['/mnt/hadoop/se/store/user/milliqan/trees/v34/1000/MilliQan_Run1006.4_v34.root:t']

# define the necessary branches to run over
branches = ['pickupFlag', 'boardsMatched', 'timeFit_module_calibrated', 'height', 'area', 'column', 'row', 'layer', 'chan', 'ipulse', 'type']

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
h_1d = r.TH1F("h_1d", "Time Difference 1D Hist", 80, -40, 40)
h_1d.GetXaxis().SetTitle("time difference between layer 0 and 1")

# add root histogram to plotter
myplotter.addHistograms(h_1d, 'timeDiff')

# defining the cutflow
cutflow = [boardMatchCut, pickupCut, mycuts.layerCut, mycuts.straightLineCut, mycuts.getTimeDiff, myplotter.dict['h_1d']]

# create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

# print out the schedule
myschedule.printSchedule()

# create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

# run the milliqan processor
myiterator.run()

# create a new TFile
f = r.TFile("1DhistTimeDiff.root", "recreate")

# write the histograms to the file
h_1d.Write()

# close the file
f.Close()
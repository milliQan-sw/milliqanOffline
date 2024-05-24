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

# define the function to get the rows and columns of straight lines
def getRowColumn(self):

    max_heightsL0 = {}
    max_timeL0 = {}

    max_heightsL1 = {}
    max_timeL1 = {}

    max_heightsL2 = {}
    max_timeL2 = {}

    max_heightsL3 = {}
    max_timeL3 = {}

    rows = []
    columns = []

    # remove events with panel pulses that pass the height cut (1D boolean list)
    panel_pulse_mask = (self.events['type'] == 2) & (self.events['height'] > 1200)
    events_without_panel_pulses = ~ak.any(panel_pulse_mask, axis = 1)

    # keep only events that have less than 2 pulses whose heights are bigger than 1000 (1D boolean list)
    high_pulse_count_mask = ak.sum(self.events['height'] > 1000, axis=1) <= 2

    # combine masks to get valid events (1D boolean list)
    conbined_mask = events_without_panel_pulses #& high_pulse_count_mask

# iterate over row and column combinations
    for row in range(4):
        for column in range(4):
            # pulse_based 2D boolean masks determined by channel and height
            pulse_maskL0 = (self.events['row'] == row) & (self.events['column'] == column) & (self.events['layer'] == 0) & (self.events['height'] > 1000)
            pulse_maskL1 = (self.events['row'] == row) & (self.events['column'] == column) & (self.events['layer'] == 1) & (self.events['height'] > 1000)
            pulse_maskL2 = (self.events['row'] == row) & (self.events['column'] == column) & (self.events['layer'] == 2) & (self.events['height'] > 1000)
            pulse_maskL3 = (self.events['row'] == row) & (self.events['column'] == column) & (self.events['layer'] == 3) & (self.events['height'] > 1000)

            # event_based 1D boolean mask determined by event
            event_mask = ak.any(pulse_maskL0, axis = 1) & ak.any(pulse_maskL1, axis = 1) & ak.any(pulse_maskL2, axis = 1) & ak.any(pulse_maskL3, axis = 1)

            # combine all the masks
            mask0 = event_mask & pulse_maskL0 & conbined_mask
            mask1 = event_mask & pulse_maskL1 & conbined_mask
            mask2 = event_mask & pulse_maskL2 & conbined_mask
            mask3 = event_mask & pulse_maskL3 & conbined_mask

            heightsL0 = self.events['height'][mask0]
            timeL0 = self.events['timeFit_module_calibrated'][mask0]

            heightsL1 = self.events['height'][mask1]
            timeL1 = self.events['timeFit_module_calibrated'][mask1]

            heightsL2 = self.events['height'][mask2]
            timeL2 = self.events['timeFit_module_calibrated'][mask2]

            heightsL3 = self.events['height'][mask3]
            timeL3 = self.events['timeFit_module_calibrated'][mask3]

            # store heights and times into dictionaries
            key = (row, column)

            if len(heightsL0) > 0:
                # 1D max heights of each event
                max_heightsL0[key] = ak.max(heightsL0, axis=1)

                # broadcast to get a 2D list with every pulse being max height
                # then get a 2D boolean list to pick out which pulse has the max height so we can extract its time later
                max_maskL0 = (heightsL0 == ak.broadcast_arrays(max_heightsL0[key], heightsL0)[0])

                # get a 2D list of the times for the pulses with max heights
                raw_max_timesL0 = ak.mask(timeL0, max_maskL0)

                # pull down the time of each sublist to get a 1D list of times
                max_timeL0[key] = ak.Array([
                    min((item for item in sublist if item is not None), default=None)
                    if sublist else None
                    for sublist in ak.to_list(raw_max_timesL0)
                ])
            else:
                max_timeL0[key] = [None] * len(self.events)

            # do the same for other 3 layers
            if len(heightsL1) > 0:
                max_heightsL1[key] = ak.max(heightsL1, axis=1)
                max_maskL1 = (heightsL1 == ak.broadcast_arrays(max_heightsL1[key], heightsL1)[0])
                raw_max_timesL1 = ak.mask(timeL1, max_maskL1)
                max_timeL1[key] = ak.Array([
                    min((item for item in sublist if item is not None), default=None)
                    if sublist else None
                    for sublist in ak.to_list(raw_max_timesL1)
                ])
            else:
                max_timeL1[key] = [None] * len(self.events)

            if len(heightsL2) > 0:
                max_heightsL2[key] = ak.max(heightsL2, axis=1)
                max_maskL2 = (heightsL2 == ak.broadcast_arrays(max_heightsL2[key], heightsL2)[0])
                raw_max_timesL2 = ak.mask(timeL2, max_maskL2)
                max_timeL2[key] = ak.Array([
                    min((item for item in sublist if item is not None), default=None)
                    if sublist else None
                    for sublist in ak.to_list(raw_max_timesL2)
                ])
            else:
                max_timeL2[key] = [None] * len(self.events)

            if len(heightsL3) > 0:
                max_heightsL3[key] = ak.max(heightsL3, axis=1)
                max_maskL3 = (heightsL3 == ak.broadcast_arrays(max_heightsL3[key], heightsL3)[0])
                raw_max_timesL3 = ak.mask(timeL3, max_maskL3)
                max_timeL3[key] = ak.Array([
                    min((item for item in sublist if item is not None), default=None)
                    if sublist else None
                    for sublist in ak.to_list(raw_max_timesL3)
                ])
            else:
                max_timeL3[key] = [None] * len(self.events)

            # iterate over each event in current row and column combination
            for event in range(len(max_timeL0[key])):
                if max_timeL0[key][event] is not None and max_timeL1[key][event] is not None and max_timeL2[key][event] is not None and max_timeL3[key][event] is not None:
                    rows.append(row)
                    columns.append(column)

    for i in range(len(rows)):
        print(columns[i], rows[i])

    # extend the final lists to match the size of the current file
    num_events = len(self.events)
    num_nones = num_events - len(rows)
    rows.extend([None] * num_nones)
    columns.extend([None] * num_nones)

    # define custom branches
    self.events['rows'] = rows
    self.events['columns'] = columns

# add our custom function to milliqanCuts
setattr(milliqanCuts, 'getRowColumn', getRowColumn)

# check if command line arguments are provided
if len(sys.argv) != 3:
    print("Usage: python3 [file_name] [start_file_index] [end_file_index]")
    sys.exit(1)

# assign start and end indices from command line
start_index = int(sys.argv[1])
end_index = int(sys.argv[2])

# define a file list to run over
filelist = [
    f"/home/bpeng/muonAnalysis/MilliQan_Run1118.{i}_v34.root"
    for i in range(start_index, end_index + 1)
]

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

# create a 2D root histogram
h_2d = r.TH2F("h_2d", "Rows VS Columns", 4, 0, 4, 4, 0, 4)
h_2d.GetXaxis().SetTitle("Column")
h_2d.GetYaxis().SetTitle("Row")

# add root histogram to plotter
myplotter.addHistograms(h_2d, ['columns', 'rows'], cut=None)

# defining the cutflow
cutflow = [boardMatchCut, pickupCut, mycuts.layerCut, mycuts.getRowColumn, myplotter.dict['h_2d']]

# create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

# print out the schedule
myschedule.printSchedule()

# create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

# run the milliqan processor
myiterator.run()

# create a new TFile
f = r.TFile("2DhistRowVsColumn.root", "recreate")

# write the histograms to the file
h_2d.Write()

# close the file
f.Close()
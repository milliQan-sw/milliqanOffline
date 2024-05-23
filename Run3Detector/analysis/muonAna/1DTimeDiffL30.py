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

    max_heightsL0 = {}
    max_timeL0 = {}
    max_heightsL1 = {}
    max_timeL1 = {}
    max_heightsL2 = {}
    max_timeL2 = {}
    max_heightsL3 = {}
    max_timeL3 = {}

    time_diffsL30 = []

    # Remove events with panel pulses that pass the height cut
    panel_pulse_mask = (self.events['type'] == 2) & (self.events['height'] > 1200)
    events_without_panel_pulses = ~ak.any(panel_pulse_mask, axis=1)

    # Keep only events that have less than 2 pulses whose heights are bigger than 1000
    high_pulse_count_mask = ak.sum(self.events['height'] > 1000, axis=1) <= 2

    # Combine masks to get valid events
    valid_events_mask = events_without_panel_pulses & high_pulse_count_mask

    # Print the number of events before and after applying the mask
    num_events_before = len(self.events)
    num_valid_events = ak.sum(valid_events_mask)
    print(f"Number of events before filtering: {num_events_before}")
    print(f"Number of valid events after filtering: {num_valid_events}")

    # Apply the valid events mask to the entire events dataset
    valid_events = self.events[valid_events_mask]

    # Iterate over straight line passes
    for row in range(4):
        for column in range(4):
            # Pulse-based 2D boolean masks determined by channel and height
            pulse_maskL0 = (valid_events['row'] == row) & (valid_events['column'] == column) & (valid_events['layer'] == 0) & (valid_events['height'] > 1000)
            pulse_maskL1 = (valid_events['row'] == row) & (valid_events['column'] == column) & (valid_events['layer'] == 1) & (valid_events['height'] > 1000)
            pulse_maskL2 = (valid_events['row'] == row) & (valid_events['column'] == column) & (valid_events['layer'] == 2) & (valid_events['height'] > 1000)
            pulse_maskL3 = (valid_events['row'] == row) & (valid_events['column'] == column) & (valid_events['layer'] == 3) & (valid_events['height'] > 1000)

            # Event-based 1D boolean mask determined by event
            event_mask = ak.any(pulse_maskL0, axis=1) & ak.any(pulse_maskL1, axis=1) & ak.any(pulse_maskL2, axis=1) & ak.any(pulse_maskL3, axis=1)

            # Combine all the masks
            mask0 = event_mask & pulse_maskL0
            mask1 = event_mask & pulse_maskL1
            mask2 = event_mask & pulse_maskL2
            mask3 = event_mask & pulse_maskL3

            heightsL0 = valid_events['height'][mask0]
            timeL0 = valid_events['timeFit_module_calibrated'][mask0]

            heightsL1 = valid_events['height'][mask1]
            timeL1 = valid_events['timeFit_module_calibrated'][mask1]

            heightsL2 = valid_events['height'][mask2]
            timeL2 = valid_events['timeFit_module_calibrated'][mask2]

            heightsL3 = valid_events['height'][mask3]
            timeL3 = valid_events['timeFit_module_calibrated'][mask3]

            # Store heights and times into dictionaries
            key = (row, column)

            if len(heightsL0) > 0:
                # 1D max heights of each event
                max_heightsL0[key] = ak.max(heightsL0, axis=1)

                # Broadcast to get a 2D list with every pulse being max height
                # Then get a 2D boolean list to pick out which pulse has the max height so we can extract its time later
                max_maskL0 = (heightsL0 == ak.broadcast_arrays(max_heightsL0[key], heightsL0)[0])

                # Get a 2D list of the times for the pulses with max heights
                raw_max_timesL0 = ak.mask(timeL0, max_maskL0)

                # Pull down the time of each sublist to get a 1D list of times
                max_timeL0[key] = ak.Array([
                    min((item for item in sublist if item is not None), default=None)
                    if sublist else None
                    for sublist in ak.to_list(raw_max_timesL0)
                ])
            else:
                max_timeL0[key] = [None] * len(valid_events)

            # Do the same for other 3 layers
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
                max_timeL1[key] = [None] * len(valid_events)

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
                max_timeL2[key] = [None] * len(valid_events)

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
                max_timeL3[key] = [None] * len(valid_events)

            # Debug statements to check intermediate results
            print(f"Processing row {row}, column {column}")
            print(f"max_timeL0: {max_timeL0[key]}")
            print(f"max_timeL1: {max_timeL1[key]}")
            print(f"max_timeL2: {max_timeL2[key]}")
            print(f"max_timeL3: {max_timeL3[key]}")

            # Iterate over each event
            for event in range(len(valid_events)):
                if max_timeL0[key][event] is not None and max_timeL1[key][event] is not None and max_timeL2[key][event] is not None and max_timeL3[key][event] is not None:
                    time_diffsL30.append(max_timeL3[key][event] - max_timeL0[key][event])

    print(time_diffsL30)

    # Extend the final list to match the size of the current file
    num_events = len(self.events)
    num_nones = num_events - len(time_diffsL30)
    time_diffsL30.extend([None] * num_nones)

    # Define custom branch
    self.events['timeDiff'] = time_diffsL30

# add our custom function to milliqanCuts
setattr(milliqanCuts, 'getTimeDiff', getTimeDiff)

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

# create a 1D root histogram
h_1d = r.TH1F("h_1d", "Time Differences between Layer 3 and 0", 200, -100, 100)
h_1d.GetXaxis().SetTitle("Time Differences")

# add root histogram to plotter
myplotter.addHistograms(h_1d, 'timeDiff')

# defining the cutflow
cutflow = [boardMatchCut, pickupCut, mycuts.layerCut, mycuts.getTimeDiff, myplotter.dict['h_1d']]

# create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

# print out the schedule
myschedule.printSchedule()

# create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

# run the milliqan processor
myiterator.run()

# create a new TFile
f = r.TFile("1DhistTimeDiffL30.root", "recreate")

# write the histograms to the file
h_1d.Write()

# close the file
f.Close()
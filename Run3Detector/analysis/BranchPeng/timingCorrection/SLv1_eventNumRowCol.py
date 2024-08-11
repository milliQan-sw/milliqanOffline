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

# Define the function to count events for each channel
def countEventsPerChannel(self):
    print("Starting countEventsPerChannel function...")
    # Define the cut to keep only events with straight line paths
    straight_line_events = []
    for event_index, event in enumerate(self.events):
        event_kept = False  # A boolean variable used for checking pass or not
        for row in range(4):
            for column in range(4):
                # Create boolean masks for each layer at the specific row and column
                pulse_maskL0 = (event['row'] == row) & (event['column'] == column) & (event['layer'] == 0)
                pulse_maskL1 = (event['row'] == row) & (event['column'] == column) & (event['layer'] == 1)
                pulse_maskL2 = (event['row'] == row) & (event['column'] == column) & (event['layer'] == 2)
                pulse_maskL3 = (event['row'] == row) & (event['column'] == column) & (event['layer'] == 3)

                # Check if the event has pulses in all four layers at this (row, column)
                if ak.any(pulse_maskL0) and ak.any(pulse_maskL1) and ak.any(pulse_maskL2) and ak.any(pulse_maskL3):
                    event_kept = True
                    break  # No need to check other row/column combinations for this event
            if event_kept:
                break

        if event_kept:
            straight_line_events.append(event)
        else:
            straight_line_events.append(None)  # Replace events without straight line paths with None

        # Debug output
        if event_index % 100 == 0:
            print(f"Processed {event_index + 1}/{len(self.events)} events")

    print("Finished filtering events. Starting to count events per channel...")

    # Initialize a dictionary to store the count of events for each (row, column, layer) combination
    channel_counts = {(row, column, layer): 0 for row in range(4) for column in range(4) for layer in range(4)}

    for event_index, event in enumerate(straight_line_events):
        if event is None:
            continue  # Skip events that were cut out
        for row in range(4):
            for column in range(4):
                for layer in range(4):
                    # Boolean mask for the specific channel
                    channel_mask = (event['row'] == row) & (event['column'] == column) & (event['layer'] == layer)
                    # If the event has any pulse in this channel, count the event
                    if ak.any(channel_mask):
                        channel_counts[(row, column, layer)] += 1
                        break  # Count the event only once per channel

        # Debug output
        if event_index % 100 == 0:
            print(f"Counted {event_index + 1}/{len(straight_line_events)} events")

    print("Finished counting events per channel.")
    return channel_counts

# Add our custom functions to milliqanCuts
setattr(milliqanCuts, 'countEventsPerChannel', countEventsPerChannel)

# Define the range of runs (from Run1000-1009 to Run1620-1629: 63 histograms)
start_run_number = 1000 #################################################################################################################
end_run_number = 1000 ###################################################################################################################

# Define a file list to run over
filelist = []

for run_number in range(start_run_number, end_run_number + 1):
    print(f"Processing run number: {run_number}")
    file_number = 0
    consecutive_missing_files = 0
    while True:
        file_path = f"/home/bpeng/muonAnalysis/1000/MilliQan_Run{run_number}.{file_number}_v34.root" ####################################
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

# Defining the cutflow
cutflow = [mycuts.countEventsPerChannel]

# Create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts)

# Print out the schedule
myschedule.printSchedule()

# Create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts)

# Initialize a dictionary to accumulate total event counts for each channel (row, column, layer)
total_channel_counts = {(row, column, layer): 0 for row in range(4) for column in range(4) for layer in range(4)}

# Run the milliqan processor and accumulate the results
for events in myiterator.run():
    event_counts = mycuts.countEventsPerChannel()
    for channel, count in event_counts.items():
        total_channel_counts[channel] += count

# Print out the final event counts for each channel
print("Final event counts for each channel (row, column, layer):")
for (row, column, layer), count in total_channel_counts.items():
    print(f"Row {row}, Column {column}, Layer {layer}: {count} events")
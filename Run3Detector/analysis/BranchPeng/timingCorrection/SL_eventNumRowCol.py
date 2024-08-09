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

def process_file(file_path):
    print(f"Processing file: {file_path}")
    try:
        # Open the ROOT file and retrieve the events
        with uproot.open(file_path) as file:
            events = file["t"].arrays(branches, library="ak")  # Use the correct tree name
            print(f"Successfully retrieved events from: {file_path}")
            return countEventsPerChannel(events)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

def countEventsPerChannel(events):
    print("Starting countEventsPerChannel function...")
    # Define the cut to keep only events with straight line paths
    straight_line_events = []
    for event_index, event in enumerate(events):
        event_kept = False
        for row in range(4):
            for column in range(4):
                pulse_maskL0 = (event['row'] == row) & (event['column'] == column) & (event['layer'] == 0)
                pulse_maskL1 = (event['row'] == row) & (event['column'] == column) & (event['layer'] == 1)
                pulse_maskL2 = (event['row'] == row) & (event['column'] == column) & (event['layer'] == 2)
                pulse_maskL3 = (event['row'] == row) & (event['column'] == column) & (event['layer'] == 3)

                if ak.any(pulse_maskL0) and ak.any(pulse_maskL1) and ak.any(pulse_maskL2) and ak.any(pulse_maskL3):
                    event_kept = True
                    break
            if event_kept:
                break

        if event_kept:
            straight_line_events.append(event)

        if event_index % 100 == 0:
            print(f"Processed {event_index + 1}/{len(events)} events")

    print("Finished filtering events. Starting to count events per channel...")

    channel_counts = {(row, column, layer): 0 for row in range(4) for column in range(4) for layer in range(4)}

    for event_index, event in enumerate(straight_line_events):
        for row in range(4):
            for column in range(4):
                for layer in range(4):
                    channel_mask = (event['row'] == row) & (event['column'] == column) & (event['layer'] == layer)
                    if ak.any(channel_mask):
                        channel_counts[(row, column, layer)] += 1
                        break

        if event_index % 100 == 0:
            print(f"Counted {event_index + 1}/{len(straight_line_events)} events")

    print("Finished counting events per channel.")
    return channel_counts

def process_files_in_parallel(filelist):
    total_channel_counts = {(row, column, layer): 0 for row in range(4) for column in range(4) for layer in range(4)}

    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:  # Set to 8 workers
        for event_counts in executor.map(process_file, filelist):
            if event_counts is None:
                continue
            for channel, count in event_counts.items():
                total_channel_counts[channel] += count

    return total_channel_counts

# Define the range of runs
start_run_number = 1000
end_run_number = 1001

# Define a file list to run over
filelist = []

for run_number in range(start_run_number, end_run_number + 1):
    print(f"Processing run number: {run_number}")
    file_number = 0
    consecutive_missing_files = 0
    while True:
        file_path = f"/home/bpeng/muonAnalysis/1000/MilliQan_Run{run_number}.{file_number}_v34.root"
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

# Process files in parallel and accumulate results
total_channel_counts = process_files_in_parallel(filelist)

# Print out the final event counts for each channel
print("Final event counts for each channel (row, column, layer):")
for (row, column, layer), count in total_channel_counts.items():
    print(f"Row {row}, Column {column}, Layer {layer}: {count} events")
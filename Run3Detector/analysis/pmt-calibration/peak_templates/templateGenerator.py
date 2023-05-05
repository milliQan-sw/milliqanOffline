#!/usr/bin/env python3
import ROOT as r
import sys
from array import array

# Load in data file
dataDir = "/home/rsantos/Data/PostProcessData/"
peakTemplateFile = r.TFile(dataDir + sys.argv[1])
tree = peakTemplateFile.Get("Events")

# Define area to store plots
if len(sys.argv) == 3:
    plotDir = sys.argv[2]
else:
    plotDir = "."

# Plot the waveform and save it in a ROOT file
tree.GetEvent(1)
voltages = array('d', tree.voltages)
times = array('d', tree.times)

# Determine offset



# Determine Noise



# Determine Voltage Range


graph = r.TGraph(len(voltages), times, voltages)
graph.Draw()

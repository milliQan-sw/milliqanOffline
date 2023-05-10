#!/usr/bin/env python3
import ROOT as r
import sys
import numpy as np
import os

sys.path.insert(0 , '/home/rsantos/milliqanOffline/Run3Detector/analysis/')
from pmt_calibration.python.TemplateTools import averageOfLists


# Load in data file
dataDir = "/home/rsantos/Data/PostProcessData/"
peakTemplateFile = r.TFile(dataDir + sys.argv[1])
tree = peakTemplateFile.Get("Events")

tree.GetEvent(1)
nEvents = tree.GetEntries()
nEntries = len(tree.voltages)

if os.path.isfile("./voltages.npy"):
    voltageArray = np.load("./voltages.npy")
else:
    voltageArray = np.empty([nEvents, nEntries])
if os.path.isfile("./times.npy"):
    timesArray = np.load("./times.npy")
else:
    timesArray = np.empty([nEvents, nEntries])
    for i, event in enumerate(tree):
        voltageArray[i] = event.voltages
        timesArray[i] = event.times
        if i % 100 == 0:
            print(i)
    np.save('voltages.npy', voltageArray)
    np.save('times.npy', timesArray)



# Define area to store plots
if len(sys.argv) == 3:
    plotDir = sys.argv[2]
else:
    plotDir = "."

voltageAverage = np.mean(voltageArray, axis=0)
outputFile = r.TFile.Open("template.root", "RECREATE")
print("About to graph")
graph = r.TGraph(nEntries, timesArray[0], voltageAverage)
graph.Draw("AC*")
graph.Write()




# Determine Noise



# Determine Voltage Range


#graph = r.TGraph(len(voltages), times, voltages)
#graph.Draw()

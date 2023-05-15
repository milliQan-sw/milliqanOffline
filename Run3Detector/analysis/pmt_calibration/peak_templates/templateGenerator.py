#!/usr/bin/env python3
import ROOT as r
import sys
import numpy as np
import os

sys.path.insert(0 , '/home/rsantos/milliqanOffline/Run3Detector/analysis/')
from pmt_calibration.python.TemplateTools import averageOfLists, movingAverage

reuseValues = True
NANOSECONDS_PER_SAMPLE = 2.

# Load in data file
dataDir = "/home/rsantos/Data/PostProcessData/"
peakTemplateFile = r.TFile(dataDir + sys.argv[1])
tree = peakTemplateFile.Get("Events")

tree.GetEvent(1)
nEvents = tree.GetEntries()
nEntries = len(tree.voltages)

# Should save numpy arrays and load if possible because it takes ~40 minutes to produce.
if reuseValues:
    voltageArray = np.load("savedArrays/voltages847.npy")
else:
    voltageArray = np.empty([nEvents, nEntries])
    for i, event in enumerate(tree):
        voltageArray[i] = event.voltages

        if i % 100 == 0:
            print(i)
    np.save('savedArrays/voltages847.npy', voltageArray)

timesArray = np.arange(0, NANOSECONDS_PER_SAMPLE * len(voltageArray), 2.5)
assert len(voltageArray) == len(timesArray)

# Define area to store plots
if len(sys.argv) == 3:
    plotDir = sys.argv[2]
else:
    plotDir = "."

voltageAverage = np.mean(voltageArray, axis=0)
outputFile = r.TFile.Open("template847.root", "RECREATE")
print("About to graph")

canvas = r.TCanvas("c", "c")

graph = r.TGraph(nEntries, timesArray, voltageAverage)
graph.Draw("AC")

# Select time region that contains the whole signal
# To do this find the maximum value inside the numpy array and then place
# arbitrary cutoffs at points that visually look like they are outside the signal region
# Looks like 1900, 1160 would be good
timeCutoffBand = 150 # May need to change this value
sampleBand = 50 # How many values before/after the signal region you want to use to calculate baseline
maximumIndex = np.argmax(voltageAverage)

lowerSignalCutoff = maximumIndex - timeCutoffBand
upperSignalCutoff = maximumIndex + timeCutoffBand

signalCutoffLineUpper = r.TLine(timesArray[upperSignalCutoff], 0, timesArray[upperSignalCutoff], 100)
signalCutoffLineUpper.SetLineColor(2)
signalCutoffLineLower = r.TLine(timesArray[lowerSignalCutoff], 0, timesArray[lowerSignalCutoff], 100)
signalCutoffLineLower.SetLineColor(2)
signalCutoffLineUpper.Draw()
signalCutoffLineLower.Draw()

interpolatedTimes = timesArray[lowerSignalCutoff:upperSignalCutoff+1] # +1 to include end point
# Loop over each individual waveform
integratedChargeHistogram = r.TH1D('Area', 'Area', 5000, -1000, 4000 )
tempAreaArray  = np.zeros(len(voltageArray), dtype = float)
for i, waveform in enumerate(voltageArray):
    # To form baseline take results from before signal and after signal and average them together
    # Each sample is taken every 2.5 ns so taking 10 voltage entries gives 25ns
    movingAverageBuffer = 5 # When taking moving average, the number of items in list you take average of at a time
    lowerMovingAverage = np.array(movingAverage(waveform[lowerSignalCutoff - sampleBand: lowerSignalCutoff], n = movingAverageBuffer), dtype=float)
    upperMovingAverage = np.array(movingAverage(waveform[upperSignalCutoff + 1 : upperSignalCutoff + sampleBand+1], n=movingAverageBuffer), dtype = float)
    interpolation = np.interp(interpolatedTimes,
                              np.concatenate((timesArray[lowerSignalCutoff-sampleBand: lowerSignalCutoff-(movingAverageBuffer -1)], timesArray[upperSignalCutoff : upperSignalCutoff + (sampleBand +1 - movingAverageBuffer)]), axis=None),
                              np.concatenate((lowerMovingAverage, upperMovingAverage), axis=None))
    #print(interpolation)
    baseline = np.concatenate((lowerMovingAverage, interpolation, upperMovingAverage), axis = None)
    # Plot everything together for an example plot
    baselineSubtractedWaveform = np.subtract(waveform[lowerSignalCutoff-50:upperSignalCutoff+43], baseline)
    integratedChargeHistogram.Fill(np.trapz(baselineSubtractedWaveform))
    tempAreaArray[i] = np.trapz(baselineSubtractedWaveform)

     # Only plot the first graphs as example
    if i == 0:
        canvas.Clear()
        waveform_graph = r.TGraph(len(waveform[lowerSignalCutoff-50:upperSignalCutoff+51]), timesArray[lowerSignalCutoff-50:upperSignalCutoff+51], waveform[lowerSignalCutoff-50:upperSignalCutoff+51])
        baseline_graph = r.TGraph(len(baseline),timesArray[lowerSignalCutoff-50:upperSignalCutoff+51],baseline)
        baseline_graph.SetLineColor(2)
        waveform_graph.Draw()
        baseline_graph.Draw("SAME")
        canvas.Write("ExampleWaveformAndBaseline")

        canvas.Clear()
        print(len(waveform[lowerSignalCutoff-50:upperSignalCutoff+43]))
        print(len(baseline))
        assert len(waveform[lowerSignalCutoff-50:upperSignalCutoff+43]) == len(baseline)
        baselineSubtractedGraph = r.TGraph(len(baselineSubtractedWaveform), timesArray[lowerSignalCutoff-50:upperSignalCutoff+43], baselineSubtractedWaveform)
        baselineSubtractedGraph.Draw()
        waveform_graph.SetLineColor(2)
        waveform_graph.Draw("SAME")
        canvas.Write("BaselineSubtractedWaveform")

# Plot histogram of Areas
integratedChargeHistogram.Draw()
canvas.Write("IntegratedChargeHist")
print(np.amax(tempAreaArray))
print(np.amin(tempAreaArray))

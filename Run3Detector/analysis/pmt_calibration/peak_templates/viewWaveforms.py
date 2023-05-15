#!/usr/bin/env python3

import ROOT as r
import numpy as np
NANOSECONDS_PER_SAMPLE  = 2.5
datafile = '/home/rsantos/Data/PostProcessData/MilliQan_Run852_default_peak_template.root'
outputFile = r.TFile.Open("waveforms.root", "RECREATE")
times = np.array([x*2.5 for x in range(1024)])

rootFile = r.TFile(datafile)
tree = rootFile.Get("Events")

tree.GetEvent(1)
nEvents = tree.GetEntries()
nEntries = len(tree.voltages)

canvas = r.TCanvas("c", "c")
timesArray = np.arange(0, NANOSECONDS_PER_SAMPLE * nEntries, 2.5)
voltageArray = np.empty([nEvents, nEntries])
for i, event in enumerate(tree):
    if i > 100:
        break
    canvas.Clear()
    voltageArray[i] = event.voltages
    if i % 100 == 0:
        print(i)

    graph = r.TGraph(nEntries, timesArray, voltageArray)
    graph.Draw("AC")
    outputFile.WriteObject(canvas, f'Waveform_{i}')
outputFile.Close()

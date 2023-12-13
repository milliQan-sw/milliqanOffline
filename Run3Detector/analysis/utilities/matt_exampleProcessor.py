import ROOT as r
import uproot
import hist
import matplotlib.pyplot as plt
import awkward as ak
import numpy as np
import array as arr
from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *
import os
import sys
from functools import partial
import argparse
from utils import getData_dir, makeFilelist

parser = argparse.ArgumentParser(description='Running milliqan processor')
parser.add_argument('-r', '--runs', type=str, nargs='+', help='This the list of runs you want to process, for example: 1031 1033 1065')
args = parser.parse_args()

runs = args.runs

filelist = makeFilelist(pruns = runs, pfilepath = getData_dir())

#define the necessary branches to run over
branches = ['boardsMatched', 'timeFit_module_calibrated', 'height', 'area', 'column', 'row', 'layer', 'type', 'pickupFlag']

#define the milliqan cuts object
mycuts = milliqanCuts()

#define the milliqan cuts object
mycuts = milliqanCuts()

#require pulses are not pickup
pickupCut = mycuts.getCut(mycuts.pickupCut, 'pickupCut', cut=True, branches=branches)

#require that all digitizer boards are matched
boardMatchCut = mycuts.getCut(mycuts.boardsMatched, 'boardMatchCut', cut=True, branches=branches)

#make custumized area cut
areaCut500k = mycuts.getCut(mycuts.areaCut, 'areaCut500k', cut=500000)

#example of creating a combined cut
eventCuts = mycuts.getCut(mycuts.combineCuts, 'eventCuts', ['fourLayerCut','barCut','areaCut500k'])


#define milliqan plotter
myplotter = milliqanPlotter()

#create root histogram
h_column = r.TH1F("h_column", "Column", 7, -2, 5)

#add root histogram to plotter
myplotter.addHistograms(h_column, 'column', 'eventCuts')

#defining the cutflow
cutflow = [boardMatchCut, pickupCut, mycuts.fourLayerCut, mycuts.barCut, areaCut500k, eventCuts, myplotter.dict['h_column']]

#create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

#print out the schedule
myschedule.printSchedule()

#create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter, max_events=10000)

#set custom functions inside iterator if desired
#myiterator.setCustomFunction(getMaxPulseTime)

#run the milliqan processor
myiterator.run()

fout = r.TFile('output.root','recreate')
h_column.Write()
fout.Close()
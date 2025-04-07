import sys
sys.path.append('/root/lib/')

import ROOT as r
import os
import json
import pandas as pd
import uproot
import awkward as ak
import array as arr
import numpy as np
import shutil
import tarfile

# Append utilities directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utilities'))
from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *


#################################################################
################ Global Setup and Helper Functions ##############
#################################################################

# Build a global lookup for pmt type from channel mapping.
# The configuration file is assumed to be local now.
try:
    with open('configRun19_present.json', 'r') as f:
        config_data = json.load(f)
    chanMap = config_data['chanMap']  # each entry: [col, row, layer, pmt]
    pmt_lookup = np.array([entry[3] for entry in chanMap])
except Exception as e:
    print("Could not build pmt lookup: ", e)
    pmt_lookup = None

if pmt_lookup is None:
    raise RuntimeError("pmt_lookup is not defined. Check that configRun19_present.json exists and is valid.")


def getFileList(filelist, job):
    with open(filelist, 'r') as fin:
        data = json.load(fin)
    mylist = data[job]
    return mylist

def extract_tar_file(tar_file='milliqanProcessing.tar.gz'):
    with tarfile.open(tar_file, "r:gz") as tar:
        tar.extractall()

##################################################################
def checkBeam(mqLumis, run, file, branch='beam'):
    beam = mqLumis[branch].loc[(mqLumis['run'] == run) & (mqLumis['file'] == file)]
    if beam.size == 0:
        return None
    beam = beam.values[0]
    return beam

def loadJson(jsonFile):
    with open(jsonFile, 'r') as fin:
        data = json.load(fin)
    lumis = pd.DataFrame(data['data'], columns=data['columns'])
    return lumis

def getRunFile(filename):
    run = filename.split('Run')[1].split('.')[0]
    file = filename.split('.')[1].split('_')[0]
    return [int(run), int(file)]

def getLumiofFileList(filelist):
    inputFiles = [getRunFile(x.split('/')[-1]) for x in filelist]
    lumis = pd.read_json('mqLumis.json', orient='split', compression='infer')
    lumis['start'] = pd.to_datetime(lumis['start'])
    lumis['stop'] = pd.to_datetime(lumis['stop'])
    myfiles = lumis[lumis.apply(lambda row: [int(row['run']), int(row['file'])] in inputFiles, axis=1)]
    totalLumi = myfiles['lumiEst'].sum()
    runTime = getRunTimes(myfiles)
    print("Running over {} files \n total of {} pb^-1 \n total run time {}s".format(len(filelist), totalLumi, runTime))

def getRunTimes(df):
    runTimes = df['stop'] - df['start']
    total_time = runTimes.sum()
    return total_time

##################################################################
# NEW: Updated findChannel for the slab detector layout.
# The new chanMap entries are of the form [col, row, layer, pmt].
# Do NOT change this function.
def findChannel(layer, row, col, p, config='configRun19_present.json'):
    with open(config, 'r') as fin:
        data = json.load(fin)
    chan_list = data['chanMap']  # list of lists: [col, row, layer, pmt]
    for idx, mapping in enumerate(chan_list):
        if mapping[0] == col and mapping[1] == row and mapping[2] == layer and mapping[3] == p:
            return idx
    return None

##################################################################
# NEW: Straight Line Cut redefinition for the slab layout.
# Requirement: at least one (row, col) combination must have hits in all 4 layers
# with the same PMT (either 0 or 1).
@mqCut
def straightLineCut(self, cutName='straightLineCut', cut=True, branches=None):
    # Initialize a boolean mask per event.
    valid = ak.zeros_like(self.events.event, dtype=bool)
    # Loop over all possible (row, col, pmt) combinations.
    # New detector: 4 rows, 3 columns, 2 PMTs.
    for row in range(4):
        for col in range(3):
            for p in [0, 1]:
                # Use ak.take to index pmt_lookup with a possibly jagged self.events.chan.
                mask = (self.events.row == row) & (self.events.column == col) & (ak.take(pmt_lookup, self.events.chan) == p)
                unique_layers = ak.num(ak.unique(self.events.layer[mask]))
                valid_candidate = (unique_layers == 4)
                valid = valid | valid_candidate
    self.events[cutName] = valid
    if cut:
        for branch in branches:
            self.events[branch] = self.events[branch][valid]

##################################################################
# NEW: The getTimeDiffs function now loops over 24 possible four‐in‐line paths.
@mqCut
def getTimeDiffs(self):
    # Loop over all possible 4 in line paths (4 rows x 3 cols x 2 PMTs = 24 lines)
    for i in range(24):
        cut0 = self.events['threeHitPath{}_p0'.format(i)]
        cut1 = self.events['threeHitPath{}_p1'.format(i)]
        cut2 = self.events['threeHitPath{}_p2'.format(i)]
        cut3 = self.events['threeHitPath{}_p3'.format(i)]

        cutName0_12 = 'timeDiff_path{}_line{}_layers{}_{}'.format(i, 0, 1, 2)
        cutName0_13 = 'timeDiff_path{}_line{}_layers{}_{}'.format(i, 0, 1, 3)
        cutName0_23 = 'timeDiff_path{}_line{}_layers{}_{}'.format(i, 0, 2, 3)

        cutName1_02 = 'timeDiff_path{}_line{}_layers{}_{}'.format(i, 1, 0, 2)
        cutName1_03 = 'timeDiff_path{}_line{}_layers{}_{}'.format(i, 1, 0, 3)
        cutName1_23 = 'timeDiff_path{}_line{}_layers{}_{}'.format(i, 1, 2, 3)

        cutName2_01 = 'timeDiff_path{}_line{}_layers{}_{}'.format(i, 2, 0, 1)
        cutName2_03 = 'timeDiff_path{}_line{}_layers{}_{}'.format(i, 2, 0, 3)
        cutName2_13 = 'timeDiff_path{}_line{}_layers{}_{}'.format(i, 2, 1, 3)

        cutName3_01 = 'timeDiff_path{}_line{}_layers{}_{}'.format(i, 3, 0, 1)
        cutName3_02 = 'timeDiff_path{}_line{}_layers{}_{}'.format(i, 3, 0, 2)
        cutName3_12 = 'timeDiff_path{}_line{}_layers{}_{}'.format(i, 3, 1, 2)

        times0_1 = self.events['timeFit_module_calibrated'][(cut0) & (self.events.layer == 1)]
        times0_2 = self.events['timeFit_module_calibrated'][(cut0) & (self.events.layer == 2)]
        times0_3 = self.events['timeFit_module_calibrated'][(cut0) & (self.events.layer == 3)]

        times1_0 = self.events['timeFit_module_calibrated'][(cut1) & (self.events.layer == 0)]
        times1_2 = self.events['timeFit_module_calibrated'][(cut1) & (self.events.layer == 2)]
        times1_3 = self.events['timeFit_module_calibrated'][(cut1) & (self.events.layer == 3)]

        times2_0 = self.events['timeFit_module_calibrated'][(cut2) & (self.events.layer == 0)]
        times2_1 = self.events['timeFit_module_calibrated'][(cut2) & (self.events.layer == 1)]
        times2_3 = self.events['timeFit_module_calibrated'][(cut2) & (self.events.layer == 3)]

        times3_0 = self.events['timeFit_module_calibrated'][(cut3) & (self.events.layer == 0)]
        times3_1 = self.events['timeFit_module_calibrated'][(cut3) & (self.events.layer == 1)]
        times3_2 = self.events['timeFit_module_calibrated'][(cut3) & (self.events.layer == 2)]

        self.events[cutName0_12] = ak.pad_none(times0_2, 1, axis=1) - ak.pad_none(times0_1, 1, axis=1)
        self.events[cutName0_13] = ak.pad_none(times0_3, 1, axis=1) - ak.pad_none(times0_1, 1, axis=1)
        self.events[cutName0_23] = ak.pad_none(times0_3, 1, axis=1) - ak.pad_none(times0_2, 1, axis=1)

        self.events[cutName1_02] = ak.pad_none(times1_2, 1, axis=1) - ak.pad_none(times1_0, 1, axis=1)
        self.events[cutName1_03] = ak.pad_none(times1_3, 1, axis=1) - ak.pad_none(times1_0, 1, axis=1)
        self.events[cutName1_23] = ak.pad_none(times1_3, 1, axis=1) - ak.pad_none(times1_2, 1, axis=1)

        self.events[cutName2_01] = ak.pad_none(times2_1, 1, axis=1) - ak.pad_none(times2_0, 1, axis=1)
        self.events[cutName2_03] = ak.pad_none(times2_3, 1, axis=1) - ak.pad_none(times2_0, 1, axis=1)
        self.events[cutName2_13] = ak.pad_none(times2_3, 1, axis=1) - ak.pad_none(times2_1, 1, axis=1)

        self.events[cutName3_01] = ak.pad_none(times3_1, 1, axis=1) - ak.pad_none(times3_0, 1, axis=1)
        self.events[cutName3_02] = ak.pad_none(times3_2, 1, axis=1) - ak.pad_none(times3_0, 1, axis=1)
        self.events[cutName3_12] = ak.pad_none(times3_2, 1, axis=1) - ak.pad_none(times3_1, 1, axis=1)

##################################################################
# NEW: Updated timeDiff function.
# In addition to the “all pulses” branch, the straight-line part now loops
# over 4 layers, 4 rows, 3 columns and, for each cell, separately for PMT type 0 and 1.
@mqCut
def timeDiff(self, cutName='timeDiff'):
    allPulses = True
    allStraightLine = True

    if allPulses:
        times0 = self.events.timeFit[(self.events['layer'] == -1) & (self.events['type'] == 1)]
        times3 = self.events.timeFit[self.events.layer == 3]

        timesNoCorr0 = self.events.timeFit[self.events.layer == 0]
        timesNoCorr3 = self.events.timeFit[self.events.layer == 3]

        combos = ak.cartesian([times0, times3], axis=1)
        combosNoCorr = ak.cartesian([timesNoCorr0, timesNoCorr3], axis=1)

        diff = combos['1'] - combos['0']
        diffNoCorr = combosNoCorr['1'] - combosNoCorr['0']

        self.events[cutName] = diff
        self.events[cutName + 'NoCorr'] = diffNoCorr

    if allStraightLine:
        frontPanelTimes = self.events.timeFit[(self.events['type'] == 1) & (self.events['layer'] == -1)]
        # Loop over 4 layers, 4 rows, 3 columns and for each PMT type.
        for layer in range(4):
            for row in range(4):
                for col in range(3):
                    for p in [0, 1]:
                        chanTimes = self.events.timeFit[
                            (self.events['threeHitPath_allPulses']) &
                            (self.events['layer'] == layer) &
                            (self.events['row'] == row) &
                            (self.events['column'] == col) &
                            (ak.take(pmt_lookup, self.events.chan) == p)
                        ]
                        t_combo = ak.cartesian([chanTimes, frontPanelTimes], axis=1)
                        t_diff = t_combo['0'] - t_combo['1']
                        channel = int(findChannel(layer, row, col, p))
                        branchName = cutName + str(channel)
                        self.events[branchName] = t_diff

##################################################################
# The pulseTime function is left mostly unchanged.
@mqCut
def pulseTime(self):
    events = self.events
    straightPath = self.events['straightLineCutPulse']
    timeToUse = 'timeFit_module_calibrated'

    self.events['straightPathL0Time'] = events[timeToUse][(events.layer == 0) & straightPath]
    self.events['straightPathL1Time'] = events[timeToUse][(events.layer == 1) & straightPath]
    self.events['straightPathL2Time'] = events[timeToUse][(events.layer == 2) & straightPath]
    self.events['straightPathL3Time'] = events[timeToUse][(events.layer == 3) & straightPath]

    height0 = ak.max(events['height'][(events.layer == 0) & straightPath], axis=1)
    height1 = ak.max(events['height'][(events.layer == 1) & straightPath], axis=1)
    height2 = ak.max(events['height'][(events.layer == 2) & straightPath], axis=1)
    height3 = ak.max(events['height'][(events.layer == 3) & straightPath], axis=1)

    mask0 = (events['height'][(events.layer == 0) & straightPath] == height0)
    mask1 = (events['height'][(events.layer == 1) & straightPath] == height1)
    mask2 = (events['height'][(events.layer == 2) & straightPath] == height2)
    mask3 = (events['height'][(events.layer == 3) & straightPath] == height3)

    self.events['straightPathL0Time'] = self.events['straightPathL0Time'][mask0]
    self.events['straightPathL1Time'] = self.events['straightPathL1Time'][mask1]
    self.events['straightPathL2Time'] = self.events['straightPathL2Time'][mask2]
    self.events['straightPathL3Time'] = self.events['straightPathL3Time'][mask3]

    self.events['timeDiffOld'] = self.events['straightPathL3Time'] - self.events['straightPathL0Time']

##################################################################
if __name__ == "__main__":
    goodRuns = loadJson('/share/scratch0/peng/CMSSW_12_4_11_patch3/src/milliqanOffline/Run3Detector/configuration/slabConfigs/goodRunsList.json')
    lumis = loadJson('/share/scratch0/peng/CMSSW_12_4_11_patch3/src/milliqanOffline/Run3Detector/configuration/slabConfigs/mqLumis.json')

    # Define a file list to run over.
    filelist = [
        '/share/scratch0/peng/CMSSW_12_4_11_patch3/src/milliqanOffline/Run3Detector/analysis/skim/MilliQan_Run900_v35_cosmic_beamOff_tight_slab.root',
        '/share/scratch0/peng/CMSSW_12_4_11_patch3/src/milliqanOffline/Run3Detector/analysis/skim/MilliQan_Run1000_v35_cosmic_beamOff_tight_slab.root'
    ]

    print("Running on files {}".format(filelist))

    # Optionally, check the luminosity.
    # getLumiofFileList(filelist)

    # Define the necessary branches.
    branches = ['event', 'tTrigger', 'boardsMatched', 'pickupFlag', 'pickupFlagTight', 'fileNumber', 'runNumber',
                'type', 'ipulse', 'nPE', 'chan', 'time_module_calibrated', 'timeFit_module_calibrated',
                'row', 'column', 'layer', 'height', 'area', 'npulses', 'timeFit']

    # Define the milliqan cuts object.
    mycuts = milliqanCuts()

    # Replace the old methods with the updated versions.
    setattr(milliqanCuts, "getTimeDiffs", getTimeDiffs)
    setattr(milliqanCuts, 'timeDiff', timeDiff)
    setattr(milliqanCuts, "pulseTime", pulseTime)
    setattr(milliqanCuts, "straightLineCut", straightLineCut)

    # Set up the cuts.
    pickupCut = getCutMod(mycuts.pickupCut, mycuts, 'pickupCut', tight=True, cut=True, branches=branches)
    boardMatchCut = getCutMod(mycuts.boardsMatched, mycuts, 'boardMatchCut', cut=True, branches=branches)
    hitInAllLayers = getCutMod(mycuts.oneHitPerLayerCut, mycuts, 'hitInAllLayers', cut=True, branches=branches, multipleHits=False)
    oneHitPerLayer = getCutMod(mycuts.oneHitPerLayerCut, mycuts, 'oneHitPerLayer', cut=True, branches=branches, multipleHits=False)
    fourLayerCut = getCutMod(mycuts.fourLayerCut, mycuts, 'fourLayerCut', cut=True, branches=branches)
    firstPulseCut = getCutMod(mycuts.firstPulseCut, mycuts, 'firstPulseCut', cut=True, branches=branches)
    centralTime = getCutMod(mycuts.centralTime, mycuts, 'centralTime', cut=True, branches=branches)

    ##################################################################
    # NEW: Histogram output for time differences.
    # For each (row, col, pmt) combination (24 total), create a histogram for the time difference
    # between layer n (n = 1,2,3) and layer 0: 3 x 24 = 72 histograms.
    nbins = 100
    minx = -50
    maxx = 50

    # Create containers for histograms for each non-baseline layer.
    canvasHistos = {1: [], 2: [], 3: []}
    cutNames = {1: [], 2: [], 3: []}

    # Loop over all positions in the slab detector: 4 rows, 3 columns, 2 PMTs.
    for row in range(4):
        for col in range(3):
            for p in [0, 1]:
                # Get the base channel index for layer 0 (for labeling).
                baseChannel = findChannel(0, row, col, p)
                for layer in [1, 2, 3]:
                    histName = "h_timeDiff_L{}_r{}_c{}_p{}".format(layer, row, col, p)
                    title = "Time Diff: L{} - L0 for row {}, col {}, pmt {}".format(layer, row, col, p)
                    h = r.TH1F(histName, title, nbins, minx, maxx)
                    canvasHistos[layer].append(h)
                    cutNames[layer].append("timeDiff_L{}_channel{}".format(layer, baseChannel))

    myplotter = milliqanPlotter()
    myplotter.dict.clear()

    # (Optional: Add global histograms.)
    h_channels = r.TH1F('h_channels', 'Channel', 96, 0, 96)
    h_timeDiff = r.TH1F('h_timeDiff', 'Time Difference L3-L0', 50, -50, 100)
    h_timeDiffNoCorr = r.TH1F('h_timeDiffNoCorr', 'Time Difference L3-L0', 50, -50, 100)
    h_timeDiffOld = r.TH1F('h_timeDiffOld', 'Time Difference L3-L0', 50, -50, 100)

    myplotter.addHistograms(h_channels, 'chan')
    myplotter.addHistograms(h_timeDiff, 'timeDiff')
    myplotter.addHistograms(h_timeDiffNoCorr, 'timeDiffNoCorr')
    myplotter.addHistograms(h_timeDiffOld, 'timeDiffOld')

    # Add the 72 new histograms, grouping by non-baseline layer.
    for layer in [1, 2, 3]:
        for h, n in zip(canvasHistos[layer], cutNames[layer]):
            myplotter.addHistograms(h, n)

    ##################################################################
    # Build the cutflow.
    cutflow = [mycuts.totalEventCounter, mycuts.fullEventCounter,
               boardMatchCut,
               pickupCut,
               firstPulseCut,
               centralTime,
               fourLayerCut,
               mycuts.straightLineCut,
               mycuts.pulseTime,
               mycuts.timeDiff,
               mycuts.getTimeDiffs
              ]
    
    for key, value in myplotter.dict.items():
        if value not in cutflow:
            cutflow.append(value)

    myschedule = milliQanScheduler(cutflow, mycuts, myplotter)
    myschedule.printSchedule()

    myiterator = milliqanProcessor(filelist, branches, myschedule, step_size=10000, qualityLevel='override')
    myiterator.run()

    myschedule.cutFlowPlots()
    myplotter.saveHistograms("timingCorrection{}_slabDetector.root".format('_beamOff'))
    mycuts.getCutflowCounts()

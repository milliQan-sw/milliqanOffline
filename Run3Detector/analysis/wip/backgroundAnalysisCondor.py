


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

sys.path.append(os.path.dirname(__file__) + '/utilities/')
print(sys.path)
from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *

print(sys.path)

#################################################################
################ condor function definitions ####################

def getFileList(filelist, job):

    with open(filelist, 'r') as fin:
        data = json.load(fin)

    mylist = data[job]

    return mylist

def extract_tar_file(tar_file='milliqanProcessing.tar.gz'):
    with tarfile.open(tar_file, "r:gz") as tar:
        tar.extractall()

##################################################################

def loadJson(jsonFile):
    fin = open(jsonFile)
    data = json.load(fin)
    lumis = pd.DataFrame(data['data'], columns=data['columns'])
    return lumis


def getRunFile(filename):
    run = filename.split('Run')[1].split('.')[0]
    file = filename.split('.')[1].split('_')[0]
    return [int(run), int(file)]


def getLumiofFileList(filelist):

    inputFiles = [getRunFile(x.split('/')[-1]) for x in filelist]

    #mqLumis = shutil.copy('/eos/experiment/milliqan/Configs/mqLumis.json', 'mqLumis.json')
    lumis = pd.read_json('mqLumis.json', orient = 'split', compression = 'infer')

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


@mqCut
def threeInLine(self):
    npeCut = 1

    for path in range(16):

        row = path//4
        col = path%4

        outputName = 'threeHitPath{}'.format(path)

        #print("Checking three in line for path {}, row {}, col {}, with area cut {}".format(path, row, col, areaCut))

        layer0 = (self.events.layer0) & (self.events.nPE >= npeCut) & (self.events.row == row) & (self.events.column == col)
        layer1 = (self.events.layer1) & (self.events.nPE >= npeCut) & (self.events.row == row) & (self.events.column == col)
        layer2 = (self.events.layer2) & (self.events.nPE >= npeCut) & (self.events.row == row) & (self.events.column == col)
        layer3 = (self.events.layer3) & (self.events.nPE >= npeCut) & (self.events.row == row) & (self.events.column == col)

        threeStraight_f0 = ak.any(layer1, axis=1) & ak.any(layer2, axis=1) & ak.any(layer3, axis=1)
        threeStraight_f1 = ak.any(layer0, axis=1) & ak.any(layer2, axis=1) & ak.any(layer3, axis=1)
        threeStraight_f2 = ak.any(layer0, axis=1) & ak.any(layer1, axis=1) & ak.any(layer3, axis=1)
        threeStraight_f3 = ak.any(layer0, axis=1) & ak.any(layer1, axis=1) & ak.any(layer2, axis=1)

        self.events[outputName+'_f0'] = threeStraight_f0
        self.events[outputName+'_f1'] = threeStraight_f1
        self.events[outputName+'_f2'] = threeStraight_f2
        self.events[outputName+'_f3'] = threeStraight_f3

        #get just the pulses that pass that made the selections
        _, b0 = ak.broadcast_arrays(self.events.nPE, threeStraight_f0)
        _, b1 = ak.broadcast_arrays(self.events.nPE, threeStraight_f1)
        _, b2 = ak.broadcast_arrays(self.events.nPE, threeStraight_f2)
        _, b3 = ak.broadcast_arrays(self.events.nPE, threeStraight_f3)

        self.events[outputName+'_p0'] = (b0) & ((layer1) | (layer2) | (layer3))
        self.events[outputName+'_p1'] = (b1) & ((layer0) | (layer2) | (layer3))
        self.events[outputName+'_p2'] = (b2) & ((layer0) | (layer1) | (layer3))
        self.events[outputName+'_p3'] = (b3) & ((layer0) | (layer1) | (layer2))

        self.events[outputName+'_s0'] = (threeStraight_f0) & (self.events.layer0) & (self.events.nPE >= npeCut)
        self.events[outputName+'_s1'] = (threeStraight_f1) & (self.events.layer1) & (self.events.nPE >= npeCut)
        self.events[outputName+'_s2'] = (threeStraight_f2) & (self.events.layer2) & (self.events.nPE >= npeCut)
        self.events[outputName+'_s3'] = (threeStraight_f3) & (self.events.layer3) & (self.events.nPE >= npeCut)
        

@mqCut
def firstPulseCut(self, cutName='firstPulse', cut=False, branches=None):

    self.events[cutName] = self.events.ipulse == 0

    if cut:
        for branch in branches:
            self.events[branch] = self.events[branch][self.events[cutName]]

@mqCut
def timeDiff(self, cutName='pulseDiff', cut=False, branches=None):

    for path in range(16):

        row = path//4
        col = path%4

        cutName0 = 'threeHitPath{}_s0'.format(path)
        cutName1 = 'threeHitPath{}_s1'.format(path)
        cutName2 = 'threeHitPath{}_s2'.format(path)
        cutName3 = 'threeHitPath{}_s3'.format(path)

        pulseCutName0 = 'threeHitPath{}_p0'.format(path)
        pulseCutName1 = 'threeHitPath{}_p1'.format(path)
        pulseCutName2 = 'threeHitPath{}_p2'.format(path)
        pulseCutName3 = 'threeHitPath{}_p3'.format(path)

        #anyPath = (self.events[cutName0]) | (self.events[cutName1]) | (self.events[cutName2]) | (self.events[cutName3])
        anyPath = ((self.events[pulseCutName0]) | (self.events[pulseCutName1]) | (self.events[pulseCutName2]) | (self.events[pulseCutName3]))

        anyPath0 = anyPath & (self.events.layer0)
        anyPath3 = anyPath & (self.events.layer3)

        times = self.events['timeFit_module_calibrated'][anyPath]
        times0 = self.events['timeFit_module_calibrated'][anyPath0]
        times3 = self.events['timeFit_module_calibrated'][anyPath3]

        combinations = ak.combinations(times, 2, axis=1)

        diffs = abs(combinations['0'] - combinations['1'])

        min_ = ak.min(diffs, axis=1, keepdims=True)
        max_ = ak.max(diffs, axis=1, keepdims=True)   

        diff03 = ak.pad_none(times3, 1, axis=1) - ak.pad_none(times0, 1, axis=1)

        if path == 0:
            allmin = min_
            allmax = max_ 
            allDiff = diffs
            allDiff03 = diff03
            notStraight = ~anyPath
        else:
            allmin = ak.concatenate([allmin, min_], axis=1)
            allmax = ak.concatenate([allmax, max_], axis=1)
            allDiff = ak.concatenate([allDiff, diffs], axis=1)
            allDiff03 = ak.concatenate([allDiff03, diff03], axis=1)
            notStraight = notStraight & ~anyPath

    #find the times of pulses that are not in straight lines
    c_times0 = notStraight & self.events.layer0
    c_times3 = notStraight & self.events.layer3

    times0 = self.events['timeFit_module_calibrated'][c_times0]
    times3 = self.events['timeFit_module_calibrated'][c_times3]

    diffNotStraight03 = ak.cartesian([times0, times3], axis=1)
    diffNotStraight03 = diffNotStraight03['1'] - diffNotStraight03['0']

    self.events['allTimeDiff'] = allDiff
    self.events['maxTimeDiff'] = allmax
    self.events['minTimeDiff'] = allmin
    self.events['timeDiff03'] = allDiff03
    self.events['timeDiffNotStraight03'] = diffNotStraight03

if __name__ == "__main__":

    '''goodRunsName = '/eos/experiment/milliqan/Configs/goodRunsList.json'
    lumisName = '/eos/experiment/milliqan/Configs/mqLumis.json'
    shutil.copy(goodRunsName, 'goodRunsList.json')
    shutil.copy(lumisName, 'mqLumis.json')'''

    goodRuns = loadJson('goodRunsList.json')
    lumis = loadJson('mqLumis.json')

    #get list of files to look at
    files = []

    beam = False

#get the filelist and job number
filelist = '/'.join([sys.argv[3], sys.argv[1]])
job = sys.argv[2]

#define a file list to run over
filelist = getFileList(filelist, job)
#filelist = filelist[:10] #temporary
print("Running on files {}".format(filelist))

#find the luminosity of files in filelist
getLumiofFileList(filelist)

#define the necessary branches to run over
branches = ['event', 'tTrigger', 'boardsMatched', 'pickupFlag', 'fileNumber', 'runNumber', 'type', 'ipulse', 'nPE', 'chan',
            'time_module_calibrated', 'timeFit_module_calibrated', 'row', 'column', 'layer', 'height', 'area', 'npulses']

#define the milliqan cuts object
mycuts = milliqanCuts()

#require pulses are not pickup
pickupCut = mycuts.getCut(mycuts.pickupCut, 'pickupCut', cut=True, branches=branches)

#require that all digitizer boards are matched
boardMatchCut = mycuts.getCut(mycuts.boardsMatched, 'boardMatchCut', cut=True, branches=branches)

#require pulses to be near trigger window
pulseTime = mycuts.getCut(mycuts.centralTime, 'centralTimeCut', cut=True, branches=branches)

#height cut to get large pulses
muonHeightCut = mycuts.getCut(mycuts.heightCut, 'muonHeightCut', heightCut=1200, cut=True, branches=branches)

#muon area cut
muonAreaCut = getCutMod(mycuts.areaCut, mycuts, 'muonAreaCut', areaCut=0, cut=True, branches=branches)

#nPE cut
nPECut = getCutMod(mycuts.nPECut, mycuts, 'nPECut', nPECut=2, cut=True, branches=branches)

#bar only cut
barCut = getCutMod(mycuts.barCut, mycuts, 'barCut', cut=True, branches=branches)

#get rid of any zero bias triggers
triggerCutNot = mycuts.getCut(mycuts.triggerCutNot, 'notzbTrigger', trigger=4096, cut=True, branches=branches)

#select only zero bias triggers (for sfs)
triggerCut = mycuts.getCut(mycuts.triggerCut, 'zbTrigger', trigger=4096, cut=True, branches=branches)

#define milliqan plotter
myplotter = milliqanPlotter()
myplotter.dict.clear()

#create root histogram 
bins = 400
xmin = 1100
xmax = 1500

'''h_pulseTime03 = r.TH2F("h_pulseTime03", "Pulse Times Between Layer 0 and 3", bins, xmin, xmax, bins, xmin, xmax)
h_L0Times = r.TH1F('h_L0Times', "Pulse Times Layer 0", 400, 1100, 1500)
h_L3Times = r.TH1F('h_L3Times', "Pulse Times Layer 3", 400, 1100, 1500)'''
h_TimeDiffStraight = r.TH1F('h_TimeDiffStraight', "Difference in Layer 0 and 3 Times Pointing Paths", 100, -50, 50)
h_TimeDiff = r.TH1F('h_TimeDiff', "Difference in Layer 0 and 3 Times Non-Pointing Paths", 100, -50, 50)

h_height = r.TH1F('h_height', "Height of Passing Pulses", 650, 0, 1300)
h_area = r.TH1F('h_area', "Area of Passing Pulses", 1000, 0, 100e4)
h_layer = r.TH1F('h_layer', 'Layer of Passing Pulses', 4, 0, 4)
h_fourLayer = r.TH1F('h_fourLayer', 'Layer of Passing Pulses in Events with 4 Layers', 4, 0, 4)
h_trigger = r.TH1F('h_trigger', 'Triggers Passing Cuts', 5000, 0, 5000)
h_channel = r.TH1F('h_channel', 'Channel of Hits', 80, 0, 80)

h_minTimeDiff = r.TH1F('h_minTimeDiff', 'Min Time Difference Between Straight Path Hits', 100, 0, 100)
h_maxTimeDiff = r.TH1F('h_maxTimeDiff', 'Max Time Difference Between Straight Path Hits', 100, 0, 100)
h_allTimeDiff = r.TH1F('h_allTimeDiff', 'All Time Differences Between Straight Path Hits', 100, 0, 100)

h_triggers = r.TH1F('h_triggers', 'Triggers of Passing Events', 16, 0, 16)
h_row = r.TH1F('h_row', 'Row of Passing Pulses', 4, 0, 4)
h_column = r.TH1F('h_column', 'Column of Passing Pulses', 4, 0, 4)
h_posL0 = r.TH2F('h_posL0', 'Row/Col of Passing Pulses in Layer 0', 4, 0, 4, 4, 0, 4)
h_posL1 = r.TH2F('h_posL1', 'Row/Col of Passing Pulses in Layer 1', 4, 0, 4, 4, 0, 4)
h_posL2 = r.TH2F('h_posL2', 'Row/Col of Passing Pulses in Layer 2', 4, 0, 4, 4, 0, 4)
h_posL3 = r.TH2F('h_posL3', 'Row/Col of Passing Pulses in Layer 3', 4, 0, 4, 4, 0, 4)

h_threeInLinePath0_f0 = r.TH2F('h_threeInLinePath0_f0', 'Row/Col of Layer 0 Pulse After 3 In Line Path 0', 4, 0, 4, 4, 0, 4)
h_threeInLinePath1_f0 = r.TH2F('h_threeInLinePath1_f0', 'Row/Col of Layer 0 Pulse After 3 In Line Path 1', 4, 0, 4, 4, 0, 4)
h_threeInLinePath2_f0 = r.TH2F('h_threeInLinePath2_f0', 'Row/Col of Layer 0 Pulse After 3 In Line Path 2', 4, 0, 4, 4, 0, 4)
h_threeInLinePath3_f0 = r.TH2F('h_threeInLinePath3_f0', 'Row/Col of Layer 0 Pulse After 3 In Line Path 3', 4, 0, 4, 4, 0, 4)
h_threeInLinePath4_f0 = r.TH2F('h_threeInLinePath4_f0', 'Row/Col of Layer 0 Pulse After 3 In Line Path 4', 4, 0, 4, 4, 0, 4)
h_threeInLinePath5_f0 = r.TH2F('h_threeInLinePath5_f0', 'Row/Col of Layer 0 Pulse After 3 In Line Path 5', 4, 0, 4, 4, 0, 4)
h_threeInLinePath6_f0 = r.TH2F('h_threeInLinePath6_f0', 'Row/Col of Layer 0 Pulse After 3 In Line Path 6', 4, 0, 4, 4, 0, 4)
h_threeInLinePath7_f0 = r.TH2F('h_threeInLinePath7_f0', 'Row/Col of Layer 0 Pulse After 3 In Line Path 7', 4, 0, 4, 4, 0, 4)
h_threeInLinePath8_f0 = r.TH2F('h_threeInLinePath8_f0', 'Row/Col of Layer 0 Pulse After 3 In Line Path 8', 4, 0, 4, 4, 0, 4)
h_threeInLinePath9_f0 = r.TH2F('h_threeInLinePath9_f0', 'Row/Col of Layer 0 Pulse After 3 In Line Path 9', 4, 0, 4, 4, 0, 4)
h_threeInLinePath10_f0 = r.TH2F('h_threeInLinePath10_f0', 'Row/Col of Layer 0 Pulse After 3 In Line Path 10', 4, 0, 4, 4, 0, 4)
h_threeInLinePath11_f0 = r.TH2F('h_threeInLinePath11_f0', 'Row/Col of Layer 0 Pulse After 3 In Line Path 11', 4, 0, 4, 4, 0, 4)
h_threeInLinePath12_f0 = r.TH2F('h_threeInLinePath12_f0', 'Row/Col of Layer 0 Pulse After 3 In Line Path 12', 4, 0, 4, 4, 0, 4)
h_threeInLinePath13_f0 = r.TH2F('h_threeInLinePath13_f0', 'Row/Col of Layer 0 Pulse After 3 In Line Path 13', 4, 0, 4, 4, 0, 4)
h_threeInLinePath14_f0 = r.TH2F('h_threeInLinePath14_f0', 'Row/Col of Layer 0 Pulse After 3 In Line Path 14', 4, 0, 4, 4, 0, 4)
h_threeInLinePath15_f0 = r.TH2F('h_threeInLinePath15_f0', 'Row/Col of Layer 0 Pulse After 3 In Line Path 15', 4, 0, 4, 4, 0, 4)

h_threeInLinePath0_f1 = r.TH2F('h_threeInLinePath0_f1', 'Row/Col of Layer 1 Pulse After 3 In Line Path 0', 4, 0, 4, 4, 0, 4)
h_threeInLinePath1_f1 = r.TH2F('h_threeInLinePath1_f1', 'Row/Col of Layer 1 Pulse After 3 In Line Path 1', 4, 0, 4, 4, 0, 4)
h_threeInLinePath2_f1 = r.TH2F('h_threeInLinePath2_f1', 'Row/Col of Layer 1 Pulse After 3 In Line Path 2', 4, 0, 4, 4, 0, 4)
h_threeInLinePath3_f1 = r.TH2F('h_threeInLinePath3_f1', 'Row/Col of Layer 1 Pulse After 3 In Line Path 3', 4, 0, 4, 4, 0, 4)
h_threeInLinePath4_f1 = r.TH2F('h_threeInLinePath4_f1', 'Row/Col of Layer 1 Pulse After 3 In Line Path 4', 4, 0, 4, 4, 0, 4)
h_threeInLinePath5_f1 = r.TH2F('h_threeInLinePath5_f1', 'Row/Col of Layer 1 Pulse After 3 In Line Path 5', 4, 0, 4, 4, 0, 4)
h_threeInLinePath6_f1 = r.TH2F('h_threeInLinePath6_f1', 'Row/Col of Layer 1 Pulse After 3 In Line Path 6', 4, 0, 4, 4, 0, 4)
h_threeInLinePath7_f1 = r.TH2F('h_threeInLinePath7_f1', 'Row/Col of Layer 1 Pulse After 3 In Line Path 7', 4, 0, 4, 4, 0, 4)
h_threeInLinePath8_f1 = r.TH2F('h_threeInLinePath8_f1', 'Row/Col of Layer 1 Pulse After 3 In Line Path 8', 4, 0, 4, 4, 0, 4)
h_threeInLinePath9_f1 = r.TH2F('h_threeInLinePath9_f1', 'Row/Col of Layer 1 Pulse After 3 In Line Path 9', 4, 0, 4, 4, 0, 4)
h_threeInLinePath10_f1 = r.TH2F('h_threeInLinePath10_f1', 'Row/Col of Layer 1 Pulse After 3 In Line Path 10', 4, 0, 4, 4, 0, 4)
h_threeInLinePath11_f1 = r.TH2F('h_threeInLinePath11_f1', 'Row/Col of Layer 1 Pulse After 3 In Line Path 11', 4, 0, 4, 4, 0, 4)
h_threeInLinePath12_f1 = r.TH2F('h_threeInLinePath12_f1', 'Row/Col of Layer 1 Pulse After 3 In Line Path 12', 4, 0, 4, 4, 0, 4)
h_threeInLinePath13_f1 = r.TH2F('h_threeInLinePath13_f1', 'Row/Col of Layer 1 Pulse After 3 In Line Path 13', 4, 0, 4, 4, 0, 4)
h_threeInLinePath14_f1 = r.TH2F('h_threeInLinePath14_f1', 'Row/Col of Layer 1 Pulse After 3 In Line Path 14', 4, 0, 4, 4, 0, 4)
h_threeInLinePath15_f1 = r.TH2F('h_threeInLinePath15_f1', 'Row/Col of Layer 1 Pulse After 3 In Line Path 15', 4, 0, 4, 4, 0, 4)

h_threeInLinePath0_f2 = r.TH2F('h_threeInLinePath0_f2', 'Row/Col of Layer 2 Pulse After 3 In Line Path 1', 4, 0, 4, 4, 0, 4)
h_threeInLinePath1_f2 = r.TH2F('h_threeInLinePath1_f2', 'Row/Col of Layer 2 Pulse After 3 In Line Path 2', 4, 0, 4, 4, 0, 4)
h_threeInLinePath2_f2 = r.TH2F('h_threeInLinePath2_f2', 'Row/Col of Layer 2 Pulse After 3 In Line Path 3', 4, 0, 4, 4, 0, 4)
h_threeInLinePath3_f2 = r.TH2F('h_threeInLinePath3_f2', 'Row/Col of Layer 2 Pulse After 3 In Line Path 4', 4, 0, 4, 4, 0, 4)
h_threeInLinePath4_f2 = r.TH2F('h_threeInLinePath4_f2', 'Row/Col of Layer 2 Pulse After 3 In Line Path 5', 4, 0, 4, 4, 0, 4)
h_threeInLinePath5_f2 = r.TH2F('h_threeInLinePath5_f2', 'Row/Col of Layer 2 Pulse After 3 In Line Path 6', 4, 0, 4, 4, 0, 4)
h_threeInLinePath6_f2 = r.TH2F('h_threeInLinePath6_f2', 'Row/Col of Layer 2 Pulse After 3 In Line Path 7', 4, 0, 4, 4, 0, 4)
h_threeInLinePath7_f2 = r.TH2F('h_threeInLinePath7_f2', 'Row/Col of Layer 2 Pulse After 3 In Line Path 8', 4, 0, 4, 4, 0, 4)
h_threeInLinePath8_f2 = r.TH2F('h_threeInLinePath8_f2', 'Row/Col of Layer 2 Pulse After 3 In Line Path 9', 4, 0, 4, 4, 0, 4)
h_threeInLinePath9_f2 = r.TH2F('h_threeInLinePath9_f2', 'Row/Col of Layer 2 Pulse After 3 In Line Path 10', 4, 0, 4, 4, 0, 4)
h_threeInLinePath10_f2 = r.TH2F('h_threeInLinePath10_f2', 'Row/Col of Layer 2 Pulse After 3 In Line Path 11', 4, 0, 4, 4, 0, 4)
h_threeInLinePath11_f2 = r.TH2F('h_threeInLinePath11_f2', 'Row/Col of Layer 2 Pulse After 3 In Line Path 12', 4, 0, 4, 4, 0, 4)
h_threeInLinePath12_f2 = r.TH2F('h_threeInLinePath12_f2', 'Row/Col of Layer 2 Pulse After 3 In Line Path 13', 4, 0, 4, 4, 0, 4)
h_threeInLinePath13_f2 = r.TH2F('h_threeInLinePath13_f2', 'Row/Col of Layer 2 Pulse After 3 In Line Path 14', 4, 0, 4, 4, 0, 4)
h_threeInLinePath14_f2 = r.TH2F('h_threeInLinePath14_f2', 'Row/Col of Layer 2 Pulse After 3 In Line Path 15', 4, 0, 4, 4, 0, 4)
h_threeInLinePath15_f2 = r.TH2F('h_threeInLinePath15_f2', 'Row/Col of Layer 2 Pulse After 3 In Line Path 16', 4, 0, 4, 4, 0, 4)

h_threeInLinePath0_f3 = r.TH2F('h_threeInLinePath0_f3', 'Row/Col of Layer 3 Pulse After 3 In Line Path 0', 4, 0, 4, 4, 0, 4)
h_threeInLinePath1_f3 = r.TH2F('h_threeInLinePath1_f3', 'Row/Col of Layer 3 Pulse After 3 In Line Path 1', 4, 0, 4, 4, 0, 4)
h_threeInLinePath2_f3 = r.TH2F('h_threeInLinePath2_f3', 'Row/Col of Layer 3 Pulse After 3 In Line Path 2', 4, 0, 4, 4, 0, 4)
h_threeInLinePath3_f3 = r.TH2F('h_threeInLinePath3_f3', 'Row/Col of Layer 3 Pulse After 3 In Line Path 3', 4, 0, 4, 4, 0, 4)
h_threeInLinePath4_f3 = r.TH2F('h_threeInLinePath4_f3', 'Row/Col of Layer 3 Pulse After 3 In Line Path 4', 4, 0, 4, 4, 0, 4)
h_threeInLinePath5_f3 = r.TH2F('h_threeInLinePath5_f3', 'Row/Col of Layer 3 Pulse After 3 In Line Path 5', 4, 0, 4, 4, 0, 4)
h_threeInLinePath6_f3 = r.TH2F('h_threeInLinePath6_f3', 'Row/Col of Layer 3 Pulse After 3 In Line Path 6', 4, 0, 4, 4, 0, 4)
h_threeInLinePath7_f3 = r.TH2F('h_threeInLinePath7_f3', 'Row/Col of Layer 3 Pulse After 3 In Line Path 7', 4, 0, 4, 4, 0, 4)
h_threeInLinePath8_f3 = r.TH2F('h_threeInLinePath8_f3', 'Row/Col of Layer 3 Pulse After 3 In Line Path 8', 4, 0, 4, 4, 0, 4)
h_threeInLinePath9_f3 = r.TH2F('h_threeInLinePath9_f3', 'Row/Col of Layer 3 Pulse After 3 In Line Path 9', 4, 0, 4, 4, 0, 4)
h_threeInLinePath10_f3 = r.TH2F('h_threeInLinePath10_f3', 'Row/Col of Layer 3 Pulse After 3 In Line Path 10', 4, 0, 4, 4, 0, 4)
h_threeInLinePath11_f3 = r.TH2F('h_threeInLinePath11_f3', 'Row/Col of Layer 3 Pulse After 3 In Line Path 11', 4, 0, 4, 4, 0, 4)
h_threeInLinePath12_f3 = r.TH2F('h_threeInLinePath12_f3', 'Row/Col of Layer 3 Pulse After 3 In Line Path 12', 4, 0, 4, 4, 0, 4)
h_threeInLinePath13_f3 = r.TH2F('h_threeInLinePath13_f3', 'Row/Col of Layer 3 Pulse After 3 In Line Path 13', 4, 0, 4, 4, 0, 4)
h_threeInLinePath14_f3 = r.TH2F('h_threeInLinePath14_f3', 'Row/Col of Layer 3 Pulse After 3 In Line Path 14', 4, 0, 4, 4, 0, 4)
h_threeInLinePath15_f3 = r.TH2F('h_threeInLinePath15_f3', 'Row/Col of Layer 3 Pulse After 3 In Line Path 15', 4, 0, 4, 4, 0, 4)


h_threeInLineCountPath0_f0 = r.TH1F('h_threeInLineCountPath0_f0', 'Events Passing Three In Line Path 0 Free Layer 0', 2, 0, 2)
h_threeInLineCountPath1_f0 = r.TH1F('h_threeInLineCountPath1_f0', 'Events Passing Three In Line Path 1 Free Layer 0', 2, 0, 2)
h_threeInLineCountPath2_f0 = r.TH1F('h_threeInLineCountPath2_f0', 'Events Passing Three In Line Path 2 Free Layer 0', 2, 0, 2)
h_threeInLineCountPath3_f0 = r.TH1F('h_threeInLineCountPath3_f0', 'Events Passing Three In Line Path 3 Free Layer 0', 2, 0, 2)
h_threeInLineCountPath4_f0 = r.TH1F('h_threeInLineCountPath4_f0', 'Events Passing Three In Line Path 4 Free Layer 0', 2, 0, 2)
h_threeInLineCountPath5_f0 = r.TH1F('h_threeInLineCountPath5_f0', 'Events Passing Three In Line Path 5 Free Layer 0', 2, 0, 2)
h_threeInLineCountPath6_f0 = r.TH1F('h_threeInLineCountPath6_f0', 'Events Passing Three In Line Path 6 Free Layer 0', 2, 0, 2)
h_threeInLineCountPath7_f0 = r.TH1F('h_threeInLineCountPath7_f0', 'Events Passing Three In Line Path 7 Free Layer 0', 2, 0, 2)
h_threeInLineCountPath8_f0 = r.TH1F('h_threeInLineCountPath8_f0', 'Events Passing Three In Line Path 8 Free Layer 0', 2, 0, 2)
h_threeInLineCountPath9_f0 = r.TH1F('h_threeInLineCountPath9_f0', 'Events Passing Three In Line Path 9 Free Layer 0', 2, 0, 2)
h_threeInLineCountPath10_f0 = r.TH1F('h_threeInLineCountPath10_f0', 'Events Passing Three In Line Path 10 Free Layer 0', 2, 0, 2)
h_threeInLineCountPath11_f0 = r.TH1F('h_threeInLineCountPath11_f0', 'Events Passing Three In Line Path 11 Free Layer 0', 2, 0, 2)
h_threeInLineCountPath12_f0 = r.TH1F('h_threeInLineCountPath12_f0', 'Events Passing Three In Line Path 12 Free Layer 0', 2, 0, 2)
h_threeInLineCountPath13_f0 = r.TH1F('h_threeInLineCountPath13_f0', 'Events Passing Three In Line Path 13 Free Layer 0', 2, 0, 2)
h_threeInLineCountPath14_f0 = r.TH1F('h_threeInLineCountPath14_f0', 'Events Passing Three In Line Path 14 Free Layer 0', 2, 0, 2)
h_threeInLineCountPath15_f0 = r.TH1F('h_threeInLineCountPath15_f0', 'Events Passing Three In Line Path 15 Free Layer 0', 2, 0, 2)

h_threeInLineCountPath0_f1 = r.TH1F('h_threeInLineCountPath0_f1', 'Events Passing Three In Line Path 0 Free Layer 1', 2, 0, 2)
h_threeInLineCountPath1_f1 = r.TH1F('h_threeInLineCountPath1_f1', 'Events Passing Three In Line Path 1 Free Layer 1', 2, 0, 2)
h_threeInLineCountPath2_f1 = r.TH1F('h_threeInLineCountPath2_f1', 'Events Passing Three In Line Path 2 Free Layer 1', 2, 0, 2)
h_threeInLineCountPath3_f1 = r.TH1F('h_threeInLineCountPath3_f1', 'Events Passing Three In Line Path 3 Free Layer 1', 2, 0, 2)
h_threeInLineCountPath4_f1 = r.TH1F('h_threeInLineCountPath4_f1', 'Events Passing Three In Line Path 4 Free Layer 1', 2, 0, 2)
h_threeInLineCountPath5_f1 = r.TH1F('h_threeInLineCountPath5_f1', 'Events Passing Three In Line Path 5 Free Layer 1', 2, 0, 2)
h_threeInLineCountPath6_f1 = r.TH1F('h_threeInLineCountPath6_f1', 'Events Passing Three In Line Path 6 Free Layer 1', 2, 0, 2)
h_threeInLineCountPath7_f1 = r.TH1F('h_threeInLineCountPath7_f1', 'Events Passing Three In Line Path 7 Free Layer 1', 2, 0, 2)
h_threeInLineCountPath8_f1 = r.TH1F('h_threeInLineCountPath8_f1', 'Events Passing Three In Line Path 8 Free Layer 1', 2, 0, 2)
h_threeInLineCountPath9_f1 = r.TH1F('h_threeInLineCountPath9_f1', 'Events Passing Three In Line Path 9 Free Layer 1', 2, 0, 2)
h_threeInLineCountPath10_f1 = r.TH1F('h_threeInLineCountPath10_f1', 'Events Passing Three In Line Path 10 Free Layer 1', 2, 0, 2)
h_threeInLineCountPath11_f1 = r.TH1F('h_threeInLineCountPath11_f1', 'Events Passing Three In Line Path 11 Free Layer 1', 2, 0, 2)
h_threeInLineCountPath12_f1 = r.TH1F('h_threeInLineCountPath12_f1', 'Events Passing Three In Line Path 12 Free Layer 1', 2, 0, 2)
h_threeInLineCountPath13_f1 = r.TH1F('h_threeInLineCountPath13_f1', 'Events Passing Three In Line Path 13 Free Layer 1', 2, 0, 2)
h_threeInLineCountPath14_f1 = r.TH1F('h_threeInLineCountPath14_f1', 'Events Passing Three In Line Path 14 Free Layer 1', 2, 0, 2)
h_threeInLineCountPath15_f1 = r.TH1F('h_threeInLineCountPath15_f1', 'Events Passing Three In Line Path 15 Free Layer 1', 2, 0, 2)

h_threeInLineCountPath0_f2 = r.TH1F('h_threeInLineCountPath0_f2', 'Events Passing Three In Line Path 0 Free Layer 2', 2, 0, 2)
h_threeInLineCountPath1_f2 = r.TH1F('h_threeInLineCountPath1_f2', 'Events Passing Three In Line Path 1 Free Layer 2', 2, 0, 2)
h_threeInLineCountPath2_f2 = r.TH1F('h_threeInLineCountPath2_f2', 'Events Passing Three In Line Path 2 Free Layer 2', 2, 0, 2)
h_threeInLineCountPath3_f2 = r.TH1F('h_threeInLineCountPath3_f2', 'Events Passing Three In Line Path 3 Free Layer 2', 2, 0, 2)
h_threeInLineCountPath4_f2 = r.TH1F('h_threeInLineCountPath4_f2', 'Events Passing Three In Line Path 4 Free Layer 2', 2, 0, 2)
h_threeInLineCountPath5_f2 = r.TH1F('h_threeInLineCountPath5_f2', 'Events Passing Three In Line Path 5 Free Layer 2', 2, 0, 2)
h_threeInLineCountPath6_f2 = r.TH1F('h_threeInLineCountPath6_f2', 'Events Passing Three In Line Path 6 Free Layer 2', 2, 0, 2)
h_threeInLineCountPath7_f2 = r.TH1F('h_threeInLineCountPath7_f2', 'Events Passing Three In Line Path 7 Free Layer 2', 2, 0, 2)
h_threeInLineCountPath8_f2 = r.TH1F('h_threeInLineCountPath8_f2', 'Events Passing Three In Line Path 8 Free Layer 2', 2, 0, 2)
h_threeInLineCountPath9_f2 = r.TH1F('h_threeInLineCountPath9_f2', 'Events Passing Three In Line Path 9 Free Layer 2', 2, 0, 2)
h_threeInLineCountPath10_f2 = r.TH1F('h_threeInLineCountPath10_f2', 'Events Passing Three In Line Path 10 Free Layer 2', 2, 0, 2)
h_threeInLineCountPath11_f2 = r.TH1F('h_threeInLineCountPath11_f2', 'Events Passing Three In Line Path 11 Free Layer 2', 2, 0, 2)
h_threeInLineCountPath12_f2 = r.TH1F('h_threeInLineCountPath12_f2', 'Events Passing Three In Line Path 12 Free Layer 2', 2, 0, 2)
h_threeInLineCountPath13_f2 = r.TH1F('h_threeInLineCountPath13_f2', 'Events Passing Three In Line Path 13 Free Layer 2', 2, 0, 2)
h_threeInLineCountPath14_f2 = r.TH1F('h_threeInLineCountPath14_f2', 'Events Passing Three In Line Path 14 Free Layer 2', 2, 0, 2)
h_threeInLineCountPath15_f2 = r.TH1F('h_threeInLineCountPath15_f2', 'Events Passing Three In Line Path 15 Free Layer 2', 2, 0, 2)

h_threeInLineCountPath0_f3 = r.TH1F('h_threeInLineCountPath0_f3', 'Events Passing Three In Line Path 0 Free Layer 3', 2, 0, 2)
h_threeInLineCountPath1_f3 = r.TH1F('h_threeInLineCountPath1_f3', 'Events Passing Three In Line Path 1 Free Layer 3', 2, 0, 2)
h_threeInLineCountPath2_f3 = r.TH1F('h_threeInLineCountPath2_f3', 'Events Passing Three In Line Path 2 Free Layer 3', 2, 0, 2)
h_threeInLineCountPath3_f3 = r.TH1F('h_threeInLineCountPath3_f3', 'Events Passing Three In Line Path 3 Free Layer 3', 2, 0, 2)
h_threeInLineCountPath4_f3 = r.TH1F('h_threeInLineCountPath4_f3', 'Events Passing Three In Line Path 4 Free Layer 3', 2, 0, 2)
h_threeInLineCountPath5_f3 = r.TH1F('h_threeInLineCountPath5_f3', 'Events Passing Three In Line Path 5 Free Layer 3', 2, 0, 2)
h_threeInLineCountPath6_f3 = r.TH1F('h_threeInLineCountPath6_f3', 'Events Passing Three In Line Path 6 Free Layer 3', 2, 0, 2)
h_threeInLineCountPath7_f3 = r.TH1F('h_threeInLineCountPath7_f3', 'Events Passing Three In Line Path 7 Free Layer 3', 2, 0, 2)
h_threeInLineCountPath8_f3 = r.TH1F('h_threeInLineCountPath8_f3', 'Events Passing Three In Line Path 8 Free Layer 3', 2, 0, 2)
h_threeInLineCountPath9_f3 = r.TH1F('h_threeInLineCountPath9_f3', 'Events Passing Three In Line Path 9 Free Layer 3', 2, 0, 2)
h_threeInLineCountPath10_f3 = r.TH1F('h_threeInLineCountPath10_f3', 'Events Passing Three In Line Path 10 Free Layer 3', 2, 0, 2)
h_threeInLineCountPath11_f3 = r.TH1F('h_threeInLineCountPath11_f3', 'Events Passing Three In Line Path 11 Free Layer 3', 2, 0, 2)
h_threeInLineCountPath12_f3 = r.TH1F('h_threeInLineCountPath12_f3', 'Events Passing Three In Line Path 12 Free Layer 3', 2, 0, 2)
h_threeInLineCountPath13_f3 = r.TH1F('h_threeInLineCountPath13_f3', 'Events Passing Three In Line Path 13 Free Layer 3', 2, 0, 2)
h_threeInLineCountPath14_f3 = r.TH1F('h_threeInLineCountPath14_f3', 'Events Passing Three In Line Path 14 Free Layer 3', 2, 0, 2)
h_threeInLineCountPath15_f3 = r.TH1F('h_threeInLineCountPath15_f3', 'Events Passing Three In Line Path 15 Free Layer 3', 2, 0, 2)

'''setattr(milliqanCuts, "centralTime", centralTime)
setattr(milliqanCuts, "pulseTime", pulseTime)'''
#setattr(milliqanCuts, "triggerCut", triggerCut)
setattr(milliqanCuts, "threeInLine", threeInLine)
setattr(milliqanCuts, "firstPulseCut", firstPulseCut)
setattr(milliqanCuts, "timeDiff", timeDiff)

triggerCut1 = getCutMod(mycuts.triggerCut, mycuts, 'triggerCut1', cutName='triggerCut1', trigger=1, cut=False, branches=branches)
triggerCut2 = getCutMod(mycuts.triggerCut, mycuts, 'triggerCut2', cutName='triggerCut2', trigger=2, cut=True, branches=branches)


#first pulse only cut
firstPulse = getCutMod(mycuts.firstPulseCut, mycuts, 'firstPulseCut', cutName='firstPulseCut', cut=True, branches=branches)

#add root histogram to plotter
'''myplotter.addHistograms(h_pulseTime03, ['straightPathL0Time', 'straightPathL3Time'])
myplotter.addHistograms(h_L0Times, 'straightPathL0Time')
myplotter.addHistograms(h_L3Times, 'straightPathL3Time')'''
myplotter.addHistograms(h_TimeDiffStraight, 'timeDiff03')
myplotter.addHistograms(h_TimeDiff, 'timeDiffNotStraight03')
myplotter.addHistograms(h_height, 'height')
myplotter.addHistograms(h_area, 'area')
myplotter.addHistograms(h_layer, 'layer')
myplotter.addHistograms(h_trigger, 'tTrigger')
myplotter.addHistograms(h_channel, 'chan')

#myplotter.addHistograms(h_triggers, 'triggerCut2')
myplotter.addHistograms(h_row, 'row')
myplotter.addHistograms(h_column, 'column')
myplotter.addHistograms(h_posL0, ['column', 'row'], 'layer0')
myplotter.addHistograms(h_posL1, ['column', 'row'], 'layer1')
myplotter.addHistograms(h_posL2, ['column', 'row'], 'layer2')
myplotter.addHistograms(h_posL3, ['column', 'row'], 'layer3')

myplotter.addHistograms(h_fourLayer, 'layer', 'fourLayerCut')

myplotter.addHistograms(h_maxTimeDiff, 'maxTimeDiff')
myplotter.addHistograms(h_minTimeDiff, 'minTimeDiff')
myplotter.addHistograms(h_allTimeDiff, 'allTimeDiff')


myplotter.addHistograms(h_threeInLinePath0_f0, ['column', 'row'], 'threeHitPath0_s0')
myplotter.addHistograms(h_threeInLinePath1_f0, ['column', 'row'], 'threeHitPath1_s0')
myplotter.addHistograms(h_threeInLinePath2_f0, ['column', 'row'], 'threeHitPath2_s0')
myplotter.addHistograms(h_threeInLinePath3_f0, ['column', 'row'], 'threeHitPath3_s0')
myplotter.addHistograms(h_threeInLinePath4_f0, ['column', 'row'], 'threeHitPath4_s0')
myplotter.addHistograms(h_threeInLinePath5_f0, ['column', 'row'], 'threeHitPath5_s0')
myplotter.addHistograms(h_threeInLinePath6_f0, ['column', 'row'], 'threeHitPath6_s0')
myplotter.addHistograms(h_threeInLinePath7_f0, ['column', 'row'], 'threeHitPath7_s0')
myplotter.addHistograms(h_threeInLinePath8_f0, ['column', 'row'], 'threeHitPath8_s0')
myplotter.addHistograms(h_threeInLinePath9_f0, ['column', 'row'], 'threeHitPath9_s0')
myplotter.addHistograms(h_threeInLinePath10_f0, ['column', 'row'], 'threeHitPath10_s0')
myplotter.addHistograms(h_threeInLinePath11_f0, ['column', 'row'], 'threeHitPath11_s0')
myplotter.addHistograms(h_threeInLinePath12_f0, ['column', 'row'], 'threeHitPath12_s0')
myplotter.addHistograms(h_threeInLinePath13_f0, ['column', 'row'], 'threeHitPath13_s0')
myplotter.addHistograms(h_threeInLinePath14_f0, ['column', 'row'], 'threeHitPath14_s0')
myplotter.addHistograms(h_threeInLinePath15_f0, ['column', 'row'], 'threeHitPath15_s0')

myplotter.addHistograms(h_threeInLinePath0_f1, ['column', 'row'], 'threeHitPath0_s1')
myplotter.addHistograms(h_threeInLinePath1_f1, ['column', 'row'], 'threeHitPath1_s1')
myplotter.addHistograms(h_threeInLinePath2_f1, ['column', 'row'], 'threeHitPath2_s1')
myplotter.addHistograms(h_threeInLinePath3_f1, ['column', 'row'], 'threeHitPath3_s1')
myplotter.addHistograms(h_threeInLinePath4_f1, ['column', 'row'], 'threeHitPath4_s1')
myplotter.addHistograms(h_threeInLinePath5_f1, ['column', 'row'], 'threeHitPath5_s1')
myplotter.addHistograms(h_threeInLinePath6_f1, ['column', 'row'], 'threeHitPath6_s1')
myplotter.addHistograms(h_threeInLinePath7_f1, ['column', 'row'], 'threeHitPath7_s1')
myplotter.addHistograms(h_threeInLinePath8_f1, ['column', 'row'], 'threeHitPath8_s1')
myplotter.addHistograms(h_threeInLinePath9_f1, ['column', 'row'], 'threeHitPath9_s1')
myplotter.addHistograms(h_threeInLinePath10_f1, ['column', 'row'], 'threeHitPath10_s1')
myplotter.addHistograms(h_threeInLinePath11_f1, ['column', 'row'], 'threeHitPath11_s1')
myplotter.addHistograms(h_threeInLinePath12_f1, ['column', 'row'], 'threeHitPath12_s1')
myplotter.addHistograms(h_threeInLinePath13_f1, ['column', 'row'], 'threeHitPath13_s1')
myplotter.addHistograms(h_threeInLinePath14_f1, ['column', 'row'], 'threeHitPath14_s1')
myplotter.addHistograms(h_threeInLinePath15_f1, ['column', 'row'], 'threeHitPath15_s1')

myplotter.addHistograms(h_threeInLinePath0_f2, ['column', 'row'], 'threeHitPath0_s2')
myplotter.addHistograms(h_threeInLinePath1_f2, ['column', 'row'], 'threeHitPath1_s2')
myplotter.addHistograms(h_threeInLinePath2_f2, ['column', 'row'], 'threeHitPath2_s2')
myplotter.addHistograms(h_threeInLinePath3_f2, ['column', 'row'], 'threeHitPath3_s2')
myplotter.addHistograms(h_threeInLinePath4_f2, ['column', 'row'], 'threeHitPath4_s2')
myplotter.addHistograms(h_threeInLinePath5_f2, ['column', 'row'], 'threeHitPath5_s2')
myplotter.addHistograms(h_threeInLinePath6_f2, ['column', 'row'], 'threeHitPath6_s2')
myplotter.addHistograms(h_threeInLinePath7_f2, ['column', 'row'], 'threeHitPath7_s2')
myplotter.addHistograms(h_threeInLinePath8_f2, ['column', 'row'], 'threeHitPath8_s2')
myplotter.addHistograms(h_threeInLinePath9_f2, ['column', 'row'], 'threeHitPath9_s2')
myplotter.addHistograms(h_threeInLinePath10_f2, ['column', 'row'], 'threeHitPath10_s2')
myplotter.addHistograms(h_threeInLinePath11_f2, ['column', 'row'], 'threeHitPath11_s2')
myplotter.addHistograms(h_threeInLinePath12_f2, ['column', 'row'], 'threeHitPath12_s2')
myplotter.addHistograms(h_threeInLinePath13_f2, ['column', 'row'], 'threeHitPath13_s2')
myplotter.addHistograms(h_threeInLinePath14_f2, ['column', 'row'], 'threeHitPath14_s2')
myplotter.addHistograms(h_threeInLinePath15_f2, ['column', 'row'], 'threeHitPath15_s2')

myplotter.addHistograms(h_threeInLinePath0_f3, ['column', 'row'], 'threeHitPath0_s3')
myplotter.addHistograms(h_threeInLinePath1_f3, ['column', 'row'], 'threeHitPath1_s3')
myplotter.addHistograms(h_threeInLinePath2_f3, ['column', 'row'], 'threeHitPath2_s3')
myplotter.addHistograms(h_threeInLinePath3_f3, ['column', 'row'], 'threeHitPath3_s3')
myplotter.addHistograms(h_threeInLinePath4_f3, ['column', 'row'], 'threeHitPath4_s3')
myplotter.addHistograms(h_threeInLinePath5_f3, ['column', 'row'], 'threeHitPath5_s3')
myplotter.addHistograms(h_threeInLinePath6_f3, ['column', 'row'], 'threeHitPath6_s3')
myplotter.addHistograms(h_threeInLinePath7_f3, ['column', 'row'], 'threeHitPath7_s3')
myplotter.addHistograms(h_threeInLinePath8_f3, ['column', 'row'], 'threeHitPath8_s3')
myplotter.addHistograms(h_threeInLinePath9_f3, ['column', 'row'], 'threeHitPath9_s3')
myplotter.addHistograms(h_threeInLinePath10_f3, ['column', 'row'], 'threeHitPath10_s3')
myplotter.addHistograms(h_threeInLinePath11_f3, ['column', 'row'], 'threeHitPath11_s3')
myplotter.addHistograms(h_threeInLinePath12_f3, ['column', 'row'], 'threeHitPath12_s3')
myplotter.addHistograms(h_threeInLinePath13_f3, ['column', 'row'], 'threeHitPath13_s3')
myplotter.addHistograms(h_threeInLinePath14_f3, ['column', 'row'], 'threeHitPath14_s3')
myplotter.addHistograms(h_threeInLinePath15_f3, ['column', 'row'], 'threeHitPath15_s3')

myplotter.addHistograms(h_threeInLineCountPath0_f0, 'threeHitPath0_f0')
myplotter.addHistograms(h_threeInLineCountPath1_f0, 'threeHitPath1_f0')
myplotter.addHistograms(h_threeInLineCountPath2_f0, 'threeHitPath2_f0')
myplotter.addHistograms(h_threeInLineCountPath3_f0, 'threeHitPath3_f0')
myplotter.addHistograms(h_threeInLineCountPath4_f0, 'threeHitPath4_f0')
myplotter.addHistograms(h_threeInLineCountPath5_f0, 'threeHitPath5_f0')
myplotter.addHistograms(h_threeInLineCountPath6_f0, 'threeHitPath6_f0')
myplotter.addHistograms(h_threeInLineCountPath7_f0, 'threeHitPath7_f0')
myplotter.addHistograms(h_threeInLineCountPath8_f0, 'threeHitPath8_f0')
myplotter.addHistograms(h_threeInLineCountPath9_f0, 'threeHitPath9_f0')
myplotter.addHistograms(h_threeInLineCountPath10_f0, 'threeHitPath10_f0')
myplotter.addHistograms(h_threeInLineCountPath11_f0, 'threeHitPath11_f0')
myplotter.addHistograms(h_threeInLineCountPath12_f0, 'threeHitPath12_f0')
myplotter.addHistograms(h_threeInLineCountPath13_f0, 'threeHitPath13_f0')
myplotter.addHistograms(h_threeInLineCountPath14_f0, 'threeHitPath14_f0')
myplotter.addHistograms(h_threeInLineCountPath15_f0, 'threeHitPath15_f0')

myplotter.addHistograms(h_threeInLineCountPath0_f1, 'threeHitPath0_f1')
myplotter.addHistograms(h_threeInLineCountPath1_f1, 'threeHitPath1_f1')
myplotter.addHistograms(h_threeInLineCountPath2_f1, 'threeHitPath2_f1')
myplotter.addHistograms(h_threeInLineCountPath3_f1, 'threeHitPath3_f1')
myplotter.addHistograms(h_threeInLineCountPath4_f1, 'threeHitPath4_f1')
myplotter.addHistograms(h_threeInLineCountPath5_f1, 'threeHitPath5_f1')
myplotter.addHistograms(h_threeInLineCountPath6_f1, 'threeHitPath6_f1')
myplotter.addHistograms(h_threeInLineCountPath7_f1, 'threeHitPath7_f1')
myplotter.addHistograms(h_threeInLineCountPath8_f1, 'threeHitPath8_f1')
myplotter.addHistograms(h_threeInLineCountPath9_f1, 'threeHitPath9_f1')
myplotter.addHistograms(h_threeInLineCountPath10_f1, 'threeHitPath10_f1')
myplotter.addHistograms(h_threeInLineCountPath11_f1, 'threeHitPath11_f1')
myplotter.addHistograms(h_threeInLineCountPath12_f1, 'threeHitPath12_f1')
myplotter.addHistograms(h_threeInLineCountPath13_f1, 'threeHitPath13_f1')
myplotter.addHistograms(h_threeInLineCountPath14_f1, 'threeHitPath14_f1')
myplotter.addHistograms(h_threeInLineCountPath15_f1, 'threeHitPath15_f1')

myplotter.addHistograms(h_threeInLineCountPath0_f2, 'threeHitPath0_f2')
myplotter.addHistograms(h_threeInLineCountPath1_f2, 'threeHitPath1_f2')
myplotter.addHistograms(h_threeInLineCountPath2_f2, 'threeHitPath2_f2')
myplotter.addHistograms(h_threeInLineCountPath3_f2, 'threeHitPath3_f2')
myplotter.addHistograms(h_threeInLineCountPath4_f2, 'threeHitPath4_f2')
myplotter.addHistograms(h_threeInLineCountPath5_f2, 'threeHitPath5_f2')
myplotter.addHistograms(h_threeInLineCountPath6_f2, 'threeHitPath6_f2')
myplotter.addHistograms(h_threeInLineCountPath7_f2, 'threeHitPath7_f2')
myplotter.addHistograms(h_threeInLineCountPath8_f2, 'threeHitPath8_f2')
myplotter.addHistograms(h_threeInLineCountPath9_f2, 'threeHitPath9_f2')
myplotter.addHistograms(h_threeInLineCountPath10_f2, 'threeHitPath10_f2')
myplotter.addHistograms(h_threeInLineCountPath11_f2, 'threeHitPath11_f2')
myplotter.addHistograms(h_threeInLineCountPath12_f2, 'threeHitPath12_f2')
myplotter.addHistograms(h_threeInLineCountPath13_f2, 'threeHitPath13_f2')
myplotter.addHistograms(h_threeInLineCountPath14_f2, 'threeHitPath14_f2')
myplotter.addHistograms(h_threeInLineCountPath15_f2, 'threeHitPath15_f2')

myplotter.addHistograms(h_threeInLineCountPath0_f3, 'threeHitPath0_f3')
myplotter.addHistograms(h_threeInLineCountPath1_f3, 'threeHitPath1_f3')
myplotter.addHistograms(h_threeInLineCountPath2_f3, 'threeHitPath2_f3')
myplotter.addHistograms(h_threeInLineCountPath3_f3, 'threeHitPath3_f3')
myplotter.addHistograms(h_threeInLineCountPath4_f3, 'threeHitPath4_f3')
myplotter.addHistograms(h_threeInLineCountPath5_f3, 'threeHitPath5_f3')
myplotter.addHistograms(h_threeInLineCountPath6_f3, 'threeHitPath6_f3')
myplotter.addHistograms(h_threeInLineCountPath7_f3, 'threeHitPath7_f3')
myplotter.addHistograms(h_threeInLineCountPath8_f3, 'threeHitPath8_f3')
myplotter.addHistograms(h_threeInLineCountPath9_f3, 'threeHitPath9_f3')
myplotter.addHistograms(h_threeInLineCountPath10_f3, 'threeHitPath10_f3')
myplotter.addHistograms(h_threeInLineCountPath11_f3, 'threeHitPath11_f3')
myplotter.addHistograms(h_threeInLineCountPath12_f3, 'threeHitPath12_f3')
myplotter.addHistograms(h_threeInLineCountPath13_f3, 'threeHitPath13_f3')
myplotter.addHistograms(h_threeInLineCountPath14_f3, 'threeHitPath14_f3')
myplotter.addHistograms(h_threeInLineCountPath15_f3, 'threeHitPath15_f3')

#defining the cutflow
#cutflow = [boardMatchCut, pickupCut, 
'''cutflow = [boardMatchCut, pickupCut, triggerCut2, pulseTime, muonAreaCut, mycuts.layerCut,
            myplotter.dict['h_height'], myplotter.dict['h_area'], myplotter.dict['h_layer'], myplotter.dict['h_triggers']]'''

cutflow = [mycuts.totalEventCounter, 
            boardMatchCut, 
            triggerCutNot,
            pickupCut, 
            barCut, 
            pulseTime, 
            firstPulse, 
            nPECut, 
            mycuts.layerCut, mycuts.threeInLine, mycuts.fourLayerCut, mycuts.timeDiff,
            myplotter.dict['h_height'], myplotter.dict['h_area'], myplotter.dict['h_layer'], myplotter.dict['h_fourLayer'],
            myplotter.dict['h_row'], myplotter.dict['h_column'], 
            myplotter.dict['h_posL0'], myplotter.dict['h_posL1'], myplotter.dict['h_posL2'], myplotter.dict['h_posL3']]

for key, value in myplotter.dict.items():
    if value not in cutflow:
        cutflow.append(value)

#create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

#print out the schedule
myschedule.printSchedule()

#create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, step_size=10000)

#run the milliqan processor
myiterator.run()

myschedule.cutFlowPlots()

#save plots
myplotter.saveHistograms("bgAnalysis_{}.root".format(job))

mycuts.getCutflowCounts()

shutil.copy("bgAnalysis_{}.root".format(job), sys.argv[3])

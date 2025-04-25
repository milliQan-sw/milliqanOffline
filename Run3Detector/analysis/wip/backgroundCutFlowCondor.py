


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

sys.path.append(os.path.dirname(__file__) + '/../utilities/')
from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *


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
def firstPulseMax(self, cutName='firstPulseMax', cut=False, branches=None):

    for i in range(80):
        channelCut = self.events.chan == i
        channelNPE = self.events.nPE[channelCut]
        maxIndex = ak.argmax(channelNPE, axis=1, keepdims=True)
        ipulseCut = self.events.ipulse[maxIndex] == 0
        ipulseCut = ak.fill_none(ipulseCut, True, axis=1)
        if i ==0:
            firstPulseMax = ipulseCut
        else:
            firstPulseMax = firstPulseMax & ipulseCut

    _, firstPulseMax = ak.broadcast_arrays(self.events.npulses, ak.flatten(firstPulseMax, axis=1))
    
    '''out1 = self.events.nPE[firstPulseMax]
    out2 = self.events.ipulse[firstPulseMax]
    mask1 = ak.num(out1) > 0
    mask2 = ak.num(out2) > 0
    print(out1[mask1])
    print(out2[mask2])'''
    self.events[cutName] = firstPulseMax
    if cut:
        for branch in branches:
            self.events[branch] = self.events[branch][self.events[cutName]]

@mqCut
def vetoEarlyPulse(self, cutName="vetoEarlyPulse", timeCut=700, cut=False, branches=None):
    earlyPulse = ak.min(self.events.timeFit_module_calibrated, axis=1) < timeCut
    earlyPulse = ak.fill_none(earlyPulse, False)
    _, earlyPulse = ak.broadcast_arrays(self.events.npulses, ~earlyPulse)
    self.events[cutName] = earlyPulse
    if cut:
        for branch in branches:
            self.events[branch] = self.events[branch][self.events[cutName]]

@mqCut
def nPEMaxMin(self, cutName='nPEMaxMin', cut=False, branches=None):
    maxNPE = ak.max(self.events.nPE, axis=1)
    minNPE = ak.min(self.events.nPE, axis=1)

    nPEDiff = maxNPE - minNPE
    nPECut = nPEDiff < 10

    nPECut = ak.fill_none(nPECut, False)

    _, nPECut = ak.broadcast_arrays(self.events.npulses, nPECut)
    self.events[cutName] = nPECut
    if cut:
        for branch in branches:
            self.events[branch] = self.events[branch][self.events[cutName]]


@mqCut
def timeMaxMin(self, cutName='timeMaxMin', cut=False, branches=None):
    maxTime = ak.max(self.events.timeFit_module_calibrated, axis=1)
    minTime = ak.min(self.events.timeFit_module_calibrated, axis=1)

    timeDiff = maxTime - minTime
    timeCut = timeDiff < 15

    timeCut = ak.fill_none(timeCut, False)
    _, timeCut = ak.broadcast_arrays(self.events.npulses, timeCut)
    self.events[cutName] = timeCut
    if cut:
        for branch in branches:
            self.events[branch] = self.events[branch][self.events[cutName]]

@mqCut
def beamMuonPanelVeto(self, cutName='beamMuonPanelVeto', cut=False, branches=None):
    nPECut = self.events.nPE > 100
    panelCut = self.events.type == 1

    finalCut = nPECut & panelCut
    finalCut = ak.any(finalCut, axis=1)
    finalCut = ~finalCut
    finalCut = ak.fill_none(finalCut, False)
    _, finalCut = ak.broadcast_arrays(self.events.npulses, finalCut)
    self.events[cutName] = finalCut
    if cut:
        for branch in branches:
            self.events[branch] = self.events[branch][self.events[cutName]]

@mqCut
def timeDiff(self, cutName='timeDiff'):


    times0 = self.events.timeFit_module_calibrated[self.events.layer==0]
    times3 = self.events.timeFit_module_calibrated[self.events.layer==3]

    combos = ak.cartesian([times0, times3], axis=1)

    diff = combos['1'] - combos['0']

    self.events[cutName] = diff

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
    filelist = sys.argv[1]
    job = sys.argv[2]

    #define a file list to run over
    filelist = getFileList(filelist, job)
    '''filelist = filelist[:10] #temporary'''
    '''filelist = [        
        "/store/user/milliqan/trees/v35/bar/1700/MilliQan_Run1702.59_v35.root:t",
        "/store/user/milliqan/trees/v35/bar/1700/MilliQan_Run1702.60_v35.root:t",
        "/store/user/milliqan/trees/v35/bar/1700/MilliQan_Run1702.61_v35.root:t",
        "/store/user/milliqan/trees/v35/bar/1700/MilliQan_Run1702.62_v35.root:t",
        "/store/user/milliqan/trees/v35/bar/1700/MilliQan_Run1702.63_v35.root:t",
        "/store/user/milliqan/trees/v35/bar/1700/MilliQan_Run1702.64_v35.root:t",
        "/store/user/milliqan/trees/v35/bar/1700/MilliQan_Run1702.65_v35.root:t",
        "/store/user/milliqan/trees/v35/bar/1700/MilliQan_Run1702.66_v35.root:t",
        "/store/user/milliqan/trees/v35/bar/1700/MilliQan_Run1702.67_v35.root:t",
        "/store/user/milliqan/trees/v35/bar/1700/MilliQan_Run1702.68_v35.root:t"
        ]

    filelist = filelist'''
    print("Running on files {}".format(filelist))

    #find the luminosity of files in filelist
    getLumiofFileList(filelist)

    #define the necessary branches to run over
    branches = ['event', 'tTrigger', 'boardsMatched', 'pickupFlag', 'fileNumber', 'runNumber', 'type', 'ipulse', 'nPE', 'chan',
                'time_module_calibrated', 'timeFit_module_calibrated', 'row', 'column', 'layer', 'height', 'area', 'npulses']


    #define the milliqan cuts object
    mycuts = milliqanCuts()

    setattr(milliqanCuts, "firstPulseMax", firstPulseMax)
    setattr(milliqanCuts, "vetoEarlyPulse", vetoEarlyPulse)
    setattr(milliqanCuts, 'nPEMaxMin', nPEMaxMin)
    setattr(milliqanCuts, 'timeMaxMin', timeMaxMin)
    setattr(milliqanCuts, 'beamMuonPanelVeto', beamMuonPanelVeto)
    setattr(milliqanCuts, 'timeDiff', timeDiff)

    #require pulses are in trigger window
    centralTimeCut = getCutMod(mycuts.centralTime, mycuts, 'centralTimeCut', cut=True, branches=branches)

    #require first pulse in channel
    firstPulseCut = getCutMod(mycuts.firstPulse, mycuts, 'firstPulseCut', cut=True, branches=branches)

    #require pulses are not pickup
    pickupCut = getCutMod(mycuts.pickupCut, mycuts, 'pickupCut', cut=True, branches=branches)

    #require that all digitizer boards are matched
    boardMatchCut = getCutMod(mycuts.boardsMatched, mycuts, 'boardMatchCut', cut=True, branches=branches)

    #greater than or equal to one hit per layer
    hitInAllLayers = getCutMod(mycuts.oneHitPerLayerCut, mycuts, 'hitInAllLayers', cut=True, branches=branches, multipleHits=True)

    #exactly one hit per layer
    oneHitPerLayer = getCutMod(mycuts.oneHitPerLayerCut, mycuts, 'oneHitPerLayer', cut=True, branches=branches, multipleHits=False)

    #panel veto
    panelVeto = getCutMod(mycuts.panelVeto, mycuts, 'panelVeto', cut=True, branches=branches)

    #first pulse max
    firstPulseMax = getCutMod(mycuts.firstPulseMax, mycuts, 'firstPulseMax', cut=True, branches=branches)

    #veto events with an early pulse
    vetoEarlyPulse = getCutMod(mycuts.vetoEarlyPulse, mycuts, 'vetoEarlyPylse', cut=True, branches=branches)

    #four in line cut
    straightLineCut = getCutMod(mycuts.straightLineCut, mycuts, 'straightLineCut', cut=True, branches=branches)

    #npe max-min < 10 cut
    nPEMaxMin = getCutMod(mycuts.nPEMaxMin, mycuts, 'nPEMaxMin', cut=True, branches=branches)

    #time max-min < 15 cut
    timeMaxMin = getCutMod(mycuts.timeMaxMin, mycuts, 'timeMaxMin', cut=True, branches=branches)

    #veto events with large hit in front/back panels
    beamMuonPanelVeto = getCutMod(mycuts.beamMuonPanelVeto, mycuts, 'beamMuonPanelVeto', cut=True, branches=branches)


    #define histograms
    h_timeDiff1 = r.TH1F('h_timeDiff1', "Layer 3 and 0 Time Difference", 100, -50, 50)
    h_timeDiff2 = r.TH1F('h_timeDiff2', "Layer 3 and 0 Time Difference", 100, -50, 50)
    h_timeDiff3 = r.TH1F('h_timeDiff3', "Layer 3 and 0 Time Difference", 100, -50, 50)
    h_timeDiff4 = r.TH1F('h_timeDiff4', "Layer 3 and 0 Time Difference", 100, -50, 50)
    h_timeDiff5 = r.TH1F('h_timeDiff5', "Layer 3 and 0 Time Difference", 100, -50, 50)
    h_timeDiff6 = r.TH1F('h_timeDiff6', "Layer 3 and 0 Time Difference", 100, -50, 50)
    h_timeDiff7 = r.TH1F('h_timeDiff7', "Layer 3 and 0 Time Difference", 100, -50, 50)
    h_timeDiff8 = r.TH1F('h_timeDiff8', "Layer 3 and 0 Time Difference", 100, -50, 50)
    h_timeDiff9 = r.TH1F('h_timeDiff9', "Layer 3 and 0 Time Difference", 100, -50, 50)

    #define milliqan plotter
    myplotter = milliqanPlotter()
    myplotter.dict.clear()

    myplotter.addHistograms(h_timeDiff1, 'timeDiff')
    myplotter.addHistograms(h_timeDiff2, 'timeDiff')
    myplotter.addHistograms(h_timeDiff3, 'timeDiff')
    myplotter.addHistograms(h_timeDiff4, 'timeDiff')
    myplotter.addHistograms(h_timeDiff5, 'timeDiff')
    myplotter.addHistograms(h_timeDiff6, 'timeDiff')
    myplotter.addHistograms(h_timeDiff7, 'timeDiff')
    myplotter.addHistograms(h_timeDiff8, 'timeDiff')
    myplotter.addHistograms(h_timeDiff9, 'timeDiff')

    cutflow = [mycuts.totalEventCounter, mycuts.fullEventCounter, 
                mycuts.timeDiff,
                myplotter.dict['h_timeDiff1'],
                boardMatchCut, 
                pickupCut, 
                centralTimeCut,
                firstPulseCut,
                mycuts.timeDiff,
                myplotter.dict['h_timeDiff2'],
                hitInAllLayers,
                mycuts.timeDiff,
                myplotter.dict['h_timeDiff3'],
                oneHitPerLayer,
                mycuts.timeDiff,
                myplotter.dict['h_timeDiff4'],
                panelVeto,
                mycuts.timeDiff,
                myplotter.dict['h_timeDiff5'],
                beamMuonPanelVeto,
                mycuts.timeDiff,
                myplotter.dict['h_timeDiff6'],
                straightLineCut,
                mycuts.timeDiff,
                myplotter.dict['h_timeDiff7'],
                #firstPulseMax,
                #vetoEarlyPulse,
                nPEMaxMin,
                mycuts.timeDiff,
                myplotter.dict['h_timeDiff8'],
                timeMaxMin,
                mycuts.timeDiff,
                myplotter.dict['h_timeDiff9'],
            ]

    for key, value in myplotter.dict.items():
        if value not in cutflow:
            cutflow.append(value)

    #create a schedule of the cuts
    myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

    #print out the schedule
    myschedule.printSchedule()

    #create the milliqan processor object
    myiterator = milliqanProcessor(filelist, branches, myschedule, step_size=10000, qualityLevel='override')

    #run the milliqan processor
    myiterator.run()

    myschedule.cutFlowPlots()

    #save plots
    myplotter.saveHistograms("bgCutFlow_{}.root".format(job))

    mycuts.getCutflowCounts()

    #shutil.copy("bgCutFlow_{}.root".format(job), sys.argv[3])

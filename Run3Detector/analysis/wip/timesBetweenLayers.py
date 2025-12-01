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
import sys

sys.path.append(os.getcwd() + '/../utilities/')
from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *

def loadJson(jsonFile):
    fin = open(jsonFile)
    data = json.load(fin)
    lumis = pd.DataFrame(data['data'], columns=data['columns'])
    return lumis

def getFileList(dataDir, beam, goodRuns, lumis):
    files = []

    for ifile, filename in enumerate(os.listdir(dataDir)):
        if not filename.endswith('root'): continue
        
        runNum = int(filename.split('Run')[1].split('.')[0])
        fileNum = int(filename.split('.')[1].split('_')[0])
            
        goodRun = goodRuns['goodRunTight'].loc[(goodRuns['run'] == runNum) & (goodRuns['file'] == fileNum)]
        beamOn = lumis['beam'].loc[(lumis['run'] == runNum) & (lumis['file'] == fileNum)]

        if len(goodRun) == 0 or len(beamOn) == 0: continue

        #print(filename, runNum, fileNum, beamOn.item(), goodRun.item())
        
        if beam:
            if goodRun.item() and beamOn.item(): files.append(dataDir+filename)
        else:
            print("file {} beam {}".format(filename, beamOn.item()))
            if goodRun.item() and not beamOn.item(): files.append(dataDir+filename)

    print("returning {} files for beam {}".format(len(files), beam))

    return files

@mqCut
def pulseTime(self):
    events = self.events
    straightPath = self.events['straightLineCutPulse']

    timeToUse = 'timeFit_module_calibrated'

    self.events['straightPathL0Time'] = events[timeToUse][events['layer0'] & events['straightLineCutPulse']]
    self.events['straightPathL1Time'] = events[timeToUse][events['layer1'] & events['straightLineCutPulse']]
    self.events['straightPathL2Time'] = events[timeToUse][events['layer2'] & events['straightLineCutPulse']]
    self.events['straightPathL3Time'] = events[timeToUse][events['layer3'] & events['straightLineCutPulse']]

    height0 = ak.max(self.events['height'][events['layer0'] & events['straightLineCutPulse']], axis=1)
    height1 = ak.max(self.events['height'][events['layer1'] & events['straightLineCutPulse']], axis=1)
    height2 = ak.max(self.events['height'][events['layer2'] & events['straightLineCutPulse']], axis=1)
    height3 = ak.max(self.events['height'][events['layer3'] & events['straightLineCutPulse']], axis=1)

    mask0 = (self.events['height'][events['layer0'] & events['straightLineCutPulse']] == height0)
    mask1 = (self.events['height'][events['layer1'] & events['straightLineCutPulse']] == height1)
    mask2 = (self.events['height'][events['layer2'] & events['straightLineCutPulse']] == height2)
    mask3 = (self.events['height'][events['layer3'] & events['straightLineCutPulse']] == height3)

    self.events['straightPathL0Time'] = self.events['straightPathL0Time'][mask0]
    self.events['straightPathL1Time'] = self.events['straightPathL1Time'][mask1]
    self.events['straightPathL2Time'] = self.events['straightPathL2Time'][mask2]
    self.events['straightPathL3Time'] = self.events['straightPathL3Time'][mask3]

    self.events['straightPathDiffL03'] = self.events['straightPathL3Time'] - self.events['straightPathL0Time']


@mqCut
def centralTime(self):
    events = self.events
    timeCut = (events['timeFit_module_calibrated'] > 1100) & (events['timeFit_module_calibrated'] < 1400)
    drop_empty = ak.num(timeCut) > 0
    #newEvents = events[timeCut]
    newEvents = drop_empty & timeCut
    #print()
    #self.events = events[newEvents]
    for branch in branches:
        #print(branch, type(branch))
        self.events[branch] = self.events[branch][newEvents]


if __name__ == "__main__":

    milliqanOfflinePath = '/home/mcarrigan/scratch0/milliQan/analysis/milliqanOffline/Run3Detector/'

    goodRuns = loadJson(milliqanOfflinePath + '/configuration/barConfigs/goodRunsList.json')

    lumis = loadJson(milliqanOfflinePath + '/configuration/barConfigs/mqLumis.json')
    lumis['file'] = lumis['file'].astype(int)

    dataDir = '/store/user/milliqan/trees/v34/1300/'
    beam = False

    files = getFileList(dataDir, beam, goodRuns, lumis)

    #define a file list to run over
    filelist = files[:4]
    #print(filelist)
    #filelist = ['/store/user/milliqan/trees/v34/1300/MilliQan_Run1364.1_v34.root', '/store/user/milliqan/trees/v34/1300/MilliQan_Run1364.2_v34.root', '/store/user/milliqan/trees/v34/1300/MilliQan_Run1364.3_v34.root', '/store/user/milliqan/trees/v34/1300/MilliQan_Run1365.100_v34.root']

    #define the necessary branches to run over
    branches = ['event', 'tTrigger', 'boardsMatched', 'pickupFlag', 'fileNumber', 'runNumber', 
                'time_module_calibrated', 'timeFit_module_calibrated', 'row', 'column', 'layer', 'height', 'area']

    #define the milliqan cuts object
    mycuts = milliqanCuts()

    #require pulses are not pickup
    pickupCut = mycuts.getCut(mycuts.pickupCut, 'pickupCut', cut=True, branches=branches)

    #require that all digitizer boards are matched
    boardMatchCut = mycuts.getCut(mycuts.boardsMatched, 'boardMatchCut', cut=True, branches=branches)

    #height cut to get large pulses
    muonHeightCut = mycuts.getCut(mycuts.heightCut, 'muonHeightCut', heightCut=1200, cut=True, branches=branches)

    #muon area cut
    muonAreaCut = getCutMod(mycuts.areaCut, mycuts, 'muonAreaCut', areaCut=500000, cut=True, branches=branches)

    #straight line cut
    straightLineCutMod = getCutMod(mycuts.straightLineCut, mycuts, 'straightLineCutMod', allowedMove=True)

    #muonAreaCut = mycuts.areaCut('muonAreaCut, areaCut=500000', cut=True, branches=branches)
    #muonAreaCut = mycuts.getCut(mycuts.areaCut, 'muonAreaCut', areaCut=500000, cut=True, branches=branches)

    #define milliqan plotter
    myplotter = milliqanPlotter()

    #create root histogram 
    bins = 400
    xmin = 1100
    xmax = 1500

    h_pulseTime03 = r.TH2F("h_pulseTime03", "Pulse Times Between Layer 0 and 3", bins, xmin, xmax, bins, xmin, xmax)
    h_L0Times = r.TH1F('h_L0Times', "Pulse Times Layer 0", 400, 1100, 1500)
    h_L3Times = r.TH1F('h_L3Times', "Pulse Times Layer 3", 400, 1100, 1500)
    h_TimeDiff = r.TH1F('h_TimeDiff', "Difference in Layer 0 and 3 Times", 100, -50, 50)
    h_height = r.TH1F('h_height', "Height of Passing Pulses", 650, 0, 1300)
    h_area = r.TH1F('h_area', "Area of Passing Pulses", 1000, 0, 100e4)

    setattr(milliqanCuts, "centralTime", centralTime)
    setattr(milliqanCuts, "pulseTime", pulseTime)

    #add root histogram to plotter
    myplotter.addHistograms(h_pulseTime03, ['straightPathL0Time', 'straightPathL3Time'])
    myplotter.addHistograms(h_L0Times, 'straightPathL0Time')
    myplotter.addHistograms(h_L3Times, 'straightPathL3Time')
    myplotter.addHistograms(h_TimeDiff, 'straightPathDiffL03')
    myplotter.addHistograms(h_height, 'height')
    myplotter.addHistograms(h_area, 'area')

    #defining the cutflow
    cutflow = [boardMatchCut, pickupCut, muonAreaCut, mycuts.centralTime, mycuts.layerCut, straightLineCutMod, 
                mycuts.pulseTime, myplotter.dict['h_pulseTime03'], myplotter.dict['h_height'], myplotter.dict['h_area'],
                myplotter.dict['h_L0Times'], myplotter.dict['h_L3Times'], myplotter.dict['h_TimeDiff']]

    #create a schedule of the cuts
    myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

    #print out the schedule
    myschedule.printSchedule()

    #create the milliqan processor object
    myiterator = milliqanProcessor(filelist, branches, myschedule, step_size=10000)

    #run the milliqan processor
    myiterator.run()

    #save plots
    myplotter.saveHistograms("layerTimes_beamOff_1300_v34_lineMod.root")

    mycuts.getCutflowCounts()
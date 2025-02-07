


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

def checkBeam(mqLumis, run, file, branch='beam'):
    #print("check beam run {} file {}".format(run, file))
    beam = mqLumis[branch].loc[(mqLumis['run'] == run) & (mqLumis['file'] == file)]
    if beam.size == 0: return None
    beam = beam.values[0]
    return beam

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

def findChannel(layer, row, col, htype=0, config='../../configuration/barConfigs/configRun1296_present.json'):
    with open(config, 'r') as fin:
        df = json.load(fin)['chanMap']
        df = pd.DataFrame(df, columns=['col', 'row', 'layer', 'type'])
    chan = df[(df['col'] == col) & (df['row'] == row) & (df['layer'] == layer) & (df['type'] == htype)].index[0]
    return chan

@mqCut
def getTimeDiffs(self):

    #loop over all possible 4 in line paths
    for i in range(16):
        #each of these is a mask for the pulses that are 3 in row, 0 for layers 1, 2, 3
        cut0 = self.events['threeHitPath{}_p0'.format(i)] #layers 1, 2, 3
        cut1 = self.events['threeHitPath{}_p1'.format(i)] #layers 0, 2, 3
        cut2 = self.events['threeHitPath{}_p2'.format(i)] #layers 0, 1, 3
        cut3 = self.events['threeHitPath{}_p3'.format(i)] #layers 0, 1, 2

        #create names for every possible time difference, each path (16), line (4), layer combination (3)
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

        #get the times for each layer passing the three in line paths
        times0_1 = self.events['timeFit_module_calibrated'][(cut0) & (self.events.layer==1)]
        times0_2 = self.events['timeFit_module_calibrated'][(cut0) & (self.events.layer==2)]
        times0_3 = self.events['timeFit_module_calibrated'][(cut0) & (self.events.layer==3)]

        times1_0 = self.events['timeFit_module_calibrated'][(cut1) & (self.events.layer==0)]
        times1_2 = self.events['timeFit_module_calibrated'][(cut1) & (self.events.layer==2)]
        times1_3 = self.events['timeFit_module_calibrated'][(cut1) & (self.events.layer==3)]

        times2_0 = self.events['timeFit_module_calibrated'][(cut2) & (self.events.layer==0)]
        times2_1 = self.events['timeFit_module_calibrated'][(cut2) & (self.events.layer==1)]
        times2_3 = self.events['timeFit_module_calibrated'][(cut2) & (self.events.layer==3)]

        times3_0 = self.events['timeFit_module_calibrated'][(cut3) & (self.events.layer==0)]
        times3_1 = self.events['timeFit_module_calibrated'][(cut3) & (self.events.layer==1)]
        times3_2 = self.events['timeFit_module_calibrated'][(cut3) & (self.events.layer==2)]

        #create branches of the time differences between layers
        #note: last layer is always first in subtraction
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

@mqCut
def frontPanelHit(self, cutName = 'frontPanelHit', cut=False, branches=None, both=False):
    frontPanelHit = ak.any((self.events['type']==1) & (self.events['layer'] == -1), axis=1)
    if both:
        backPanelHit = ak.any((self.events['type']==1) & (self.events['layer'] == 4), axis=1)
        panelHit = frontPanelHit & backPanelHit
    else:
        panelHit = frontPanelHit
    _, self.events[cutName] = ak.broadcast_arrays(self.events.npulses, panelHit)
    if cut:
        for branch in branches:
            self.events[branch] = self.events[branch][self.events[cutName]]

@mqCut
def timeDiff(self, cutName='timeDiff'):

    allPulses = True
    allStraightLine = True

    if allPulses:

        times0 = self.events.timeFit[(self.events['layer']==-1) & (self.events['type']==1)]
        times3 = self.events.timeFit[self.events.layer==3]

        timesNoCorr0 = self.events.timeFit[self.events.layer==0]
        timesNoCorr3 = self.events.timeFit[self.events.layer==3]

        combos = ak.cartesian([times0, times3], axis=1)
        combosNoCorr = ak.cartesian([timesNoCorr0, timesNoCorr3], axis=1)

        diff = combos['1'] - combos['0']
        diffNoCorr = combosNoCorr['1'] - combosNoCorr['0']

        self.events[cutName] = diff
        self.events[cutName+'NoCorr'] = diffNoCorr

    if allStraightLine:

        frontPanelTimes = self.events.timeFit[(self.events['type']==1) & (self.events['layer']==-1)]

        for layer in range(4):
            for row in range(4):
                for col in range(4):
                    chanTimes = self.events.timeFit[(self.events['threeHitPath_allPulses']) & (self.events['layer'] == layer) & (self.events['row'] == row) & (self.events['column'] == col)]
                    t_combo = ak.cartesian([chanTimes, frontPanelTimes], axis=1)

                    t_diff = t_combo['0'] - t_combo['1']

                    channel = int(findChannel(layer, row, col))
                    if channel == 78: channel=24
                    if channel == 79: channel=25

                    self.events[cutName+str(channel)] = t_diff


@mqCut
def pulseTime(self):
    events = self.events
    straightPath = self.events['straightLineCutPulse']

    timeToUse = 'timeFit_module_calibrated'

    self.events['straightPathL0Time'] = events[timeToUse][(events.layer==0) & events['straightLineCutPulse']]
    self.events['straightPathL1Time'] = events[timeToUse][(events.layer==1) & events['straightLineCutPulse']]
    self.events['straightPathL2Time'] = events[timeToUse][(events.layer==2) & events['straightLineCutPulse']]
    self.events['straightPathL3Time'] = events[timeToUse][(events.layer==3) & events['straightLineCutPulse']]

    height0 = ak.max(self.events['height'][(events.layer==0) & events['straightLineCutPulse']], axis=1)
    height1 = ak.max(self.events['height'][(events.layer==1) & events['straightLineCutPulse']], axis=1)
    height2 = ak.max(self.events['height'][(events.layer==2) & events['straightLineCutPulse']], axis=1)
    height3 = ak.max(self.events['height'][(events.layer==3) & events['straightLineCutPulse']], axis=1)

    mask0 = (self.events['height'][(events.layer==0) & events['straightLineCutPulse']] == height0)
    mask1 = (self.events['height'][(events.layer==1) & events['straightLineCutPulse']] == height1)
    mask2 = (self.events['height'][(events.layer==2) & events['straightLineCutPulse']] == height2)
    mask3 = (self.events['height'][(events.layer==3) & events['straightLineCutPulse']] == height3)

    self.events['straightPathL0Time'] = self.events['straightPathL0Time'][mask0]
    self.events['straightPathL1Time'] = self.events['straightPathL1Time'][mask1]
    self.events['straightPathL2Time'] = self.events['straightPathL2Time'][mask2]
    self.events['straightPathL3Time'] = self.events['straightPathL3Time'][mask3]

    self.events['timeDiffOld'] = self.events['straightPathL3Time'] - self.events['straightPathL0Time']
    #print("testing", ak.drop_none(self.events['timeDiffOld']), ak.drop_none(self.events['straightPathL0Time']), ak.drop_none(self.events['straightPathL3Time']))


if __name__ == "__main__":


    goodRuns = loadJson('goodRunsList.json')
    lumis = loadJson('mqLumis.json')

    #get list of files to look at
    files = []

    beam = True

    #get the filelist and job number
    '''filelist = sys.argv[1]
    job = sys.argv[2]'''
    job = 0

    #define a file list to run over
    #TODO select only beam on or beam off
    dataDir = '/store/user/milliqan/trees/v35/bar/1500/'
    '''filelist = []
    for filename in os.listdir(dataDir):
        if 'Run1541' not in filename: continue
        run = int(filename.split('Run')[1].split('.')[0])
        file = int(filename.split('.')[1].split('_')[0])
        #beamOn = checkBeam(lumis, run, file, branch='beamInFill')
        #if beam and not beamOn: continue
        #if not beam and beamOn: continue
        filelist.append('/'.join([dataDir, filename])+':t')'''
    
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
        ]'''
    filelist = [
        #'../skim/MilliQan_Run1000_v35_skim_beamOn_tight.root',
        #'../skim/MilliQan_Run1100_v35_skim_beamOn_tight.root',
        #'../skim/MilliQan_Run1200_v35_skim_beamOn_tight.root',
        #'../skim/MilliQan_Run1300_v35_skim_beamOn_tight.root',
        '../skim/MilliQan_Run1400_v35_skim_beamOn_tight.root',
        '../skim/MilliQan_Run1500_v35_skim_beamOn_tight.root',
        '../skim/MilliQan_Run1600_v35_skim_beamOn_tight.root',
        '../skim/MilliQan_Run1700_v35_skim_beamOn_tight.root'
    ]

    '''filelist = [
        '../skim/MilliQan_Run1300_v35_skim_beamOff_tight.root',
        '../skim/MilliQan_Run1400_v35_skim_beamOff_tight.root',
        '../skim/MilliQan_Run1500_v35_skim_beamOff_tight.root',
        '../skim/MilliQan_Run1600_v35_skim_beamOff_tight.root',
        '../skim/MilliQan_Run1700_v35_skim_beamOff_tight.root',
    ]'''

    print("Running on files {}".format(filelist))

    #find the luminosity of files in filelist
    #getLumiofFileList(filelist)

    #define the necessary branches to run over
    branches = ['event', 'tTrigger', 'boardsMatched', 'pickupFlag', 'pickupFlagTight', 'fileNumber', 'runNumber', 'type', 'ipulse', 'nPE', 'chan',
                'time_module_calibrated', 'timeFit_module_calibrated', 'row', 'column', 'layer', 'height', 'area', 'npulses', 'timeFit']


    #define the milliqan cuts object
    mycuts = milliqanCuts()

    setattr(milliqanCuts, "getTimeDiffs", getTimeDiffs)
    setattr(milliqanCuts, 'frontPanelHit', frontPanelHit)
    setattr(milliqanCuts, 'timeDiff', timeDiff)
    setattr(milliqanCuts, "pulseTime", pulseTime)

    #require pulses are not pickup
    pickupCut = getCutMod(mycuts.pickupCut, mycuts, 'pickupCut', tight=True, cut=True, branches=branches)

    #require that all digitizer boards are matched
    boardMatchCut = getCutMod(mycuts.boardsMatched, mycuts, 'boardMatchCut', cut=True, branches=branches)

    #greater than or equal to one hit per layer
    hitInAllLayers = getCutMod(mycuts.oneHitPerLayerCut, mycuts, 'hitInAllLayers', cut=True, branches=branches, multipleHits=False)

    #exactly one hit per layer
    oneHitPerLayer = getCutMod(mycuts.oneHitPerLayerCut, mycuts, 'oneHitPerLayer', cut=True, branches=branches, multipleHits=False)

    #four layer cut
    fourLayerCut = getCutMod(mycuts.fourLayerCut, mycuts, 'fourLayerCut', cut=True, branches=branches)

    #panel veto
    panelVeto = getCutMod(mycuts.panelVeto, mycuts, 'panelVeto', nPECut=40e3, cut=True, branches=branches)

    #nPE Cut
    nPECut = getCutMod(mycuts.nPECut, mycuts, 'nPECut', nPECut=200, cut=True, branches=branches)

    #area cut
    areaCut = getCutMod(mycuts.areaCut, mycuts, 'areaCut', areaCut=300000, cut=True, branches=branches)

    #first pulse cut
    firstPulseCut = getCutMod(mycuts.firstPulseCut, mycuts, 'firstPulseCut', cut=True, branches=branches)

    #require front panel has hit
    #frontPanelHit = getCutMod(mycuts.frontPanelHit, mycuts, 'frontPanelHit', cut=True, branches=branches)

    #require boths panels have hit
    frontPanelHit = getCutMod(mycuts.frontPanelHit, mycuts, 'frontBackPanelsHit', cut=True, branches=branches, both=True)

    #require hit time is in trigger window
    centralTime = getCutMod(mycuts.centralTime, mycuts, 'centralTime', cut=True, branches=branches)

    #create all plots for timing differences 64 paths, 3 timing differences each
    timingHistos = []
    cutNames = []
    nbins = 100
    minx = -50
    maxx = 50
    for i in range(16):
        h_name1 = 'h_timeDiff{}_{}_layers{}{}'.format(i, 0, 1, 2)
        h_name2 = 'h_timeDiff{}_{}_layers{}{}'.format(i, 0, 1, 3)
        h_name3 = 'h_timeDiff{}_{}_layers{}{}'.format(i, 0, 2, 3)
        h_name4 = 'h_timeDiff{}_{}_layers{}{}'.format(i, 1, 0, 2)
        h_name5 = 'h_timeDiff{}_{}_layers{}{}'.format(i, 1, 0, 3)
        h_name6 = 'h_timeDiff{}_{}_layers{}{}'.format(i, 1, 2, 3)
        h_name7 = 'h_timeDiff{}_{}_layers{}{}'.format(i, 2, 0, 1)
        h_name8 = 'h_timeDiff{}_{}_layers{}{}'.format(i, 2, 0, 3)
        h_name9 = 'h_timeDiff{}_{}_layers{}{}'.format(i, 2, 1, 3)
        h_name10 = 'h_timeDiff{}_{}_layers{}{}'.format(i, 3, 0, 1)
        h_name11 = 'h_timeDiff{}_{}_layers{}{}'.format(i, 3, 0, 2)
        h_name12 = 'h_timeDiff{}_{}_layers{}{}'.format(i, 3, 1, 2)

        h1 = r.TH1F(h_name1, 'Time Difference Path {}, Cut {}, Layers {} and {}'.format(i, 0, 1, 2), nbins, minx, maxx)
        h2 = r.TH1F(h_name2, 'Time Difference Path {}, Cut {}, Layers {} and {}'.format(i, 0, 1, 3), nbins, minx, maxx)
        h3 = r.TH1F(h_name3, 'Time Difference Path {}, Cut {}, Layers {} and {}'.format(i, 0, 2, 3), nbins, minx, maxx)
        h4 = r.TH1F(h_name4, 'Time Difference Path {}, Cut {}, Layers {} and {}'.format(i, 1, 0, 2), nbins, minx, maxx)
        h5 = r.TH1F(h_name5, 'Time Difference Path {}, Cut {}, Layers {} and {}'.format(i, 1, 0, 3), nbins, minx, maxx)
        h6 = r.TH1F(h_name6, 'Time Difference Path {}, Cut {}, Layers {} and {}'.format(i, 1, 2, 3), nbins, minx, maxx)
        h7 = r.TH1F(h_name7, 'Time Difference Path {}, Cut {}, Layers {} and {}'.format(i, 2, 0, 1), nbins, minx, maxx)
        h8 = r.TH1F(h_name8, 'Time Difference Path {}, Cut {}, Layers {} and {}'.format(i, 2, 0, 3), nbins, minx, maxx)
        h9 = r.TH1F(h_name9, 'Time Difference Path {}, Cut {}, Layers {} and {}'.format(i, 2, 1, 3), nbins, minx, maxx)
        h10 = r.TH1F(h_name10, 'Time Difference Path {}, Cut {}, Layers {} and {}'.format(i, 3, 0, 1), nbins, minx, maxx)
        h11 = r.TH1F(h_name11, 'Time Difference Path {}, Cut {}, Layers {} and {}'.format(i, 3, 0, 2), nbins, minx, maxx)
        h12 = r.TH1F(h_name12, 'Time Difference Path {}, Cut {}, Layers {} and {}'.format(i, 3, 1, 2), nbins, minx, maxx)

        timingHistos.append(h1)
        timingHistos.append(h2)
        timingHistos.append(h3)
        timingHistos.append(h4)
        timingHistos.append(h5)
        timingHistos.append(h6)
        timingHistos.append(h7)
        timingHistos.append(h8)
        timingHistos.append(h9)
        timingHistos.append(h10)
        timingHistos.append(h11)
        timingHistos.append(h12)

        cutNames.append('timeDiff_path{}_line{}_layers{}_{}'.format(i, 0, 1, 2))
        cutNames.append('timeDiff_path{}_line{}_layers{}_{}'.format(i, 0, 1, 3))
        cutNames.append('timeDiff_path{}_line{}_layers{}_{}'.format(i, 0, 2, 3))
        cutNames.append('timeDiff_path{}_line{}_layers{}_{}'.format(i, 1, 0, 2))
        cutNames.append('timeDiff_path{}_line{}_layers{}_{}'.format(i, 1, 0, 3))
        cutNames.append('timeDiff_path{}_line{}_layers{}_{}'.format(i, 1, 2, 3))
        cutNames.append('timeDiff_path{}_line{}_layers{}_{}'.format(i, 2, 0, 1))
        cutNames.append('timeDiff_path{}_line{}_layers{}_{}'.format(i, 2, 0, 3))
        cutNames.append('timeDiff_path{}_line{}_layers{}_{}'.format(i, 2, 1, 3))
        cutNames.append('timeDiff_path{}_line{}_layers{}_{}'.format(i, 3, 0, 1))
        cutNames.append('timeDiff_path{}_line{}_layers{}_{}'.format(i, 3, 0, 2))
        cutNames.append('timeDiff_path{}_line{}_layers{}_{}'.format(i, 3, 1, 2))

    channelToPanelHists = []
    chanToPanelNames = []
    nbins = 100
    minx = -50
    maxx = 50
    for i in range(64):
        h_name = 'h_timeDiffFrontPanel{}'.format(i)
        h = r.TH1F(h_name, "Time Difference Between Front Panel and Channel {}".format(i), nbins, minx, maxx)
        channelToPanelHists.append(h)
        cutName = 'timeDiff{}'.format(i)
        chanToPanelNames.append(cutName)

    h_channels = r.TH1F('h_channels', 'Channel', 80, 0, 80)
    h_timeDiff = r.TH1F('h_timeDiff', 'Time Difference L3-L0', 100, -100, 100)
    h_timeDiffNoCorr = r.TH1F('h_timeDiffNoCorr', 'Time Difference L3-L0', 100, -100, 100)
    h_timeDiffOld = r.TH1F('h_timeDiffOld', 'Time Difference L3-L0', 100, -100, 100)

    cutflow = [mycuts.totalEventCounter, mycuts.fullEventCounter, 
                boardMatchCut, 
                pickupCut, 
                panelVeto, #only use with beam on data
                firstPulseCut,
                nPECut,
                centralTime,
                fourLayerCut,
                frontPanelHit,
                mycuts.straightLineCut, 
                mycuts.pulseTime,
                mycuts.threeInLine,
                mycuts.timeDiff,
                mycuts.getTimeDiffs
            ]
    
    #define milliqan plotter
    myplotter = milliqanPlotter()
    myplotter.dict.clear()

    myplotter.addHistograms(h_channels, 'chan')
    myplotter.addHistograms(h_timeDiff, 'timeDiff')
    myplotter.addHistograms(h_timeDiffNoCorr, 'timeDiffNoCorr')
    myplotter.addHistograms(h_timeDiffOld, 'timeDiffOld')

    for h, n in zip(channelToPanelHists, chanToPanelNames):
        myplotter.addHistograms(h, n)

    for h, n in zip(timingHistos, cutNames):
        myplotter.addHistograms(h, n)

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
    myplotter.saveHistograms("timingCorrection{}.root".format('_beamOn_frontBackVeto'))

    mycuts.getCutflowCounts()

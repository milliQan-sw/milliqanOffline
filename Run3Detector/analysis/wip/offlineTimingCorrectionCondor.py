


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
def frontPanelHit(self, cutName = 'frontPanelHit', cut=False, branches=None):
    panelHit = ak.any(self.events['chan']==74, axis=1)
    _, self.events[cutName] = ak.broadcast_arrays(self.events.npulses, panelHit)
    if cut:
        for branch in branches:
            self.events[branch] = self.events[branch][self.events[cutName]]

@mqCut
def timeDiff(self, cutName='timeDiff'):

    times0 = self.events.timeFit_module_calibrated[self.events.layer==0]
    times3 = self.events.timeFit_module_calibrated[self.events.layer==3]

    max0 = ak.max(self.events.nPE[self.events.layer==0], axis=1)
    max3 = ak.max(self.events.nPE[self.events.layer==3], axis=1)

    mask0 = self.events.nPE[self.events.layer==0] == max0
    mask3 = self.events.nPE[self.events.layer==3] == max3

    diff = times3[mask3] - times0[mask0]

    timesFit0 = self.events.timeFit[self.events.layer==0]
    timesFit3 = self.events.timeFit[self.events.layer==3]

    #create plots showing difference without timing corrections
    diffNoCorr = timesFit3[mask3] - timesFit0[mask0]

    testCut = ak.num(ak.drop_none(diff)) > 0

    self.events[cutName] = diff
    self.events[cutName+'NoCorr'] = diffNoCorr



if __name__ == "__main__":


    goodRuns = loadJson('goodRunsList.json')
    lumis = loadJson('mqLumis.json')

    #get list of files to look at
    files = []

    beam = False

    #get the filelist and job number
    filelist = '/'.join([sys.argv[3], sys.argv[1]])
    job = sys.argv[2]
    #job = 0

    filelist = getFileList(filelist, job)
    print("Running on files {}".format(filelist))

    #find the luminosity of files in filelist
    getLumiofFileList(filelist)

    #define the necessary branches to run over
    branches = ['event', 'tTrigger', 'boardsMatched', 'pickupFlag', 'fileNumber', 'runNumber', 'type', 'ipulse', 'nPE', 'chan',
                'time_module_calibrated', 'timeFit_module_calibrated', 'row', 'column', 'layer', 'height', 'area', 'npulses', 'timeFit']


    #define the milliqan cuts object
    mycuts = milliqanCuts()

    setattr(milliqanCuts, "getTimeDiffs", getTimeDiffs)
    setattr(milliqanCuts, 'frontPanelHit', frontPanelHit)
    setattr(milliqanCuts, 'timeDiff', timeDiff)

    #require pulses are not pickup
    pickupCut = getCutMod(mycuts.pickupCut, mycuts, 'pickupCut', cut=True, branches=branches)

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

    #first pulse cut
    firstPulseCut = getCutMod(mycuts.firstPulseCut, mycuts, 'firstPulseCut', cut=True, branches=branches)

    #require front panel has hit
    frontPanelHit = getCutMod(mycuts.frontPanelHit, mycuts, 'frontPanelHit', cut=True, branches=branches)

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

    h_channels = r.TH1F('h_channels', 'Channel', 80, 0, 80)
    h_timeDiff = r.TH1F('h_timeDiff', 'Time Difference L3-L0', 400, -200, 200)
    h_timeDiffNoCorr = r.TH1F('h_timeDiffNoCorr', 'Time Difference L3-L0', 400, -200, 200)


    '''cutflow = [mycuts.totalEventCounter, mycuts.fullEventCounter, 
                boardMatchCut, 
                pickupCut, 
                firstPulseCut,
                nPECut,
                #hitInAllLayers,
                panelVeto,
                mycuts.threeInLine,
                mycuts.getTimeDiffs,
            ]'''

    cutflow = [mycuts.totalEventCounter, mycuts.fullEventCounter, 
                boardMatchCut, 
                pickupCut, 
                #panelVeto,
                firstPulseCut,
                nPECut,
                fourLayerCut,
                #frontPanelHit,
                mycuts.timeDiff,
            ]
    
    #define milliqan plotter
    myplotter = milliqanPlotter()
    myplotter.dict.clear()

    myplotter.addHistograms(h_channels, 'chan')
    myplotter.addHistograms(h_timeDiff, 'timeDiff')
    myplotter.addHistograms(h_timeDiffNoCorr, 'timeDiffNoCorr')

    '''for h, n in zip(timingHistos, cutNames):
        myplotter.addHistograms(h, n)'''

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
    myplotter.saveHistograms("timingCorrection_{}.root".format(job))

    mycuts.getCutflowCounts()

    shutil.copy("timingCorrection_{}.root".format(job), sys.argv[3])

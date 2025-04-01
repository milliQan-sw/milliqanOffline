


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
import itertools

sys.path.append(os.path.dirname(__file__) + '/../utilities/')
from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *
from utilities import *

@mqCut
def cosmicMuonCut(self, cutName='cosmicMuonCut', nBarsRequired = 2, areaCut=10e3, cut=False, branches=None):


    frontPanels = ak.any((self.events['type']==2) & self.events['layer']==0, axis=1)
    backPanels = ak.any((self.events['type']==2) & self.events['layer']==2, axis=1)

    nBarsL1 = ak.sum((self.events['type']==0) & (self.events['layer']==0) & (self.events['area'] > areaCut), axis=1) > nBarsRequired
    nBarsL2 = ak.sum((self.events['type']==0) & (self.events['layer']==1) & (self.events['area'] > areaCut), axis=1) > nBarsRequired
    nBarsL3 = ak.sum((self.events['type']==0) & (self.events['layer']==2) & (self.events['area'] > areaCut), axis=1) > nBarsRequired
    nBarsL4 = ak.sum((self.events['type']==0) & (self.events['layer']==3) & (self.events['area'] > areaCut), axis=1) > nBarsRequired

    frontBars = nBarsL1 | nBarsL2  
    backBars = nBarsL3 | nBarsL4

    #cosmicCut = (frontPanels & frontBars) | (backPanels & backBars)
    cosmicCut = frontBars | backBars

    _, cosmicCut = ak.broadcast_arrays(self.events['npulses'], cosmicCut)

    self.events[cutName] = cosmicCut

    if cut:
        self.cutBranches(branches, cutName)

@mqCut
def cosmicMuonCutHard(self, cutName='cosmicMuonCutHard', nBarsRequired=4, areaCut=300e3, cut=False, branches=None):

    L1 = (self.events['type'] == 0) & (self.events['layer'] == 0) & (self.events['area'] >= areaCut)
    L4 = (self.events['type'] == 0) & (self.events['layer'] == 3) & (self.events['area'] >= areaCut)

    for i in range(4):
        if i==0:
            passes1 = ak.sum(L1 & (self.events['column'] == i), axis=1) >= nBarsRequired
            passes4 = ak.sum(L4 & (self.events['column'] == i), axis=1) >= nBarsRequired
        else:
            passes1 = passes1 | (ak.sum(L1 & (self.events['column'] == i), axis=1) >= nBarsRequired)
            passes4 = passes4 | (ak.sum(L4 & (self.events['column'] == i), axis=1) >= nBarsRequired)

    passes = passes1 | passes4

    _, passes = ak.broadcast_arrays(self.events['npulses'], passes)
    self.events[cutName] = passes

    if cut:
        self.cutBranches(branches, cutName)


@mqCut
def frontBackPanelInfo(self, cutName='frontBackPanelInfo', cut=False, areaCut=100e3, branches=None):

    frontPanelCut = (self.events['type']==1) & (self.events['layer']==-1) 
    backPanelCut = (self.events['type']==1) & (self.events['layer']==4)

    frontPanelCut = frontPanelCut & (self.events['area']>=areaCut)
    backPanelCut = backPanelCut & (self.events['area']>=areaCut)
    
    self.events['frontArea'] = self.events['area'][frontPanelCut]
    self.events['backArea'] = self.events['area'][backPanelCut]

    self.events['frontNPE'] = self.events['nPE'][frontPanelCut]
    self.events['backNPE'] = self.events['nPE'][backPanelCut]

    self.events['frontHeight'] = self.events['height'][frontPanelCut]
    self.events['backHeight'] = self.events['height'][backPanelCut]

    self.events['frontDuration'] = self.events['duration'][frontPanelCut]
    self.events['backDuration'] = self.events['duration'][backPanelCut]

    self.events['frontRiseSamples'] = self.events['riseSamples'][frontPanelCut]
    self.events['backRiseSamples'] = self.events['riseSamples'][backPanelCut]

    self.events['frontFallSamples'] = self.events['fallSamples'][frontPanelCut]
    self.events['backFallSamples'] = self.events['fallSamples'][backPanelCut]

    _, self.events['frontHits'] = ak.broadcast_arrays(self.events['npulses'], ak.count(self.events['npulses'][frontPanelCut], axis=1))
    _, self.events['backHits'] = ak.broadcast_arrays(self.events['npulses'], ak.count(self.events['npulses'][backPanelCut], axis=1))

    frontTime = ak.max(self.events['timeFit_module_calibrated'][frontPanelCut], axis=1, keepdims=True)
    backTime = ak.max(self.events['timeFit_module_calibrated'][backPanelCut], axis=1, keepdims=True)

    timeDiff = backTime - frontTime

    self.events['panelTimeDiff'] = timeDiff


@mqCut
def timeDiffBars(self, cutName='timeDiffBars'):

    frontPanelCut = (self.events['type']==1) & (self.events['layer']==-1) & (self.events['area']>100e3)

    L0Mask = (self.events['layer'] == 0) & (self.events['type']==0) #& (self.events['straightLineCutModPulse'])
    L1Mask = (self.events['layer'] == 1) & (self.events['type']==0) #& (self.events['straightLineCutModPulse'])
    L2Mask = (self.events['layer'] == 2) & (self.events['type']==0) #& (self.events['straightLineCutModPulse'])
    L3Mask = (self.events['layer'] == 3) & (self.events['type']==0) #& (self.events['straightLineCutModPulse'])

    #changes
    maxL0 = ak.argmax(self.events['area'][L0Mask], axis=1, keepdims=True)
    maxL1 = ak.argmax(self.events['area'][L1Mask], axis=1, keepdims=True)
    maxL2 = ak.argmax(self.events['area'][L2Mask], axis=1, keepdims=True)
    maxL3 = ak.argmax(self.events['area'][L3Mask], axis=1, keepdims=True)

    frontPanelExists = ak.any(frontPanelCut, axis=1) & ak.any(L0Mask, axis=1)
    _, frontPanelExists = ak.broadcast_arrays(self.events['npulses'], frontPanelExists)

    #L0Front = L0Mask[maxL0]
    #L1Front = L1Mask[maxL1]
    #L2Front = L2Mask[maxL2]
    #L3Front = L3Mask[maxL3]

    maxL0Front = ak.argmax(self.events['area'][L0Mask&frontPanelExists], axis=1, keepdims=True)
    maxL1Front = ak.argmax(self.events['area'][L1Mask&frontPanelExists], axis=1, keepdims=True)
    maxL2Front = ak.argmax(self.events['area'][L2Mask&frontPanelExists], axis=1, keepdims=True)
    maxL3Front = ak.argmax(self.events['area'][L3Mask&frontPanelExists], axis=1, keepdims=True)

    timesL0Front = ak.drop_none(self.events['timeFit_module_calibrated'][L0Mask&frontPanelExists][maxL0Front])
    timesL1Front = ak.drop_none(self.events['timeFit_module_calibrated'][L1Mask&frontPanelExists][maxL1Front])
    timesL2Front = ak.drop_none(self.events['timeFit_module_calibrated'][L2Mask&frontPanelExists][maxL2Front])
    timesL3Front = ak.drop_none(self.events['timeFit_module_calibrated'][L3Mask&frontPanelExists][maxL3Front])

    timesFront = self.events['timeFit_module_calibrated'][frontPanelCut & ak.any(L0Mask, axis=1)]
    
    timesL0 = self.events['timeFit_module_calibrated'][L0Mask]
    timesL1 = self.events['timeFit_module_calibrated'][L1Mask]
    timesL2 = self.events['timeFit_module_calibrated'][L2Mask]
    timesL3 = self.events['timeFit_module_calibrated'][L3Mask]

    timesL0 = timesL0[maxL0]
    timesL1 = timesL1[maxL1]
    timesL2 = timesL2[maxL2]
    timesL3 = timesL3[maxL3]
    #changes
    
    timeDiffL30 = timesL3 - timesL0
    timeDiffL20 = timesL2 - timesL0
    timeDiffL10 = timesL1 - timesL0
    
    #timeDiffFront0 = ak.drop_none(ak.mask(timesL0, frontPanelExists))-ak.drop_none(ak.mask(timesFront, layer0Exists))
    #timeDiffFront1 = ak.drop_none(ak.mask(timesL1, frontPanelExists))-ak.drop_none(ak.mask(timesFront, layer0Exists))
    #timeDiffFront2 = ak.drop_none(ak.mask(timesL2, frontPanelExists))-ak.drop_none(ak.mask(timesFront, layer0Exists))
    #timeDiffFront3 = ak.drop_none(ak.mask(timesL3, frontPanelExists))-ak.drop_none(ak.mask(timesFront, layer0Exists))
    timeDiffFront0 = timesL0Front - timesFront
    timeDiffFront1 = timesL1Front - timesFront
    timeDiffFront2 = timesL2Front - timesFront
    timeDiffFront3 = timesL3Front - timesFront

    self.events['timeDiffL30'] = timeDiffL30
    self.events['timeDiffL20'] = timeDiffL20
    self.events['timeDiffL10'] = timeDiffL10
    
    self.events['timeDiffFront0'] = timeDiffFront0
    self.events['timeDiffFront1'] = timeDiffFront1
    self.events['timeDiffFront2'] = timeDiffFront2
    self.events['timeDiffFront3'] = timeDiffFront3

    self.events['nPEL3'] = self.events['nPE'][L3Mask&frontPanelExists&(self.events['chan']==60)]
    self.events['nPEFront'] = self.events['nPE'][frontPanelCut & ak.any(L0Mask, axis=1)]


@mqCut
def cutStraightPulses(self, cutName='cutStraightPulses', cut=False, branches=None):

    self.events[cutName] = ~self.events['straightLineCutPulses']

    #for row
        # for col
            #L1 = self.events['layer'] ==1
            #thisRow = self.events['row'] == row
            #thisCol = self.events['column'] == col
            #straightL1 = L1 & straightLineCutPulses & thisRow & thisCol
            

    if cut:
        self.cutBranches(branches, cutName)

@mqCut
def panelRequired(self, cutName='panelRequired', cut=False, branches=None):

    panelCut = ak.any(self.events['type']==2, axis=1)

    _, panelCut = ak.broadcast_arrays(self.events['npulses'], panelCut)

    self.events[cutName] = panelCut

    if cut:
        self.cutBranches(branches, cutName)

@mqCut
def frontAndBackRequired(self, cutName='frontAndBackRequired', areaCut=1e5, timeCut=None, cut=False, branches=None):

    frontPanelCut = ak.any((self.events['type']==1) & (self.events['layer']==-1) & (self.events['area']>areaCut), axis=1)
    backPanelCut = ak.any((self.events['type']==1) & (self.events['layer']==4) & (self.events['area']>areaCut), axis=1)

    maxFront = ak.argmax(self.events['area'][(self.events['type']==1) & (self.events['layer']==-1) & (self.events['area']>areaCut)], axis=1, keepdims=True)
    maxBack = ak.argmax(self.events['area'][(self.events['type']==1) & (self.events['layer']==4) & (self.events['area']>areaCut)], axis=1, keepdims=True)

    timesFront = ak.fill_none(self.events['timeFit_module_calibrated'][(self.events['type']==1) & (self.events['layer']==-1) & (self.events['area']>areaCut)][maxFront], 0)
    timesBack = ak.fill_none(self.events['timeFit_module_calibrated'][(self.events['type']==1) & (self.events['layer']==4) & (self.events['area']>areaCut)][maxBack], 1e10)

    timeDiff = ak.firsts(abs(timesFront-timesBack), axis=1)
    
    requireBoth = frontPanelCut & backPanelCut

    if timeCut=='beam':
        passTime = timeDiff < 15
    elif timeCut=='cosmic':
        passTime = timeDiff >=15

    if timeCut is None:
        requireBoth = requireBoth
    else:
        requireBoth = requireBoth & passTime

    _, requireBoth = ak.broadcast_arrays(self.events['npulses'], requireBoth)
    
    self.events[cutName] = requireBoth

    if cut:
        self.cutBranches(branches, cutName)

@mqCut
def beamMuonCut(self, cutName='beamMuonCut', timeCut=None, cut=False, branches=None):

    layer0Mask = (self.events['layer'] == 0) & (self.events['type']==0)
    layer1Mask = (self.events['layer'] == 1) & (self.events['type']==0)
    layer2Mask = (self.events['layer'] == 2) & (self.events['type']==0)
    layer3Mask = (self.events['layer'] == 3) & (self.events['type']==0)

    max0 = ak.argmax(self.events['area'][layer0Mask], axis=1, keepdims=True)
    max1 = ak.argmax(self.events['area'][layer1Mask], axis=1, keepdims=True)
    max2 = ak.argmax(self.events['area'][layer2Mask], axis=1, keepdims=True)
    max3 = ak.argmax(self.events['area'][layer3Mask], axis=1, keepdims=True)

    time0 = self.events['timeFit_module_calibrated'][layer0Mask][max0]
    time1 = self.events['timeFit_module_calibrated'][layer1Mask][max1]
    time2 = self.events['timeFit_module_calibrated'][layer2Mask][max2]
    time3 = self.events['timeFit_module_calibrated'][layer3Mask][max3]

    passing = ak.any(layer0Mask, axis=1) & \
                ak.any(layer1Mask, axis=1) & \
                ak.any(layer2Mask, axis=1) & \
                ak.any(layer3Mask, axis=1)

    self.events['timeDiffL30'] = time3-time0
    self.events['timeDiffL20'] = time2-time0
    self.events['timeDiffL10'] = time1-time0
    
    if timeCut is not None:
        timeMask = abs(time3-time0) < timeCut
        passing = passing & ak.any(timeMask, axis=1)
    
    #self.events['timeDiffL30'] = ak.where(passing, time3-time0, 1e10)

    passing = ak.fill_none(passing, False)
    _, passing = ak.broadcast_arrays(self.events['npulses'], passing)
    self.events[cutName] = passing

    if cut:
        self.cutBranches(branches, cutName)
    

if __name__ == "__main__":

    beam = True
    skim = True
    sim = False
    outputFile = 'beamMuonPlots/beamMuonArea_beamOff_300kDebug.root'
    qualityLevel = 'override'
    maxEvents = None
    stepSize = 20000
    makeCut = True

    #filelist = ['/eos/experiment/milliqan/sim/bar/beam/beamMuonTree_v2.root']

    '''filelist = [     
        '/eos/experiment/milliqan/skims/beam/MilliQan_Run1000_v36_beam_beamOn_medium.root',      
        '/eos/experiment/milliqan/skims/beam/MilliQan_Run1100_v36_beam_beamOn_medium.root',      
        '/eos/experiment/milliqan/skims/beam/MilliQan_Run1400_v36_beam_beamOn_medium.root',      
        '/eos/experiment/milliqan/skims/beam/MilliQan_Run1500_v36_beam_beamOn_medium.root',      
        '/eos/experiment/milliqan/skims/beam/MilliQan_Run1600_v36_beam_beamOn_medium.root',      
        '/eos/experiment/milliqan/skims/beam/MilliQan_Run1700_v36_beam_beamOn_medium.root',      
        '/eos/experiment/milliqan/skims/beam/MilliQan_Run1800_v36_beam_beamOn_medium.root',      
        '/eos/experiment/milliqan/skims/beam/MilliQan_Run1900_v36_beam_beamOn_medium.root', 
    ]'''

    filelist = [     
        '/eos/experiment/milliqan/skims/beam/MilliQan_Run1000_v36_beam_beamOff_medium.root',      
        '/eos/experiment/milliqan/skims/beam/MilliQan_Run1100_v36_beam_beamOff_medium.root', 
        '/eos/experiment/milliqan/skims/beam/MilliQan_Run1300_v36_beam_beamOff_medium.root',
        '/eos/experiment/milliqan/skims/beam/MilliQan_Run1400_v36_beam_beamOff_medium.root',      
        '/eos/experiment/milliqan/skims/beam/MilliQan_Run1500_v36_beam_beamOff_medium.root',      
        '/eos/experiment/milliqan/skims/beam/MilliQan_Run1600_v36_beam_beamOff_medium.root',      
        '/eos/experiment/milliqan/skims/beam/MilliQan_Run1700_v36_beam_beamOff_medium.root',      
        '/eos/experiment/milliqan/skims/beam/MilliQan_Run1800_v36_beam_beamOff_medium.root',      
        '/eos/experiment/milliqan/skims/beam/MilliQan_Run1900_v36_beam_beamOff_medium.root', 
    ]

    '''filelist = [     
        #'/eos/experiment/milliqan/skims/beam/MilliQan_Run1000_v35_beam_beamOn_tight.root',      
        #'/eos/experiment/milliqan/skims/beam/MilliQan_Run1100_v35_beam_beamOn_tight.root',      
        '/eos/experiment/milliqan/skims/beam/MilliQan_Run1400_v35_beam_beamOn_tight.root',      
        '/eos/experiment/milliqan/skims/beam/MilliQan_Run1500_v35_beam_beamOn_tight.root',      
        '/eos/experiment/milliqan/skims/beam/MilliQan_Run1600_v35_beam_beamOn_tight.root',      
        '/eos/experiment/milliqan/skims/beam/MilliQan_Run1700_v35_beam_beamOn_tight.root',      
        '/eos/experiment/milliqan/skims/beam/MilliQan_Run1800_v35_beam_beamOn_tight.root',      
        '/eos/experiment/milliqan/skims/beam/MilliQan_Run1900_v35_beam_beamOn_tight.root', 
    ]'''

    '''filelist = [

        '/eos/experiment/milliqan/skims/cosmic/MilliQan_Run1000_v36_cosmic_beamOff_medium.root',
        '/eos/experiment/milliqan/skims/cosmic/MilliQan_Run1100_v36_cosmic_beamOff_medium.root',
        '/eos/experiment/milliqan/skims/cosmic/MilliQan_Run1300_v36_cosmic_beamOff_medium.root',
        '/eos/experiment/milliqan/skims/cosmic/MilliQan_Run1400_v36_cosmic_beamOff_medium.root',
        '/eos/experiment/milliqan/skims/cosmic/MilliQan_Run1500_v36_cosmic_beamOff_medium.root',
        '/eos/experiment/milliqan/skims/cosmic/MilliQan_Run1600_v36_cosmic_beamOff_medium.root',
        '/eos/experiment/milliqan/skims/cosmic/MilliQan_Run1700_v36_cosmic_beamOff_medium.root',
        '/eos/experiment/milliqan/skims/cosmic/MilliQan_Run1800_v36_cosmic_beamOff_medium.root',
        '/eos/experiment/milliqan/skims/cosmic/MilliQan_Run1900_v36_cosmic_beamOff_medium.root',

    ]'''


    if skim:
        qualityLevel = 'override'

    if len(sys.argv) > 7:
        beam = (sys.argv[1] == 'True')
        skim = (sys.argv[2] == 'True')
        sim = (sys.argv[3] == 'True')
        outputFile = str(sys.argv[4])
        qualityLevel = str(sys.argv[5])
        filelist = sys.argv[6].split(',')
        if sys.argv[7] == 'None':
            maxEvents = None
        else:
            maxEvents = int(sys.argv[7])

    print("Running on files {}".format(filelist))

    goodRunsName = '/eos/experiment/milliqan/Configs/goodRunsList.json'
    lumisName = '/eos/experiment/milliqan/Configs/mqLumis.json'
    shutil.copy(goodRunsName, 'goodRunsList.json')
    shutil.copy(lumisName, 'mqLumis.json')

    #goodRuns = loadJson('goodRunsList.json')
    #lumis = loadJson('mqLumis.json')

    if skim:
        lumi, runTime = getSkimLumis(filelist)
    elif not sim:
        lumi, runTime = getLumiofFileList(filelist)
    else:
        lumi, runTime = 0, 0 #TODO scale to data 

    #define the necessary branches to run over
    branches = ['event', 'tTrigger', 'boardsMatched', 'pickupFlag', 'pickupFlagTight', 'fileNumber', 
                'runNumber', 'type', 'ipulse', 'nPE', 'chan','time_module_calibrated', 'timeFit_module_calibrated', 
                'row', 'column', 'layer', 'height', 'area', 'npulses', 'sidebandRMS', 'duration', 'riseSamples', 'fallSamples']


    #define the milliqan cuts object
    mycuts = milliqanCuts()

    setattr(milliqanCuts, "frontBackPanelInfo", frontBackPanelInfo)
    setattr(milliqanCuts, "comsicMuonCut", cosmicMuonCut)
    setattr(milliqanCuts, "comsicMuonCutHard", cosmicMuonCutHard)
    setattr(milliqanCuts, "cutStraightPulses", cutStraightPulses)
    setattr(milliqanCuts, "timeDiffBars", timeDiffBars)
    setattr(milliqanCuts, "panelRequired", panelRequired)
    setattr(milliqanCuts, "frontAndBackRequired", frontAndBackRequired)
    setattr(milliqanCuts, 'beamMuonCut', beamMuonCut)



    #require pulses are in trigger window
    centralTimeCut = getCutMod(mycuts.centralTime, mycuts, 'centralTimeCut', cut=makeCut)

    #require pulses are not pickup
    pickupCut = getCutMod(mycuts.pickupCut, mycuts, 'pickupCut', cut=makeCut, tight=True)

    #require that all digitizer boards are matched
    boardMatchCut = getCutMod(mycuts.boardsMatched, mycuts, 'boardMatchCut', cut=makeCut, branches=branches)

    #greater than or equal to one hit per layer
    hitInAllLayers = getCutMod(mycuts.oneHitPerLayerCut, mycuts, 'hitInAllLayers', cut=makeCut, multipleHits=True)

    #exactly one hit per layer
    oneHitPerLayer = getCutMod(mycuts.oneHitPerLayerCut, mycuts, 'oneHitPerLayer', cut=makeCut, multipleHits=False)

    #panel veto
    panelVeto = getCutMod(mycuts.panelVeto, mycuts, 'panelVeto', cut=makeCut, nPECut=None)
    #panelVeto = getCutMod(mycuts.panelVetoMod, mycuts, 'panelVeto', cut=makeCut, nPECut=None, areaCut=100e3, panelsAllowed=1)

    panelRequired = getCutMod(mycuts.panelRequired, mycuts, 'panelRequired', cut=makeCut)

    #first pulse max
    firstPulseMax = getCutMod(mycuts.firstPulseMax, mycuts, 'firstPulseMax', cut=makeCut)

    #veto events with an early pulse
    vetoEarlyPulse = getCutMod(mycuts.vetoEarlyPulse, mycuts, 'vetoEarlyPulse', cut=makeCut)

    #four in line cut
    #straightLineCutMod = getCutMod(mycuts.straightLineCutMod, mycuts, 'straightLineCutMod', cut=makeCut)

    #npe max-min < 10 cut
    nPEMaxMin = getCutMod(mycuts.nPEMaxMin, mycuts, 'nPEMaxMin', nPECut=20, cut=makeCut)
    #nPEMaxMin = getCutMod(mycuts.nPEStdDev, mycuts, 'nPEStdDev', std=5, cut=makeCut)

    nPEMaxCut = getCutMod(mycuts.nPEMaxCut, mycuts, 'nPEMaxCut', nPECut=20, cut=makeCut)

    #time max-min < 15 cut
    timeMaxMinNoCut = getCutMod(mycuts.timeMaxMin, mycuts, 'timeMaxMinPlot', timeCut=20)
    timeMaxMin = getCutMod(mycuts.timeMaxMin, mycuts, 'timeMaxMin', timeCut=15, cut=makeCut, straight=False)

    #veto events with large hit in front/back panels, SR1 only
    #beamMuonPanelVeto = getCutMod(mycuts.beamMuonPanelVeto, mycuts, 'beamMuonPanelVeto', cut=makeCut, nPECut=0)

    #veto front/back panel events if nPE > 50, SR2 only
    #beamMuonPanelVeto50 = getCutMod(mycuts.beamMuonPanelVeto, mycuts, 'beamMuonPanelVeto', cut=makeCut, nPECut=0)

    #require # bars in event  < cut
    nBarsCut = getCutMod(mycuts.nBarsCut, mycuts, 'nBarsCut', nBarsCut=4, cut=makeCut)

    #require < nBars within deltaT
    nBarsDeltaTCut = getCutMod(mycuts.nBarsDeltaTCut, mycuts, 'nBarsDeltaTCut', nBarsCut=4, timeCut=100, cut=makeCut)

    #sideband RMS cut
    sidebandRMSCut = getCutMod(mycuts.sidebandRMSCut, mycuts, 'sidebandRMSCut', cutVal=2, cut=makeCut)

    #use first pulse in a channel only
    firstPulseCut = getCutMod(mycuts.firstPulseCut, mycuts, 'firstPulseCut', cut=makeCut)

    #cut out all pulses except bars
    barsCut = getCutMod(mycuts.barCut, mycuts, 'barCut', cut=makeCut)

    #require a hit in front and/or back panel
    frontBackPanelRequired = getCutMod(mycuts.requireFrontBackPanel, mycuts, 'frontBackPanelRequired', cut=True)

    cosmicMuonCut = getCutMod(cosmicMuonCut, mycuts, 'cosmicMuonCut', cut=makeCut)
    cosmicMuonCutHard = getCutMod(cosmicMuonCutHard, mycuts, 'cosmicMuonCutHard', cut=makeCut)

    straightLineCut = getCutMod(mycuts.straightLineCut, mycuts, 'straightLineCut', cut=makeCut, allowedMove=False)

    #straightLineCutMod = getCutMod(mycuts.straightLineCutModWiggle, mycuts, 'straightLineCutMod', timeCut=15, cut=True, allowedMove=True)
    straightLineCutMod = getCutMod(mycuts.straightLineCutMod, mycuts, 'straightLineCutMod', restrictPaths=True, timeCut=None, cut=False, allowedMove=True)

    cutStraightPulses = getCutMod(mycuts.cutStraightPulses, mycuts, 'cutStraightPulses', cut=True)

    nPECut = getCutMod(mycuts.nPECut, mycuts, 'nPECut', nPECut=20, cut=True)
    areaCut = getCutMod(mycuts.areaCut, mycuts, 'areaCut', areaCut=300e3, barsOnly=True, cut=True)

    threeInLine = getCutMod(mycuts.threeInLine, mycuts, 'threeInLine', cut=True)

    frontAndBackRequired = getCutMod(mycuts.frontAndBackRequired, mycuts, 'frontAndBackRequired', timeCut='beam', cut=True)

    beamMuonCut = getCutMod(mycuts.beamMuonCut, mycuts, 'beamMuonCut', timeCut=15, cut=True)
    
    h_frontPanelHits = r.TH1F('h_frontPanelHits', 'Number of Front Panel Hits;# Panels;Events', 10, 0, 10)
    h_backPanelHits = r.TH1F('h_backPanelHits', 'Number of Back Panel Hits;# Panels;Events', 10, 0, 10)
    h_frontPanelNPE = r.TH1F('h_frontPanelNPE', 'nPE of Front Panel;nPE;# Pulses', 3000, 0, 6e6)
    h_frontPanelArea = r.TH1F('h_frontPanelArea', 'Area of Front;Area;# Pulses', 900, 0, 9e5)
    h_backPanelNPE = r.TH1F('h_backPanelNPE', 'nPE of Back Panel;nPE;# Pulses', 3000, 0, 6e6)
    h_backPanelArea = r.TH1F('h_backPanelArea', 'Area of Back Panel;Area;# Pulses', 900, 0, 9e5)
    h_frontPanelHeight = r.TH1F('h_frontPanelHeight', 'Height of Front Panel;Height;# Pulses', 130, 0, 1300)
    h_backPanelHeight = r.TH1F('h_backPanelHeight', 'Height of Back Panel;Height;# Pulses', 130, 0, 1300)
    h_frontPanelDuration = r.TH1F('h_frontPanelDuration', 'Duration of Front Panel;Duration (ns);# Pulses', 200, 0, 1200)
    h_backPanelDuration = r.TH1F('h_backPanelDuration', 'Duration of Back Panel;Duration (ns);# Pulses', 200, 0, 1200)
    h_frontPanelRiseSamples = r.TH1F('h_frontPanelRiseSamples', 'Rise Samples in Front Panel;Rise Samples;# Pulses', 60, 0, 60)
    h_backPanelRiseSamples = r.TH1F('h_backPanelRiseSamples', 'Rise Samples in Front Panel;Rise Samples;# Pulses', 60, 0, 60)
    h_frontPanelFallSamples = r.TH1F('h_frontPanelFallSamples', 'Fall Samples in Front Panel;Rise Samples;# Pulses', 120, 0, 120)
    h_backPanelFallSamples = r.TH1F('h_backPanelFallSamples', 'Fall Samples in Front Panel;Rise Samples;# Pulses', 120, 0, 120)
    
    h_frontPanelAreaVsHeight = r.TH2F('h_frontPanelAreaVsHeight', 'Area vs Height Front Panel;Area;Height', 900, 0, 9e5, 130, 0, 1300)
    h_backPanelAreaVsHeight = r.TH2F('h_backPanelAreaVsHeight', 'Area vs Height Back Panel;Area;Height', 900, 0, 9e5, 130, 0, 1300)
    h_frontPanelDurationVsHeight = r.TH2F('h_frontPanelDurationVsHeight', 'Duration vs Height Front Panel', 200, 0, 600, 130, 0, 1300)
    h_backPanelDurationVsHeight = r.TH2F('h_backPanelDurationVsHeight', 'Duration vs Height Back Panel', 200, 0, 600, 130, 0, 1300)
    h_timeDiffL30 = r.TH1F('h_timeDiffL30', 'Time Between Front/Back Layer', 800, -200, 200)
    h_timeDiffL20 = r.TH1F('h_timeDiffL20', 'Time Between Front/Back Layer', 800, -200, 200)
    h_timeDiffL10 = r.TH1F('h_timeDiffL10', 'Time Between Front/Back Layer', 800, -200, 200)

    h_timeDiffFront0 = r.TH1F('h_timeDiffFront0', 'Time Between Front/Back Layer', 800, -200, 200)
    h_timeDiffFront1 = r.TH1F('h_timeDiffFront1', 'Time Between Front/Back Layer', 800, -200, 200)
    h_timeDiffFront2 = r.TH1F('h_timeDiffFront2', 'Time Between Front/Back Layer', 800, -200, 200)
    h_timeDiffFront3 = r.TH1F('h_timeDiffFront3', 'Time Between Front/Back Layer', 800, -200, 200)

    h_timeDiffPanel = r.TH1F('h_timeDiffPanel', 'Time Between Front/Back Panel', 200, -200, 200)
    h_timeDiffPanelRun = r.TH2F('h_timeDiffPanelRun', 'Time Between Front/Back Panel Per Run', 400, -200, 200, 100, 1000, 2000)

    h_nPEL3 = r.TH1F('h_nPEL3', '', 500, 0, 1000)
    h_nPEFront = r.TH1F('h_nPEFront', '', 500, 0, 1000)

    h_beamMuonPerRun = r.TH1F('h_beamMuonPerRun', 'Beam Muons Per Run;Run Number;# Events', 1000, 1000, 2000)

    h_chanVsTime = r.TH2F('h_chanVsTime', 'Channel vs Time', 80, 0, 80, 2400, 0, 2400)
    h_nPEFrontPanel = r.TH1F('h_nPEFrontPanel', 'NPE Front Panel;NPE;Pulses', 75, 0, 150)
    h_nPEBackPanel = r.TH1F('h_nPEBackPanel', 'NPE Back Panel;NPE;Pulses', 75, 0, 150)
    h_nPEPanels = r.TH2F('h_nPEPanels', 'NPE of Panels;Front Panel NPE;Back Panel NPE', 76, -2, 150, 76, -2, 150)
    h_numPanels = r.TH1F('h_numPanels', 'Number of Front/Back Panels;Panels Hit;Events', 4, 0, 4)
    #define milliqan plotter
    myplotter = milliqanPlotter()
    myplotter.dict.clear()


    myplotter.addHistograms(h_frontPanelHits, 'frontHits', 'first')
    myplotter.addHistograms(h_backPanelHits, 'backHits', 'first')
    myplotter.addHistograms(h_frontPanelNPE, 'frontNPE')
    myplotter.addHistograms(h_backPanelNPE, 'backNPE')
    myplotter.addHistograms(h_frontPanelArea, 'frontArea')
    myplotter.addHistograms(h_backPanelArea, 'backArea')
    myplotter.addHistograms(h_frontPanelHeight, 'frontHeight')
    myplotter.addHistograms(h_backPanelHeight, 'backHeight')
    myplotter.addHistograms(h_frontPanelDuration, 'frontDuration')
    myplotter.addHistograms(h_backPanelDuration, 'backDuration')
    myplotter.addHistograms(h_frontPanelRiseSamples, 'frontRiseSamples')
    myplotter.addHistograms(h_backPanelRiseSamples, 'backRiseSamples')
    myplotter.addHistograms(h_frontPanelFallSamples, 'frontFallSamples')
    myplotter.addHistograms(h_backPanelFallSamples, 'backFallSamples')    
    myplotter.addHistograms(h_frontPanelAreaVsHeight, ['frontArea', 'frontHeight'])
    myplotter.addHistograms(h_backPanelAreaVsHeight, ['backArea', 'backHeight'])
    myplotter.addHistograms(h_frontPanelDurationVsHeight, ['frontDuration', 'frontHeight'])
    myplotter.addHistograms(h_backPanelDurationVsHeight, ['backDuration', 'backHeight'])
    myplotter.addHistograms(h_beamMuonPerRun, 'runNumber', 'first')
    myplotter.addHistograms(h_timeDiffL30, 'timeDiffL30')
    myplotter.addHistograms(h_timeDiffL20, 'timeDiffL20')
    myplotter.addHistograms(h_timeDiffL10, 'timeDiffL10')

    myplotter.addHistograms(h_timeDiffFront0, 'timeDiffFront0')
    myplotter.addHistograms(h_timeDiffFront1, 'timeDiffFront1')
    myplotter.addHistograms(h_timeDiffFront2, 'timeDiffFront2')
    myplotter.addHistograms(h_timeDiffFront3, 'timeDiffFront3')

    #myplotter.addHistograms(h_nPEL3, 'nPEL3')
    #myplotter.addHistograms(h_nPEFront, 'nPEFront')

    myplotter.addHistograms(h_timeDiffPanel, 'panelTimeDiff')
    #myplotter.addHistograms(h_timeDiffPanel, ['panelTimeDiff', 'runNumber'])

    myplotter.addHistograms(h_chanVsTime, ['chan', 'timeFit_module_calibrated'])
    myplotter.addHistograms(h_nPEFrontPanel, 'frontNPE')
    myplotter.addHistograms(h_nPEBackPanel, 'backNPE')
    myplotter.addHistograms(h_nPEPanels, ['frontNPE', 'backNPE'])
    myplotter.addHistograms(h_numPanels, 'nPanels')


    
    cutflow = [mycuts.totalEventCounter, 
                mycuts.fullEventCounter, 
                boardMatchCut, 
                pickupCut, 
                firstPulseCut,
                centralTimeCut,
                #frontBackPanelRequired,
                #panelVeto,
                #panelRequired,
                areaCut,
                #straightLineCut,
                #threeInLine,
                #frontAndBackRequired,
                beamMuonCut,
                #straightLineCutMod,

                #straightLineCut,
                #timeMaxMin,
                #mycuts.frontBackPanelInfo,
                mycuts.timeDiffBars,
                mycuts.panelInfo,
            ]

    for key, value in myplotter.dict.items():
        if value not in cutflow:
            print("appending", value)
            cutflow.append(value)

    #create a schedule of the cuts
    myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

    #print out the schedule
    myschedule.printSchedule()

    #create the milliqan processor object
    myiterator = milliqanProcessor(filelist, branches, myschedule, step_size=stepSize, qualityLevel=qualityLevel, max_events=maxEvents, goodRunsList=os.getcwd()+'/goodRunsList.json', sim=sim)

    #run the milliqan processor
    myiterator.run()

    myschedule.cutFlowPlots()

    #save plots
    myplotter.saveHistograms(outputFile)
    print("--------------------------------------------------------")
    print("|\033[1;34m Total run time {}s and luminosity {}pb^-1 \033[0m|".format(runTime, lumi))
    print("--------------------------------------------------------")

    mycuts.getCutflowCounts()
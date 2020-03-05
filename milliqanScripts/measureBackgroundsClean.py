import ROOT as r
import pickle
import os,re
import numpy as np
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(0)
from uncertainties import ufloat
from collections import defaultdict
from collections import OrderedDict as odict
from array import array
import pandas as pd
from progressbar import ProgressBar
import numpy as np
layersMap = {1:[0,1,24,25,8,9],2:[6,7,16,17,12,13],3:[2,3,22,23,4,5]}
allBars = [0,1,24,25,8,9,6,7,16,17,12,13,2,3,22,23,4,5]
restrictList = set([24,25,16,17,22,23])

d = os.path.dirname(os.path.abspath(__file__))
versionTag = "V16_finalForPreliminaryLimitNewSideband_addNPECorrAddMaxMin10"
inputArray = np.loadtxt(d+"/timeCalcV16_withExtraRuns.txt",delimiter=":")
timingSel = 15
tagOrig = "{0}_{1}ns".format(versionTag,timingSel)
inputArray = np.array([x for x in inputArray])
beamTime = sum(inputArray[:,1]*inputArray[:,3])
noBeamTime = sum(inputArray[:,2]*inputArray[:,4])
totalRunTime = {"beam":beamTime,"noBeam":noBeamTime}
# print (totalRunTime)
# exit()
#col,row,layer,type (xyz) 
channelSPEAreasOld = [62.,66.,77.,65.,68.,84.,70.,75.,100.,62.,85.,80.,60.,95.,65.,1.,48.,46.,80.,82.,60.,80.,118.,52.,46.,32.,60.,73.,70.,47.,75.,65.]
channelSPEAreasNew = [62.,54.,73.,55.,62.,74.,68.,69.,92.,61.,85.,80.,51.,76.,65.,1.,52.,47.,80.,82.,60.,80.,86.,40.,51.,30.,60.,73.,70.,47.,75.,65.]

npeCorrDictDataOvSim = {}
for iC in range(len(channelSPEAreasOld)):
    npeCorrDictDataOvSim[iC] = channelSPEAreasNew[iC]/channelSPEAreasOld[iC]

npeForQ1Sim = {0:5300, 1:3900, 2:4300, 3:6000, 4:4000,
            6:3300, 7:5900, 12:4700, 13:3400, 16:9000,
            8:3200, 9:6300, 17:4900, 24:7200, 25:6400,
            5:6400, 22:2300, 23:3800, 27:45, 29:25, 30:65, 19:45, 31:50, 26:50,
            10:21, 11:40, 14:24,18:300, 20:390, 21: 410, 28:190,15:1}

npeCorrDictSimOvData = {}
for x,y in npeCorrDictDataOvSim.items():
    npeCorrDictSimOvData[x] = 1./y 

#type=- bars:0, slabs:1, sheets=2
#for sheets: column is -1,0,+1 for left, top, right
#for slabs: column is 0
#For slabs/sheets: row is redundant with type (= -1*type) 
chanMap =[[1,3,1,0], #0.0
    [2,3,1,0], #0.1
    [1,3,3,0], #0.2
    [2,3,3,0], #0.3
    [1,1,3,0], #0.4
    [2,1,3,0], #0.5
    [1,3,2,0], #0.6
    [2,3,2,0], #0.7
    [1,1,1,0], #0.8
    [2,1,1,0], #0.9
    [0,-2,1,2], #0.10
    [0,-2,2,2], #0.11
    [1,1,2,0], #0.12
    [2,1,2,0], #0.13
    [0,-2,3,2], #0.14 
    [0,0,0,3], #0.15, timing card
    [1,2,2,0], #1.0
    [2,2,2,0], #1.1
    [0,-1,0,1], #1.2
    [1,-2,2,2], #1.3
    [0,-1,1,1], #1.4
    [0,-1,3,1], #1.5
    [1,2,3,0], #1.6
    [2,2,3,0], #1.7
    [1,2,1,0], #1.8
    [2,2,1,0], #1.9
    [1,-2,3,2], #1.10
    [-1,-2,1,2], #1.11
    [0,-1,2,1], #1.12
    [1,-2,1,2], #1.13
    [-1,-2,2,2], #1.14
    [-1,-2,3,2] #1.15
];
extraPathsLists = [[7,12,2],[3,5,1],[0,8,7]]
extraPaths = []
# for path in extraPathsLists:
#     extraPaths.append(tuple(sorted(path)))

# binsNPE = array('d',[0]+np.logspace(0.1,3,6))
binsNPE = array('d',[0,0.5,1.5,5,10,20,50,100,1000,10000])
binsQ = array('d',[0,0.001,0.01,0.02,0.05,0.1,0.2,1])
binsDeltaT = array('d',np.linspace(-120,120,385))
binsNumAfter = array('d',range(11))

firstNPEVsNumAfterPulsesWithSlab = r.TH2D("firstNPEVsNumAfterWithSlab",";firstNPE;num after",len(binsNPE)-1,binsNPE,len(binsNumAfter)-1,binsNumAfter)
minNPEVsMaxNPEWithSlab = r.TH2D("minNPEVsMaxNPEWithSlab",";minNPE; maxNPE",len(binsNPE)-1,binsNPE,len(binsNPE)-1,binsNPE)
minQVsMaxQWithSlab = r.TH2D("minQVsMaxQWithSlab",";minQ; maxQ",100,0,1,100,0,1)
minNPEVsMaxNPECorrWithSlab = r.TH2D("minNPEVsMaxNPECorrWithSlab",";minNPE; maxNPE",len(binsNPE)-1,binsNPE,len(binsNPE)-1,binsNPE)
chanVsNumAfterPulsesWithSlab = r.TH2D("chanVsNumAfterWithSlab",";chan;num after",32,0,32,10,0,10)
chanVsNPEWithSlab = r.TH2D("chanVsNPEWithSlab",";chan;NPE",32,0,32,len(binsNPE)-1,binsNPE)
chanVsNPECorrWithSlab = r.TH2D("chanVsNPECorrWithSlab",";chan;NPE",32,0,32,len(binsNPE)-1,binsNPE)
firstPulseTimeWithSlab = r.TH1D("firstPulseTimeWithSlab",";time;",240,0,600)
chanMultWithSlab = r.TH1D("chanMultWithSlab",";chan;",32,0,32)
chanMultNoAfterWithSlab = r.TH1D("chanMultNoAfterWithSlab",";chan;",32,0,32)
chanVsQWithSlab = r.TH2D("chanVsQWithSlab",";chan;Q",32,0,32,100,0,1)

firstNPEVsNumAfterPulses = r.TH2D("firstNPEVsNumAfter",";firstNPE;num after",len(binsNPE)-1,binsNPE,len(binsNumAfter)-1,binsNumAfter)
minNPEVsMaxNPE = r.TH2D("minNPEVsMaxNPE",";minNPE; maxNPE",len(binsNPE)-1,binsNPE,len(binsNPE)-1,binsNPE)
minNPEVsMaxNPECorr = r.TH2D("minNPEVsMaxNPECorr",";minNPE; maxNPE",len(binsNPE)-1,binsNPE,len(binsNPE)-1,binsNPE)
minQVsMaxQ = r.TH2D("minQVsMaxQ",";minQ; maxQ",100,0,1,100,0,1)
chanVsNumAfterPulses = r.TH2D("chanVsNumAfter",";chan;num after",32,0,32,10,0,10)
chanVsNPE = r.TH2D("chanVsNPE",";chan;NPE",32,0,32,len(binsNPE)-1,binsNPE)
chanVsNPECorr = r.TH2D("chanVsNPECorr",";chan;NPE",32,0,32,len(binsNPE)-1,binsNPE)
firstPulseTime = r.TH1D("firstPulseTime",";time;",240,0,600)
chanMult = r.TH1D("chanMult",";chan;",32,0,32)
chanMultNoAfter = r.TH1D("chanMultNoAfter",";chan;",32,0,32)
chanVsQ = r.TH2D("chanVsQ",";chan;Q",32,0,32,100,0,1)

afterPulseTimeSinceFirstPulseWithSlab = {}
afterPulseTimeSinceFirstPulse = {}

for chan in range(32):
    if chanMap[chan][-1] != 2:
        afterPulseTimeSinceFirstPulseWithSlab[chan] = r.TH1D("timeSinceFirstPulseWithSlab_chan{0}".format(chan),"time diff",100,0,500)
        afterPulseTimeSinceFirstPulse[chan] = r.TH1D("timeSinceFirstPulse_chan{0}".format(chan),"time diff",100,0,500)
def preparePaths(badChans = [6,4],slabs=[18,20,28]):
    slabs = tuple(sorted(slabs))
    paths = []
    straight = []
    badStraight = []
    noBadStraight = []
    bentDiffDigi = []
    bentSameDigi = []
    badBentSameDigi = []
    noBadBentSameDigi = []
    straightPlusSlab = []
    straightPlusTwoSlab = []
    straightPlusThreeSlab = []
    straightPlusFourSlab = []
    badStraightPlusSlab = []
    noBadStraightPlusSlab = []
    bentDiffDigiPlusSlab = []
    bentSameDigiPlusSlab = []
    badBentSameDigiPlusSlab = []
    noBadBentSameDigiPlusSlab = []
    straightPlusTwoOrMoreSlabs = []
    badStraightPlusTwoOrMoreSlabs = []
    noBadStraightPlusTwoOrMoreSlabs = []
    bentSameDigiPlusTwoOrMoreSlabs = []
    badBentSameDigiPlusTwoOrMoreSlabs = []
    noBadBentSameDigiPlusTwoOrMoreSlabs = []
    bentDiffDigiPlusTwoOrMoreSlabs = []
    slabPaths = {}
    for iC1,chan1 in enumerate(layersMap[1]):
        for iC2,chan2 in enumerate(layersMap[2]):
            for iC3,chan3 in enumerate(layersMap[3]):
                path = tuple(sorted(set([chan1,chan2,chan3])))
                pathPlusSlab1 = tuple(sorted(set([18,chan1,chan2,chan3])))
                pathPlusSlab2 = tuple(sorted(set([21,chan1,chan2,chan3])))
                pathPlusSlab3 = tuple(sorted(set([28,chan1,chan2,chan3])))
                pathPlusSlab4 = tuple(sorted(set([20,chan1,chan2,chan3])))
                pathsPlus2Slab = []
                pathsPlus3Slab = []
                pathsPlus4Slab = []
                pathsPlus4Slab.append(tuple(sorted(set([18,20,21,28,chan1,chan2,chan3]))))
                pathsPlus1Slab = []
                # pathsPlus1Slab.append(pathPlusSlab1)
                # pathsPlus1Slab.append(pathPlusSlab2)
                # pathsPlus1Slab.append(pathPlusSlab3)
                # pathsPlus1Slab.append(pathPlusSlab4)
                for ix,x in enumerate([18,21,28,20]):
                    for iy,y in enumerate([18,21,28,20]):
                        if ix < iy:
                            pathsPlus2Slab.append(tuple(sorted(set([x,y,chan1,chan2,chan3]))))
                        for iz,z in enumerate([18,21,28,20]):
                            if ix < iy:
                                if iz < ix:
                                    pathsPlus3Slab.append(tuple(sorted(set([x,y,z,chan1,chan2,chan3]))))
                paths.append(path)
                paths.append(pathPlusSlab1)
                paths.append(pathPlusSlab2)
                paths.append(pathPlusSlab3)
                paths.append(pathPlusSlab4)
                paths.extend(pathsPlus2Slab)
                paths.extend(pathsPlus3Slab)
                paths.extend(pathsPlus4Slab)
                if iC1 == iC2 and iC2 == iC3:
                    straight.append(path)
                    straightPlusSlab.append(pathPlusSlab1)
                    straightPlusSlab.append(pathPlusSlab2)
                    straightPlusSlab.append(pathPlusSlab3)
                    straightPlusSlab.append(pathPlusSlab4)
                    straightPlusTwoSlab.extend(pathsPlus2Slab)
                    straightPlusThreeSlab.extend(pathsPlus3Slab)
                    straightPlusFourSlab.extend(pathsPlus4Slab)

                    straightPlusTwoOrMoreSlabs.extend(pathsPlus1Slab+pathsPlus2Slab+pathsPlus3Slab+pathsPlus4Slab)
                    if chan1 in badChans or chan2 in badChans or chan3 in badChans:
                        badStraight.append(path)
                        badStraightPlusSlab.append(pathPlusSlab1)
                        badStraightPlusSlab.append(pathPlusSlab2)
                        badStraightPlusSlab.append(pathPlusSlab3)
                        badStraightPlusSlab.append(pathPlusSlab4)
                        badStraightPlusTwoOrMoreSlabs.extend(pathsPlus1Slab+pathsPlus2Slab+pathsPlus3Slab+pathsPlus4Slab)
                    else:
                        noBadStraight.append(path)
                        noBadStraightPlusSlab.append(pathPlusSlab1)
                        noBadStraightPlusSlab.append(pathPlusSlab2)
                        noBadStraightPlusSlab.append(pathPlusSlab3)
                        noBadStraightPlusSlab.append(pathPlusSlab4)
                        noBadStraightPlusTwoOrMoreSlabs.extend(pathsPlus1Slab+pathsPlus2Slab+pathsPlus3Slab+pathsPlus4Slab)
                else:
                    if int(chan1/16) == int(chan2/16) and int(chan2/16) == int(chan3/16):
                        bentSameDigi.append(path)
                        bentSameDigiPlusSlab.append(pathPlusSlab1)
                        bentSameDigiPlusSlab.append(pathPlusSlab2)
                        bentSameDigiPlusSlab.append(pathPlusSlab3)
                        bentSameDigiPlusSlab.append(pathPlusSlab4)
                        bentSameDigiPlusTwoOrMoreSlabs.extend(pathsPlus1Slab+pathsPlus2Slab+pathsPlus3Slab+pathsPlus4Slab)
                        if chan1 in badChans or chan2 in badChans or chan3 in badChans:
                            badBentSameDigi.append(path)
                            badBentSameDigiPlusSlab.append(pathPlusSlab1)
                            badBentSameDigiPlusSlab.append(pathPlusSlab2)
                            badBentSameDigiPlusSlab.append(pathPlusSlab3)
                            badBentSameDigiPlusSlab.append(pathPlusSlab4)
                            badBentSameDigiPlusTwoOrMoreSlabs.extend(pathsPlus1Slab+pathsPlus2Slab+pathsPlus3Slab+pathsPlus4Slab)
                        else:
                            noBadBentSameDigi.append(path)
                            noBadBentSameDigiPlusSlab.append(pathPlusSlab1)
                            noBadBentSameDigiPlusSlab.append(pathPlusSlab2)
                            noBadBentSameDigiPlusSlab.append(pathPlusSlab3)
                            noBadBentSameDigiPlusSlab.append(pathPlusSlab4)
                            noBadBentSameDigiPlusTwoOrMoreSlabs.extend(pathsPlus1Slab+pathsPlus2Slab+pathsPlus3Slab+pathsPlus4Slab)
                    else:
                        bentDiffDigi.append(path)
                        bentDiffDigiPlusSlab.append(pathPlusSlab1)
                        bentDiffDigiPlusSlab.append(pathPlusSlab2)
                        bentDiffDigiPlusSlab.append(pathPlusSlab3)
                        bentDiffDigiPlusSlab.append(pathPlusSlab4)
                        bentDiffDigiPlusTwoOrMoreSlabs.extend(pathsPlus1Slab+pathsPlus2Slab+pathsPlus3Slab+pathsPlus4Slab)
    # paths.extend(extraPaths)
    # paths.append(slabs)
    allPaths={"Straight1":[(0,2,6)],"Straight2":[(1,3,7)],"Straight3":[(16,22,24)],"Straight4":[(17,23,25)],"Straight5":[(4,8,12)],"Straight6":[(5,9,13)],"Straight":straight,"badStraight":badStraight,"noBadStraight":noBadStraight,"BentSameDigi":bentSameDigi,
            "badBentSameDigi":badBentSameDigi,"noBadBentSameDigi":noBadBentSameDigi,"BentDiffDigi":bentDiffDigi,"Slabs":[slabs],"ExtraPaths":extraPaths,
            "StraightPlusSlab":straightPlusSlab,"StraightPlusTwoSlab":straightPlusTwoSlab,"StraightPlusThreeSlab":straightPlusThreeSlab,"StraightPlusFourSlab":straightPlusFourSlab,"badStraightPlusSlab":badStraightPlusSlab,"noBadStraightPlusSlab":noBadStraightPlusSlab,"BentSameDigiPlusSlab":bentSameDigiPlusSlab,
            "badBentSameDigiPlusSlab":badBentSameDigiPlusSlab,"noBadBentSameDigiPlusSlab":noBadBentSameDigiPlusSlab,"BentDiffDigi":bentDiffDigiPlusSlab,"Slabs":[slabs],"ExtraPaths":extraPaths,
            "StraightPlusTwoOrMoreSlabs":straightPlusTwoOrMoreSlabs,"badStraightPlusTwoOrMoreSlabs":badStraightPlusTwoOrMoreSlabs,"noBadStraightPlusTwoOrMoreSlabs":noBadStraightPlusTwoOrMoreSlabs,"BentSameDigiPlusTwoOrMoreSlabs":bentSameDigiPlusTwoOrMoreSlabs,
            "badBentSameDigiPlusTwoOrMoreSlabs":badBentSameDigiPlusTwoOrMoreSlabs,"noBadBentSameDigiPlusTwoOrMoreSlabs":noBadBentSameDigiPlusTwoOrMoreSlabs,"BentDiffDigi":bentDiffDigiPlusTwoOrMoreSlabs}
    return allPaths,paths
def measureBackgrounds(inputFile,blind,beamString,useSaved,nPEStrings,deltaTStrings,selections,slabs,signal):
    npeCorrDict = {}
    for x in npeCorrDictSimOvData:
        if not signal:
            npeCorrDict[x] = npeCorrDictSimOvData[x]
        else:
            npeCorrDict[x] = 1
    for x in npeCorrDictSimOvData:
        npeCorrDict[x] = npeCorrDict[x]/(npeForQ1Sim[x])
    allPaths,paths = preparePaths(slabs=slabs)
    tree = inputFile.Get("t")
    nTot = 0
    nPassQuiet = 0
    nPassMaxMin = 0
    nPassCosmic = 0
    nPassSidebandRMS = 0
    nPassStraightPath = 0
    nPassStraightPlusSlabPath = 0
    nPassStraightPlusTwoOrMoreSlabsPath = 0
    nPassOnePulse = 0
    nPassPulseTimeSelection = 0
    nPassTiming = 0
    nPassMaxNPE = 0
    beamReq = False
    totalEffsPerPath = {}
    numVsRunBent = r.TH1D("numVsRunBent",";run;",500,1000,1500)
    rateVsRunBent = r.TH1D("rateVsRunBent",";run;",500,1000,1500)
    numVsRunBentNPE10 = r.TH1D("numVsRunBentNPE10",";run;",500,1000,1500)
    rateVsRunBentNPE10 = r.TH1D("rateVsRunBentNPE10",";run;",500,1000,1500)
    runTimeDict = {}
    runTimeDict[1] = 1
    for entry in inputArray:
        if beamString == "beam":
            runTimeDict[entry[0]] = entry[1]*entry[3]/3600.
        else:
            runTimeDict[entry[0]] = entry[2]*entry[4]/3600.
    for path in range(-1,2*(len(allPaths["Straight"]))):
        if path == -1:
            totalEffsPerPath[path] = r.TH1D("pathTupleAll",";nPE;",len(binsNPE)-1,binsNPE)
        elif path < (len(allPaths["Straight"])):
            totalEffsPerPath[path] = r.TH1D("pathTuple"+"_".join(str(x) for x in allPaths["Straight"][path]),";nPE;",len(binsNPE)-1,binsNPE)
        else:
            totalEffsPerPath[path] = r.TH1D("pathTuplePlusTwoOrMoreSlabs"+"_".join(str(x) for x in allPaths["Straight"][path-(len(allPaths["Straight"]))]),";nPE;",len(binsNPE)-1,binsNPE)
    totalEffsPerPath["Straight"] = r.TH1D("pathTupleStraight",";nPE;",len(binsNPE)-1,binsNPE)
    totalEffsPerPath["StraightPlusTwoOrMoreSlabs"] = r.TH1D("pathTupleStraightPlusTwoOrMoreSlabs",";nPE;",len(binsNPE)-1,binsNPE)
    totalEffsPerPath["StraightPlusSlab"] = r.TH1D("pathTupleStraightPlusSlab",";nPE;",len(binsNPE)-1,binsNPE)
    if beamString == "beam":
        beamReq = True
    if useSaved:
        recreate = ""
    else:
        recreate = "RECREATE"
    if blind:
        outputFile = r.TFile("{0}backgroundMeasurementsBlind{1}.root".format(beamString,tag),recreate)
    else:
        outputFile = r.TFile("{0}backgroundMeasurements{1}.root".format(beamString,tag),recreate)
    outputPlots = defaultdict(dict)
    if useSaved:
        return outputFile,allPaths
    maxPathLength = max(len(x) for x in paths)
    for sel in selections:
        for path in paths+list(allPaths.keys()):
            if type(path) == str:
                pathString = path
            else:
                pathString = "_".join(str(x) for x in path)
            for deltaT in deltaTStrings:
                for nPE in nPEStrings:
                    outputPlots[nPE+"Vs"+deltaT+sel][path] = r.TH2D(pathString+"_"+nPE+"_"+deltaT+sel,";nPE;deltaT",len(binsNPE)-1,binsNPE,len(binsDeltaT)-1,binsDeltaT)

    nEvents = tree.GetEntries()
    extraPathsSet = [set(extraPath) for extraPath in allPaths["ExtraPaths"]]
    pbar = ProgressBar()
    for iE in pbar(range(nEvents)):
    # for iE in range(nEvents):
        tree.GetEntry(iE)
        if not signal:
            if tree.groupTDC_b0[0] != tree.groupTDC_b1[0]:
                continue
            if tree.beam != beamReq:
                continue
            if tree.run == 1395:
                continue
        # if (tree.beam and tree.t_since_fill_start > 7200): 
        #     continue
        # if (tree.hardNoBeam and (tree.t_until_next_fill < 3600 or tree.t_until_next_fill > 10800)):
        #     continue
        # if (not tree.beam and not tree.hardNoBeam):
        #     continue
        layers = []
        types = []
        chans = []
        durations = []
        time_module_calibrateds = []
        nPEs = []
        nPECorrs = []
        Qs = []
        panelPresent = False
        for iC,chan in enumerate(tree.chan):
            if chan == 15: continue
            if chanMap[chan][3] == 2:
                panelPresent = True
                continue
            layers.append(chanMap[chan][2])
            types.append(chanMap[chan][3])
            chans.append(tree.chan[iC])
            durations.append(tree.duration[iC])
            time_module_calibrateds.append(tree.time_module_calibrated[iC])
            nPEs.append(tree.nPE[iC])
            if chanMap[chan][3] == 2:
                nPECorrs.append(tree.nPE[iC])
                Qs.append(-1.0)
            else:
                if chanMap[chan][3] == 0:
                    nPECorrs.append(tree.nPE[iC]*npeCorrDict[tree.chan[iC]]*5000)
                else:
                    nPECorrs.append(tree.nPE[iC]*npeCorrDict[tree.chan[iC]]*400)
                if tree.nPE[iC] > 0:
                    Qs.append((tree.nPE[iC]*npeCorrDict[tree.chan[iC]])**0.5)
                else:
                    Qs.append(0)
        nTot += 1
        chansHit = set(chans)
        # if len(chansHit & restrictList) == 0: continue
        if 15 in chansHit:
            chansHit.remove(15)
        #Only N chans hit
        if len(chansHit) > maxPathLength: continue
        #chans hit in paths
        chanSet = tuple(sorted(set(chans)))
        if chanSet not in paths:
            continue
        nPassQuiet += tree.scale1fb*37
        #No noisy RMS
        sideband_RMS = list(tree.sideband_RMS)
        sideband_RMS = sideband_RMS[:15]+sideband_RMS[16:]
        if max(sideband_RMS) > 1.3: continue
        nPassSidebandRMS += tree.scale1fb*37
        #Max pulses
        pulses = {1:[],2:[],3:[]}
        failCosmic = False
        # if len(chanSet) == 4:
        #     pulses[0] = []
        if (chansHit == set(slabs)):
            #Slabs are offset by 1
            for nPE,nPECorr,Q,time,layer,chan,duration in zip(nPEs,nPECorrs,Qs,time_module_calibrateds,layers,chan,durations):
                pulses[layer+1].append([nPE,time,chan,nPECorr,Q])
        elif len(chansHit) == 3:
            #Only bars hit
            if 1 in types or 2 in types: continue
            #Hit in each layer
            if set(list(layers)) != set([1,2,3]): continue
            for nPE,nPECorr,Q,time,layer,chan,duration in zip(nPEs,nPECorrs,Qs,time_module_calibrateds,layers,chans,durations):
                pulses[layer].append([nPE,time,chan,nPECorr,Q])
        elif len(chansHit) >= 4:
            #bars hit + N slab
            if 2 in types: continue
            #Hit in each layer
            layers4Slab = []
            for nPE,nPECorr,Q,time,layer,chan,duration,typeC in zip(nPEs,nPECorrs,Qs,time_module_calibrateds,layers,chans,durations,types):
                if chan in [18,20,21] and nPE > 300: 
                    failCosmic= True
                elif chan == 28 and nPE > 200: 
                    failCosmic= True

                if chan in [18,20,21,28]: layerT = chan
                else: 
                    layerT = layer
                    layers4Slab.append(layerT)
                if layerT not in pulses:
                    pulses[layerT] = []
                pulses[layerT].append([nPE,time,chan,nPECorr,Q])
            if set(layers4Slab) != set([1,2,3]): continue
        elif any(chansHit == extraPathSet for extraPathSet in extraPathsSet):
            extraPathIndex = extraPathsSet.index(chansHit)
            for nPE,nPECorrs,Qs,time,chan,duration in zip(nPEs,nPECorrs,Qs,time_module_calibrateds,chans,durations):
                pulses[allPaths["ExtraPaths"][extraPathIndex].index(chan)+1].append([nPE,nPECorrs,Qs,time,chan])

        # elif len(chansHit) == 4:
        #     #bars hit + 1 slab
        #     if 2 in types: continue
        #     #Hit in each layer
        #     layers4Slab = []
        #     for nPE,time,layer,chan,duration in zip(tree.nPE,tree.time_module_calibrated,layers,tree.chan,tree.duration):
        #         if chan in [18,20,21,28]: layerT = 0
        #         else: layerT = layer
        #         pulses[layerT].append([nPE,time,chan])
        #         layers4Slab.append(layerT)
        #     if set(layers4Slab) != set([0,1,2,3]): continue
        # for nPE,time,layer,chan in zip(tree.nPE,tree.time,layers,tree.chan):
        #Check first pulse is maximal
        if failCosmic: 
            continue
        nPassCosmic += tree.scale1fb*37
        singlePulse = True
        failAllSelection = False
        failPulseTimeSelection = False
        for layer,pulsesList in pulses.items():
            if pulsesList[0][1] < 300 or pulsesList[0][1] > 440:
                failPulseTimeSelection = True
                break
            if len(pulsesList) == 0: 
                failAllSelection = True
                break
            if len(pulsesList) != 1:
                singlePulse = False
            if pulsesList[0] != max(pulsesList):
                failAllSelection = True
                break
        if failAllSelection: continue
        nPassOnePulse += tree.scale1fb*37
        if failPulseTimeSelection: continue
        nPassPulseTimeSelection += tree.scale1fb*37
        selsOrig = ["NoPrePulse"]
        if singlePulse:
            selsOrig.append("NoOtherPulse")
        sels = []
        if panelPresent:
            for sel in selsOrig:
                sel += "PlusPanelHit"
                sels.append(sel)
        else:
            sels = selsOrig

        # chanSet = tuple(sorted(set(chans)))
        allDeltaTs = []
        if len(pulses) == 3:
            minNPE = min([pulses[1][0][0],pulses[2][0][0],pulses[3][0][0]])
            maxNPE = max([pulses[1][0][0],pulses[2][0][0],pulses[3][0][0]])
            minNPECorr = min([pulses[1][0][3],pulses[2][0][3],pulses[3][0][3]])
            maxNPECorr = max([pulses[1][0][3],pulses[2][0][3],pulses[3][0][3]])
            minQ = min([pulses[1][0][4],pulses[2][0][4],pulses[3][0][4]])
            maxQ = max([pulses[1][0][4],pulses[2][0][4],pulses[3][0][4]])

            deltaTL3L1 = pulses[3][0][1] - pulses[1][0][1]
            deltaTL3L2 = pulses[3][0][1] - pulses[2][0][1]
            deltaTL2L1 = pulses[2][0][1] - pulses[1][0][1]
            allDeltaTs = [deltaTL3L1,deltaTL3L2,deltaTL2L1]
        elif len(pulses) >= 4:
            # minNPE = min([pulses[1][0][0],pulses[2][0][0],pulses[3][0][0],pulses[0][0][0]])
            # maxNPE = max([pulses[1][0][0],pulses[2][0][0],pulses[3][0][0],pulses[0][0][0]])
            minNPE = min([pulses[1][0][0],pulses[2][0][0],pulses[3][0][0]])
            maxNPE = max([pulses[1][0][0],pulses[2][0][0],pulses[3][0][0]])#,pulses[0][0][0]])
            minNPECorr = min([pulses[1][0][3],pulses[2][0][3],pulses[3][0][3]])
            maxNPECorr = max([pulses[1][0][3],pulses[2][0][3],pulses[3][0][3]])
            minQ = min([pulses[1][0][4],pulses[2][0][4],pulses[3][0][4]])
            maxQ = max([pulses[1][0][4],pulses[2][0][4],pulses[3][0][4]])

            deltaTL3L1 = pulses[3][0][1] - pulses[1][0][1]
            deltaTL3L2 = pulses[3][0][1] - pulses[2][0][1]
            deltaTL2L1 = pulses[2][0][1] - pulses[1][0][1]

            # deltaTL3L0 = pulses[3][0][1] - pulses[0][0][1]
            # deltaTL2L0 = pulses[2][0][1] - pulses[0][0][1]
            # deltaTL1L0 = pulses[1][0][1] - pulses[0][0][1]
            # allDeltaTs = [deltaTL3L1,deltaTL3L2,deltaTL2L1,deltaTL3L0,deltaTL2L0,deltaTL1L0]
            allDeltaTs = [deltaTL3L1,deltaTL3L2,deltaTL2L1]#,deltaTL3L0,deltaTL2L0,deltaTL1L0]

        minDeltaT = min(allDeltaTs,key = lambda x:abs(x))
        maxDeltaT = max(allDeltaTs,key = lambda x:abs(x))
        if blind:
            if tuple(sorted(list(chanSet))) in allPaths["Straight"] or tuple(sorted(list(chanSet))) in allPaths["StraightPlusSlab"] or tuple(sorted(list(chanSet))) in allPaths["StraightPlusTwoOrMoreSlabs"]:
                if abs(maxDeltaT) < timingSel: continue
                if abs(abs(maxDeltaT/timingSel) - 1) < 0.01: continue

        if not signal:
            tree.scale1fb = 1./37.
        if abs(maxDeltaT) < 100 and not panelPresent:
            if tuple(sorted(list(chanSet))) in (allPaths["BentSameDigi"]+allPaths["Straight"]+allPaths["BentSameDigiPlusTwoOrMoreSlabs"]+allPaths["StraightPlusTwoOrMoreSlabs"]):
                #npe,time,chan
                if len(pulses) >= 4:
                    for layer,pulseList in pulses.items():
                        chanVsNumAfterPulsesWithSlab.Fill(pulseList[0][2],len(pulseList)-1)
                        chanMultWithSlab.Fill(pulseList[0][2])
                        firstPulseTimeWithSlab.Fill(pulseList[0][1])
                        if len(sels) == 2:
                            chanMultNoAfterWithSlab.Fill(pulseList[0][2])
                        firstNPEVsNumAfterPulsesWithSlab.Fill(pulseList[0][0],len(pulseList)-1)
                        for pulse in pulseList[1:]:
                            afterPulseTimeSinceFirstPulseWithSlab[pulseList[0][2]].Fill(pulse[1]-pulseList[0][1])
                        chanVsNPEWithSlab.Fill(pulseList[0][2],pulseList[0][0])
                        chanVsNPECorrWithSlab.Fill(pulseList[0][2],pulseList[0][3])
                        chanVsQWithSlab.Fill(pulseList[0][2],pulseList[0][4])
                    minNPEVsMaxNPEWithSlab.Fill(minNPE,maxNPE)
                    minNPEVsMaxNPECorrWithSlab.Fill(minNPECorr,maxNPECorr)
                    minQVsMaxQWithSlab.Fill(minQ,maxQ)
                elif len(pulses) == 3:
                    for layer,pulseList in pulses.items():
                        chanVsNumAfterPulses.Fill(pulseList[0][2],len(pulseList)-1)
                        chanMult.Fill(pulseList[0][2])
                        firstPulseTime.Fill(pulseList[0][1])
                        if len(sels) == 2:
                            chanMultNoAfter.Fill(pulseList[0][2])
                        firstNPEVsNumAfterPulses.Fill(pulseList[0][0],len(pulseList)-1)
                        for pulse in pulseList[1:]:
                            afterPulseTimeSinceFirstPulse[pulseList[0][2]].Fill(pulse[1]-pulseList[0][1])
                        chanVsNPE.Fill(pulseList[0][2],pulseList[0][0])
                        chanVsNPECorr.Fill(pulseList[0][2],pulseList[0][3])
                        chanVsQ.Fill(pulseList[0][2],pulseList[0][4])
                    minNPEVsMaxNPE.Fill(minNPE,maxNPE)
                    minNPEVsMaxNPECorr.Fill(minNPECorr,maxNPECorr)
                    minQVsMaxQ.Fill(minQ,maxQ)
        if tuple(sorted(list(chanSet))) in allPaths["BentSameDigi"]:
            if (abs(maxDeltaT) < 100 and len(sels) == 2 and not panelPresent) :
                numVsRunBent.Fill(tree.run)
                rateVsRunBent.Fill(tree.run,1./runTimeDict[tree.run])
                if minNPE > 10:
                    numVsRunBentNPE10.Fill(tree.run)
                    rateVsRunBentNPE10.Fill(tree.run,1./runTimeDict[tree.run])
        # if maxNPE > 10 and (maxNPE/minNPE) > 3: continue
        # if (maxNPE-minNPE)/((minNPE + maxNPE)**0.5) > 3: continue
        if maxNPECorr/minNPECorr > 10: 
            continue
        nPassMaxMin += tree.scale1fb*37
        if (abs(maxDeltaT) < timingSel or abs(abs(maxDeltaT/timingSel) - 1) < 0.01) and not panelPresent:
            if not (abs(maxDeltaT/timingSel - 1) < 0.01):
                nPassTiming += tree.scale1fb*37
            # if True:
                if len(sels) > 0:
                    if tuple(sorted(list(chanSet))) in allPaths["Straight"]:
                        chanSetBars = [x for x in chanSet if x in allBars]
                        pathIndex = allPaths["Straight"].index(tuple(sorted(list(chanSetBars))))
                        nPassStraightPath += tree.scale1fb*37.
                            #skip npe for now
                        totalEffsPerPath[pathIndex].Fill(minNPECorr)
                        totalEffsPerPath["Straight"].Fill(minNPECorr,tree.scale1fb*37.)
                        totalEffsPerPath[-1].Fill(minNPECorr)
                    if tuple(sorted(list(chanSet))) in allPaths["StraightPlusSlab"]:
                        totalEffsPerPath["StraightPlusSlab"].Fill(minNPECorr,tree.scale1fb*37.)
                        nPassStraightPlusSlabPath += tree.scale1fb*37.
                        chanSetBars = [x for x in chanSet if x in allBars]
                        pathIndex = 6+allPaths["Straight"].index(tuple(sorted(list(chanSetBars))))
                        totalEffsPerPath[pathIndex].Fill(minNPECorr)
                    if tuple(sorted(list(chanSet))) in allPaths["StraightPlusTwoOrMoreSlabs"]:
                        totalEffsPerPath["StraightPlusTwoOrMoreSlabs"].Fill(minNPECorr,tree.scale1fb*37.)
                        nPassStraightPlusTwoOrMoreSlabsPath += tree.scale1fb*37.
                        # if maxNPE < 100:
                        #     nPassMaxNPE += 1
                        # if maxNPE/minNPE > 2: 
                        #     nPassMaxNPE += 1
                        #     continue

        # if maxNPE > 100: continue
        # if minNPE > binsNPE[-1]: continue
        # if abs(maxDeltaT) < timingSel:
        #     if len(pulses) == 4 and singlePulse:
        #         if tuple(sorted(list(chanSet))) in allPaths["StraightPlusSlab"]:
        #             print( "s",chanSet,tree.run,tree.file,tree.event,maxNPE
        #         elif tuple(sorted(list(chanSet))) in allPaths["BentSameDigiPlusSlab"]:
        #             print( "b",chanSet,tree.run,tree.file,tree.event,maxNPE
        nPEDict = {"NPEMin":minNPE,"NPEMax":maxNPE,"NPEMinCorr":minNPECorr,"NPEMaxCorr":maxNPECorr}
        deltaTDict = {"max":maxDeltaT}
        # deltaTDict = {"min":minDeltaT,"max":maxDeltaT}
        for sel in sels:
            for deltaTString in deltaTStrings:
                for nPEString in nPEStrings:
                    # if nPEDict[nPEString.replace("Min","Max")]/nPEDict[nPEString.replace("Max","Min")] < 5:
                    outputPlots[nPEString+"Vs"+deltaTString+sel][chanSet].Fill(nPEDict[nPEString],deltaTDict[deltaTString])

        #Check time distributions
        # if abs(pulses[3][0][1] - pulses[1][0][1]) > 30: continue
        # if abs(pulses[2][0][1] - pulses[1][0][1]) > 20: continue


    outputFile.cd()
    numVsRunBent.Write()
    rateVsRunBent.Write()
    numVsRunBentNPE10.Write()
    rateVsRunBentNPE10.Write()
    outDirNoS = outputFile.mkdir("noSlab")
    outDirNoS.cd()
    chanMult.Write()
    chanMultNoAfter.Write()
    minNPEVsMaxNPE.Write()
    minQVsMaxQ.Write()
    minNPEVsMaxNPECorr.Write()
    firstNPEVsNumAfterPulses.Write()
    firstPulseTime.Write()
    chanVsNumAfterPulses.Write()
    chanVsNPE.Write()
    chanVsNPECorr.Write()
    chanVsQ.Write()
    outDir = outDirNoS.mkdir("afterPulseTimeSinceFirst")
    outDir.cd()
    for chan in afterPulseTimeSinceFirstPulse:
        afterPulseTimeSinceFirstPulse[chan].Write()
    outputFile.cd()
    outDirWS = outputFile.mkdir("withSlab")
    outDirWS.cd()
    chanMultWithSlab.Write()
    chanMultNoAfterWithSlab.Write()
    minNPEVsMaxNPEWithSlab.Write()
    minQVsMaxQWithSlab.Write()
    minNPEVsMaxNPECorrWithSlab.Write()
    firstNPEVsNumAfterPulsesWithSlab.Write()
    firstPulseTimeWithSlab.Write()
    chanVsNumAfterPulsesWithSlab.Write()
    chanVsNPEWithSlab.Write()
    chanVsNPECorrWithSlab.Write()
    chanVsQWithSlab.Write()
    outDir = outDirWS.mkdir("afterPulseTimeSinceFirst")
    outDir.cd()
    for chan in afterPulseTimeSinceFirstPulse:
        afterPulseTimeSinceFirstPulse[chan].Write()
    outputFile.cd()

    for path in totalEffsPerPath:
        # totalEffsPerPath[path].Scale(1./nTot)
        totalEffsPerPath[path].Write()
    if not blind:
        print( nTot)
        print( "Q", nPassQuiet*1./nTot)
        print( nPassCosmic*1./nTot)
        print( "OP",nPassOnePulse*1./nTot)
        print( "Pulse time selection",nPassPulseTimeSelection*1./nTot)
        print( "MaxMin",nPassMaxMin*1./nTot)
        print( "Timing",nPassTiming*1./nTot)
        print( "Straight",nPassStraightPath*1.)
        print( "StraightPlusSlab",nPassStraightPlusSlabPath*1.)
        print( "StraightPlusTwoOrMoreSlabs",nPassStraightPlusTwoOrMoreSlabsPath*1.)
    # overallEff = r.TH1D("eff",";eff",6,0,6)
    # overallEffPerPath = r.TH2D("effVsNPE",";eff",6,0,6)
    # overallEff.SetBinContent(1,nPassQuiet*1./nTot)
    # overallEff.SetBinContent(2,nPassSidebandRMS*1./nTot)
    # overallEff.SetBinContent(3,nPassOnePulse*1./nTot)
    # overallEff.SetBinContent(4,nPassStraightPath*1./nTot)
    # overallEff.SetBinContent(5,nPassTiming*1./nTot)
    # overallEff.SetBinContent(6,nPassMaxNPE*1./nTot)
    # overallEff.GetXaxis().SetBinLabel(1,"nPassQuiet")
    # overallEff.GetXaxis().SetBinLabel(2,"nPassSidebandRMS")
    # overallEff.GetXaxis().SetBinLabel(3,"nPassOnePulse")
    # overallEff.GetXaxis().SetBinLabel(4,"nPassStraightPath")
    # overallEff.GetXaxis().SetBinLabel(5,"nPassTiming")
    # overallEff.GetXaxis().SetBinLabel(6,"nPassMaxNPE")
    # overallEff.Write()
    if signal:
        return None,None
    for plotType,plots in outputPlots.items():
        outDir = outputFile.mkdir(plotType)
        outDir.cd()
        outDirValid = outDir.mkdir("allPaths")
        outDirValid.cd()
        for path in paths:
            plot = outputPlots[plotType][path]
            # plot.Scale(3600./totalRunTime)
            plot.Write()
            for pathType in allPaths:
                if path in allPaths[pathType]:
                    outputPlots[plotType][pathType].Add(plot)
        outDirSummary = outDir.mkdir("summary")
        outDirSummary.cd()
        for pathType in allPaths:
            outputPlots[plotType][pathType].Write()

    return outputFile,allPaths
def makeABCDPredictions(inputFile,beamString,blind,nPEStrings,deltaTStrings,selections,allPaths,signalNorm):
    if inputFile == None:
        return
    blindString = ""
    if blind:
        blindString = "Blind"
    outputFileABCD = r.TFile("outputFileABCD{0}{1}{2}.root".format(beamString,blindString,tag),"RECREATE")
    # totalRunTime = {"beam":418*3600,"noBeam":418*3600}
    # totalRunTime = {"beam":1.44E6,"noBeam":1.45E6}
    outDir = outputFileABCD.mkdir("sep_paths")
    outDir.cd()
    for deltaTString in ["min","max"][-1:]:
        if deltaTString == "": continue
        outDirDT = outDir.mkdir(deltaTString)
        outDirDT.cd()
        pathList = []
        for pathType,paths in allPaths.items():
            if pathType == "Slabs":continue
            for path in paths:
                if path not in pathList:
                    straightPlot = inputFile.Get("{0}Vs{1}{2}/allPaths/{3}_{0}_{1}{2}".format("NPEMin",deltaTString,"NoOtherPulse","_".join(str(x) for x in path)))
                    straightDeltaT = straightPlot.ProjectionY()
                    straightDeltaT.Scale(3600./totalRunTime[beamString])
                    straightDeltaT.Write()
                    pathList.append(path)
    for selection in selections:
        validationHists = {}
        outputDirSel = outputFileABCD.mkdir(selection)
        for deltaTString in deltaTStrings:
            if deltaTString == "": continue
            outputDirDT = outputDirSel.mkdir(deltaTString)
            for nPEString in nPEStrings:
                if nPEString == "": continue
                outputDirNPE = outputDirDT.mkdir(nPEString)
                outputDirNPE.cd()
                for plusSlab in ["","PlusSlab","PlusTwoOrMoreSlabs"]:
                    for pathType in ["","bad","noBad"]:
                        if pathType == "":
                            pathTypeString = "All"+plusSlab
                        else:
                            pathTypeString = pathType+plusSlab
                        for scaleByPath in [True,False]:
                            if scaleByPath:
                                outputDir = outputDirNPE.mkdir(pathTypeString+"_scaleByPath")
                            else:
                                outputDir = outputDirNPE.mkdir(pathTypeString)
                            outputDir.cd()
                            straightPlot = inputFile.Get("{0}Vs{1}{2}/summary/{3}Straight{4}_{0}_{1}{2}".format(nPEString,deltaTString,selection,pathType,plusSlab))
                            bentPlot = inputFile.Get("{0}Vs{1}{2}/summary/{3}BentSameDigi{4}_{0}_{1}{2}".format(nPEString,deltaTString,selection,pathType,plusSlab))
                            straightDeltaT = straightPlot.ProjectionY()
                            bentDeltaT = bentPlot.ProjectionY()


                            histA = straightPlot.ProjectionX("A",straightPlot.GetYaxis().FindBin(-timingSel),straightPlot.GetYaxis().FindBin(timingSel)-1)
                            histB = straightPlot.ProjectionX("B",straightPlot.GetYaxis().FindBin(-100),straightPlot.GetYaxis().FindBin(-timingSel)-1)
                            histB2 = straightPlot.ProjectionX("B2",straightPlot.GetYaxis().FindBin(timingSel),straightPlot.GetYaxis().FindBin(100))
                            histB.Add(histB2)

                            histD = bentPlot.ProjectionX("D",bentPlot.GetYaxis().FindBin(-timingSel),bentPlot.GetYaxis().FindBin(timingSel)-1)
                            histC = bentPlot.ProjectionX("C",bentPlot.GetYaxis().FindBin(-100),bentPlot.GetYaxis().FindBin(-timingSel)-1)
                            histC2 = bentPlot.ProjectionX("C2",bentPlot.GetYaxis().FindBin(timingSel),bentPlot.GetYaxis().FindBin(100))
                            histC.Add(histC2)

                            histA.SetTitle("deltaTWithintimingSelStraightPred")
                            histB.SetTitle("deltaTOutsidetimingSelStraight")
                            histC.SetTitle("deltaTOutsidetimingSelBent")
                            histD.SetTitle("deltaTWithintimingSelBent")

                            for hist in [histA,histB,histC,histD]:
                                for iBin in range(1,hist.GetNbinsX()+1):
                                    hist.SetBinError(iBin,hist.GetBinContent(iBin)**0.5)
                            histAPred = histB.Clone("APred")
                            histAPred.Multiply(histD)
                            histAPred.Divide(histC)
                            histAPred.SetTitle("deltaTWithintimingSelStraightObs")

                            histAPred.SetLineColor(r.kRed)
                            histA.SetLineColor(r.kBlue)
                            if signalNorm != None:
                                straightDeltaT.Scale(1./signalNorm)
                                bentDeltaT.Scale(1./signalNorm)

                                histA.Scale(1./signalNorm)
                                histAPred.Scale(1./signalNorm)
                                histB.Scale(1./signalNorm)
                                histC.Scale(1./signalNorm)
                                histD.Scale(1./signalNorm)
                            else:
                                straightDeltaT.Scale(3600./totalRunTime[beamString])
                                bentDeltaT.Scale(3600./totalRunTime[beamString])

                                histA.Scale(3600./totalRunTime[beamString])
                                histAPred.Scale(3600./totalRunTime[beamString])
                                histB.Scale(3600./totalRunTime[beamString])
                                histC.Scale(3600./totalRunTime[beamString])
                                histD.Scale(3600./totalRunTime[beamString])
                            if scaleByPath:
                                straightDeltaT.Scale(1./len(allPaths[pathType+"Straight"+plusSlab]))
                                bentDeltaT.Scale(1./len(allPaths[pathType+"BentSameDigi"+plusSlab]))
                                histA.Scale(1./len(allPaths[pathType+"Straight"+plusSlab]))
                                histAPred.Scale(1./len(allPaths[pathType+"Straight"+plusSlab]))
                                histB.Scale(1./len(allPaths[pathType+"Straight"+plusSlab]))
                                histC.Scale(1./len(allPaths[pathType+"BentSameDigi"+plusSlab]))
                                histD.Scale(1./len(allPaths[pathType+"BentSameDigi"+plusSlab]))
                                # singlesPred = histAPred.Clone(histAPred.GetName()+"SinglesPred")
                                # for iBin in range(1,singlesPred.GetNbinsX()+2):
                                #     singlesPred.SetBinContent(iBin,(singlesPred.GetBinContent(iBin)*3600/(100E-9*100E-9))**(1./3.))
                                #     singlesPred.SetBinError(iBin,(singlesPred.GetBinError(iBin)*3600/(100E-9*100E-9))**(1./3.))

                            histAPred.Write()
                            histA.Write()
                            histB.Write()
                            histC.Write()
                            histD.Write()
                            # singlesPred.Write()
                            perPathDir = outputDir.mkdir("perPathRates")
                            perPathDir.cd()
                            for pathNum in range(1,7):
                                perPathHist2D = inputFile.Get("{0}Vs{1}{2}/allPaths/{3}_{0}_{1}{2}".format("NPEMin",deltaTString,"NoOtherPulse","_".join(str(x) for x in allPaths["Straight"+str(pathNum)][0])))
                                perPathHist = perPathHist2D.ProjectionX("A",straightPlot.GetYaxis().FindBin(-timingSel),straightPlot.GetYaxis().FindBin(timingSel)-1)
                                perPathHist.SetName("Path_"+"_".join(str(x) for x in allPaths["Straight"+str(pathNum)][0]))
                                for iBin in range(1,perPathHist.GetNbinsX()+1):
                                    hist.SetBinError(iBin,perPathHist.GetBinContent(iBin)**0.5)
                                perPathHist.Scale(3600./totalRunTime[beamString])
                                perPathHist.Write()
                            if scaleByPath:
                                validDir = outputDir.mkdir("validation_scaleByPath")
                            else:
                                validDir = outputDir.mkdir("validation")
                            validDir.cd()

                            straightDeltaT.SetName(pathType+"Straight"+plusSlab+"_"+deltaTString)
                            bentDeltaT.SetName(pathType+"BentSameDigi"+plusSlab+"_"+deltaTString)
                            if not scaleByPath:
                                validationHists[selection,deltaTString,pathType+"Straight"+plusSlab] = straightDeltaT
                                validationHists[selection,deltaTString,pathType+"BentSameDigi"+plusSlab] = bentDeltaT
        validDir = outputDirSel.mkdir("validation")
        for pathType in ["","bad","noBad"]:
            for plusSlab in ["","PlusTwoOrMoreSlabs"]:
                validDirPathDirStraight = validDir.mkdir(pathType+"Straight"+plusSlab)
                validDirPathDirStraight.cd()
                for deltaTString in deltaTStrings[1:]:
                    validationHists[selection,deltaTString,pathType+"Straight"].Write()
                validDirPathDirBent = validDir.mkdir(pathType+"BentSameDigi"+plusSlab)
                validDirPathDirBent.cd()
                for deltaTString in deltaTStrings[1:]:
                    validationHists[selection,deltaTString,pathType+"BentSameDigi"].Write()
    outputFileABCD.Close()



if __name__=="__main__":
    nPEStrings = ["NPEMin","NPEMax","NPEMinCorr","NPEMaxCorr"]
    deltaTStrings = ["min","max"][-1:]
    selections = ["NoOtherPulse","NoOtherPulsePlusPanelHit","NoPrePulse","NoPrePulsePlusPanelHit"]
    blind = False
    useSaved = False
    beamString = "beam"
    signal = False
    for beamString in ["beam","noBeam"]:
        if signal and beamString == "noBeam":
            continue
        if beamString  == "beam" and not signal:
            blind = True
        else:
            blind = False
        for signalQ in ["0p005","0p01","0p02","0p03","0p05","0p07","0p1","0p14","0p2","0p3"]:
            if not signal and signalQ != "0p005":continue
            if signal:
                inputFile = r.TFile("signalInputs/mcp_m1p0_q{0}_geant_NTUPLE_testmixv2.root".format(signalQ))
                tag = tagOrig + "Signal"+signalQ
                inputTree = inputFile.Get("t")
                signalNorm = inputTree.GetEntries()
            else:
                tag = tagOrig
                # inputFile = r.TFile("{0}TwoLayerHitsOrThreeSlabHits.root".format(beamString))
                # inputFile = r.TFile("../allTrees/allPhysicsAndTripleChannelSinceTS1_threeLayerHitPlusSlab_191204.root".format(beamString))
                # inputFile = r.TFile("../allTrees/allPhysicsAndTripleChannelSinceTS1_threeLayerHitPlusSlab_200303.root".format(beamString))
                inputFile = r.TFile("../allTrees/allPhysicsAndTripleChannelSinceTS1_threeLayerHit_200303.root".format(beamString))
                # inputFile = r.TFile("../allTrees/allPhysicsAndTripleChannelSinceTS1_threeLayerHit_191204.root".format(beamString))
                signalNorm = None
            slabs = [18,20,28]
            outputFile,allPaths = measureBackgrounds(inputFile,blind,beamString,useSaved,nPEStrings,deltaTStrings,selections,slabs,signal)
            if not signal:
                makeABCDPredictions(outputFile,beamString,blind,nPEStrings,deltaTStrings,selections,allPaths,signalNorm)
            if outputFile:
                outputFile.Close()
            if inputFile:
                inputFile.Close()

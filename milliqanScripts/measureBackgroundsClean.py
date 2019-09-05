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
layers = {1:[0,1,24,25,8,9],2:[6,7,16,17,12,13],3:[2,3,22,23,4,5]}
extraPathsLists = [[7,12,2],[3,5,1],[0,8,7]]
extraPaths = []
for path in extraPathsLists:
    extraPaths.append(tuple(sorted(path)))

# binsNPE = array('d',[0]+np.logspace(0.1,3,6))
binsNPE = array('d',[0,0.5,1.5,5,10,20,50,100,1000,10000])
binsDeltaT = array('d',np.linspace(-120,120,385))
timingSel = 15
tagOrig = "remakePredictionsFixCh15MaxMinSel2_{0}ns".format(timingSel)
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
    badStraightPlusSlab = []
    noBadStraightPlusSlab = []
    bentDiffDigiPlusSlab = []
    bentSameDigiPlusSlab = []
    badBentSameDigiPlusSlab = []
    noBadBentSameDigiPlusSlab = []
    slabPaths = {}
    for iC1,chan1 in enumerate(layers[1]):
        for iC2,chan2 in enumerate(layers[2]):
            for iC3,chan3 in enumerate(layers[3]):
                path = tuple(sorted(set([chan1,chan2,chan3])))
                pathPlusSlab1 = tuple(sorted(set([18,chan1,chan2,chan3])))
                pathPlusSlab2 = tuple(sorted(set([21,chan1,chan2,chan3])))
                pathPlusSlab3 = tuple(sorted(set([28,chan1,chan2,chan3])))
                pathPlusSlab4 = tuple(sorted(set([20,chan1,chan2,chan3])))
                paths.append(path)
                paths.append(pathPlusSlab1)
                paths.append(pathPlusSlab2)
                paths.append(pathPlusSlab3)
                paths.append(pathPlusSlab4)
                if iC1 == iC2 and iC2 == iC3:
                    straight.append(path)
                    straightPlusSlab.append(pathPlusSlab1)
                    straightPlusSlab.append(pathPlusSlab2)
                    straightPlusSlab.append(pathPlusSlab3)
                    straightPlusSlab.append(pathPlusSlab4)
                    if chan1 in badChans or chan2 in badChans or chan3 in badChans:
                        badStraight.append(path)
                        badStraightPlusSlab.append(pathPlusSlab1)
                        badStraightPlusSlab.append(pathPlusSlab2)
                        badStraightPlusSlab.append(pathPlusSlab3)
                        badStraightPlusSlab.append(pathPlusSlab4)
                    else:
                        noBadStraight.append(path)
                        noBadStraightPlusSlab.append(pathPlusSlab1)
                        noBadStraightPlusSlab.append(pathPlusSlab2)
                        noBadStraightPlusSlab.append(pathPlusSlab3)
                        noBadStraightPlusSlab.append(pathPlusSlab4)
                else:
                    if int(chan1/16) == int(chan2/16) and int(chan2/16) == int(chan3/16):
                        bentSameDigi.append(path)
                        bentSameDigiPlusSlab.append(pathPlusSlab1)
                        bentSameDigiPlusSlab.append(pathPlusSlab2)
                        bentSameDigiPlusSlab.append(pathPlusSlab3)
                        bentSameDigiPlusSlab.append(pathPlusSlab4)
                        if chan1 in badChans or chan2 in badChans or chan3 in badChans:
                            badBentSameDigi.append(path)
                            badBentSameDigiPlusSlab.append(pathPlusSlab1)
                            badBentSameDigiPlusSlab.append(pathPlusSlab2)
                            badBentSameDigiPlusSlab.append(pathPlusSlab3)
                            badBentSameDigiPlusSlab.append(pathPlusSlab4)
                        else:
                            noBadBentSameDigi.append(path)
                            noBadBentSameDigiPlusSlab.append(pathPlusSlab1)
                            noBadBentSameDigiPlusSlab.append(pathPlusSlab2)
                            noBadBentSameDigiPlusSlab.append(pathPlusSlab3)
                            noBadBentSameDigiPlusSlab.append(pathPlusSlab4)
                    else:
                        bentDiffDigi.append(path)
                        bentDiffDigiPlusSlab.append(pathPlusSlab1)
                        bentDiffDigiPlusSlab.append(pathPlusSlab2)
                        bentDiffDigiPlusSlab.append(pathPlusSlab3)
                        bentDiffDigiPlusSlab.append(pathPlusSlab4)
    paths.extend(extraPaths)
    paths.append(slabs)
    allPaths={"Straight1":[(0,2,6)],"Straight2":[(1,3,7)],"Straight3":[(16,22,24)],"Straight4":[(17,23,25)],"Straight5":[(4,8,12)],"Straight6":[(5,9,13)],"Straight":straight,"badStraight":badStraight,"noBadStraight":noBadStraight,"BentSameDigi":bentSameDigi,
            "badBentSameDigi":badBentSameDigi,"noBadBentSameDigi":noBadBentSameDigi,"BentDiffDigi":bentDiffDigi,"Slabs":[slabs],"ExtraPaths":extraPaths,
            "StraightPlusSlab":straightPlusSlab,"badStraightPlusSlab":badStraightPlusSlab,"noBadStraightPlusSlab":noBadStraightPlusSlab,"BentSameDigiPlusSlab":bentSameDigiPlusSlab,
            "badBentSameDigiPlusSlab":badBentSameDigiPlusSlab,"noBadBentSameDigiPlusSlab":noBadBentSameDigiPlusSlab,"BentDiffDigi":bentDiffDigiPlusSlab,"Slabs":[slabs],"ExtraPaths":extraPaths}
    return allPaths,paths
def measureBackgrounds(inputFile,blind,beamString,useSaved,nPEStrings,deltaTStrings,selections,slabs,signal):
    allPaths,paths = preparePaths(slabs=slabs)
    tree = inputFile.Get("t")
    nTot = 0
    nPassQuiet = 0
    nPassSidebandRMS = 0
    nPassStraightPath = 0
    nPassOnePulse = 0
    nPassTiming = 0
    nPassMaxNPE = 0
    beamReq = False
    totalEffsPerPath = {}
    for path in range(-1,6):
        if path > -1:
            totalEffsPerPath[path] = r.TH1D("pathTuple"+"_".join(str(x) for x in allPaths["Straight"][path]),";nPE;",len(binsNPE)-1,binsNPE)
        else:
            totalEffsPerPath[path] = r.TH1D("pathTupleAll",";nPE;",len(binsNPE)-1,binsNPE)
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
        if tree.groupTDC_b0[0] != tree.groupTDC_b1[0]:
            continue
        if tree.beam != beamReq:
            continue
        # if run > 1341:
        #     continue
        nTot += 1
        chansHit = set(tree.chan)
        if 15 in chansHit: chansHit.remove(15)
        #Only N chans hit
        if len(chansHit) > maxPathLength: continue
        #chans hit in paths
        chanSet = tuple(sorted(set(tree.chan)))
        if chanSet not in paths:
            continue
        nPassQuiet += 1
        #No noisy RMS
        sideband_RMS = list(tree.sideband_RMS)
        sideband_RMS = sideband_RMS[:15]+sideband_RMS[16:]
        if max(sideband_RMS) > 1.3: continue
        nPassSidebandRMS += 1
        #Max pulses
        pulses = {1:[],2:[],3:[]}
        if len(chanSet) == 4:
            pulses[0] = []
        if (chansHit == set(slabs)):
            #Slabs are offset by 1
            for nPE,time,layer,chan,duration in zip(tree.nPE,tree.time_module_calibrated,tree.layer,tree.chan,tree.duration):
                pulses[layer+1].append([nPE,time,chan])
        elif any(chansHit == extraPathSet for extraPathSet in extraPathsSet):
            extraPathIndex = extraPathsSet.index(chansHit)
            for nPE,time,chan,duration in zip(tree.nPE,tree.time_module_calibrated,tree.chan,tree.duration):
                pulses[allPaths["ExtraPaths"][extraPathIndex].index(chan)+1].append([nPE,time,chan])
        elif len(chansHit) == 3:
            #Only bars hit
            if 1 in tree.type or 2 in tree.type: continue
            #Hit in each layer
            if set(list(tree.layer)) != set([1,2,3]): continue
            for nPE,time,layer,chan,duration in zip(tree.nPE,tree.time_module_calibrated,tree.layer,tree.chan,tree.duration):
                pulses[layer].append([nPE,time,chan])
        elif len(chansHit) == 4:
            #bars hit + 1 slab
            if 2 in tree.type: continue
            #Hit in each layer
            layers = []
            for nPE,time,layer,chan,duration in zip(tree.nPE,tree.time_module_calibrated,tree.layer,tree.chan,tree.duration):
                if chan in [18,20,21,28]: layerT = 0
                else: layerT = layer
                pulses[layerT].append([nPE,time,chan])
                layers.append(layerT)
            if set(layers) != set([0,1,2,3]): continue
        # for nPE,time,layer,chan in zip(tree.nPE,tree.time,tree.layer,tree.chan):
        #Check first pulse is maximal
        singlePulse = True
        failAllSelection = False
        for layer,pulsesList in pulses.items():
            if len(pulsesList) == 0: 
                failAllSelection = True
                break
            if len(pulsesList) != 1:
                singlePulse = False
            if pulsesList[0] != max(pulsesList):
                failAllSelection = True
                break

        if failAllSelection: continue
        nPassOnePulse += 1
        sels = ["NoPrePulse"]
        if singlePulse:
            sels.append("NoOtherPulse")

        chanSet = tuple(sorted(set(tree.chan)))
        allDeltaTs = []
        if len(pulses) == 3:
            minNPE = min([pulses[1][0][0],pulses[2][0][0],pulses[3][0][0]])
            maxNPE = max([pulses[1][0][0],pulses[2][0][0],pulses[3][0][0]])

            deltaTL3L1 = pulses[3][0][1] - pulses[1][0][1]
            deltaTL3L2 = pulses[3][0][1] - pulses[2][0][1]
            deltaTL2L1 = pulses[2][0][1] - pulses[1][0][1]
            allDeltaTs = [deltaTL3L1,deltaTL3L2,deltaTL2L1]
        elif len(pulses) == 4:
            minNPE = min([pulses[1][0][0],pulses[2][0][0],pulses[3][0][0],pulses[0][0][0]])
            maxNPE = max([pulses[1][0][0],pulses[2][0][0],pulses[3][0][0],pulses[0][0][0]])

            deltaTL3L1 = pulses[3][0][1] - pulses[1][0][1]
            deltaTL3L2 = pulses[3][0][1] - pulses[2][0][1]
            deltaTL2L1 = pulses[2][0][1] - pulses[1][0][1]

            deltaTL3L0 = pulses[3][0][1] - pulses[0][0][1]
            deltaTL2L0 = pulses[2][0][1] - pulses[0][0][1]
            deltaTL1L0 = pulses[1][0][1] - pulses[0][0][1]
            allDeltaTs = [deltaTL3L1,deltaTL3L2,deltaTL2L1,deltaTL3L0,deltaTL2L0,deltaTL1L0]

        minDeltaT = min(allDeltaTs,key = lambda x:abs(x))
        maxDeltaT = max(allDeltaTs,key = lambda x:abs(x))
        if tuple(sorted(list(chanSet))) in allPaths["Straight"]:
            pathIndex = allPaths["Straight"].index(tuple(sorted(list(chanSet))))
            nPassStraightPath += 1
            if abs(maxDeltaT) < timingSel:
                nPassTiming += 1
                #skip npe for now
                totalEffsPerPath[pathIndex].Fill(minNPE)
                totalEffsPerPath[-1].Fill(minNPE)
                # if maxNPE < 100:
                #     nPassMaxNPE += 1

        # if maxNPE > 100: continue
        # if minNPE > binsNPE[-1]: continue
        if maxNPE/minNPE > 2: 
            nPassMaxNPE += 1
            continue
        if blind:
            if tuple(sorted(list(chanSet))) in allPaths["Straight"] and abs(maxDeltaT) < timingSel: continue
        # if abs(maxDeltaT) < timingSel:
        #     if len(pulses) == 4 and singlePulse:
        #         if tuple(sorted(list(chanSet))) in allPaths["StraightPlusSlab"]:
        #             print( "s",chanSet,tree.run,tree.file,tree.event,maxNPE
        #         elif tuple(sorted(list(chanSet))) in allPaths["BentSameDigiPlusSlab"]:
        #             print( "b",chanSet,tree.run,tree.file,tree.event,maxNPE
        nPEDict = {"NPEMin":minNPE,"NPEMax":maxNPE}
        deltaTDict = {"min":minDeltaT,"max":maxDeltaT}
        for sel in sels:
            for deltaTString in deltaTStrings:
                for nPEString in nPEStrings:
                    outputPlots[nPEString+"Vs"+deltaTString+sel][chanSet].Fill(nPEDict[nPEString],deltaTDict[deltaTString])

        #Check time distributions
        # if abs(pulses[3][0][1] - pulses[1][0][1]) > 30: continue
        # if abs(pulses[2][0][1] - pulses[1][0][1]) > 20: continue


    outputFile.cd()
    for path in totalEffsPerPath:
        totalEffsPerPath[path].Scale(1./nTot)
        totalEffsPerPath[path].Write()
    print( nTot)
    print( "Q", nPassQuiet*1./nTot)
    # print( nPassSidebandRMS*1./nTot)
    print( "OP",nPassOnePulse*1./nTot)
    print( "Straight",nPassStraightPath*1./nTot)
    print( "Timing",nPassTiming*1./nTot)
    print( "nPE",nPassMaxNPE*1./nTot)
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
    totalRunTime = {"beam":3.34E6,"noBeam":3.92E6}
    outDir = outputFileABCD.mkdir("sep_paths")
    outDir.cd()
    for deltaTString in ["min","max"]:
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
                for pathType in ["","bad","noBad"]:
                    if pathType == "":
                        pathTypeString = "All"
                    else:
                        pathTypeString = pathType
                    for scaleByPath in [True,False]:
                        if scaleByPath:
                            outputDir = outputDirNPE.mkdir(pathTypeString+"_scaleByPath")
                        else:
                            outputDir = outputDirNPE.mkdir(pathTypeString)
                        outputDir.cd()
                        straightPlot = inputFile.Get("{0}Vs{1}{2}/summary/{3}Straight_{0}_{1}{2}".format(nPEString,deltaTString,selection,pathType))
                        bentPlot = inputFile.Get("{0}Vs{1}{2}/summary/{3}BentSameDigi_{0}_{1}{2}".format(nPEString,deltaTString,selection,pathType))
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
                            straightDeltaT.Scale(1./len(allPaths[pathType+"Straight"]))
                            bentDeltaT.Scale(1./len(allPaths[pathType+"BentSameDigi"]))
                            histA.Scale(1./len(allPaths[pathType+"Straight"]))
                            histAPred.Scale(1./len(allPaths[pathType+"Straight"]))
                            histB.Scale(1./len(allPaths[pathType+"Straight"]))
                            histC.Scale(1./len(allPaths[pathType+"BentSameDigi"]))
                            histD.Scale(1./len(allPaths[pathType+"BentSameDigi"]))
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

                        straightDeltaT.SetName(pathType+"Straight"+"_"+deltaTString)
                        bentDeltaT.SetName(pathType+"BentSameDigi"+"_"+deltaTString)
                        if not scaleByPath:
                            validationHists[selection,deltaTString,pathType+"Straight"] = straightDeltaT
                            validationHists[selection,deltaTString,pathType+"BentSameDigi"] = bentDeltaT
        validDir = outputDirSel.mkdir("validation")
        for pathType in ["","bad","noBad"]:
            validDirPathDirStraight = validDir.mkdir(pathType+"Straight")
            validDirPathDirStraight.cd()
            for deltaTString in deltaTStrings[1:]:
                validationHists[selection,deltaTString,pathType+"Straight"].Write()
            validDirPathDirBent = validDir.mkdir(pathType+"BentSameDigi")
            validDirPathDirBent.cd()
            for deltaTString in deltaTStrings[1:]:
                validationHists[selection,deltaTString,pathType+"BentSameDigi"].Write()



if __name__=="__main__":
    nPEStrings = ["NPEMin","NPEMax"]
    deltaTStrings = ["min","max"]
    selections = ["NoOtherPulse","NoPrePulse"]
    blind = False
    useSaved = False
    beamString = "beam"
    for beamString in ["beam","noBeam"]:
        if beamString  == "beam":
            blind = True
        else:
            blind = False
        signal = False
        for signalQ in ["0p001","0p002","0p005","0p01","0p02","0p05","0p1"]:
            if not signal and signalQ != "0p005":continue
            if signal:
                inputFile = r.TFile("signalInjectionQ"+signalQ+"NoLPFilter.root")
                tag = tagOrig + "Signal"+signalQ
                inputTree = inputFile.Get("t")
                signalNorm = inputTree.GetEntries()
            else:
                tag = tagOrig
                # inputFile = r.TFile("{0}TwoLayerHitsOrThreeSlabHits.root".format(beamString))
                inputFile = r.TFile("../allTrees/allPhysicsAndTripleChannelSinceTS1_threeLayerHit_181017.root".format(beamString))
                signalNorm = None
            slabs = [18,20,28]
            outputFile,allPaths = measureBackgrounds(inputFile,blind,beamString,useSaved,nPEStrings,deltaTStrings,selections,slabs,signal)
            makeABCDPredictions(outputFile,beamString,blind,nPEStrings,deltaTStrings,selections,allPaths,signalNorm)

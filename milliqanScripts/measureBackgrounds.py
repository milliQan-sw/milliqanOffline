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
tagOrig = "ForWorkshop"
layers = {1:[0,1,24,25,8,9],2:[6,7,16,17,12,13],3:[2,3,22,23,4,5]}
extraPathsLists = [[7,12,2],[3,5,1],[0,8,7]]
extraPaths = []
for path in extraPathsLists:
    extraPaths.append(tuple(sorted(path)))

binsNPE = array('d',[0,0.5,1.5,5,10,20,50,100,1000,10000])
binsDeltaT = array('d',np.linspace(-120,120,385))
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
    for iC1,chan1 in enumerate(layers[1]):
        for iC2,chan2 in enumerate(layers[2]):
            for iC3,chan3 in enumerate(layers[3]):
                path = tuple(sorted(set([chan1,chan2,chan3])))
                paths.append(path)
                if iC1 == iC2 and iC2 == iC3:
                    straight.append(path)
                    if chan1 in badChans or chan2 in badChans or chan3 in badChans:
                        badStraight.append(path)
                    else:
                        noBadStraight.append(path)
                else:
                    if chan1/16 == chan2/16 and chan2/16 == chan3/16:
                        bentSameDigi.append(path)
                        if chan1 in badChans or chan2 in badChans or chan3 in badChans:
                            badBentSameDigi.append(path)
                        else:
                            noBadBentSameDigi.append(path)
                    else:
                        bentDiffDigi.append(path)
    paths.extend(extraPaths)
    paths.append(slabs)
    allPaths={"Straight":straight,"badStraight":badStraight,"noBadStraight":noBadStraight,"BentSameDigi":bentSameDigi,
            "badBentSameDigi":badBentSameDigi,"noBadBentSameDigi":noBadBentSameDigi,"BentDiffDigi":bentDiffDigi,"Slabs":[slabs],"ExtraPaths":extraPaths}
    return allPaths,paths
def measureBackgrounds(inputFile,blind,beamString,useSaved,nPEStrings,deltaTStrings,selections,slabs,signal):
    allPaths,paths = preparePaths(slabs=slabs)
    tree = inputFile.Get("t")
    nTot = 0
    nPassQuiet = 0
    nPassSidebandRMS = 0
    nPassOnePulse = 0
    nPassTiming = 0
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
    for sel in selections:
        for path in paths+allPaths.keys():
            if type(path) == str:
                pathString = path
            else:
                pathString = "_".join(str(x) for x in path)
            for iD,deltaT in enumerate(deltaTStrings):
                for nPE in nPEStrings:
                    if deltaT == nPE: continue
                    if nPE == "":
                        outputPlots[deltaT+sel][path] = r.TH1D(pathString+"_"+deltaT+sel,";deltaT;",len(binsDeltaT)-1,binsDeltaT)
                    elif deltaT == "":
                        outputPlots[nPE+sel][path] = r.TH1D(pathString+"_"+nPE+sel,";nPE;",len(binsDeltaT)-1,binsDeltaT)
                    else:
                        outputPlots[nPE+"Vs"+deltaT+sel][path] = r.TH2D(pathString+"_"+nPE+"_"+deltaT+sel,";nPE;deltaT",len(binsNPE)-1,binsNPE,len(binsDeltaT)-1,binsDeltaT)
                for deltaT2 in deltaTStrings[iD:]:
                        if deltaT == "": continue
                        if deltaT2 == "": continue
                        outputPlots[deltaT+"Vs"+deltaT2+sel][path] = r.TH2D(pathString+"_"+deltaT+"_"+deltaT2+sel,";deltaT;deltaT",len(binsDeltaT)-1,binsDeltaT,len(binsDeltaT)-1,binsDeltaT)

    iE = -1
    nEvents = tree.GetEntries()
    extraPathsSet = [set(extraPath) for extraPath in allPaths["ExtraPaths"]]
    pbar = ProgressBar()
    for iE in pbar(range(nEvents)):
        tree.GetEntry(iE)
        if tree.groupTDC_b0[0] != tree.groupTDC_b1[0]:
            continue
        nTot += 1
        chansHit = set(tree.chan)
        #Only three chans hit
        if len(chansHit) > 3: continue
        nPassQuiet += 1
        #No noisy RMS
        if max(tree.sideband_RMS) > 1.3: continue
        nPassSidebandRMS += 1
        #Max pulses
        pulses = {1:[],2:[],3:[]}
        if (chansHit == set(slabs)):
            #Slabs are offset by 1
            for nPE,time,layer,chan,duration in zip(tree.nPE,tree.time_module_calibrated,tree.layer,tree.chan,tree.duration):
                pulses[layer+1].append([nPE,time,chan])
        elif any(chansHit == extraPathSet for extraPathSet in extraPathsSet):
            extraPathIndex = extraPathsSet.index(chansHit)
            for nPE,time,chan,duration in zip(tree.nPE,tree.time_module_calibrated,tree.chan,tree.duration):
                pulses[allPaths["ExtraPaths"][extraPathIndex].index(chan)+1].append([nPE,time,chan])
        else:
            #Only bars hit
            if 1 in tree.type or 2 in tree.type: continue
            #Hit in each layer
            if set(list(tree.layer)) != set([1,2,3]): continue
            for nPE,time,layer,chan,duration in zip(tree.nPE,tree.time_module_calibrated,tree.layer,tree.chan,tree.duration):
                pulses[layer].append([nPE,time,chan])
        # for nPE,time,layer,chan in zip(tree.nPE,tree.time,tree.layer,tree.chan):
        #Check first pulse is maximal
        singlePulse = True
        failAllSelection = False
        for layer,pulsesList in pulses.iteritems():
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
        minNPE = min([pulses[1][0][0],pulses[2][0][0],pulses[3][0][0]])
        maxNPE = max([pulses[1][0][0],pulses[2][0][0],pulses[3][0][0]])

        deltaTL3L1 = pulses[3][0][1] - pulses[1][0][1]
        deltaTL3L2 = pulses[3][0][1] - pulses[2][0][1]
        deltaTL2L1 = pulses[2][0][1] - pulses[1][0][1]

        minDeltaT = min([deltaTL3L1,deltaTL2L1,deltaTL3L2],key = lambda x:abs(x))
        maxDeltaT = max([deltaTL3L1,deltaTL2L1,deltaTL3L2],key = lambda x:abs(x))
        if abs(maxDeltaT) < 30:
            nPassTiming += 1

        # if minNPE > binsNPE[-1]: continue
        if blind:
            if tuple(sorted(list(chanSet))) in allPaths["Straight"] and abs(maxDeltaT) < 30: continue
        nPEDict = {"NPEMin":minNPE,"NPEMax":maxNPE}
        deltaTDict = {"DeltaTL3L1":deltaTL3L1,"DeltaTL2L1":deltaTL2L1,"DeltaTL3L2":deltaTL3L2,"min":minDeltaT,"max":maxDeltaT}
        for sel in sels:
            for iD,deltaTString in enumerate(deltaTStrings):
                for nPEString in nPEStrings:
                    if nPEString == deltaTString: continue
                    if nPEString == "":
                        outputPlots[deltaTString+sel][chanSet].Fill(deltaTDict[deltaTString])
                    elif deltaTString == "":
                        outputPlots[nPEString+sel][chanSet].Fill(nPEDict[nPEString])
                    else:
                        outputPlots[nPEString+"Vs"+deltaTString+sel][chanSet].Fill(nPEDict[nPEString],deltaTDict[deltaTString])
                for deltaTString2 in deltaTStrings[iD+1:]:
                    if deltaTString == "": continue
                    if deltaTString2 == "": continue
                    outputPlots[deltaTString+"Vs"+deltaTString2+sel][chanSet].Fill(deltaTDict[deltaTString],deltaTDict[deltaTString2])

        #Check time distributions
        # if abs(pulses[3][0][1] - pulses[1][0][1]) > 30: continue
        # if abs(pulses[2][0][1] - pulses[1][0][1]) > 20: continue


    outputFile.cd()
    print nTot
    print nPassQuiet*1./nTot
    print nPassSidebandRMS*1./nPassQuiet
    print nPassOnePulse*1./nPassSidebandRMS
    print nPassTiming*1./nPassOnePulse
    overallEff = r.TH1D("eff",";eff",4,0,4)
    overallEff.SetBinContent(1,nPassQuiet*1./nTot)
    overallEff.SetBinContent(2,nPassSidebandRMS*1./nPassQuiet)
    overallEff.SetBinContent(3,nPassOnePulse*1./nPassSidebandRMS)
    overallEff.SetBinContent(4,nPassTiming*1./nPassOnePulse)
    overallEff.GetXaxis().SetBinLabel(1,"nPassQuiet")
    overallEff.GetXaxis().SetBinLabel(2,"nPassSidebandRMS")
    overallEff.GetXaxis().SetBinLabel(3,"nPassOnePulse")
    overallEff.GetXaxis().SetBinLabel(4,"nPassTiming")
    overallEff.Write()
    if signal:
        return None,None
    for plotType,plots in outputPlots.iteritems():
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
            print plotType,pathType,outputPlots[plotType][pathType].Integral()

    return outputFile,allPaths
def makeABCDPredictions(inputFile,beamString,blind,nPEStrings,deltaTStrings,selections,allPaths,signalNorm):
    if inputFile == None:
        return
    blindString = ""
    if blind:
        blindString = "Blind"
    outputFileABCD = r.TFile("outputFileABCD{0}{1}{2}.root".format(beamString,blindString,tag),"RECREATE")
    totalRunTime = {"beam":1.44E6,"noBeam":1.45E6}
    outDir = outputFileABCD.mkdir("sep_paths")
    outDir.cd()
    for deltaTString in ["min","max"]:
        if deltaTString == "": continue
        outDirDT = outDir.mkdir(deltaTString)
        outDirDT.cd()
        pathList = []
        for pathType,paths in allPaths.iteritems():
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


                        histA = straightPlot.ProjectionX("A",straightPlot.GetYaxis().FindBin(-30),straightPlot.GetYaxis().FindBin(30)-1)
                        histB = straightPlot.ProjectionX("B",straightPlot.GetYaxis().FindBin(-100),straightPlot.GetYaxis().FindBin(-30)-1)
                        histB2 = straightPlot.ProjectionX("B2",straightPlot.GetYaxis().FindBin(30),straightPlot.GetYaxis().FindBin(100))
                        histB.Add(histB2)

                        histD = bentPlot.ProjectionX("D",bentPlot.GetYaxis().FindBin(-30),bentPlot.GetYaxis().FindBin(30)-1)
                        histC = bentPlot.ProjectionX("C",bentPlot.GetYaxis().FindBin(-100),bentPlot.GetYaxis().FindBin(-30)-1)
                        histC2 = bentPlot.ProjectionX("C2",bentPlot.GetYaxis().FindBin(30),bentPlot.GetYaxis().FindBin(100))
                        histC.Add(histC2)

                        histA.SetTitle("deltaTWithin30StraightPred")
                        histB.SetTitle("deltaTOutside30Straight")
                        histC.SetTitle("deltaTOutside30Bent")
                        histD.SetTitle("deltaTWithin30Bent")

                        for hist in [histA,histB,histC,histD]:
                            for iBin in range(1,hist.GetNbinsX()+1):
                                hist.SetBinError(iBin,hist.GetBinContent(iBin)**0.5)
                        histAPred = histB.Clone("APred")
                        histAPred.Multiply(histD)
                        histAPred.Divide(histC)
                        histAPred.SetTitle("deltaTWithin30StraightObs")

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
    nPEStrings = ["","NPEMin","NPEMax"]
    deltaTStrings = ["","DeltaTL3L1","DeltaTL2L1","DeltaTL3L2","min","max"]
    selections = ["NoOtherPulse","NoPrePulse"]
    blind = False
    useSaved = False
    beamString = "noBeam"
    if beamString  == "beam":
        blind = True
    signal = True
    for signalQ in ["0p001","0p002","0p005","0p01","0p02","0p05","0p1"][:2]:
        if not signalQ and signalQ != "0p005":continue
        if signal:
            inputFile = r.TFile("signalInjectionQ"+signalQ+"NoLPFilter.root")
            tag = tagOrig + "Signal"+signalQ
            inputTree = inputFile.Get("t")
            signalNorm = inputTree.GetEntries()
        else:
            tag = tagOrig
            # inputFile = r.TFile("{0}TwoLayerHitsOrThreeSlabHits.root".format(beamString))
            inputFile = r.TFile("{0}ThreeLayerHits.root".format(beamString))
            signalNorm = None
        slabs = [18,20,28]
        outputFile,allPaths = measureBackgrounds(inputFile,blind,beamString,useSaved,nPEStrings,deltaTStrings,selections,slabs,signal)
        makeABCDPredictions(outputFile,beamString,blind,nPEStrings,deltaTStrings,selections,allPaths,signalNorm)

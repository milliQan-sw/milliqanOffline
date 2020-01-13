import ROOT as r
from array import array
import numpy as np
from collections import defaultdict
import collections
import random
from progressbar import *
from measureBackgrounds import layers,preparePaths
from prepareInputsFromDouble import prepareInputsFromDouble
r.gROOT.SetBatch()
channelCalibrations = [33.125, 33.125, 13.75, 25.0, 24.375, 35.0, 30.0, 29.375, 24.375, 33.75, 3.125, 15.625, 26.875, 34.375, 9.375, 0.0, 27.5, 30.0, 0.0, 11.25, 7.5, 12.5, 28.125, 20.625, 33.75, 26.875, -3.125, 8.75, 13.75, 0.0, 14.375]

chanToLayer = {}
for layer,chans in layers.iteritems():
    for chan in chans:
        chanToLayer[chan] = layer

calibrateTime = True

allPaths,paths = preparePaths()
pathsNoSlabs = []
for iP,path in enumerate(paths):
    if not (path in allPaths["Slabs"]):
        pathsNoSlabs.append(path)
paths = pathsNoSlabs
paths = sorted(paths)
# paths = allPaths["ExtraPaths"]
pathsToBeShuffled = [list (x) for x in paths]
rand = r.TRandom3()
mult = 1
binsDeltaT = array('d',np.linspace(-120,120,(192)*2*mult+1))
binWidth = binsDeltaT[1]-binsDeltaT[0]
combos = []
comboLabels = []
totalN = 0
testPulse = [0,0,0]
testPulseLabel = [0,0,0]
timeBins = np.linspace(-120,0,192*mult+1)#int(100/binWidth)+1)
for lastPulse in [1,2,3]:
    testPulse[lastPulse-1] = 0.
    testPulseLabel[lastPulse-1] = 0.
    for testPulseA in timeBins:
        testPulse[lastPulse%3] = testPulseA*1
        testPulseLabel[lastPulse%3] = 1
        for testPulseB in timeBins:
            testPulse[(lastPulse+1)%3] = testPulseB*1
            testPulseLabel[(lastPulse+1)%3] = 1
            if testPulse == [0.,0.,0.]:
                continue
            # if tuple(testPulse) in combos: 
            #     continue
            totalN += 1
            combos.append(tuple(testPulse))
            comboLabels.append(tuple(testPulseLabel))
combos = list(set(combos))
def getSinglesRates(inputTemplatesSingles):
    singlesRates = {}
    for chan in range(32):
        if chan == 15: continue
        inputTemplateHist = inputTemplatesSingles.Get("QuietSinglePulseInChan/"+str(chan))
        #Last bin is inclusive so integrate up to but not including
        singlesRates[chan] = inputTemplateHist.Integral(1,inputTemplateHist.GetNbinsX()-1)
    return singlesRates
# def makeFakeDoublesRates2D(singlesRates,realDoubles):
#     outputHists= {}
#     tempFile = r.TFile("test.root","RECREATE")
#     tempFile.cd()
#     for chans in realDoubles:
#         histName = "double_chans_{0}_{1}_fake2D".format(chans[0],chans[1])
#         outputHist = r.TH2D(histName,"",len(binsDeltaT)-1,binsDeltaT,len(binsDeltaT)-1,binsDeltaT)
#         histName = "double_chans_{0}_{1}_fake3D".format(chans[0],chans[1])
#         outputHist3D = r.TH3D(histName,"",len(binsDeltaT)-1,binsDeltaT,len(binsDeltaT)-1,binsDeltaT,len(binsDeltaT)-1,binsDeltaT)
#         rate = 100*1E-9*singlesRates[chans[0]]*singlesRates[chans[1]]
#         for iBinX in range(1,outputHist.GetNbinsX()+1):
#             for iBinY in range(1,outputHist.GetNbinsY()+1):
#                 binLowX = outputHist.GetXaxis().GetBinLowEdge(iBinX)
#                 binUpX = outputHist.GetXaxis().GetBinUpEdge(iBinX)
#                 binLowY = outputHist.GetYaxis().GetBinLowEdge(iBinY)
#                 binUpY = outputHist.GetYaxis().GetBinUpEdge(iBinY)
#                 maxBinUp = max(binUpX,binUpY)
#                 minBinUp = min(binUpX,binUpY)
#                 minBinLow = min(binLowX,binLowY)
#                 maxBinLow = max(binLowX,binLowY)
#                 maxDelta = maxBinUp-minBinLow
#                 minDelta = minBinUp-maxBinLow
#                 propWith100 = 1
#                 if maxDelta > 100:
#                     propWith100 = 100./(maxDelta-minDelta)
#                 outputHist.SetBinContent(iBinX,iBinY,1*propWith100)
#                 outputHist.SetBinError(iBinX,iBinY,0)
#                 for iBinZ in range(1,outputHist.GetNbinsZ()+1):
#         outputHist.Scale(rate/outputHist.Integral())
#         outputHists[chans] = outputHist
#         outputHist.Write()
#     return outputHists
def makeFakeDoublesRates(singlesRates,realDoubles):
    outputHists= {}
    tempFile = r.TFile("test.root","RECREATE")
    tempFile.cd()
    for chans in realDoubles:
        histName = "double_chans_{0}_{1}_fake".format(chans[0],chans[1])
        outputHist = r.TH1D(histName,"",len(binsDeltaT)-1,binsDeltaT)
        rate = 100*1E-9*singlesRates[chans[0]]*singlesRates[chans[1]]
        for iBin in range(1,outputHist.GetNbinsX()+1):
            if (outputHist.GetBinLowEdge(iBin)<-100 or outputHist.GetXaxis().GetBinUpEdge(iBin)>100): continue
            outputHist.SetBinContent(iBin,1)
            outputHist.SetBinError(iBin,0)
        outputHist.Scale(rate/outputHist.Integral())
        outputHists[chans] = outputHist
        outputHist.Write()
    return outputHists,tempFile
def prepareBlankTemplates(paths,baseHists,tag=""):
    if tag == "" or tag[0] == "_":
        pass
    else:
        tag = "_"+tag
    histDict = defaultdict(list)
    for path in paths:
        for hist in baseHists:
            histClone = hist.Clone("_".join(str(x) for x in path)+"_"+hist.GetName()+tag)
            histDict[path].append(histClone)
    return histDict
def writeOutput(histDictPureSingles,outDirBase,singlesRates,baseHists):
    outDir = outDirBase.mkdir("sep_paths")
    outDir.cd()
    for path,hists in histDictPureSingles.iteritems():
        for hist in hists:
            if hist.Integral() < 1E-9: continue
            hist.Write()
    for pathType,pathsT in allPaths.iteritems():
        if pathType == "Slabs": continue
        outDir = outDirBase.mkdir(pathType)
        outDir.cd()
        histCloneMin = baseHists[0].Clone(pathType+"_"+baseHists[0].GetName())
        histCloneMin.Reset()
        histCloneMax = baseHists[1].Clone(pathType+"_"+baseHists[1].GetName())
        histCloneMax.Reset()
        for path in pathsT:
            if path in histDictPureSingles:
                histCloneMin.Add(histDictPureSingles[path][0])
                histCloneMax.Add(histDictPureSingles[path][1])
        histCloneMin.Write()
        histCloneMax.Write()
def makeTriplePredictionFromDoubles(histDictFromDoubles,chanForSingle,paths,singlesRates,doublesHists,doublesHistsFake):
    layerForSingle = chanToLayer[chanForSingle]
    otherLayers = [1,2,3]
    del otherLayers[layerForSingle-1]

    pathsWithSingle = []
    pathsDoubleChans = []
    layersDoubleChans = []
    for path in paths:
        if chanForSingle in path:
            pathDoubleChans = list(path[:])
            del pathDoubleChans[pathDoubleChans.index(chanForSingle)]
            pathDoubleChans = tuple(sorted(pathDoubleChans))
            if pathDoubleChans not in doublesHists:
                continue
            pathsDoubleChans.append(pathDoubleChans)
            if path in allPaths["ExtraPaths"]:
                layersDoubleChans.append((path.index(pathDoubleChans[0])+1,path.index(pathDoubleChans[1])+1))
            else:
                layersDoubleChans.append(sorted(chanToLayer[x] for x in pathDoubleChans))
            pathsWithSingle.append(path)
    pbar = ProgressBar()
    # for i in range(10000):
    fakeNorm = defaultdict(float)
    for iC,testPulse in enumerate(combos):
        for path,pathDouble,layerDoubleChans in zip(pathsWithSingle,pathsDoubleChans,layersDoubleChans):
            testPulseCalib = list(testPulse)
            testPulseLabel = comboLabels[iC]
            if calibrateTime:
                for chan in path:
                    testPulseCalib[chanToLayer[chan]-1] += channelCalibrations[chan]
            maxDeltaT = max([testPulseCalib[1]-testPulseCalib[0],testPulseCalib[2]-testPulseCalib[1],testPulseCalib[2]-testPulseCalib[0]],key = lambda x: abs(x))
            minDeltaT = min([testPulseCalib[1]-testPulseCalib[0],testPulseCalib[2]-testPulseCalib[1],testPulseCalib[2]-testPulseCalib[0]],key = lambda x: abs(x))
            # totalWeight = doublesHists[pathDouble].GetBinContent(doublesHists[pathDouble].FindBin(testPulseCalib[layerDoubleChans[1]-1]-testPulseCalib[layerDoubleChans[0]-1]))
            blah = doublesHists[pathDouble].GetBinContent(doublesHists[pathDouble].FindFixBin(testPulseCalib[layerDoubleChans[1]-1]-testPulseCalib[layerDoubleChans[0]-1]))
            # print 0.5*binWidth*1E-9*singlesRates[pathDouble[0]]*singlesRates[pathDouble[1]]/blah
            # print
            iBin = doublesHists[pathDouble].FindFixBin(testPulse[layerDoubleChans[1]-1]-testPulse[layerDoubleChans[0]-1])
            if (testPulse[layerDoubleChans[1]-1]-testPulse[layerDoubleChans[0]-1]) == 100:
                iBin -= 1
            totalWeight = doublesHists[pathDouble].GetBinContent(iBin)
            totalWeightFake = doublesHistsFake[pathDouble].GetBinContent(iBin)
            scalingFactor = ((0.5*binWidth*1E-9*singlesRates[chanForSingle]))*3600.
            fakeNorm[path] += totalWeightFake*((0.5*binWidth*1E-9*singlesRates[chanForSingle]))*3600.
            # print totalWeight/((singlesRates[pathDouble[0]]*singlesRates[pathDouble[1]]*100*1E-9)/)
            histDictFromDoubles[path][0].Fill(minDeltaT,totalWeight*scalingFactor)
            histDictFromDoubles[path][1].Fill(maxDeltaT,totalWeight*scalingFactor)
    for pathDouble in pathsDoubleChans:
        pathTriple = tuple(sorted(pathDouble+tuple([chanForSingle])))
        # scalingFactor = 100*1E-9*singlesRates[chanForSingle]*doublesHists[pathDouble].Integral()*3600
        scalingFactor = 100*100*1E-18*singlesRates[chanForSingle]*singlesRates[pathDouble[0]]*singlesRates[pathDouble[1]]*3600#*doublesHists[pathDouble].Integral()*3600
        # print binWidth, scalingFactor/histDictFromDoubles[pathTriple][0].Integral()
        totallyWellMotivatedScaling = scalingFactor/fakeNorm[pathTriple]
        histDictFromDoubles[pathTriple][0].Scale(scalingFactor/fakeNorm[pathTriple])
        histDictFromDoubles[pathTriple][1].Scale(totallyWellMotivatedScaling)
    return histDictFromDoubles

def makeTriplePredictionFromUniform(histDictPureSingles,paths,singlesRates):
    pbar = ProgressBar()
    # for i in range(10000):
    timeBins = np.linspace(-100,0,int(100/binWidth)+1)
    nBins = len(timeBins)
    for testPulse in combos:
        for path in paths:
            testPulseCalib = list(testPulse)
            if calibrateTime:
                for chan in path:
                    testPulseCalib[chanToLayer[chan]-1] += channelCalibrations[chan]
            maxDeltaT = max([testPulseCalib[1]-testPulseCalib[0],testPulseCalib[2]-testPulseCalib[1],testPulseCalib[2]-testPulseCalib[0]],key = lambda x: abs(x))
            minDeltaT = min([testPulseCalib[1]-testPulseCalib[0],testPulseCalib[2]-testPulseCalib[1],testPulseCalib[2]-testPulseCalib[0]],key = lambda x: abs(x))
            scalingFactor = 1#((100*singlesRates[path[0]]*singlesRates[path[1]]*singlesRates[path[2]])/(totalN))*3600.
            histDictPureSingles[path][0].Fill(minDeltaT,scalingFactor)
            histDictPureSingles[path][1].Fill(maxDeltaT,scalingFactor)
    for path in paths:
        scalingFactor = (100*100*1E-18*singlesRates[path[0]]*singlesRates[path[1]]*singlesRates[path[2]])*3600.
        histDictPureSingles[path][0].Scale(scalingFactor/histDictPureSingles[path][0].Integral())
        histDictPureSingles[path][1].Scale(scalingFactor/histDictPureSingles[path][1].Integral())
    return histDictPureSingles

def makeTriplePrediction():
    singlesRates = getSinglesRates(r.TFile("nPEValidationUnbiased.root"))
    temp,doublesHistsReal = prepareInputsFromDouble(True)
    doublesHistsFake,_ = makeFakeDoublesRates(singlesRates,doublesHistsReal)
    # test = makeFakeDoublesRates2D(singlesRates,doublesHistsReal)
    # histAll = r.TH1D("all","all",len(binsDeltaT)-1,binsDeltaT)
    histMin = r.TH1D("min","min",len(binsDeltaT)-1,binsDeltaT)
    histMax = r.TH1D("max","max",len(binsDeltaT)-1,binsDeltaT)
    # histTest = r.TH1D("test","test",len(binsDeltaT)-1,binsDeltaT)
    baseHists = [histMin,histMax]#,histAll]

    outFile = r.TFile("templatesCalibTimeUniformTEST.root","RECREATE")
    histDictFromUniform = prepareBlankTemplates(paths,baseHists)
    histDictFromUniform = makeTriplePredictionFromUniform(histDictFromUniform,paths,singlesRates)
    writeOutput(histDictFromUniform,outFile,singlesRates=singlesRates,baseHists=baseHists)
    exit()

    histDictFromDoubles = prepareBlankTemplates(paths,baseHists)
    chansForSingle = []
    for doubleChans in histDictFromDoubles:
        chansForSingle.append(doubleChans[0])
        chansForSingle.append(doubleChans[1])
        chansForSingle.append(doubleChans[2])
    chansForSingle = sorted(list(set(chansForSingle)))
    outFile = r.TFile("templatesCalibTimeDoublesScaledTEST.root","RECREATE")
    for chanForSingle in chansForSingle:
        histDictFromDoubles = prepareBlankTemplates(paths,baseHists)
        histDictFromDoubles = makeTriplePredictionFromDoubles(histDictFromDoubles,chanForSingle,paths,singlesRates,doublesHistsReal,doublesHistsFake)
        # histDictFromDoubles = makeTriplePredictionFromDoubles(histDictFromDoubles,chanForSingle,paths,singlesRates,doublesHists2D)
        outDir = outFile.mkdir(str(chanForSingle))
        writeOutput(histDictFromDoubles,outDir,singlesRates=singlesRates,baseHists=baseHists)

if __name__ =="__main__":
   makeTriplePrediction()


import ROOT as r
from array import array
import numpy as np
from collections import defaultdict
import random
from progressbar import *
from measureBackgrounds import layers,preparePaths
r.gROOT.SetBatch()
channelCalibrations = [33.125, 33.125, 13.75, 25.0, 24.375, 35.0, 30.0, 29.375, 24.375, 33.75, 3.125, 15.625, 26.875, 34.375, 9.375, 0.0, 27.5, 30.0, 0.0, 11.25, 7.5, 12.5, 28.125, 20.625, 33.75, 26.875, -3.125, 8.75, 13.75, 0.0, 14.375]

chanToLayer = {}
for layer,chans in layers.iteritems():
    for chan in chans:
        chanToLayer[chan] = layer

calibrateTime = True

allPaths,paths = preparePaths()
pathsToBeShuffled = [list (x) for x in paths]
rand = r.TRandom3()
binsDeltaT = array('d',np.linspace(-300,300,241))
binWidth = binsDeltaT[1]-binsDeltaT[0]
def getSinglesRates(inputTemplatesSingles):
    singlesRates = {}
    for chan in range(32):
        if chan == 15: continue
        inputTemplateHist = inputTemplatesSingles.Get("QuietSinglePulseInChan/"+str(chan))
        #Last bin is inclusive so integrate up to but not including
        singlesRates[chan] = inputTemplateHist.Integral(1,inputTemplateHist.GetNbinsX()-1)
    return singlesRates
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
def makeTriplePrediction():
    triggeringPulseTime = 0
    singlesRates = getSinglesRates(r.TFile("nPEValidationUnbiased.root"))
    # histAll = r.TH1D("all","all",len(binsDeltaT)-1,binsDeltaT)
    histMin = r.TH1D("min","min",len(binsDeltaT)-1,binsDeltaT)
    histMax = r.TH1D("max","max",len(binsDeltaT)-1,binsDeltaT)
    baseHists = [histMin,histMax]#,histAll]
    histDictPureSinglesFromUniform = prepareBlankTemplates(paths,baseHists)
    histDictPureSinglesFromUniform = makeTriplePredictionFromUniform(histDictPureSinglesFromUniform,paths)
    writeOutput(histDictPureSinglesFromUniform,fileName="templatesCalibTimeUniform.root",singlesRates=singlesRates,baseHists=baseHists)

def writeOutput(histDictPureSingles,fileName,singlesRates,baseHists):
    outFile = r.TFile(fileName,"RECREATE")
    outDirSingles = outFile#.mkdir("PureSingles")
    outDir = outDirSingles.mkdir("sep_paths")
    outDir.cd()
    for path,hists in histDictPureSingles.iteritems():
        scalingFactor = (100*100*1E-18*singlesRates[path[0]]*singlesRates[path[1]]*singlesRates[path[2]])*3600.
        for hist in hists:
            hist.Scale(scalingFactor/hist.Integral())
            hist.Write()
    for pathType,pathsT in allPaths.iteritems():
        if pathType == "Slabs": continue
        outDir = outDirSingles.mkdir(pathType)
        outDir.cd()
        histCloneMin = baseHists[0].Clone(pathType+"_"+baseHists[0].GetName())
        histCloneMin.Reset()
        histCloneMax = baseHists[1].Clone(pathType+"_"+baseHists[1].GetName())
        histCloneMax.Reset()
        for path in pathsT:
            histCloneMin.Add(histDictPureSingles[path][0])
            histCloneMax.Add(histDictPureSingles[path][1])
        histCloneMin.Write()
        histCloneMax.Write()
    outFile.Close()
def makeTriplePredictionFromToys(histDictPureSingles,paths):
    for i in pbar(range(10000)):
        maxDeltaT = 1000
        while abs(maxDeltaT) > 100:
            test1 = rand.Uniform(-1000,1000)
            test2 = rand.Uniform(-1000,1000)
            test3 = rand.Uniform(-1000,1000)
            maxDeltaT = max([test2-test1,test3-test2,test1-test3],key = lambda x:abs(x))

        for path in paths:
            tests = [test1*1,test2*1,test3*1]
            # if paths[iP] == (3,16,24):
            #     print path,paths[iP]
            # random.shuffle(path)
            if calibrateTime:
                for chan in path:
                    tests[chanToLayer[chan]-1] += channelCalibrations[chan]
            minDeltaT = min([tests[1]-tests[0],tests[2]-tests[1],tests[2]-tests[0]],key = lambda x:abs(x))
            maxDeltaT = max([tests[1]-tests[0],tests[2]-tests[1],tests[2]-tests[0]],key = lambda x:abs(x))
            histDictPureSingles[path][0].Fill(minDeltaT)
            histDictPureSingles[path][1].Fill(maxDeltaT)

def makeTriplePredictionFromUniform(histDictPureSingles,paths):
    pbar = ProgressBar()
    # for i in range(10000):
    timeBins = np.linspace(-100,0,int(100/binWidth)+1)
    testPulse = [0,0,0]
    combos = []
    for lastPulse in [1,2,3]:
        testPulse[lastPulse-1] = 0
        for testPulseA in timeBins:
            testPulse[lastPulse%3] = testPulseA*1
            for testPulseB in timeBins:
                testPulse[(lastPulse+1)%3] = testPulseB*1
                if tuple(testPulse) in combos:
                    continue
                combos.append(tuple(testPulse))
                for path in paths:
                    testPulseCalib = testPulse[:]
                    if calibrateTime:
                        for chan in path:
                            testPulseCalib[chanToLayer[chan]-1] += channelCalibrations[chan]
                    maxDeltaT = max([testPulseCalib[1]-testPulseCalib[0],testPulseCalib[2]-testPulseCalib[1],testPulseCalib[2]-testPulseCalib[0]],key = lambda x: abs(x))
                    minDeltaT = min([testPulseCalib[1]-testPulseCalib[0],testPulseCalib[2]-testPulseCalib[1],testPulseCalib[2]-testPulseCalib[0]],key = lambda x: abs(x))

                    histDictPureSingles[path][0].Fill(minDeltaT)
                    histDictPureSingles[path][1].Fill(maxDeltaT)
    return histDictPureSingles

if __name__ =="__main__":
   makeTriplePrediction()


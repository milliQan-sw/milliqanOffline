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
durationMap = {}
for i in range(32):
    durationMap[i] = 13
durationMap[24] = 0
durationMap[25] = 0
durationMap[9] = 0
durationMap[17] = 0
durationMap[22] = 0
durationMap[5] = 0
def measureDoubleRateHeight(inputTree,window,chans,heightLow,heightHigh,quietInRest=False,singlePulseAboveThreshInChan=False,singlePulseInChan=False):
    height = [heightLow,heightHigh]
    histName = "Chans_{0}_{1}_NPE_{2}_{3}".format(chans[0],chans[1],height[0],height[0])
    outputHist = r.TH1D(histName,"",320,0,400)
    durations = []
    for chan in chans:
        durations.append(durationMap[chan])

    extraSel = ""
    if quietInRest:
        extraSel += "&&MaxIf$(height,chan!={0}&&chan!={1}&&chan!=30)<0.1".format(*chans)
        # extraSel += "&&MaxIf$(height,chan!={0}&&chan!={1}&&chan!=30)<0.1".format(*chans)
    if singlePulseAboveThreshInChan:
        extraSel += "&&Sum$(chan=={1}&&height>{2}&&height<{3}&&duration>={5})==1&&Sum$(chan=={0}&&height>{2}&&height<{3}&&duration>={4})==1".format(chans[0],chans[1],height[0],height[1],durations[0],durations[1])
    if singlePulseInChan:
        extraSel += "&&Sum$(chan=={1}&&height>0.1&&duration>={3})==1&&Sum$(chan=={0}&&height>0.1&&duration>={2})==1".format(chans[0],chans[1],durations[0],durations[1])

    inputTree.Draw("abs(MinIf$(time,chan=={0}&&height>{2}&&height<{3}&&duration>={4})-MinIf$(time,chan=={1}&&height>{2}&&height<{3}&&duration>={5}))>>".format(chans[0],chans[1],height[0],height[1],durations[0],durations[1])+histName,"groupTDC_b1[0]==groupTDC_b0[0]&&MinIf$(time,chan=={0}&&height>{2}&&height<{3}&&duration>={4})>60&&MinIf$(time,chan=={1}&&height>{2}&&height<{3}&&duration>={5})>60{6}".format(chans[0],chans[1],height[0],height[1],durations[0],durations[1],extraSel))
    totalTime = inputTree.GetMaximum("event_time_fromTDC")-inputTree.GetMinimum("event_time_fromTDC")
    nEntries = inputTree.GetEntries()
    nEntriesEff = inputTree.Draw("","groupTDC_b1[0]==groupTDC_b0[0]","goff")
    totalTime *= nEntriesEff*1./nEntries
    outputHist.Scale(1./totalTime)
    doubleRate = outputHist.Integral(outputHist.FindBin(window[0]),outputHist.FindBin(window[1])-1)
    doubleRateError = doubleRate**0.5*(totalTime)**-0.5
    return outputHist,ufloat(doubleRate,doubleRateError)
def measureDoubleRateNPE(inputTree,window,chans,nPELow,nPEHigh,quietInRest=False,singlePulseAboveThreshInChan=False,singlePulseInChan=False,noPrePulse=False):
    nPE = [nPELow,nPEHigh]
    histName = "Chans_{0}_{1}_NPE_{2}_{3}".format(chans[0],chans[1],nPE[0],nPE[0]).replace(".","p")
    outputHist = r.TH1D(histName,"",320,0,400)
    durations = []
    for chan in chans:
        durations.append(durationMap[chan])

    extraSel = ""
    if quietInRest:
        extraSel += "&&MaxIf$(nPE,chan!={0}&&chan!={1}&&chan!=30)<0.1".format(*chans)
    if singlePulseAboveThreshInChan:
        extraSel += "&&Sum$(chan=={1}&&nPE>{2}&&nPE<{3})==1&&Sum$(chan=={0}&&nPE>{2}&&nPE<{3})==1".format(chans[0],chans[1],nPE[0],nPE[1])
    if singlePulseInChan:
        extraSel += "&&Sum$(chan=={1})==1&&Sum$(chan=={0})==1".format(chans[0],chans[1])
    if noPrePulse:
        extraSel += "&&Sum$(chan=={0}&&time<160)==0&&Sum$(chan=={1}&&time<160)==0".format(chans[0],chans[1])

    inputTree.Draw("abs(MinIf$(time,chan=={0}&&nPE>{2}&&nPE<{3})-MinIf$(time,chan=={1}&&nPE>{2}&&nPE<{3}))>>".format(chans[0],chans[1],nPE[0],nPE[1])+histName,"groupTDC_b1[0]==groupTDC_b0[0]&&MinIf$(time,chan=={0}&&nPE>{2}&&nPE<{3})>60&&MinIf$(time,chan=={1}&&nPE>{2}&&nPE<{3})>60{4}".format(chans[0],chans[1],nPE[0],nPE[1],extraSel))
    totalTime = inputTree.GetMaximum("event_time_fromTDC")-inputTree.GetMinimum("event_time_fromTDC")
    nEntries = inputTree.GetEntries()
    nEntriesEff = inputTree.Draw("","groupTDC_b1[0]==groupTDC_b0[0]","goff")
    totalTime *= nEntriesEff*1./nEntries
    outputHist.Scale(1./totalTime)
    doubleRate = outputHist.Integral(outputHist.FindBin(window[0]),outputHist.FindBin(window[1])-1)
    doubleRateError = doubleRate**0.5*(totalTime)**-0.5
    return outputHist,ufloat(doubleRate,doubleRateError)
def measureDoubleRateAllFiles(outputFile,inputFiles,nPEs,window,quietInRest,singlePulseAboveThreshInChan,singlePulseInChan,noPrePulse):
    inDir = "/Users/mcitron/milliqanOffline/milliqanScripts/dcRuns/"
    doubleRates = {}
    for nPELow,nPEHigh in zip(nPEs,nPEs[1:]+[9999]):
        for chans,inputFileName in inputFiles.items():
            inputFile = r.TFile(inDir+"/"+inputFileName)
            inputTree = inputFile.Get("t")
            # outputHist,rate = measureDoubleRate(inputTree,window,chans,nPE,quietInRest,singlePulseAboveThreshInChan,singlePulseInChan)
            outputHist,rate = measureDoubleRateNPE(inputTree,window,chans,nPELow,nPEHigh,quietInRest,singlePulseAboveThreshInChan,singlePulseInChan,noPrePulse)
            doubleRates[nPELow,chans] = rate
            outputFile.cd()
            outputHist.Write()
    return doubleRates
def getDavidData(source):
    davidData = np.loadtxt(source,delimiter=",")
    graph = r.TGraph(len(davidData),array('d',davidData[:,0].astype(int)),array('d',davidData[:,1]))
    graph.SetName("davidData")
    return graph
def makeInputDict(source):
    inputDictTemp = {}
    with open(source) as f:
        for line in f.readlines():
            if "DC" in line:
                regex = re.compile('CH([0-9]*)')
                chans = regex.findall(line)
                if len(chans) == 2:
                    chans = [int(chans[0]),int(chans[1])]

                runNum = line.split("Run ")[-1].rstrip()
                inputDictTemp[tuple(sorted(chans))] = "Run"+runNum+".root"
                # inputDict.
    inputDict = odict()
    for key in sorted(inputDictTemp.keys()):
        inputDict[key] = inputDictTemp[key]
    return inputDict
def findLoops(inputDict):
    allChans = []
    for chanA,chanB in inputDict:
        allChans.append(chanA)
        allChans.append(chanB)
    allChans = list(set(allChans))
    loopDict = defaultdict(list)
    for chanA in allChans:
        for chanB in allChans:
            for chanC in allChans:
                if tuple(sorted([chanA,chanB])) in inputDict:
                    if tuple(sorted([chanB,chanC])) in inputDict:
                        if tuple(sorted([chanA,chanC])) in inputDict:
                            if tuple(sorted([chanB,chanC])) not in loopDict[chanA]:
                                if chanB == 4 or chanB == 6: continue
                                if chanC == 4 or chanC == 6: continue
                                loopDict[chanA].append(tuple(sorted([chanB,chanC])))
    return loopDict,allChans
def findSingleRates(loopDict,doubleRates,nPE,window):
    windowLength = (window[1]-window[0])*1E-9
    xPoints = []
    yPoints = []
    yPointsErr = []
    outputHistsPerChannel = []
    yPointsFull = []
    yPointsFullErr = []
    xPointsFull = []
    for chan,loops in loopDict.items():
        outputHistPerChannel = r.TH1D(str(chan)+"PerLoopRates",";chans",len(loops),0,len(loops))
        for iBin in range(1,len(loops)+1):
            outputHistPerChannel.GetXaxis().SetBinLabel(iBin," ".join(str(x) for x in loops[iBin-1]))
        yPointsSingle = []
        xPointsFull.append(chan)
        for iL,loop in enumerate(loops):
            if doubleRates[nPE,tuple(sorted(loop))] > 0:
                singleRate = (1./windowLength * doubleRates[nPE,tuple(sorted([chan,loop[0]]))]*doubleRates[nPE,tuple(sorted([chan,loop[1]]))]/doubleRates[nPE,tuple(sorted(loop))])**0.5
            else:
                singleRate = ufloat(0,0)
            yPointsSingle.append(singleRate)
            xPoints.append(chan)
            yPoints.append(singleRate.n)
            yPointsErr.append(singleRate.s)
            outputHistPerChannel.SetBinContent(iL+1,singleRate.n)
            outputHistPerChannel.SetBinError(iL+1,singleRate.s)
        mean = sum(yPointsSingle)/len(yPointsSingle)
        yPointsFull.append(mean.n)
        yPointsFullErr.append(mean.s)
        outputHistsPerChannel.append(outputHistPerChannel)
    outputGraph = r.TGraphErrors(len(xPoints),array('d',xPoints),array('d',yPoints),array('d',[0]*len(xPoints)),array('d',yPointsErr))
    outputGraph.SetName("SingleRateNPE{0}_split".format(nPE))
    outputGraphFull = r.TGraphErrors(len(xPointsFull),array('d',xPointsFull),array('d',yPointsFull),array('d',[0]*len(xPointsFull)),array('d',yPointsFullErr))
    outputGraphFull.SetName("SingleRateNPE{0}".format(nPE))
    return outputGraphFull,outputGraph,outputHistsPerChannel
if __name__ == "__main__":
    opts = [True,False]
    for quietInRest in opts:
        for singlePulseAboveThreshInChan in [False]:
            for singlePulseInChan in opts:
                for noPrePulse in opts:
                    optString = ""
                    if singlePulseInChan and singlePulseAboveThreshInChan: continue
                    if noPrePulse and singlePulseInChan: continue
                    if noPrePulse and singlePulseAboveThreshInChan: continue
                    if quietInRest:
                        optString += "Quiet"
                    if singlePulseInChan:
                        optString += "SinglePulseInChan"
                    if singlePulseAboveThreshInChan:
                        optString += "SinglePulseAboveThreshInChan"
                    if noPrePulse:
                        optString += "NoPrePulse"
                    print ("Running Opts: "+optString)
                    window = [100,200]
                    source = "source.txt"
                    inputDict = makeInputDict(source)
                    loopDict,allChans = findLoops(inputDict)
                    outputFile = r.TFile("measureSingleRateFromDoubleNPEBinned{0}.root".format(optString),"RECREATE")
                    nPEs = [0.5,2,5,10,20,50,100]
                    colours = [r.kBlack,r.kRed,r.kBlue,r.kGreen+1,r.kMagenta,r.kCyan,r.kYellow+1]
                    doubleRates=measureDoubleRateAllFiles(outputFile,inputDict,nPEs,window,quietInRest,singlePulseAboveThreshInChan,singlePulseInChan,noPrePulse)
                    outputFile.cd()
                    dummyHist = r.TH1D("dummy","",len(allChans)+3,-1,len(allChans)+2)
                    outCanvas = r.TCanvas()
                    outCanvas.cd()
                    outCanvas.SetLogy()
                    dummyHist.SetMaximum(6E4)
                    dummyHist.SetMinimum(1E2)
                    dummyHist.Draw()
                    mg = r.TMultiGraph()
                    leg = r.TLegend(0.65,0.7,0.89,0.89)
                    leg.SetBorderSize(0)
                    for colour,nPELow,nPEHigh in zip(colours,nPEs,nPEs[1:]+[9999]):
                        nPEDir = outputFile.mkdir("nPE_{0}".format(nPELow))
                        nPEDir.cd()
                        outputGraph,outputGraphSplit,outputHistsPerChannel = findSingleRates(loopDict,doubleRates,nPELow,window)
                        outputGraph.SetMarkerColor(colour)
                        outputGraph.SetLineColor(colour)
                        leg.AddEntry(outputGraph,"nPE: {0} - {1}".format(nPELow,nPEHigh))
                        outputGraph.Write()
                        mg.Add(outputGraph)
                        for hist in outputHistsPerChannel:
                            hist.Write()
                    # davidData = getDavidData("davidData.txt")
                    # davidData.SetMarkerStyle(5)
                    # davidData.SetMarkerColor(6)
                    # davidData.SetLineColor(6)
                    # leg.AddEntry(davidData,"David data","P")
                    # mg.Add(davidData)
                    mg.Draw("P")
                    leg.Draw("same")
                    outCanvas.SaveAs("singlesRatesDoubleNPEBinnned{0}.pdf".format(optString))

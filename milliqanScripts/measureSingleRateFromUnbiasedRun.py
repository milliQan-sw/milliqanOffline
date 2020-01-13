import ROOT as r
import pickle
import os,re
import numpy as np
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(0)
from uncertainties import ufloat
from collections import defaultdict
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
layerDict = {}
layerDict[18] = 0
for ic in [0,1,24,25,8,9,10,27,29,20]:
    layerDict[ic] = 1
for ic in [6,7,16,17,12,13,11,19,30,28]:
    layerDict[ic] = 2
for ic in [2,3,22,23,4,5,28,14,31,26,21]:
    layerDict[ic] = 3

def measureSingleRateFromUnbiasedRunNPE(totalTime,inputTree,nPEs,quietInRest,singlePulseAboveThreshInChan,singlePulseInChan,noPrePulse,noEarlyPulse,outputDir):
    chans = list(range(15))+list(range(16,32))
    # chans = [0,1,24,25,8,9,6,7,16,17,12,13,2,3,22,23,4,5]
    print (chans)
    totalTime = nEvTotal*400E-9
    outputHists = {}
    for chan in chans:
        extraSel = ""
        if quietInRest:
            layer = layerDict[chan]
            # extraSel += "&&MaxIf$(nPE,chan!={0}&&chan!=30&&layer=={1}&&chan!=15)<0.1&&Max$(sideband_RMS,Iteration$!=15)<1.3".format(chan,layer)
            extraSel += "&&MaxIf$(nPE,chan!={0}&&chan!=30&&chan!=15)<0.1&&MaxIf$(sideband_RMS,Iteration$!=15)<1.3".format(chan)
        if singlePulseAboveThreshInChan:
            raise NotImplemented
        if singlePulseInChan:
            extraSel += "&&Sum$(chan=={0})==1".format(chan)
        if noPrePulse:
            extraSel += "&&Sum$(chan=={0}&&time<MaxIf$(time,chan=={0}&&nPE==MaxIf$(nPE,chan=={0}&&time>160&&time<560)))==0".format(chan)
        if noEarlyPulse:
            extraSel += "&&Sum$(chan=={0}&&time<160)==0".format(chan)
        outputHist = r.TH1D(str(chan),"nPE",len(nPEs)+0,array('d',nPEs+[nPEs[-1]+50]))
        inputTree.Draw("MaxIf$(nPE,chan=="+str(chan)+"&&time>160&&time<560)>>"+outputHist.GetName(),"groupTDC_b1[0]==groupTDC_b0[0]&&Sum$(chan=={0}&&time>160&&time<560)>=1".format(chan)+extraSel)
        outputHist.SetDirectory(0)
        outputHists[chan] = outputHist
    outputGraphs = {}
    for iBin in range(1,len(nPEs)+1):
        xPoints = []
        yPoints = []
        yPointsErr = []
        for chan in chans:
            nEvPass = outputHists[chan].GetBinContent(iBin)
            singleRate = ufloat(nEvPass,nEvPass**0.5)/totalTime
            xPoints.append(chan)
            yPoints.append(singleRate.n)
            yPointsErr.append(singleRate.s)
        nPELow = nPEs[iBin-1]
        outputGraph = r.TGraphErrors(len(xPoints),array('d',xPoints),array('d',yPoints),array('d',[0]*len(xPoints)),array('d',yPointsErr))
        outputGraph.SetName("SingleRateNPE{0}".format(nPELow).replace(".","p"))
        outputGraphs[nPELow] = outputGraph
    outputDir.cd()
    for outputHist in outputHists.values():
        outputHist.Scale(1./totalTime)
        outputHist.Write()
    return outputGraphs
def measureSingleRateVsRunNumber(totalTimeHist,inputTree,npeMin,quietInRest,singlePulseAboveThreshInChan,singlePulseInChan,noPrePulse,noEarlyPulse,outputDir):
    totalTime = nEvTotal*400E-9
    # chans = [0,1,24,25,8,9,6,7,16,17,12,13,2,3,22,23,4,5]
    chans = list(range(15))+list(range(16,32))
    outputHists = {}
    for chan in chans:
        extraSel = ""
        if quietInRest:
            layer = layerDict[chan]
            # extraSel += "&&MaxIf$(nPE,chan!={0}&&chan!=30&&layer=={1}&&chan!=15)<0.1&&MaxIf$(sideband_RMS,Iteration$!=15)<1.3".format(chan,layer)
            extraSel += "&&MaxIf$(nPE,chan!={0}&&chan!=30&&chan!=15)<0.1&&MaxIf$(sideband_RMS,Iteration$!=15)<1.3".format(chan)
        if singlePulseAboveThreshInChan:
            raise NotImplemented
        if singlePulseInChan:
            extraSel += "&&Sum$(chan=={0})==1".format(chan)
        if noPrePulse:
            extraSel += "&&Sum$(chan=={0}&&time<MaxIf$(time,chan=={0}&&nPE==MaxIf$(nPE,chan=={0}&&time>160&&time<560)))==0".format(chan)
        if noEarlyPulse:
            extraSel += "&&Sum$(chan=={0}&&time<160)==0".format(chan)
        outputHist = r.TH1D(str(chan),";runs;",2000,0,2000)
        totalN = inputTree.Draw("run>>"+outputHist.GetName(),"groupTDC_b1[0]==groupTDC_b0[0]&&run!=1402&&Sum$(chan=={0}&&nPE>{1}&&time>160&&time<560)>=1".format(chan,npeMin)+extraSel)
        print ("groupTDC_b1[0]==groupTDC_b0[0]&&run!=1402&&Sum$(chan=={0}&&nPE>{1}&&time>160&&time<560".format(chan,npeMin)+extraSel)
        # print (chan,totalN)
        outputHist.SetDirectory(0)
        outputHists[chan] = outputHist
    # outputGraphs = {}
    # for chan in chans:
    # for iBin in range(1,len(nPEs)+1):
    #     xPoints = []
    #     yPoints = []
    #     yPointsErr = []
    #     for chan in chans:
    #         nEvPass = outputHists[chan].GetBinContent(iBin)
    #         singleRate = ufloat(nEvPass,nEvPass**0.5)/totalTime
    #         xPoints.append(chan)
    #         yPoints.append(singleRate.n)
    #         yPointsErr.append(singleRate.s)
    #     nPELow = nPEs[iBin-1]
    #     outputGraph = r.TGraphErrors(len(xPoints),array('d',xPoints),array('d',yPoints),array('d',[0]*len(xPoints)),array('d',yPointsErr))
    #     outputGraph.SetName("SingleRateNPE{0}".format(nPELow).replace(".","p"))
    #     outputGraphs[nPELow] = outputGraph
    outputDir.cd()
    for outputHist in outputHists.values():
        outputHist.Divide(totalTimeHist)
        outputHist.Write()
    return 
def makeValidation(chan,target):
    targetHist = r.TH1D("unbiased_"+str(chan)+"_L1","",1000,0,1000)
    target.Draw("MaxIf$(height,chan=={0}&&time>160&&time<560)>>".format(chan)+targetHist.GetName(),"groupTDC_b1[0]==groupTDC_b0[0]&&MaxIf$(height,chan=={0}&&time>160&&time<560)>0".format(chan))
    nEntriesEff = target.Draw("","groupTDC_b1[0]==groupTDC_b0[0]","goff")
    targetHist.Scale(1./(400.E-9*nEntriesEff))
    targetHist.Rebin(4)
    targetHist.SetLineColor(r.kBlack)
    return targetHist
if __name__ =='__main__':
    opts = [True,False][:1]
    inputFileFull = r.TFile("allZeroBias.root")
    inputTreeFull = inputFileFull.Get("t")
    totalTimeHist = r.TH1D("totalTime",";runs;",2000,0,2000)
    nEvTotal = inputTreeFull.Draw("run>>"+totalTimeHist.GetName(),"groupTDC_b1[0]==groupTDC_b0[0]")
    totalTime = nEvTotal*400E-9
    totalTimeHist.Scale(400E-9)
    print (nEvTotal)
    inputFile = r.TFile("allZeroBiasWithBarOrSlabOrPanelHit.root")
    inputTree = inputFile.Get("t")
    # outputFileValidation = r.TFile("measureSingleRateFromUnbiasedRunValidationAllUnbiasedHeight.root","RECREATE")
    # del chans[15]
    # for chan in chans:
    #     outputPlot = makeValidation(chan,inputTree)
    #     outputPlot.Write()
    # outputFileValidation.Close()
    outputFileNPEValidation = r.TFile("nPEValidationUnbiasedRate.root","RECREATE")
    for quietInRest in [True]:
        for singlePulseAboveThreshInChan in [False]:
            for singlePulseInChan in [True]:
                for noPrePulse in [False]:
                    for noEarlyPulse in [False]:
                        optString = ""
                        if singlePulseInChan and singlePulseAboveThreshInChan: continue
                        if noPrePulse and singlePulseInChan: continue
                        if noPrePulse and singlePulseAboveThreshInChan: continue
                        if noEarlyPulse and singlePulseInChan: continue
                        if noEarlyPulse and singlePulseAboveThreshInChan: continue
                        if noEarlyPulse and noPrePulse: continue
                        if quietInRest:
                            optString += "Quiet"
                        if singlePulseInChan:
                            optString += "SinglePulseInChan"
                        if singlePulseAboveThreshInChan:
                            optString += "SinglePulseAboveThreshInChan"
                        if noPrePulse:
                            optString += "NoPrePulse"
                        if noEarlyPulse:
                            optString += "NoEarlyPulse"
                        print ("Running Opts: "+optString)
                        outputFile = r.TFile("measureSingleRateFromUnbiasedAllUnbiasedNPE{0}BinnedAsSignal.root".format(optString),"RECREATE")
                        if optString != "":
                            outputDirValidation = outputFileNPEValidation.mkdir(optString)
                        else:
                            outputDirValidation = outputFileNPEValidation.mkdir("Base")
                        nPEs = [0,0.5,1.5,5,10,20,50,100,1000,10000]
                        # nPEs = [0,0.5,1.5,5,10,20,50,100,1000,10000]
                        # nPEs = [0,100]
                        npeMin = 0
                        outputDirValidationVsRun = outputDirValidation.mkdir("RunNumber")
                        measureSingleRateVsRunNumber(totalTimeHist,inputTree,npeMin,quietInRest,singlePulseAboveThreshInChan,singlePulseInChan,noPrePulse,noEarlyPulse,outputDirValidationVsRun)

                        # nPEs = [0,0.5,1.5,5,10,20,50,100,1000,10000]
                        colours = [r.kBlack,r.kRed,r.kBlue,r.kGreen+1,r.kMagenta,r.kCyan,r.kYellow+1,r.kGray,r.kOrange,r.kCyan+1]
                        outCanvas = r.TCanvas()
                        outCanvas.cd()
                        outCanvas.SetLogy()
                        dummyHist = r.TH1D("dummy",";Channel; Rate [hz]",33,-1,32)
                        dummyHist.SetMaximum(6E4)
                        dummyHist.SetMinimum(1E2)
                        dummyHist.Draw()
                        mg = r.TMultiGraph()
                        mg.SetTitle(";Channel; Rate [hz]")
                        leg = r.TLegend(0.55,0.65,0.89,0.89)
                        leg.SetBorderSize(0)
                        outputDirValidationVsNPE = outputDirValidation.mkdir("NPE")
                        outputGraphs = measureSingleRateFromUnbiasedRunNPE(totalTime,inputTree,nPEs,quietInRest,singlePulseAboveThreshInChan,singlePulseInChan,noPrePulse,noEarlyPulse,outputDirValidationVsNPE)
                        for colour,nPELow,nPEHigh in zip(colours,nPEs,nPEs[1:]+[99999]):
                            print (nPELow,nPEHigh)
                            nPEDir = outputFile.mkdir("nPE_{0}".format(nPELow))
                            nPEDir.cd()
                            outputGraph = outputGraphs[nPELow]
                            outputGraph.SetMarkerColor(colour)
                            outputGraph.SetLineColor(colour)
                            outputGraph.Write()
                            mg.Add(outputGraph)
                            if nPEHigh < 99999:
                                leg.AddEntry(outputGraph,"NPE {0} to {1}".format(nPELow,nPEHigh))
                            else:
                                leg.AddEntry(outputGraph,"NPE {0} to Inf".format(nPELow,nPEHigh))
                        mg.Draw("Psame")
                        leg.Draw("same")
                        outCanvas.SaveAs("singlesRatesUnbiased{0}HeightAllUnbiasedBinnedAsSignal.pdf".format(optString))

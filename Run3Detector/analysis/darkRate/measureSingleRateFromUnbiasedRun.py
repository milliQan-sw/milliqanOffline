import ROOT as r
import pickle
import os,re
# import numpy as np
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(0)
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

def measureSingleRateFromUnbiasedRunNPE(totalTime,inputTree,heights,quietInRest,singlePulseAboveThreshInChan,singlePulseInChan,noPrePulse,noEarlyPulse,outputDir):
    chans = list(range(80))
    chans.pop(4)
    # chans = [0,1,24,25,8,9,6,7,16,17,12,13,2,3,22,23,4,5]
    print (chans)
    totalTime = nEvTotal*2000E-9
    outputHists = {}
    for chan in chans:
        pulseQual = ["!(height < 25. && duration < 4.6*(height-12.))",
        "!(height >= 25. && duration < 60.)",
        "!(0.001*area < 0.4 && duration < 150.*(0.001*area))",
        "!(0.001*area >= 0.4 && duration < 60.)",
        "!(height > 17. && 0.001*area < 0.04*(height-17.))"]
        pulseQual = "&&".join(pulseQual)
        # pulseQual = "!"+pulseQual
        # pulseQual = "1"

        extraSel = ""
        if quietInRest:
            extraSel += "&&MaxIf$(height,chan!={0}&&chan!=74)<0.1&&MaxIf$(sideband_RMS)<1.3".format(chan)
        if singlePulseAboveThreshInChan:
            raise NotImplemented
        if singlePulseInChan:
            extraSel += "&&Sum$(chan=={0})==1".format(chan)
        if noPrePulse:
            extraSel += "&&Sum$(chan=={0}&&time<MaxIf$(time,chan=={0}&&height==MaxIf$(height,chan=={0}&&time>200&&time<2200)))==0".format(chan)
        if noEarlyPulse:
            extraSel += "&&Sum$(chan=={0}&&time<160)==0".format(chan)
        outputHist = r.TH1D(str(chan),"height",len(heights)+0,array('d',heights+[heights[-1]+50]))
        inputTree.Draw("MaxIf$(height,chan=="+str(chan)+"&&time>200&&time<2200&&("+pulseQual+"))>>"+outputHist.GetName(),"Sum$(chan=={0}&&time>200&&time<2200&&({1}))>=1".format(chan,pulseQual)+extraSel)
        outputHist.SetDirectory(0)
        outputHists[chan] = outputHist
    outputGraphs = {}
    for iBin in range(1,len(heights)+1):
        xPoints = []
        yPoints = []
        yPointsErr = []
        for chan in chans:
            nEvPass = outputHists[chan].GetBinContent(iBin)
            singleRate = nEvPass/totalTime
            singleRateUnc = nEvPass**0.5/totalTime
            xPoints.append(chan)
            yPoints.append(singleRate)
            yPointsErr.append(singleRateUnc)
        heightLow = heights[iBin-1]
        outputGraph = r.TGraphErrors(len(xPoints),array('d',xPoints),array('d',yPoints),array('d',[0]*len(xPoints)),array('d',yPointsErr))
        outputGraph.SetName("SingleRateNPE{0}".format(heightLow).replace(".","p"))
        outputGraphs[heightLow] = outputGraph
    outputDir.cd()
    for outputHist in outputHists.values():
        outputHist.Scale(1./totalTime)
        outputHist.Write()
    return outputGraphs
def measureSingleRateVsRunNumber(totalTimeHist,inputTree,npeMin,quietInRest,singlePulseAboveThreshInChan,singlePulseInChan,noPrePulse,noEarlyPulse,outputDir):
    totalTime = nEvTotal*2000E-9
    # chans = [0,1,24,25,8,9,6,7,16,17,12,13,2,3,22,23,4,5]
    chans = list(range(80))
    chans.pop(4)
    outputHists = {}
    for chan in chans:
        extraSel = ""
        if quietInRest:
            layer = layerDict[chan]
            # extraSel += "&&MaxIf$(height,chan!={0}&&chan!=30&&layer=={1}&&chan!=15)<0.1&&MaxIf$(sideband_RMS,Iteration$!=15)<1.3".format(chan,layer)
            extraSel += "&&MaxIf$(height,chan!={0})<0.1&&Max$(sideband_RMS)<1.3".format(chan)
        if singlePulseAboveThreshInChan:
            raise NotImplemented
        if singlePulseInChan:
            extraSel += "&&Sum$(chan=={0})==1".format(chan)
        if noPrePulse:
            extraSel += "&&Sum$(chan=={0}&&time<MaxIf$(time,chan=={0}&&height==MaxIf$(height,chan=={0}&&time>200&&time<2200)))==0".format(chan)
        if noEarlyPulse:
            extraSel += "&&Sum$(chan=={0}&&time<160)==0".format(chan)
        outputHist = r.TH1D(str(chan),";runs;",2000,0,2000)
        totalN = inputTree.Draw("runNumber>>"+outputHist.GetName(),"Sum$(chan=={0}&&height>{1}&&time>200&&time<2200)>=1".format(chan,npeMin)+extraSel)
        outputHist.SetDirectory(0)
        outputHists[chan] = outputHist
    outputDir.cd()
    for outputHist in outputHists.values():
        outputHist.Divide(totalTimeHist)
        outputHist.Write()
    return 
def makeValidation(chan,target):
    targetHist = r.TH1D("unbiased_"+str(chan)+"_L1","",1000,0,1000)
    target.Draw("MaxIf$(height,chan=={0}&&time>200&&time<2200)>>".format(chan)+targetHist.GetName(),"MaxIf$(height,chan=={0}&&time>200&&time<2200)>0".format(chan))
    nEntriesEff = target.Draw("","","goff")
    targetHist.Scale(1./(2000.E-9*nEntriesEff))
    targetHist.Rebin(4)
    targetHist.SetLineColor(r.kBlack)
    return targetHist
if __name__ =='__main__':
    inputFileFull = r.TFile("/homes/milliqan/milliqanOffline/Run3Detector/outputRun3/MilliQan_Run490_default_v23_updateChanNumbering.root")
    inputTreeFull = inputFileFull.Get("t")
    totalTimeHist = r.TH1D("totalTime",";runs;",2000,0,2000)
    nEvTotal = inputTreeFull.Draw("runNumber>>"+totalTimeHist.GetName(),"")
    totalTime = nEvTotal*2000E-9
    totalTimeHist.Scale(2000E-9)
    # inputFile = r.TFile("../outputRun3/MilliQan_Run490_default_v23_updateChanNumbering.root")
    inputTree = inputTreeFull
    # outputFileValidation = r.TFile("measureSingleRateFromUnbiasedRunValidationAllUnbiasedHeight.root","RECREATE")
    # del chans[15]
    # for chan in chans:
    #     outputPlot = makeValidation(chan,inputTree)
    #     outputPlot.Write()
    # outputFileValidation.Close()
    outputFileNPEValidation = r.TFile("areaValidationUnbiasedRate.root","RECREATE")
    for quietInRest in [False]:
        for singlePulseAboveThreshInChan in [False]:
            for singlePulseInChan in [False]:
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
                        heights = [0,75,200,400,1000,10000]
                        # heights = [0,0.5,1.5,5,10,20,50,100,1000,10000]
                        # heights = [0,100]
                        npeMin = 0
                        outputDirValidationVsRun = outputDirValidation.mkdir("RunNumber")
                        measureSingleRateVsRunNumber(totalTimeHist,inputTree,npeMin,quietInRest,singlePulseAboveThreshInChan,singlePulseInChan,noPrePulse,noEarlyPulse,outputDirValidationVsRun)

                        # heights = [0,0.5,1.5,5,10,20,50,100,1000,10000]
                        colours = [r.kBlack,r.kRed,r.kBlue,r.kGreen+1,r.kMagenta,r.kCyan,r.kYellow+1,r.kGray,r.kOrange,r.kCyan+1]
                        outCanvas = r.TCanvas()
                        outCanvas.cd()
                        outCanvas.SetLogy()
                        dummyHist = r.TH1D("dummy",";Channel; Rate [hz]",33,-1,32)
                        dummyHist.SetMaximum(1E4)
                        dummyHist.SetMinimum(1E1)
                        dummyHist.Draw()
                        mg = r.TMultiGraph()
                        mg.SetTitle(";Channel; Rate [hz]")
                        leg = r.TLegend(0.75,0.65,0.89,0.89)
                        leg.SetBorderSize(0)
                        outputDirValidationVsNPE = outputDirValidation.mkdir("NPE")
                        outputGraphs = measureSingleRateFromUnbiasedRunNPE(totalTime,inputTree,heights,quietInRest,singlePulseAboveThreshInChan,singlePulseInChan,noPrePulse,noEarlyPulse,outputDirValidationVsNPE)
                        for colour,heightLow,heightHigh in zip(colours,heights,heights[1:]+[99999]):
                            print (heightLow,heightHigh)
                            heightDir = outputFile.mkdir("height_{0}".format(heightLow))
                            heightDir.cd()
                            outputGraph = outputGraphs[heightLow]
                            outputGraph.SetMarkerColor(colour)
                            outputGraph.SetLineColor(colour)
                            outputGraph.Write()
                            mg.Add(outputGraph)
                            if heightHigh < 99999:
                                leg.AddEntry(outputGraph,"Height {0} to {1} mV".format(heightLow,heightHigh))
                            else:
                                leg.AddEntry(outputGraph,"Height {0} to Inf mV".format(heightLow,heightHigh))
                        mg.Draw("Psame")
                        leg.Draw("same")
                        outCanvas.SaveAs("singlesRatesUnbiased{0}HeightAllUnbiasedBinnedAsSignalNoQualSel.pdf".format(optString))

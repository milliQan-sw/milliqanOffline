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

# def measureSingleRateFromUnbiasedRun(inputTree,nPE,quietInRest,singlePulseAboveThreshInChan,singlePulseInChan):
#     chans = range(32)
#     del chans[15]
#     nEvTotal = inputTree.Draw("","groupTDC_b1[0]==groupTDC_b0[0]","goff")
#     totalTime = nEvTotal*500E-9
#     xPoints = []
#     yPoints = []
#     yPointsErr = []
#     for chan in chans:
#         extraSel = ""
#         if quietInRest:
#             extraSel += "&&MaxIf$(nPE,chan!={0}&&chan!=30)<0.1".format(chan)
#         if singlePulseAboveThreshInChan:
#             extraSel += "&&Sum$(chan=={0}&&nPE>{1}&&duration>={2})==1".format(chan,nPE,durationMap[chan])
#         if singlePulseInChan:
#             extraSel += "&&Sum$(chan=={0})==1".format(chan)
#         nEvPass = inputTree.Draw("","groupTDC_b1[0]==groupTDC_b0[0]&&Sum$(chan=={0}&&duration>={1}&&time>60&&time<560&&nPE>{2})>=1".format(chan,durationMap[chan],nPE)+extraSel,"goff")
#         singleRate = ufloat(nEvPass,nEvPass**-0.5)/totalTime
#         xPoints.append(chan)
#         yPoints.append(singleRate.n)
#         yPointsErr.append(singleRate.s)
#     outputGraph = r.TGraphErrors(len(xPoints),array('d',xPoints),array('d',yPoints),array('d',[0]*len(xPoints)),array('d',yPointsErr))
#     outputGraph.SetName("SingleRateNPE{0}".format(nPE))
#     return outputGraph
def measureSingleRateFromUnbiasedRunNPE(totalTime,inputTree,nPELow,nPEHigh,quietInRest,singlePulseAboveThreshInChan,singlePulseInChan,noPrePulse):
    chans = range(32)
    del chans[15]
    totalTime = nEvTotal*500E-9
    xPoints = []
    yPoints = []
    yPointsErr = []
    for chan in chans:
        extraSel = ""
        if quietInRest:
            extraSel += "&&MaxIf$(nPE,chan!={0}&&chan!=30)<0.1".format(chan)
        if singlePulseAboveThreshInChan:
            extraSel += "&&Sum$(chan=={0}&&nPE>{1}&&nPE<{2})==1".format(chan,nPELow,nPEHigh)
        if singlePulseInChan:
            extraSel += "&&Sum$(chan=={0})==1".format(chan)
        nEvPass = inputTree.Draw("","groupTDC_b1[0]==groupTDC_b0[0]&&Sum$(chan=={0}&&time>60&&time<560&&nPE>{1}&&nPE<{2})>=1".format(chan,nPELow,nPEHigh)+extraSel,"goff")
        singleRate = ufloat(nEvPass,nEvPass**0.5)/totalTime
        xPoints.append(chan)
        yPoints.append(singleRate.n)
        yPointsErr.append(singleRate.s)
    outputGraph = r.TGraphErrors(len(xPoints),array('d',xPoints),array('d',yPoints),array('d',[0]*len(xPoints)),array('d',yPointsErr))
    outputGraph.SetName("SingleRateNPE{0}".format(nPELow).replace(".","p"))
    return outputGraph
def measureSingleRateFromUnbiasedRunHeight(inputTree,heightLow,heightHigh,quietInRest,singlePulseAboveThreshInChan,singlePulseInChan,noPrePulse):
    chans = range(32)
    del chans[15]
    nEvTotal = inputTree.Draw("","groupTDC_b1[0]==groupTDC_b0[0]","goff")
    totalTime = nEvTotal*500E-9
    xPoints = []
    yPoints = []
    yPointsErr = []
    for chan in chans:
        extraSel = ""
        if quietInRest:
            extraSel += "&&MaxIf$(height,chan!={0}&&chan!=30)<0.1".format(chan)
        if singlePulseAboveThreshInChan:
            extraSel += "&&Sum$(chan=={0}&&height>{1}&&height<{3}&&duration>={2})==1".format(chan,heightLow,durationMap[chan],heightHigh)
        if singlePulseInChan:
            extraSel += "&&Sum$(chan=={0})==1".format(chan)
        if noPrePulse:
            extraSel += "&&Sum$(chan=={0}&&time<160)==0".format(chan)
        nEvPass = inputTree.Draw("","groupTDC_b1[0]==groupTDC_b0[0]&&Sum$(chan=={0}&&duration>={1}&&time>60&&time<560&&height>{2}&&height<{3})>=1".format(chan,durationMap[chan],heightLow,heightHigh)+extraSel,"goff")
        singleRate = ufloat(nEvPass,nEvPass**0.5)/totalTime
        xPoints.append(chan)
        yPoints.append(singleRate.n)
        yPointsErr.append(singleRate.s)
    outputGraph = r.TGraphErrors(len(xPoints),array('d',xPoints),array('d',yPoints),array('d',[0]*len(xPoints)),array('d',yPointsErr))
    outputGraph.SetName("SingleRateNPE{0}".format(heightLow))
    return outputGraph
def makeValidation(chan,target):
    targetHist = r.TH1D("unbiased_"+str(chan)+"_L1","",1000,0,1000)
    target.Draw("MaxIf$(height,chan=={0}&&time>60&&time<560)>>".format(chan)+targetHist.GetName(),"groupTDC_b1[0]==groupTDC_b0[0]&&MaxIf$(height,chan=={0}&&time>60&&time<560)>0".format(chan))
    nEntriesEff = target.Draw("","groupTDC_b1[0]==groupTDC_b0[0]","goff")
    targetHist.Scale(1./(500.E-9*nEntriesEff))
    targetHist.Rebin(4)
    targetHist.SetLineColor(r.kBlack)
    return targetHist
if __name__ =='__main__':
    opts = [True,False]
    chans = range(32)
    inputFileFull = r.TFile("allUnbiased.root")
    inputTreeFull = inputFileFull.Get("t")
    nEvTotal = inputTreeFull.Draw("","groupTDC_b1[0]==groupTDC_b0[0]","goff")
    totalTime = nEvTotal*500E-9
    inputFile = r.TFile("allUnbiasedWithBarHit.root")
    inputTree = inputFile.Get("t")
    # outputFileValidation = r.TFile("measureSingleRateFromUnbiasedRunValidationAllUnbiasedHeight.root","RECREATE")
    # del chans[15]
    # for chan in chans:
    #     outputPlot = makeValidation(chan,inputTree)
    #     outputPlot.Write()
    # outputFileValidation.Close()
    for quietInRest in opts:
        for singlePulseAboveThreshInChan in opts:
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
                    print "Running Opts: "+optString
                    outputFile = r.TFile("measureSingleRateFromUnbiasedAllUnbiasedNPE{0}Binned.root".format(optString),"RECREATE")
                    nPEs = [0.5,2,5,10,20,50,100]
                    # nPEs = [0,1,10,20]
                    colours = [r.kBlack,r.kRed,r.kBlue,r.kGreen+1,r.kMagenta,r.kCyan,r.kYellow+1]
                    outCanvas = r.TCanvas()
                    outCanvas.cd()
                    outCanvas.SetLogy()
                    dummyHist = r.TH1D("dummy","",33,-1,32)
                    dummyHist.SetMaximum(6E4)
                    dummyHist.SetMinimum(1E2)
                    dummyHist.Draw()
                    mg = r.TMultiGraph()
                    leg = r.TLegend(0.65,0.7,0.89,0.89)
                    leg.SetBorderSize(0)
                    for colour,nPELow,nPEHigh in zip(colours,nPEs,nPEs[1:]+[9999]):
                        print nPELow,nPEHigh
                        nPEDir = outputFile.mkdir("nPE_{0}".format(nPELow))
                        nPEDir.cd()
                        outputGraph = measureSingleRateFromUnbiasedRunNPE(totalTime,inputTree,nPELow,nPEHigh,quietInRest,singlePulseAboveThreshInChan,singlePulseInChan,noPrePulse)
                        outputGraph.SetMarkerColor(colour)
                        outputGraph.SetLineColor(colour)
                        outputGraph.Write()
                        mg.Add(outputGraph)
                    mg.Draw("P")
                    leg.Draw("same")
                    outCanvas.SaveAs("singlesRatesUnbiased{0}HeightAllUnbiasedBinned.pdf".format(optString))

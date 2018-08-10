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
from measureSingleRateFromDouble import getDavidData
skipList = [(0,1,8,9),(6,7,12,13),(2,3,4,5)]
outputDirBaseBase = "plotHeightChecksBinned"
def main():
    opts = [True,False]
    for corr in ["UncorrRegion","CorrRegion"]:
        outputDirBase = outputDirBaseBase + corr  
        if not os.path.exists(outputDirBase):
            os.mkdir(outputDirBase)
        for quietInRest in opts:
            for singlePulseAboveThreshInChan in opts:
                for singlePulseInChan in opts:
                    for noPrePulse in opts:
                        for skipSameLayer in [True,False]:
                            optString = ""
                            outputRatios = []
                            outputRatiosErrors = []
                            outputDeltas = []
                            outputDeltasErrors = []
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
                            inputFileFromDoubles = r.TFile("measureSingleRateFromDoubleNPEBinned{0}.root".format(optString))
                            inputFileFromUnbiased = r.TFile("measureSingleRateFromUnbiasedAllUnbiasedNPE{0}Binned.root".format(optString))
                            heights = [0.5,2,5,10,20,50,100]
                            if optString != "":
                                outputDir = outputDirBase+"/" +optString
                            else:
                                outputDir = outputDirBase+"/base"
                            if skipSameLayer:
                                outputDir += "NoSameLayer"
                            else:
                                outputDir += "SameLayer"
                            if not os.path.exists(outputDir):
                                os.mkdir(outputDir)
                            # dummyHist = r.TH1D("dummy","",15,-1,14)
                            # outCanvas = r.TCanvas()
                            # outCanvas.cd()
                            # outCanvas.SetLogy()
                            # dummyHist.SetMaximum(6E4)
                            # dummyHist.SetMinimum(1E2)
                            # dummyHist.Draw()
                            # mg = r.TMultiGraph()
                            # leg = r.TLegend(0.65,0.7,0.89,0.89)
                            # leg.SetBorderSize(0)
                            for height in heights:
                                chanCombosDouble = odict()
                                chanCombosSingle = odict()
                                leg = r.TLegend(0.65,0.7,0.89,0.89)
                                leg.SetBorderSize(0)
                                mg = r.TMultiGraph()
                                for histoKey in inputFileFromDoubles.GetListOfKeys():
                                    histo = histoKey.ReadObj()
                                    histoName = histo.GetName()
                                    if "Chans" in histo.GetName():
                                        if "NPE_"+str(height).replace("0.5","0p5")+"_"+str(height).replace("0.5","0p5") in histo.GetName():
                                            error = r.Double()
                                            if corr == "CorrRegion":
                                                integral = histo.IntegralAndError(histo.FindBin(0),histo.FindBin(100)-1,error)
                                            else:
                                                integral = histo.IntegralAndError(histo.FindBin(100),histo.FindBin(200)-1,error)
                                            if skipSameLayer:
                                                skip = False
                                                for check in skipList:
                                                    if int(histoName.split("_")[1]) in check and int(histoName.split("_")[2]) in check:
                                                        skip = True
                                            else:
                                                skip = True
                                                for check in skipList:
                                                    if int(histoName.split("_")[1]) in check and int(histoName.split("_")[2]) in check:
                                                        skip = False
                                            if int(histoName.split("_")[1]) in [4,6] or int(histoName.split("_")[2]) in [4,6]:
                                                skip = True
                                            if integral == 0:
                                                skip = True
                                            if not skip:
                                                chanCombosDouble[int(histoName.split("_")[1]),int(histoName.split("_")[2])] = ufloat(integral,error)
                                if len(chanCombosDouble) == 0:
                                    continue
                                print height
                                inputGraphUnbiased = inputFileFromUnbiased.Get("nPE_{0}/SingleRateNPE{1}".format(height,str(height).replace(".","p"))) 
                                unbRates = {}
                                for i in range(inputGraphUnbiased.GetN()):
                                    unbRates[int(inputGraphUnbiased.GetX()[i])] = ufloat(inputGraphUnbiased.GetY()[i],inputGraphUnbiased.GetErrorY(i))
                                for chanCombo in chanCombosDouble:
                                    chanCombosSingle[chanCombo] = unbRates[chanCombo[0]]*unbRates[chanCombo[1]]*100E-9
                                # chanCombosSingle = sorted(chanCombosSingle)
                                # chanCombosDouble = sorted(chanCombosDouble)
                                outListSingle = []
                                outListDouble = []
                                outListDeltas = []
                                outListRatios = []
                                for combo in sorted(chanCombosSingle):
                                    outListSingle.append(chanCombosSingle[combo])
                                    outListDouble.append(chanCombosDouble[combo])
                                    outListDeltas.append(chanCombosDouble[combo]-chanCombosSingle[combo])
                                    if chanCombosSingle[combo] > 0:
                                        outListRatios.append(chanCombosDouble[combo]/chanCombosSingle[combo])
                                outputGraphSingle = r.TGraphErrors(len(chanCombosSingle),array('d',range(len(outListSingle))),array('d',[x.n for x in outListSingle]),array('d',[0]*len(outListSingle)),array('d',[x.s for x in outListSingle]))
                                outputGraphSingle.SetMarkerColor(r.kRed)
                                outputGraphSingle.SetLineColor(r.kRed)
                                outputGraphDouble = r.TGraphErrors(len(chanCombosDouble),array('d',range(len(outListDouble))),array('d',[x.n for x in outListDouble]),array('d',[0]*len(outListDouble)),array('d',[x.s for x in outListDouble]))
                                outputGraphDouble.SetMarkerColor(r.kBlue)
                                outputGraphDouble.SetLineColor(r.kBlue)
                                mg.Add(outputGraphSingle)
                                mg.Add(outputGraphDouble)
                                leg.AddEntry(outputGraphSingle,"height > {0} Single".format(height))
                                leg.AddEntry(outputGraphDouble,"height > {0} Double".format(height))
                                outputGraphDelta = r.TGraphErrors(len(outListDeltas),array('d',range(len(outListDeltas))),array('d',[x.n for x in outListDeltas]),array('d',[0]*len(outListDeltas)),array('d',[x.s for x in outListDeltas]))
                                outputGraphRatio = r.TGraphErrors(len(outListRatios),array('d',range(len(outListRatios))),array('d',[x.n for x in outListRatios]),array('d',[0]*len(outListRatios)),array('d',[x.s for x in outListRatios]))
                                dummyHist = r.TH1D(str(height),"",len(outListSingle)+2,-1,len(outListSingle)+1)
                                for iBin in range(len(chanCombosSingle)):
                                    dummyHist.GetXaxis().SetBinLabel(iBin+1," ".join(str(x) for x in sorted(chanCombosSingle)[iBin]))
                                dummyHist.SetMaximum(10)
                                dummyHist.SetMinimum(1E-3)
                                #Basic graphs
                                outCanvas = r.TCanvas()
                                outCanvas.SetLogy()
                                dummyHist.Draw()    
                                mg.Draw("P")
                                leg.Draw("same")
                                outCanvas.SaveAs(outputDir+"/doubleRatesHeight{0}.pdf".format(str(height).replace(".","p")))
                                outCanvas.Clear()
                                outCanvas.SetLogy(0)
                                outCanvas.SetGrid()
                                dummyHist.Draw()
                                dummyHist.SetMaximum(max(outListRatios).n)
                                outputGraphRatio.Draw("same")
                                fFunc = r.TF1("temp","pol0")
                                outputGraphRatio.Fit(fFunc)
                                outputRatios.append(fFunc.GetParameter(0))
                                outputRatiosErrors.append(fFunc.GetParError(0))
                                outCanvas.SaveAs(outputDir+"/doubleRatesRatio{0}.pdf".format(str(height).replace(".","p")))
                                outCanvas.Clear()
                                dummyHist.SetMaximum(max(outListDeltas).n)
                                dummyHist.Draw()
                                outputGraphDelta.Draw("same")
                                outCanvas.SaveAs(outputDir+"/doubleRatesDelta{0}.pdf".format(str(height).replace(".","p")))
                                fFuncD = r.TF1("temp","pol0")
                                outputGraphDelta.Fit(fFuncD)
                                outputDeltas.append(fFuncD.GetParameter(0))
                                outputDeltasErrors.append(fFuncD.GetParError(0))
                            outCanvas.Clear()
                            finalGraph = r.TGraphErrors(len(heights),array('d',heights),array('d',outputRatios),array('d',len(heights)*[0]),array('d',outputRatiosErrors))
                            finalGraph.SetTitle(";Height;Ratio")
                            finalGraph.SetMarkerStyle(8)
                            finalGraph.Draw("AP")
                            outCanvas.SaveAs(outputDir+"/ratioGraph.pdf")
                            outCanvas.Clear()
                            finalGraphD = r.TGraphErrors(len(heights),array('d',heights),array('d',outputDeltas),array('d',len(heights)*[0]),array('d',outputDeltasErrors))
                            finalGraphD.SetTitle(";Height;Delta")
                            finalGraphD.SetMarkerStyle(8)
                            finalGraphD.Draw("AP")
                            outCanvas.SaveAs(outputDir+"/deltaGraph.pdf")
if __name__ == "__main__":
    main()

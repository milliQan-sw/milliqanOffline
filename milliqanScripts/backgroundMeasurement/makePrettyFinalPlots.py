
import ROOT as r
import pickle
import os
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(0)
timeDictNoBeam = {(0,97):1065410,(30,50):294719,(50,70):176245.,(70,80):238232.,(80,97):356214}
timeDictBeam =   {(0,97):2085690,(30,50):564790,(50,70):446647,(70,80):513800,(80,97):560453}

def makeTimeSplitPlots(inputFile,outputFolder,blind):
    if blind: scenarios = ["BlindTimeBlindPath"]
    else: scenarios = ["","CheckPath","CheckTime","CheckTimeCheckPath"]
    if type(inputFile) == str:
        inputFile = r.TFile(inputFile)
    if not os.path.exists(outputFolder):
        os.mkdir(outputFolder)
    colors = {"30_50":r.kBlue,"50_70":r.kRed,"70_80":r.kRed-2,"80_97":r.kRed+2}
    timeSplitFancy = {"30_50":"Run 30 - 50","50_70":"Run 50 - 70","70_80":"Run 70 - 80","80_97":"Run 80 - 97"}
    for scenario in scenarios:
        tempCanvas = r.TCanvas("c1"+scenario,"",200,10,700,500)
        pad1 = r.TPad("pad1","",0,0,1,1)
        pad2 = r.TPad("pad2","",0,0,1,1)
        pad2.SetFillColor(0)
        pad2.SetFillStyle(4000)
        pad2.SetFrameFillStyle(0)
        pad1.Draw()
        pad1.cd()
        legend = r.TLegend(0.7,0.3,0.89,0.5)
        legend.SetBorderSize(0)
        sameString = ""
        for timeSplit in ["30_50","50_70","70_80","80_97"]:
            for scale in ["2","5","10"][1:2]:
                selString = "Selection"+scenario+timeSplit+"/scale"+scale+"_cumulative"
                inputHist = inputFile.Get(selString)
                inputHist.SetLineColor(colors[timeSplit])
                legend.AddEntry(inputHist,timeSplitFancy[timeSplit],'l')
                inputHist.GetXaxis().SetTitle("Maximum number of photons in event")
                inputHist.GetYaxis().SetTitleOffset(1.4)
                inputHist.Draw(sameString)
                if sameString == "":
                    inputHist.GetXaxis().SetRangeUser(0,200)
                    inputHistFirst = inputHist.Clone()
                sameString = "same"
        pad2.Draw()
        pad2.cd()
        inputHistFirst.Scale(1./3600. * timeDictNoBeam[tuple([int(x) for x in timeSplit.split("_")])])
        inputHistFirst.GetYaxis().SetTitle("Total Events")
        inputHistFirst.GetYaxis().SetTitleOffset(1.4)
        # inputHistFirst.Draw("AXISY+")
        legend.Draw("same")
        tempCanvas.SaveAs(outputFolder+"/Scenario"+scenario+".pdf")
def makeBlindBeamNotBeamPlots(inputFile,inputFileBeam,outputFolder):
    if type(inputFile) == str:
        inputFile = r.TFile(inputFile)
    if type(inputFileBeam) == str:
        inputFileBeam = r.TFile(inputFileBeam)
    beamDict = {"Beam":inputFileBeam,"NotBeam":inputFile}
    if not os.path.exists(outputFolder):
        os.mkdir(outputFolder)
    colors = {"Beam":r.kRed+2,"NotBeam":r.kRed}
    beamFancy = {"Beam":"Beam","NotBeam":"No beam"}
    timeSplit = "0_97"
    for scenario in ["BlindTimeBlindPath","CheckPathBlindTime","CheckTimeBlindPath"]:
        tempCanvas = r.TCanvas("c1"+scenario,"",200,10,700,500)
        pad1 = r.TPad("pad1","",0,0,1,1)
        pad2 = r.TPad("pad2","",0,0,1,1)
        pad2.SetFillColor(0)
        pad2.SetFillStyle(4000)
        pad2.SetFrameFillStyle(0)
        pad1.Draw()
        pad1.cd()
        legend = r.TLegend(0.7,0.3,0.89,0.5)
        legend.SetBorderSize(0)
        sameString = ""
        for beam in ["Beam","NotBeam"]:
            for scale in ["2","5","10"][1:2]:
                selString = "Selection"+scenario+timeSplit+"/scale"+scale+"_cumulative"
                inputHist = beamDict[beam].Get(selString)
                inputHist.SetLineColor(colors[beam])
                legend.AddEntry(inputHist,beamFancy[beam]+" (scale "+scale+")",'l')
                inputHist.GetXaxis().SetTitle("Maximum number of photons in event")
                inputHist.GetYaxis().SetTitleOffset(1.4)
                inputHist.Draw(sameString)
                if sameString == "":
                    # inputHist.GetXaxis().SetRangeUser(0,200)
                    # inputHist.SetMaximum(inputHist.GetMaximum()*0.8)
                    inputHistFirst = inputHist.Clone()
                sameString = "same"
        pad2.Draw()
        pad2.cd()
        # inputHistFirst.Scale(1./3600. * timeDictBeam[tuple([int(x) for x in timeSplit.split("_")])])
        # inputHistFirst.GetYaxis().SetTitle("Total events beam (not beam #times 2)")
        # inputHistFirst.GetYaxis().SetTitleOffset(1.4)
        # inputHistFirst.Draw("AXISY+")
        legend.Draw("same")
        tempCanvas.SaveAs(outputFolder+"/Scenario"+scenario+".pdf")
def getABCDInfo(inputFileBlind,inputFile,timeDict):
    if type(inputFile) == str:
        inputFile = r.TFile(inputFile)
    if type(inputFileBlind) == str:
        inputFileBlind = r.TFile(inputFileBlind)
    nPERanges = [(0,5),(5,20),(20,50),(50,100),(100,200),(200,1000)]
    timeSplit = "0_97"
    predDict = {}
    errDict = {}
    for nPERange in nPERanges:
        for scenario in ["BlindTimeBlindPath","CheckPathBlindTime","CheckTimeBlindPath","CheckTimeCheckPath"]:
            for scale in ["2","5","10"][1:2]:
                selString = "Selection"+scenario+timeSplit+"/scale"+scale
                if 'Blind' in scenario:
                    inputHist = inputFileBlind.Get(selString)
                else:
                    inputHist = inputFile.Get(selString)
                inputHist.Scale(1./3600. * timeDict[tuple([int(x) for x in timeSplit.split("_")])])
                inputHist.GetXaxis().SetRangeUser(*nPERange)
                pred = inputHist.Integral()
                error = pred**0.5
                predDict[scenario] = pred
                errDict[scenario] = error/pred
                inputHist.Scale(3600. * 1./timeDict[tuple([int(x) for x in timeSplit.split("_")])])
        pred = (predDict["CheckPathBlindTime"]*predDict["CheckTimeBlindPath"]) / predDict["BlindTimeBlindPath"]
        err = pred*(errDict["CheckPathBlindTime"]**2+errDict["CheckTimeBlindPath"]**2+errDict["BlindTimeBlindPath"]**2)**0.5
        print nPERange,pred,err,predDict["CheckTimeCheckPath"]
            


if __name__ == "__main__":
    makeTimeSplitPlots('ratePerNPEPlots.root','finalPlotsTimeSplit',False) 
    # makeTimeSplitPlots('ratePerNPEPlotsSplitBeamBlind.root','finalPlotsTimeSplitBeam',True) 
    # getABCDInfo('ratePerNPEPlotsSplitBeamBlind.root','ratePerNPEPlotsSplit.root',timeDictBeam)
    # getABCDInfo('ratePerNPEPlotsSplitBlind.root','ratePerNPEPlotsSplit.root',timeDictNoBeam)
    # getABCDInfo('ratePerNPEPlotsSplitBlind.root','ratePerNPEPlotsSplit.root',timeDictNoBeam)

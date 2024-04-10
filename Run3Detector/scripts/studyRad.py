import ROOT as r
import os
r.gROOT.SetBatch(1)
r.gStyle.SetOptStat(0)
colorDict = {0:r.kBlue,1:r.kRed,2:r.kGreen,3:r.kBlack}
def plotPerLayer(outputDict,outputDir,name):
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    iH = 0
    oC = r.TCanvas()
    leg = r.TLegend(0.6,0.6,0.8,0.8)
    for layer,hist in outputDict.items():
        if iH == 0:
            drawOpt = ""
        else:
            drawOpt = "same"
        hist.SetLineColor(colorDict[layer])
        hist.Draw(drawOpt)
        leg.AddEntry(hist,"layer = {}".format(layer))
        iH += 1
    leg.SetBorderSize(0)
    leg.Draw()
    oC.SaveAs(outputDict+"/"+name+".pdf")
    oC.SaveAs(outputDir+"/"+name+".png")

def drawHistVsTime(hist,outputDir="histsFullTime710",convertTS=True,shift=0):
    print(str(type(hist)))
    if "TH2" in str(type(hist)):
        hist.GetXaxis().SetLabelSize(0.01)
        hist.GetXaxis().SetLabelOffset(0.01)
        if convertTS:
            hist.GetXaxis().SetTimeDisplay(1); 
            hist.GetXaxis().SetTimeFormat("#splitline{%y-%m-%d}{%H:%M:%S}%F1970-01-01 "+"0"+str(shift)+":00:00")
        oC = r.TCanvas()
        if not os.path.exists(outputDir):
            os.mkdir(outputDir)
        hist.Draw("colz")
        oC.SaveAs(outputDir+"/"+hist.GetName()+".pdf")
        oC.SaveAs(outputDir+"/"+hist.GetName()+".png")
        outputProf = hist.ProfileX()
        outputProf.GetXaxis().SetLabelSize(0.02)
        outputProf.GetXaxis().SetLabelOffset(0.01)
        if convertTS:
            outputProf.GetXaxis().SetTimeDisplay(1); 
            outputProf.GetXaxis().SetTimeFormat("#splitline{%y-%m-%d}{%H:%M:%S}%F1970-01-01 "+"0"+str(shift)+":00:00")
        outputProf.Draw()
        oC.SaveAs(outputDir+"/"+hist.GetName()+"_profile.pdf")
        oC.SaveAs(outputDir+"/"+hist.GetName()+"_profile.png")
    else:
        hist.GetXaxis().SetLabelSize(0.02)
        hist.GetXaxis().SetLabelOffset(0.01)
        if convertTS:
            hist.GetXaxis().SetTimeDisplay(1); 
            hist.GetXaxis().SetTimeFormat("#splitline{%y-%m-%d}{%H:%M:%S}%F1970-01-01 "+"0"+str(shift)+":00:00")
        oC = r.TCanvas()
        if not os.path.exists(outputDir):
            os.mkdir(outputDir)
        hist.Draw("")
        oC.SaveAs(outputDir+"/"+hist.GetName()+".pdf")
        oC.SaveAs(outputDir+"/"+hist.GetName()+".png")

# inputTree = r.TChain()
# inputTree.Add("/eos/home-m/mcitron/www/formosa/formosaRun709.root/t")
outputDir = "/eos/home-m/mcitron/www/formosa/radStudy710"
inputFile = r.TFile("/eos/home-m/mcitron/formosaRun710Skimmed.root")
# inputFile = r.TFile("/eos/home-m/mcitron/www/formosa/formosaRun710.root")
inputTree = inputFile.Get("t")
#
timeWindow = 50000 #in hours
startWindowOffsetFromEnd = 30000 # in hours  

maxTimeAll = inputTree.GetMaximum("event_time_fromTDC")
minTimeAll = inputTree.GetMinimum("event_time_fromTDC")

minTime = maxTimeAll-startWindowOffsetFromEnd*3600
maxTime = minTime+timeWindow*3600
if maxTime > maxTimeAll:
    maxTime = maxTimeAll
if minTime < minTimeAll:
    minTime = minTimeAll
# print(minTime,maxTime)
# minTime = maxTimeAll - 7205-1709.89E6#inputTree.GetMinimum("event_time_fromTDC")
# maxTime = maxTimeAll - 7170-1709.89E6#inputTree.GetMinimum("event_time_fromTDC")

nBinsTime = 100

outputHist = r.TH1D("time","rate;time",nBinsTime,minTime,maxTime)
inputTree.Draw("event_time_fromTDC>>"+outputHist.GetName(),"event_time_fromTDC>{}&&event_time_fromTDC<{}".format(minTime,maxTime),"")
# print (1./((maxTime-minTime)/nBinsTime))
outputHist.SetDirectory(0)
outputHist.Scale(1./((maxTime-minTime)/nBinsTime))
drawHistVsTime(outputHist,outputDir)

allOutputs = {}
for layer in range(4):
    outputHist = r.TH1D("NumChansForLayer"+str(layer),";layer;",4,1,5)
    inputTree.Draw("Sum$(layer=={}&&type==0&&ipulse==0)>>".format(layer)+outputHist.GetName(),"Max$(layer==0)&&Max$(layer==1)&&Max$(layer==2)&&Max$(layer==3)&&Max$(chan==16)<1&&Max$(chan==18)<1".format(minTime,maxTime))
    # print(outputHist.Integral())
    outputHist.Scale(1./outputHist.Integral())
    # print (1./((maxTime-minTime)/nBinsTime))
    outputHist.SetDirectory(0)
    allOutputs[layer] = outputHist

plotPerLayer(allOutputs,outputDir,"numChansPerLayer")

for layer in range(4):
    outputHist = r.TH1D("MaxHeightPerLayer"+str(layer),";height;",100,0,200)
    inputTree.Draw("MaxIf$(height,layer=={0})>>".format(layer)+outputHist.GetName(),"Max$(layer==0)&&Max$(layer==1)&&Max$(layer==2)&&Max$(layer==3)&&Max$(chan==16)<1&&Max$(chan==18)<1".format(minTime,maxTime))
    # print(outputHist.Integral())
    outputHist.Scale(1./outputHist.Integral())
    # print (1./((maxTime-minTime)/nBinsTime))
    outputHist.SetDirectory(0)
    allOutputs[layer] = outputHist

plotPerLayer(allOutputs,outputDir,"maxHeightPerLayer")

for layer in range(4):
    outputHist = r.TH1D("MaxAreaPerLayer"+str(layer),";area;",100,0,1E3)
    inputTree.Draw("MaxIf$(area,layer=={0})>>".format(layer)+outputHist.GetName(),"Max$(layer==0)&&Max$(layer==1)&&Max$(layer==2)&&Max$(layer==3)&&Max$(chan==16)<1&&Max$(chan==18)<1".format(minTime,maxTime))
    # print(outputHist.Integral())
    outputHist.Scale(1./outputHist.Integral())
    # print (1./((maxTime-minTime)/nBinsTime))
    outputHist.SetDirectory(0)
    allOutputs[layer] = outputHist

plotPerLayer(allOutputs,outputDir,"maxAreaPerLayer")

for layer in range(4):
    outputHist = r.TH1D("SumAreaPerLayer"+str(layer),";area;",100,0,1E3)
    inputTree.Draw("Sum$(area*(layer=={0}))>>".format(layer)+outputHist.GetName(),"Max$(layer==0)&&Max$(layer==1)&&Max$(layer==2)&&Max$(layer==3)&&Max$(chan==16)<1&&Max$(chan==18)<1".format(minTime,maxTime))
    # print(outputHist.Integral())
    outputHist.Scale(1./outputHist.Integral())
    # print (1./((maxTime-minTime)/nBinsTime))
    outputHist.SetDirectory(0)
    allOutputs[layer] = outputHist

plotPerLayer(allOutputs,outputDir,"sumAreaPerLayer")

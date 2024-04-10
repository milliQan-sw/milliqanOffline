import ROOT as r
import os
r.gROOT.SetBatch(1)
r.gStyle.SetOptStat(0)

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
outputDir = "/eos/home-m/mcitron/www/formosa/histsFullTime710"
inputFile = r.TFile("/eos/home-m/mcitron/formosaRun710.root")
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
outputHist = r.TH1D("time4LayerCosmic","rate;time",nBinsTime,minTime,maxTime)
inputTree.Draw("event_time_fromTDC>>"+outputHist.GetName(),"event_time_fromTDC>{}&&event_time_fromTDC<{}&&Max$(layer==0)&&Max$(layer==1)&&Max$(layer==2)&&Max$(layer==3)&&MaxIf$(height,chan==16)>100&&MaxIf$(height,chan==18)>100".format(minTime,maxTime),"")
# print (1./((maxTime-minTime)/nBinsTime))
outputHist.SetDirectory(0)
outputHist.Scale(1./((maxTime-minTime)/nBinsTime))
drawHistVsTime(outputHist,outputDir)

nBinsTime = 100
outputHist = r.TH1D("time4LayerCosmicIgnorePanels","rate;time",nBinsTime,minTime,maxTime)
inputTree.Draw("event_time_fromTDC>>"+outputHist.GetName(),"event_time_fromTDC>{}&&event_time_fromTDC<{}&&Max$(layer==0)&&Max$(layer==1)&&Max$(layer==2)&&Max$(layer==3)&&MaxIf$(area,type==0&&layer==0)>80E3&&MaxIf$(area,type==0&&layer==1)>80E3&&MaxIf$(area,type==0&&layer==2)>80E3&&MaxIf$(area,type==0&&layer==3)>80E3".format(minTime,maxTime),"")
# print (1./((maxTime-minTime)/nBinsTime))
outputHist.SetDirectory(0)
outputHist.Scale(1./((maxTime-minTime)/nBinsTime))
drawHistVsTime(outputHist,outputDir)

nBinsTime = 100
outputHist = r.TH1D("time4LayerCosmicNoPanels","rate;time",nBinsTime,minTime,maxTime)
inputTree.Draw("event_time_fromTDC>>"+outputHist.GetName(),"event_time_fromTDC>{}&&event_time_fromTDC<{}&&Max$(layer==0)&&Max$(layer==1)&&Max$(layer==2)&&Max$(layer==3)&&Max$(chan==16)<1&&Max$(chan==18)<1&&MaxIf$(area,type==0&&layer==0)>80E3&&MaxIf$(area,type==0&&layer==1)>80E3&&MaxIf$(area,type==0&&layer==2)>80E3&&MaxIf$(area,type==0&&layer==3)>80E3".format(minTime,maxTime),"")
# print (1./((maxTime-minTime)/nBinsTime))
outputHist.SetDirectory(0)
outputHist.Scale(1./((maxTime-minTime)/nBinsTime))
drawHistVsTime(outputHist,outputDir)

nBinsTime = 100
outputHist = r.TH1D("numberOfChannelsPerLayer4LayerNoPanels","rate;time",nBinsTime,minTime,maxTime)
inputTree.Draw("layer","event_time_fromTDC>{}&&event_time_fromTDC<{}&&Max$(layer==0)&&Max$(layer==1)&&Max$(layer==2)&&Max$(layer==3)&&Max$(chan==16)<1&&Max$(chan==18)<1&&type==0".format(minTime,maxTime),"")
# print (1./((maxTime-minTime)/nBinsTime))
outputHist.SetDirectory(0)
outputHist.Scale(1./outputHist.Integral(0,-1))
drawHistVsTime(outputHist,outputDir)


if False:
    outputHist = r.TH2D("timeVsNumChannels",";time;number of pulses",100,minTime,maxTime,10,0,20)
    inputTree.Draw("Sum$(height>20):event_time_fromTDC>>"+outputHist.GetName(),"event_time_fromTDC>{}&&event_time_fromTDC<{}".format(minTime,maxTime),"colz")
    outputHist.SetDirectory(0)
    drawHistVsTime(outputHist,outputDir)

    outputHist = r.TH2D("timeVsNumLayers",";time;number of layers",100,minTime,maxTime,5,0,5)
    inputTree.Draw("Max$(layer==0)+Max$(layer==1)+Max$(layer==2)+Max$(layer==3):event_time_fromTDC>>"+outputHist.GetName(),"event_time_fromTDC>{}&&event_time_fromTDC<{}".format(minTime,maxTime),"colz")
    outputHist.SetDirectory(0)
    drawHistVsTime(outputHist,outputDir)

    outputHist = r.TH2D("timeVsSumArea",";time;max area in event",100,minTime,maxTime,100,0,10000)
    inputTree.Draw("Max$(area*(type==0)):event_time_fromTDC>>"+outputHist.GetName(),"event_time_fromTDC>{}&&event_time_fromTDC<{}".format(minTime,maxTime),"colz")
    outputHist.SetDirectory(0)
    drawHistVsTime(outputHist,outputDir)

    nBinsTime = 100
    outputHist = r.TH1D("time","rate;time",nBinsTime,minTime,maxTime)
    inputTree.Draw("event_time_fromTDC>>"+outputHist.GetName(),"event_time_fromTDC>{}&&event_time_fromTDC<{}".format(minTime,maxTime),"")
    # print (1./((maxTime-minTime)/nBinsTime))
    outputHist.SetDirectory(0)
    outputHist.Scale(1./((maxTime-minTime)/nBinsTime))
    drawHistVsTime(outputHist,outputDir)

    nBinsTime = 100
    outputHist = r.TH1D("time4Layer","rate;time",nBinsTime,minTime,maxTime)
    inputTree.Draw("event_time_fromTDC>>"+outputHist.GetName(),"event_time_fromTDC>{}&&event_time_fromTDC<{}&&Max$(layer==0)&&Max$(layer==1)&&Max$(layer==2)&&Max$(layer==3)".format(minTime,maxTime),"")
    # print (1./((maxTime-minTime)/nBinsTime))
    outputHist.SetDirectory(0)
    outputHist.Scale(1./((maxTime-minTime)/nBinsTime))
    drawHistVsTime(outputHist,outputDir)


    nBinsTime = 100
    outputHist = r.TH1D("time4LayerNoPanel","rate;time",nBinsTime,minTime,maxTime)
    inputTree.Draw("event_time_fromTDC>>"+outputHist.GetName(),"event_time_fromTDC>{}&&event_time_fromTDC<{}&&Max$(layer==0)&&Max$(layer==1)&&Max$(layer==2)&&Max$(layer==3)&&Max$(chan==18)<1&&Max$(chan==16)<1".format(minTime,maxTime),"")
    # print (1./((maxTime-minTime)/nBinsTime))
    outputHist.SetDirectory(0)
    outputHist.Scale(1./((maxTime-minTime)/nBinsTime))
    drawHistVsTime(outputHist,outputDir)

    nBinsTime = 100
    outputHist = r.TH1D("time4LayerOnePerLayer","rate;time",nBinsTime,minTime,maxTime)
    inputTree.Draw("event_time_fromTDC>>"+outputHist.GetName(),"event_time_fromTDC>{}&&event_time_fromTDC<{}&&Max$(layer==0)&&Max$(layer==1)&&Max$(layer==2)&&Max$(layer==3)&&MaxIf$(chan,layer==0)==MinIf$(chan,layer==0)&&MaxIf$(chan,layer==1)==MinIf$(chan,layer==1)&&MaxIf$(chan,layer==2)==MinIf$(chan,layer==2)&&MaxIf$(chan,layer==3)==MinIf$(chan,layer==3)".format(minTime,maxTime),"")
    # print (1./((maxTime-minTime)/nBinsTime))
    outputHist.SetDirectory(0)
    outputHist.Scale(1./((maxTime-minTime)/nBinsTime))
    drawHistVsTime(outputHist,outputDir)


    nBinsTime = 100
    outputHist = r.TH1D("time4LayerOnePerLayerNoPanel","rate;time",nBinsTime,minTime,maxTime)
    inputTree.Draw("event_time_fromTDC>>"+outputHist.GetName(),"event_time_fromTDC>{}&&event_time_fromTDC<{}&&Max$(layer==0)&&Max$(layer==1)&&Max$(layer==2)&&Max$(layer==3)&&MaxIf$(chan,layer==0)==MinIf$(chan,layer==0)&&MaxIf$(chan,layer==1)==MinIf$(chan,layer==1)&&MaxIf$(chan,layer==2)==MinIf$(chan,layer==2)&&MaxIf$(chan,layer==3)==MinIf$(chan,layer==3)&&Max$(chan==18)<1&&Max$(chan==16)<1".format(minTime,maxTime),"")
    # print (1./((maxTime-minTime)/nBinsTime))
    outputHist.SetDirectory(0)
    outputHist.Scale(1./((maxTime-minTime)/nBinsTime))
    drawHistVsTime(outputHist,outputDir)


    nBinsTime = 100
    outputHist = r.TH1D("time4LayerOnePerLayerNoPanelStraight","rate;time",nBinsTime,minTime,maxTime)
    inputTree.Draw("event_time_fromTDC>>"+outputHist.GetName(),"event_time_fromTDC>{}&&event_time_fromTDC<{}&&Max$(layer==0)&&Max$(layer==1)&&Max$(layer==2)&&Max$(layer==3)&&MaxIf$(chan,layer==0)==MinIf$(chan,layer==0)&&MaxIf$(chan,layer==1)==MinIf$(chan,layer==1)&&MaxIf$(chan,layer==2)==MinIf$(chan,layer==2)&&MaxIf$(chan,layer==3)==MinIf$(chan,layer==3)&&Max$(chan==18)<1&&Max$(chan==16)<1&&MaxIf$(row,type==0)==MinIf$(row,type==0)&&MaxIf$(column,type==0)==MinIf$(column,type==0)".format(minTime,maxTime),"")
    # print (1./((maxTime-minTime)/nBinsTime))
    outputHist.SetDirectory(0)
    outputHist.Scale(1./((maxTime-minTime)/nBinsTime))
    drawHistVsTime(outputHist,outputDir)





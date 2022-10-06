import ROOT as r
import pickle
import os
r.gROOT.SetBatch(True)
r.gStyle.SetOptFit(11111)

# inputFile = r.TFile("Run61.root")
# inputFile = r.TFile("UX5MilliQan_Run79.13_highThreshDoubleCoincidence_window200_v4.root")
inputFile = r.TFile("Run86_interModuleCalib.root")
outputFolder = "outputIntercalibration_86"
if not os.path.exists(outputFolder):
    os.mkdir(outputFolder)
colors = {1:r.kBlack,2:r.kRed,3:r.kBlue,4:r.kYellow,5:r.kGreen,6:r.kCyan,7:r.kOrange,8:r.kMagenta}

inputTree = inputFile.Get('t')
channelPairsUpDown = [(11,9),(10,8),(7,5),(6,4),(3,1)]
channelPairsDiagonal = [(11,8),(10,9),(7,4),(6,5),(2,1)]
channelPairsLeftRight = [(11,10),(9,8),(7,6),(5,4),(3,2)]
# channelPairsInterLayer = {10:[7,6,5,4],11:[7,6,5,4]}
channelPairsInterLayer = {6:[3,2,1],4:[3,2,1],7:[3,2,1],5:[3,2,1],10:[7,6,5,4],8:[7,6,5,4],11:[7,6,5,4],9:[7,6,5,4]}
channelPairs = channelPairsUpDown+channelPairsDiagonal
channelPairs = [(3,1)]
channelPairsAll = channelPairs + channelPairsLeftRight
channelThresholds = {15:100,14:100,12:100,11:500,9:100,10:500,8:100,7:100,5:100,6:100,4:100,3:100,2:100,1:100}
# channelThresholds = {15:30,14:30,12:30,11:120,9:40,10:120,8:40,7:30,5:30,6:30,4:30,3:30,1:30,2:30}
channelSidebar = {14:[11,10,9,8],12:[7,6,5,4],15:[3,2,1]}
def calibrationClosure():
    outputDict = {}
    for pair in channelPairsAll:
        tempCanvas = r.TCanvas()
        tempCanvas.cd()
        histName = "resolution_{0}_{1}(1000,-50,50)".format(pair[0],pair[1])
        inputTree.Draw("(MinIf$(time_module_calibrated,chan=={0}&&height>{2})-MinIf$(time_module_calibrated,chan=={1}&&height>{3}))>>{4}".format(pair[0],pair[1],channelThresholds[pair[0]],channelThresholds[pair[1]],histName),\
                "MinIf$(time_module_calibrated,chan=={0}&&height>{2})!=0&&MinIf$(time_module_calibrated,chan=={1}&&height>{3})!=0".format(pair[0],pair[1],channelThresholds[pair[0]],channelThresholds[pair[1]]),"")
        # inputTree.Draw("event_time".format(pair[0],pair[1],channelThresholds[pair[0]],channelThresholds[pair[1]]),"","",10000)
        hist= tempCanvas.GetListOfPrimitives()[0]
        maxBin = hist.GetMaximumBin()
        # rms = hist.GetRMS()
        bin1 = hist.FindBin(hist.GetXaxis().GetBinCenter(maxBin)-20.)
        bin2 = hist.FindBin(hist.GetXaxis().GetBinCenter(maxBin)+20.)
        hist.GetXaxis().SetRange(bin1,bin2)
        # hist.Fit('gaus',"")
        mean = hist.GetMean()
        meanError = hist.GetMeanError()
        rms = hist.GetRMS()
        rmsError = hist.GetRMSError()
        tempCanvas.SaveAs(outputFolder+"/closure_resolution_{0}_{1}".format(pair[0],pair[1])+".pdf")
        outputDict[pair] = [mean,meanError,rms,rmsError]
        print [mean,meanError,rms,rmsError]
    pickle.dump(outputDict,open(outputFolder+"/calibrationDictClosure.pkl",'w'))
    return 
def calibrationInterlayer():
    outputDict = {}
    for main,otherLayer in channelPairsInterLayer.iteritems():
        tempCanvas = r.TCanvas()
        tempCanvas.cd()

        channelSels = []
        hists = []
        histMax = 0.
        for channel in otherLayer:
            histName = "channels {0} {1} (100,-60.3,59.97)".format(main,channel)
            channelSel = "(chan=={0}&&height>{1})".format(channel,channelThresholds[channel])
            channelSels.append(channelSel)
            inputTree.Draw("(MinIf$(time_module_calibrated,chan=={0}&&height>{1})-MinIf$(time_module_calibrated,{2}))>>{3}".format(main,channelThresholds[main],channelSel,histName),\
                "(MinIf$(time_module_calibrated,chan=={0}&&height>{1})>0&&MinIf$(time_module_calibrated,{2})>0)".format(main,channelThresholds[main],channelSel),"")
            hist = tempCanvas.GetListOfPrimitives()[0]
            hist.SetDirectory(0)
            hist.SetLineColor(colors[channel])
            hist.SetTitle('')
            hists.append(hist)
            tempCanvas.Clear()
            if histMax < hist.GetMaximum():
                histMax = hist.GetMaximum()

        hists[0].Draw()
        hists[0].SetMaximum(histMax*1.2)
        r.gStyle.SetOptStat(0)
        legend = r.TLegend(0.7,0.7,0.9,0.9)
        legend.AddEntry(hists[0],"channel {0}".format(hists[0].GetName()))
        for hist in hists[1:]:
            hist.Draw("same")
            legend.AddEntry(hist,"channel {0}".format(hist.GetName()))
        legend.Draw()
        tempCanvas.SaveAs(outputFolder+"/resolution_interlayer{0}_seperate".format(main)+".pdf")
        tempCanvas.Clear()
        r.gStyle.SetOptStat(1111)
        histName = "resolution_main{0}(100,-60.3,59.97)".format(main)

        selection = "||".join(channelSels)
        inputTree.Draw("(MinIf$(time_module_calibrated,chan=={0}&&height>{1})-MinIf$(time_module_calibrated,{2}))>>{3}".format(main,channelThresholds[main],selection,histName),\
            "(MinIf$(time_module_calibrated,chan=={0}&&height>{1})>0&&MinIf$(time_module_calibrated,{2})>0)".format(main,channelThresholds[main],selection),"")
        hist= tempCanvas.GetListOfPrimitives()[0]
        maxBin = hist.GetMaximumBin()
        # rms = hist.GetRMS()
        bin1 = hist.FindBin(hist.GetXaxis().GetBinCenter(maxBin)-20.)
        bin2 = hist.FindBin(hist.GetXaxis().GetBinCenter(maxBin)+20.)
        hist.GetXaxis().SetRange(bin1,bin2)
        mean = hist.GetMean()
        meanError = hist.GetMeanError()
        rms = hist.GetRMS()
        rmsError = hist.GetRMSError()
        hist.SetTitle('')
        tempCanvas.SaveAs(outputFolder+"/resolution_interlayer{0}".format(main)+".pdf")
        outputDict[main] = [mean,meanError,rms,rmsError]
        print [mean,meanError,rms,rmsError]
    pickle.dump(outputDict,open(outputFolder+"/calibrationDictInterLayer.pkl",'w'))
    return outputDict
def calibrationSidebar():
    outputDict = {}
    for sidebar,moduleBars in channelSidebar.iteritems():
        tempCanvas = r.TCanvas()
        tempCanvas.cd()
        histName = "resolution_sidebar{0}(100,-50,50)".format(sidebar)
        channelSels = []
        for channel in moduleBars:
            channelSels.append("(chan=={0}&&height>{1})".format(channel,channelThresholds[channel]))
        selection = "||".join(channelSels)
        inputTree.Draw("(MinIf$(time,chan=={0}&&height>{1})-MinIf$(time_module_calibrated,{2}))>>{3}".format(sidebar,channelThresholds[sidebar],selection,histName),\
            "(MinIf$(time,chan=={0}&&height>{1})>0&&MinIf$(time_module_calibrated,{2})>0)".format(sidebar,channelThresholds[sidebar],selection),"")
        hist= tempCanvas.GetListOfPrimitives()[0]
        maxBin = hist.GetMaximumBin()
        # rms = hist.GetRMS()
        bin1 = hist.FindBin(hist.GetXaxis().GetBinCenter(maxBin)-20.)
        bin2 = hist.FindBin(hist.GetXaxis().GetBinCenter(maxBin)+20.)
        hist.GetXaxis().SetRange(bin1,bin2)
        mean = hist.GetMean()
        meanError = hist.GetMeanError()
        rms = hist.GetRMS()
        rmsError = hist.GetRMSError()
        tempCanvas.SaveAs(outputFolder+"/resolution_sidebar{0}".format(sidebar)+".pdf")
        outputDict[sidebar] = [mean,meanError,rms,rmsError]
        print [mean,meanError,rms,rmsError]
    pickle.dump(outputDict,open(outputFolder+"/calibrationDictSidebar.pkl",'w'))
    return outputDict

def calibrationFirstStep():
    outputDict = {}
    for pair in channelPairs:
        tempCanvas = r.TCanvas()
        tempCanvas.cd()
        histName = "resolution_{0}_{1}(100,-60,60)".format(pair[0],pair[1])
        inputTree.Draw("(MinIf$(time,chan=={0}&&height>{2})-MinIf$(time_module_calibrated,chan=={1}&&height>{3}))>>{4}".format(pair[0],pair[1],channelThresholds[pair[0]],channelThresholds[pair[1]],histName),\
                "MinIf$(time,chan=={0}&&height>{2})>0&&MinIf$(time_module_calibrated,chan=={1}&&height>{3})>0".format(pair[0],pair[1],channelThresholds[pair[0]],channelThresholds[pair[1]]),"")
        # inputTree.Draw("event_time".format(pair[0],pair[1],channelThresholds[pair[0]],channelThresholds[pair[1]]),"","",10000)
        hist= tempCanvas.GetListOfPrimitives()[0]
        maxBin = hist.GetMaximumBin()
        # rms = hist.GetRMS()
        bin1 = hist.FindBin(hist.GetXaxis().GetBinCenter(maxBin)-20.)
        bin2 = hist.FindBin(hist.GetXaxis().GetBinCenter(maxBin)+20.)
        hist.GetXaxis().SetRange(bin1,bin2)
        mean = hist.GetMean()
        meanError = hist.GetMeanError()
        rms = hist.GetRMS()
        rmsError = hist.GetRMSError()
        hist.SetTitle('')
        tempCanvas.SaveAs(outputFolder+"/resolution_{0}_{1}".format(pair[0],pair[1])+".pdf")
        outputDict[pair] = [mean,meanError,rms,rmsError]
        print pair,outputDict[pair]
    pickle.dump(outputDict,open(outputFolder+"/calibrationDict.pkl",'w'))
    return outputDict
def calibrationSecondStep(outputDict):
    calibDictFinal = {}
    calibDictFinal[11] = -outputDict[(11,9)][0]
    calibDictFinal[9] = 0
    calibDictFinal[10] = -outputDict[(10,9)][0]
    calib8_1 = outputDict[10,8][0]-outputDict[10,9][0]
    calib8_2 = outputDict[11,8][0]-outputDict[11,9][0]
    calibDictFinal[8] = sum([calib8_1,calib8_2])/2.

    calibDictFinal[7] = -outputDict[(7,5)][0]
    calibDictFinal[5] = 0
    calibDictFinal[6] = -outputDict[(6,5)][0]
    calib4_1 = outputDict[6,4][0]-outputDict[6,5][0]
    calib4_2 = outputDict[7,4][0]-outputDict[7,5][0]
    calibDictFinal[4] = sum([calib4_1,calib4_2])/2.

    calibDictFinal[3] = -outputDict[(3,1)][0]
    calibDictFinal[1] = 0
    calibDictFinal[2] = -outputDict[(2,1)][0]
    for i in range(1,12):
        print i, calibDictFinal[i]
    return calibDictFinal
def calibrationInterlayerSecondStep(outputDict):
    calibDictFinal = {}
    calibration21 = 0
    for i in range(0,4):
        calibDictFinal[i] = 0
    for i in range(4,8):
        calibration21 += -outputDict[i][0]
    calibration21 /= 4
    for i in range(4,8):
        calibDictFinal[i] = calibration21
    calibration32 = 0
    for i in range(8,12):
        calibration32 += -outputDict[i][0]
    calibration32 /= 4
    for i in range(8,12):
        calibDictFinal[i] = calibration21+calibration32
    for i in range(1,12):
        print i, calibDictFinal[i]
    return calibDictFinal
    # print calib11,calib10,calib9,sum([calib8_1,calib8_2])/2.
    # print calib7,calib5,calib6,sum([calib4_1,calib4_2])/2.
    # print calib3,calib2,calib1

if __name__=="__main__":
    calibrationFirstStep()
    # calibrationClosure()
    # calibrationSidebar()
    # calibrationInterlayer()
    # calib = pickle.load(open(outputFolder+"/calibrationDictInterLayer.pkl"))
    # calibrationInterlayerSecondStep(calib)
    # calb = pickle.load(open(outputFolder+"/calibrationDict.pkl"))
    # calibDictFinal = calibrationSecondStep(calb)
    # pickle.dump(calibDictFinal,open("calibrationDictFinal.pkl","w"))
    # for iModule,pair in channelPairsLeftRight:
    #     correction
    #     channelSels = []
    #     for channel in pairs[0]:
    #         channelSels.append("(chan=={0}&&height>{1})".format(channel,channelThresholds[channel]))
    #     if len(channelSels) > 1:
    #         selection1 = "||".join(channelSels)
    #     else:
    #         selection1 = channelSels[0]
    #     channelSels = []
    #     for channel in pairs[0]:
    #         channelSels.append("(chan=={0}&&height>{1})".format(channel,channelThresholds[channel]))
    #     if len(channelSels) > 1:
    #         selection2 = "||".join(channelSels)
    #     else:
    #         selection2 = channelSels[0]
    #     statement = "MinIf$(time,"+selection1+") - MinIf$(time,"+selection2+") >> "+histName
    #     selection = "MinIf$(time,"+selection1+")>0 && MinIf$(time,"+selection2+")>0"
    #
    #     tempCanvas = r.TCanvas()
    #     tempCanvas.cd()
    #     histName = 


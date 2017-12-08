import ROOT as r
import pickle
import os

colors = {1:r.kBlack,2:r.kRed,3:r.kBlue,4:r.kYellow,5:r.kGreen,6:r.kCyan,7:r.kOrange,8:r.kMagenta}
inputFile = r.TFile("Run61V7.root")
inputTree = inputFile.Get('t')
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(0)

outputFolder = "triplePeakStudy_interModuleCosmetics"
channelThresholds = {15:300,14:300,12:300,11:75,9:200,10:75,8:200,7:300,5:300,6:300,4:300,3:300,2:300,1:300}
if not os.path.exists(outputFolder):
    os.mkdir(outputFolder)
channelPairsInterLayer = {7:[3,2,1]}
# channelPairsInterLayer = {6:[3,2,1],4:[3,2,1],7:[3,2,1],5:[3,2,1],10:[7,6,5,4],8:[7,6,5,4],11:[7,6,5,4],9:[7,6,5,4]}
def triplePeakInterlayer():
    outputDict = {}
    for nPEScenarioName in [("cosmic","cosmic"),("rad","cosmic"),("cosmic","rad"),("rad","rad")][2:3]:
    #for nPEScenarioName in [(100,99999,100,99999),(2,20,100,99999),(100,99999,2,20)]:
        for main,otherLayer in channelPairsInterLayer.iteritems():

            tempCanvas = r.TCanvas()
            tempCanvas.cd()

            channelSels = []
            hists = []
            histMax = 0.
            for channel in otherLayer:
                nPEScenario = []
                if nPEScenarioName[0] == "cosmic":
                    nPEScenario += [channelThresholds[main],99999]
                else:
                    nPEScenario += [2,20]
                if nPEScenarioName[1] == "cosmic":
                    nPEScenario += [channelThresholds[channel],99999]
                else:
                    nPEScenario += [2,20]
                histName = "{0} {1} (100,-62.8125,62.1875)".format(main,channel)
                channelSel = "(chan=={0}&&nPE>{1}&&nPE<{2})".format(channel,nPEScenario[2],nPEScenario[3])
                channelSels.append(channelSel)
            #     inputTree.Draw("(MinIf$(time_module_calibrated,chan=={0}&&nPE>{1}&&nPE<{2})-MinIf$(time_module_calibrated,{3}))>>{4}".format(main,nPEScenario[0],nPEScenario[1],channelSel,histName),\
            #         "(MinIf$(time_module_calibrated,chan=={0}&&nPE>{1}&&nPE<{2})>0&&MinIf$(time_module_calibrated,{3})>0)".format(main,nPEScenario[0],nPEScenario[1],channelSel),"")
            #     hist = tempCanvas.GetListOfPrimitives()[0]
            #     hist.SetDirectory(0)
            #     hist.SetLineColor(colors[channel])
            #     hists.append(hist)
            #     tempCanvas.Clear()
            #     if histMax < hist.GetMaximum():
            #         histMax = hist.GetMaximum()
            #
            # hists[0].Draw()
            # hists[0].SetMaximum(histMax*1.2)
            # r.gStyle.SetOptStat(0)
            # legend = r.TLegend(0.7,0.7,0.9,0.9)
            # legend.AddEntry(hists[0],"channel {0}".format(hists[0].GetName()))
            # for hist in hists[1:]:
            #     hist.Draw("same")
            #     legend.AddEntry(hist,"channel {0}".format(hist.GetName()))
            # legend.Draw()
            # tempCanvas.SaveAs(outputFolder+"/resolution_interlayer_{0}_{1}_{2}_other_{3}_{4}_seperate".format(main,nPEScenario[0],nPEScenario[1],nPEScenario[2],nPEScenario[3])+".pdf")
            selection = "||".join(channelSels)
            print "(MinIf$(time_module_calibrated,chan=={0}&&nPE>{1}&&nPE<{2})>0&&MinIf$(time_module_calibrated,{3})>0)".format(main,nPEScenario[0],nPEScenario[1],selection)
            inputTree.Draw("(MinIf$(time_module_calibrated,chan=={0}&&nPE>{1}&&nPE<{2})-MinIf$(time_module_calibrated,{3}))>>{4}".format(main,nPEScenario[0],nPEScenario[1],selection,histName),\
                "(MinIf$(time_module_calibrated,chan=={0}&&nPE>{1}&&nPE<{2})>0&&MinIf$(time_module_calibrated,{3})>0)".format(main,nPEScenario[0],nPEScenario[1],selection),"")
            hist = tempCanvas.GetListOfPrimitives()[0]
            # maxBin = hist.GetMaximumBin()
            # # rms = hist.GetRMS()
            # bin1 = hist.FindBin(hist.GetXaxis().GetBinCenter(maxBin)-20.)
            # bin2 = hist.FindBin(hist.GetXaxis().GetBinCenter(maxBin)+20.)
            # hist.GetXaxis().SetRange(bin1,bin2)
            mean = hist.GetMean()
            meanError = hist.GetMeanError()
            rms = hist.GetRMS()
            rmsError = hist.GetRMSError()
            tempCanvas.SaveAs(outputFolder+"/resolution_interlayer_{0}_{1}_other_{2}".format(main,nPEScenarioName[0],nPEScenarioName[1])+".pdf")
            outputDict[main,nPEScenarioName[0],nPEScenarioName[1]] = [mean,meanError,rms,rmsError]
            print [mean,meanError,rms,rmsError]
    pickle.dump(outputDict,open(outputFolder+"/triplePeakDictInterLayer.pkl",'w'))
    return outputDict
    return 

if __name__=="__main__":
    triplePeakInterlayer()

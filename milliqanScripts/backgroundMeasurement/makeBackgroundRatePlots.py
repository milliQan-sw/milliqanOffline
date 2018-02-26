import ROOT as r
import pickle
import os
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(0)
#THIS SCRIPT ASSUMES YOU ARE USING THE OUTPUT WHICH PRESELECTS AS MaxIf$(chan,layer==1)==MinIf$(chan,layer==1)&&MaxIf$(chan,layer==2)==MinIf$(chan,layer==2)&&MaxIf$(chan,layer==3)==MinIf$(chan,layer==3)&&Sum$(layer==1)>0&&Sum$(layer==2)>0&&Sum$(layer==3)>0
for beam in [True,False]:
    for blind in [True,False]:
        if beam and not blind: continue

        outputFolder = "ratePerNPEPlots"
        #Length of time (for rates) of each section of runs
        timeDictNoBeam = {(0,97):1065410,(30,50):294719,(50,70):176245.,(70,80):238232.,(80,97):356214}
        timeDictBeam =   {(0,97):2085690,(30,50):564790,(50,70):446647,(70,80):513800,(80,97):560453}
        # inputFile = r.TFile("realTripleCoincOneBarPerLayerBeam.root")
        inputFileName = "./inputs/realTripleCoincOneBarPerLayerNotBeam.root"

        timeDict = timeDictNoBeam
        if beam:
            timeDict = timeDictBeam
            blind = True
            inputFileName = inputFileName.replace('NotBeam','Beam')

        if beam: outputFolder += "Beam"
        if blind: outputFolder += "Blind"
        if not os.path.exists(outputFolder):
            os.mkdir(outputFolder)
        outputFile = r.TFile(outputFolder+".root","RECREATE")

        inputFile = r.TFile(inputFileName)
        tree = inputFile.Get("t")

        runList = [(30,50),(50,70),(70,80),(80,97),(0,97)]
            

        bins = (4000,0,2000)
        scales = [2,5,10]
        colors = {2:1,5:2,10:5}
        onePulseReq = False
        checkPathString = ""
        checkOnePulseString = ""
        checkTimeString = ""
        allowedPaths = [
            {1,5,8},
            {1,5,9},
            {1,5,10},
            {1,5,11},
            {1,4,8},
            {1,4,10},
            {1,7,10},
            {1,7,11},
            {1,6,10},
            {2,6,8},
            {2,6,9},
            {2,6,10},
            {2,6,11},
            {2,4,8},
            {2,4,9},
            {2,7,11},
            {2,7,9},
            {2,5,9},
            {3,7,8},
            {3,7,9},
            {3,7,10},
            {3,7,11},
            {3,4,8},
            {3,6,10},
            {3,6,8},
            {3,5,8},
            {3,5,9},
            ]
        allPaths = []
        for l1 in [1,2,3]:
            for l2 in [4,5,6,7]:
                for l3 in [8,9,10,11]:
                    allPaths.append({l1,l2,l3})
        if blind:
            blindTimes = [True,False]
            blindPaths = [True,False]
        else:
            blindTimes = [False]
            blindPaths = [False]
        for runs in runList:
            runListString = "_".join(str(x) for x in runs)
            for blindTime in blindTimes:
                for blindPath in blindPaths:
                    for checkTime in [True,False]:
                        for checkPath in [True,False]:
                            if blindTime and checkTime: continue
                            if blindPath and checkPath: continue
                            if blind and not blindTime and not blindPath: continue
                            legend = r.TLegend(0.7,0.8,0.9,0.9)
                            hists = []
                            histsCumu = []
                            if blindPath:
                                blindPathString = "BlindPath"
                            else:
                                blindPathString = ""
                            if blindTime:
                                blindTimeString = "BlindTime"
                            else:
                                blindTimeString = ""
                            if checkPath:
                                checkPathString = "CheckPath"
                            else:
                                checkPathString = ""
                            if checkTime:
                                checkTimeString = "CheckTime"
                            else:
                                checkTimeString = ""
                            if onePulseReq:
                                checkOnePulseString = "CheckOnePulse"
                            else:
                                checkOnePulseString = ""

                            folderName = "Selection{0}{1}{2}{3}{4}".format(checkTimeString,checkPathString,blindTimeString,blindPathString,runListString)
                            folder = outputFile.mkdir(folderName)
                            folder.cd()
                            timeHist = r.TH1D('time',';delta time (ns)',200,-200,200)
                            # timeHist.SetDirectory(0)
                            pathHist = r.TH1D('paths',';;',len(allPaths),0,len(allPaths))
                            # pathHist.SetDirectory(0)
                            for iBin in range(1,pathHist.GetNbinsX()+1):
                                pathHist.GetXaxis().SetBinLabel(iBin," ".join([str(x) for x in sorted(list(allPaths[iBin-1]))]))
                            pathHist.LabelsOption("v")

                            for iS,s in enumerate(scales):
                                hist = r.TH1D("scale"+str(s),";max nPE;events per hour",*bins)
                                # hist.SetDirectory(0)
                                hist.SetLineColor(colors[s])
                                hist.SetMarkerColor(colors[s])
                                hists.append(hist) 
                                legend.AddEntry(hist,"Channel 11/10 scaling {0}".format(s))
                            for event in tree:
                                if not (event.run >= runs[0] and event.run < runs[1]):
                                    continue
                                chanSet = set(event.chan)
                                if chanSet not in allPaths: continue
                                if checkPath:
                                    if chanSet not in allowedPaths:
                                        continue
                                if blindPath:
                                    if chanSet in allowedPaths:
                                        continue
                                if onePulseReq:
                                    if len(event.chan) > 3: continue
                                timeLayer3 = [time for time,layer in zip(event.time,event.layer) if layer == 3][0]
                                timeLayer2 = [time for time,layer in zip(event.time,event.layer) if layer == 2][0]
                                timeLayer1 = [time for time,layer in zip(event.time,event.layer) if layer == 1][0]
                                if checkTime:
                                    if timeLayer3 - timeLayer1 > 14 or timeLayer3 - timeLayer1 < 6: continue
                                    # if timeLayer2 - timeLayer1 < 0 or  timeLayer2 - timeLayer1 > 15 : continue
                                if blindTime:
                                    if timeLayer3 - timeLayer1 < 14 and timeLayer3 - timeLayer1 > 6: continue
                                    # if timeLayer2 - timeLayer1 > 0 and  timeLayer2 - timeLayer1 < 15 : continue
                                timeHist.Fill(timeLayer3-timeLayer1)
                                if chanSet in allPaths:
                                    pathHist.Fill(allPaths.index(chanSet))

                                #Not sure how to calibrate nPE in chan 10/11 so present three options 
                                nPEsNotProbChannel = max([npe for npe,chan in zip(event.nPE,event.chan) if (chan != 10 and chan != 11)]+[-1])
                                nPEsProbChannel = max([npe for npe,chan in zip(event.nPE,event.chan) if (chan == 10 or chan == 11)]+[-1])
                                for iS in range(len(scales)):
                                    hists[iS].Fill(max(nPEsNotProbChannel,nPEsProbChannel*scales[iS]))

                            for hist in hists:
                                histCumu = hist.GetCumulative()
                                for iBin in range(1,histCumu.GetNbinsX()+1):
                                    histCumu.SetBinError(iBin,histCumu.GetBinContent(iBin)**0.5)
                                histCumu.Scale(3600./timeDict[runs])
                                histCumu.SetMaximum(histCumu.GetBinContent(histCumu.GetNbinsX())*1.2)
                                histsCumu.append(histCumu)
                                hist.Scale(3600./timeDict[runs])
                                hist.SetMaximum(hist.GetMaximum()*1.2)

                            tempCanvas = r.TCanvas()
                            hists[0].Draw("e")
                            hists[0].GetXaxis().SetRangeUser(0,2000)
                            for hist in hists[1:]:
                                hist.Draw("same")
                            legend.Draw("same")
                            tempCanvas.SaveAs(outputFolder+"/maxNPE{0}{1}{2}{3}{4}.pdf".format(checkTimeString,checkPathString,blindTimeString,blindPathString,runListString))
                            tempCanvas.Clear()
                            for hist in hists: hist.Write()
                            # histsCumu[0].SetMaximum(30)
                            histsCumu[0].Draw("e")
                            histsCumu[0].GetXaxis().SetRangeUser(0,2000)
                            for histCumu in histsCumu[1:]:
                                # histCumu.SetMaximum(30)
                                histCumu.Draw("samee")
                            legend.Draw("same")
                            tempCanvas.SaveAs(outputFolder+"/maxNPECumu{0}{1}{2}{3}{4}.pdf".format(checkTimeString,checkPathString,blindTimeString,blindPathString,runListString))
                            tempCanvas.Clear()
                            for histCumu in histsCumu: histCumu.Write()

                            for name,hist in {"time":timeHist,"path":pathHist}.iteritems():
                                hist.Scale(3600./timeDict[runs])
                                hist.Draw()
                                tempCanvas.SaveAs(outputFolder+"/"+name+"{0}{1}{2}{3}{4}.pdf".format(checkTimeString,checkPathString,blindTimeString,blindPathString,runListString))
                                tempCanvas.Clear()
                                hist.Write()

        outputFile.Close()



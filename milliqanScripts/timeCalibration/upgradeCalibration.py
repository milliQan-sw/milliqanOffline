import ROOT as r
import pickle
import os
import copy
r.gROOT.SetBatch(True)
r.gStyle.SetOptFit(11111)

fNameTag = '816'
# fNameTag = '423'
cosmicHeightSelections = {}
b2Delta = 16
for i in range(32):
    cosmicHeightSelections[i] = 500
cosmicHeightSelections[8+b2Delta] = 1150
cosmicHeightSelections[9+b2Delta] = 1150
cosmicHeightSelections[8] = 1150
cosmicHeightSelections[9] = 1150
cosmicHeightSelections[1+b2Delta] = 1150
cosmicHeightSelections[5] = 1150
cosmicHeightSelections[6+b2Delta] = 1150
inputFile = r.TFile("~/Run816.root")
# inputFile = r.TFile("./Run423.root")
def upgradeCalibrationIntraLayerPlots(allSlices):
    inputTree = inputFile.Get("t")
    #800
    # cosmicHeightSelections = {0:50,1:50,2:5,3:5,4:5,5:5,6:50,7:50,8:50,9:50,10:50,11:50,12:50,13:5,14:50,15:50}
    #900
    calibHistos = {}
    nEvents = inputTree.GetEntries()
    iE = 1
    for sName,slices in allSlices.iteritems():
        for sliceNum,ySlice in slices.iteritems():
            name="_".join([str(x) for x in ySlice])
            for higherChan in ySlice[1:]:
                calibHistos[sName,higherChan,ySlice[0]] = r.TH1D("chans_{0}_{1}".format(higherChan,ySlice[0],name),"",96,-30,30)
                calibHistos[sName,higherChan,ySlice[0]].SetDirectory(0)
    for event in inputTree:
        if iE % int(nEvents/5) == 0: 
            print iE*1./nEvents
        chans = event.chan
        heights = event.height
        times = event.time
        firstPulses = {}
        for chan,height,time in zip(chans,heights,times):
            if chan not in firstPulses and height > cosmicHeightSelections[chan]:
                firstPulses[chan] = time
        for sName,slices in allSlices.iteritems():
            for sliceNum,ySlice in slices.iteritems():
                if len(firstPulses) > len(ySlice):continue
                if set(ySlice).issubset(firstPulses.keys()):
                    for higherChan in ySlice[1:]:
                        calibHistos[sName,higherChan,ySlice[0]].Fill(firstPulses[higherChan]-firstPulses[ySlice[0]])
        iE += 1
    outputFile = r.TFile("calibIntraSlice"+fNameTag+".root","RECREATE")
    for sName,slices in allSlices.iteritems():
        outDirs = outputFile.mkdir(sName)
        outDirs.cd()
        for sliceNum,ySlice in slices.iteritems():
            for higherChan in ySlice[1:]:
                calibHistos[sName,higherChan,ySlice[0]].Write()
    print "DONE"
def upgradeCalibrationIntraLayerCalculateCalibration(inFile,allSlices):
    calibConstantsIntraSlice = {}
    calibConstantsIntraLayer = {}
    chanToSliceDict = {}
    tFile = r.TFile(inFile)
    inDir = tFile.Get('slicesStraight')
    sliceHists = {}
    for sliceNum,ySlice in allSlices["slicesStraight"].iteritems():
        if sliceNum % 2 == 0:
            sliceHists[sliceNum,sliceNum-1] = r.TH1D("chans_{0}_{1}".format(sliceNum,sliceNum-1),"",96,-30,30)
        sliceHists[sliceNum,sliceNum] = r.TH1D("chans_{0}_{1}".format(sliceNum,sliceNum),"",96,-30,30)
        #For straight path hists make calib to correct high channels down to bottom
        name="_".join([str(x) for x in ySlice])
        chanToSliceDict[ySlice[0]] = sliceNum
        calibConstantsIntraLayer[ySlice[0]] =0
        for higherChan in ySlice[1:]:
            histo = inDir.Get("chans_{0}_{1}".format(higherChan,ySlice[0]))
            calibConstantsIntraSlice[higherChan] = (-histo.GetMean()/0.625)*0.625
            calibConstantsIntraLayer[higherChan] = (-histo.GetMean()/0.625)*0.625
            chanToSliceDict[higherChan] = sliceNum
    for dirName,slices in allSlices.iteritems():
        if dirName == 'slicesStraight':continue
        inDir = tFile.Get(dirName)
        for sliceNum,ySlice in slices.iteritems():
            for higherChan in ySlice[1:]:
                #Take histo from each channel combination of the bent paths
                histo = inDir.Get("chans_{0}_{1}".format(higherChan,ySlice[0]))
                histoCalib = histo.Clone()
                histoCalib.Reset()
                for iBin in range(1,histo.GetNbinsX()+1):
                    xVal = histo.GetXaxis().GetBinCenter(iBin)
                    yVal = histo.GetBinContent(iBin)

                    #Shift mean of histo by calibration to bottom left (only have to do for higherChan as second is always defined as bottom channel
                    if chanToSliceDict[higherChan] >= chanToSliceDict[ySlice[0]]:
                        histoCalib.SetBinContent(histoCalib.FindBin(xVal+calibConstantsIntraSlice[higherChan]),yVal)
                    else:
                        #If higher channel is in the lower slice then must also reverse sign
                        histoCalib.SetBinContent(histoCalib.FindBin(-(xVal+calibConstantsIntraSlice[higherChan])),yVal)
                if chanToSliceDict[higherChan] > chanToSliceDict[ySlice[0]]:
                    sliceHists[chanToSliceDict[higherChan],chanToSliceDict[ySlice[0]]].Add(histoCalib)
                else:
                    sliceHists[chanToSliceDict[ySlice[0]],chanToSliceDict[higherChan]].Add(histoCalib)

    for (slice1,slice2),hist in sliceHists.iteritems():
        if slice2 == slice1-1:
            for chan in allSlices["slicesStraight"][slice1]:
                calibConstantsIntraLayer[chan] -= (hist.GetMean()/0.625)*0.625
    outFile = r.TFile('calibInterSlice'+fNameTag+'.root','RECREATE')
    outFile.cd()
    for _,sliceHist in sliceHists.iteritems():
        sliceHist.Write()
    return calibConstantsIntraLayer
def upgradeCalibrationInterLayer(calibConstantsIntraLayer,allLayerPaths):
    calibConstantsFinal = {}
    inputTree = inputFile.Get("t")
    layerToChannel = {1:(0,1,24,25,8,9),2:(6,7,16,17,12,13),3:(2,3,22,23,4,5)}
    calibHistos = {}
    for pathNum,layers in allLayerPaths.iteritems():
        for higherLayer in layers[1:]:
            calibHistos[higherLayer,layers[0]] = r.TH1D("chans_{0}_{1}".format(higherLayer,layers[0]),"",96,-30,30)
            calibHistos[higherLayer,layers[0]].SetDirectory(0)
    iE = 1
    nEvents = inputTree.GetEntries()
    for event in inputTree:
        if iE % int(nEvents/5) == 0: 
            print iE*1./nEvents
        chans = event.chan
        heights = event.height
        times = event.time
        layers = event.layer
        firstPulses = {}
        for layer,height,time,chan in zip(layers,heights,times,chans):
            if chan not in calibConstantsIntraLayer: continue
            if layer not in firstPulses and height > cosmicHeightSelections[chan]:
                firstPulses[layer] = time+calibConstantsIntraLayer[chan]
        for pathNum,layers in allLayerPaths.iteritems():
            # if len(firstPulses) > len(layers):continue
            if set(layers).issubset(firstPulses.keys()):
                for higherLayer in layers[1:]:
                    calibHistos[higherLayer,layers[0]].Fill(firstPulses[higherLayer]-firstPulses[layers[0]])
        iE += 1
    outputFile = r.TFile("calibInterLayer"+fNameTag+".root","RECREATE")
    calibConstantsInterLayer = copy.deepcopy(calibConstantsIntraLayer)
    calibMeans = {}
    for pathNum,layers in allLayerPaths.iteritems():
        for higherLayer in layers[1:]:
            calibHistos[higherLayer,layers[0]].Write()
            calibMeans[higherLayer] = (calibHistos[higherLayer,layers[0]].GetMean()/0.625)*0.625

    for layer,chans in layerToChannel.iteritems():
        for chan in chans:
            if layer == 2 or layer == 3:
                calibConstantsInterLayer[chan] -= calibMeans[2]
            if layer == 3:
                calibConstantsInterLayer[chan] -= calibMeans[3]
            calibConstantsInterLayer[chan] = round(calibConstantsInterLayer[chan]/0.625)*0.625

    return calibConstantsInterLayer
if __name__=="__main__":
    allSlices = {}
    # allSlices["slicesStraight"] = {1:(0,2,4),2:(1,3,5),3:(6,12,8),4:(7,13,9),5:(14,10),6:(15,11)}
    # allSlices["slicesBent1"] = {1:(1,2,4),2:(0,3,5),3:(7,12,8),4:(6,13,9),5:(15,10),6:(14,11)}
    # allSlices["slicesBent2"] = {1:(1,3,4),2:(0,2,5),3:(7,13,8),4:(6,12,9)}
    # allSlices["slicesBent3"] = {1:(1,2,3,4),2:(0,2,3,5),3:(7,12,13,8),4:(6,12,13,9)}
    allSlices["slicesStraight"] = {1:(0,8+b2Delta,8),2:(1,9+b2Delta,9),3:(6,0+b2Delta,12),4:(7,1+b2Delta,13),5:(2,6+b2Delta,4),6:(3,7+b2Delta,5)}
    allSlices["slicesBent1"] = {1:(1,8+b2Delta,8),2:(0,9+b2Delta,9),3:(7,0+b2Delta,12),4:(6,1+b2Delta,13),5:(3,6+b2Delta,4),6:(2,7+b2Delta,5)}
    allSlices["slicesBent2"] = {1:(1,9+b2Delta,8),2:(0,8+b2Delta,9),3:(7,1+b2Delta,12),4:(6,0+b2Delta,13),5:(3,7+b2Delta,4),6:(2,6+b2Delta,5)}
    allSlices["slicesBent3"] = {1:(1,8+b2Delta,9+b2Delta,8),2:(0,8+b2Delta,9+b2Delta,9),3:(7,0+b2Delta,1+b2Delta,12),4:(6,0+b2Delta,1+b2Delta,13),5:(3,6+b2Delta,7+b2Delta,4),6:(2,6+b2Delta,7+b2Delta,5)}
    # allSlices["slicesBent3"] = {1:(1,2,3,4),2:(0,2,3,5),3:(7,12,13,8),4:(6,12,13,9)}
    allLayerPaths = {1:(1,2),2:(2,3)}
    upgradeCalibrationIntraLayerPlots(allSlices)
    print "Done intra slice"
    calibConstantsIntraLayer = upgradeCalibrationIntraLayerCalculateCalibration("calibIntraSlice"+fNameTag+".root",allSlices)
    print "Done inter slice"
    calibConstantsInterLayer = upgradeCalibrationInterLayer(calibConstantsIntraLayer,allLayerPaths)
    print "Done inter layer"

    print calibConstantsIntraLayer
    print calibConstantsInterLayer

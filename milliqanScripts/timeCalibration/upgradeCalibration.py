import ROOT as r
import pickle
import os
import copy
r.gROOT.SetBatch(True)
r.gStyle.SetOptFit(11111)

beamOn = False
fNameTag = '834'
cosmicHeightSelections = {}
b2Delta = 16
topPanels = [10,14,30]
for i in range(32):
    cosmicHeightSelections[i] = 500
#878 + 7725s 
cosmicHeightSelections[8+b2Delta] = 90
cosmicHeightSelections[9+b2Delta] = 80
cosmicHeightSelections[8] = 10
cosmicHeightSelections[9] = 140
cosmicHeightSelections[1+b2Delta] = 100
cosmicHeightSelections[5] = 700
cosmicHeightSelections[6+b2Delta] = 500
#Panels
#Top
cosmicHeightSelections[10] = 8
cosmicHeightSelections[14] = 8
cosmicHeightSelections[14+b2Delta] = 8
#Left
cosmicHeightSelections[11] = 8
cosmicHeightSelections[11+b2Delta] = 8
cosmicHeightSelections[15+b2Delta] = 8
#Right
cosmicHeightSelections[13+b2Delta] = 6
cosmicHeightSelections[3+b2Delta] = 8
cosmicHeightSelections[10+b2Delta] = 8
#Slabs
cosmicHeightSelections[2+b2Delta] = 200
cosmicHeightSelections[4+b2Delta] = 200
cosmicHeightSelections[5+b2Delta] = 300
cosmicHeightSelections[12+b2Delta] = 60
# inputFile = r.TFile("/net/cms26/cms26r0/milliqan/milliqanOffline/testCalibration.root")
inputFile = r.TFile("./Run834.root")
def upgradeCalibrationIntraLayerPlots(allSlices,sliceExtraSelections,ignoreChans):
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
                calibHistos[sName,higherChan,ySlice[0]] = r.TH1D("chans_{0}_{1}".format(higherChan,ySlice[0],name),"",160,-50,50)
                calibHistos[sName,higherChan,ySlice[0]].SetDirectory(0)
    for event in inputTree:
        if iE % int(nEvents/5) == 0: 
            print iE*1./nEvents
        if event.beam != beamOn:
            iE += 1
            continue
        chans = event.chan
        heights = event.height
        times = event.time
        firstPulses = {}
        for chan,height,time in zip(chans,heights,times):
            if chan in ignoreChans: continue
            if chan not in firstPulses and height > cosmicHeightSelections[chan]:
                firstPulses[chan] = time
        for sName,slices in allSlices.iteritems():
            for sliceNum,ySlice in slices.iteritems():
                if len(firstPulses) > len(ySlice+sliceExtraSelections[sliceNum]):continue
                if set(ySlice+sliceExtraSelections[sliceNum]).issubset(firstPulses.keys()):
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
            sliceHists[sliceNum,sliceNum-1] = r.TH1D("chans_{0}_{1}".format(sliceNum,sliceNum-1),"",160,-50,50)
        sliceHists[sliceNum,sliceNum] = r.TH1D("chans_{0}_{1}".format(sliceNum,sliceNum),"",160,-50,50)
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
                if chan in topPanels: continue
                calibConstantsIntraLayer[chan] -= (hist.GetMean()/0.625)*0.625
    outFile = r.TFile('calibInterSlice'+fNameTag+'.root','RECREATE')
    outFile.cd()
    for _,sliceHist in sliceHists.iteritems():
        sliceHist.Write()
    return calibConstantsIntraLayer
def upgradeCalibrationSlabPanel(calibConstantsInterLayer,slabCalibrations,slabExtraSelections,panelExtraSelections):
    inputTree = inputFile.Get("t")
    calibHistosSlab = {}
    for slabNum,layers in slabCalibrations.iteritems():
        calibHistosSlab[slabNum] = r.TH1D("chans_{0}".format(slabNum),"",160,-50,50)
        calibHistosSlab[slabNum].SetDirectory(0)
    calibHistosPanel = {}
    for panelNum,layers in panelCalibrations.iteritems():
        calibHistosPanel[panelNum] = r.TH1D("chans_{0}".format(panelNum),"",160,-50,50)
        calibHistosPanel[panelNum].SetDirectory(0)
    iE = 1
    nEvents = inputTree.GetEntries()
    for event in inputTree:
        if iE % int(nEvents/5) == 0: 
            print iE*1./nEvents
        if event.beam != beamOn:
            iE += 1
            continue
        chans = event.chan
        heights = event.height
        times = event.time
        layers = event.layer
        firstPulses = {}
        firstPulsesExtra = {}
        for layer,height,time,chan in zip(layers,heights,times,chans):
            if chan not in firstPulsesExtra and height > cosmicHeightSelections[chan]:
                firstPulsesExtra[chan] = time
            if chan not in calibConstantsInterLayer: continue
            if layer not in firstPulses and height > cosmicHeightSelections[chan]:
                firstPulses[layer] = time+calibConstantsInterLayer[chan]
        if set(slabExtraSelections).issubset(set(firstPulsesExtra.keys())):
            for slabNum,layers in slabCalibrations.iteritems():
                if set(layers).issubset(firstPulses):
                    for layer in layers:
                        if slabNum in firstPulsesExtra:
                            calibHistosSlab[slabNum].Fill(firstPulsesExtra[slabNum]-firstPulses[layer])
        for panelNum,layers in panelCalibrations.iteritems():
            if set(panelExtraSelections[panelNum]).issubset(set(firstPulsesExtra.keys())):
                if set(layers).issubset(firstPulses): 
                    for layer in layers:
                        if panelNum in firstPulsesExtra:
                            calibHistosPanel[panelNum].Fill(firstPulsesExtra[panelNum]-firstPulses[layer])
        iE += 1
    outputFile = r.TFile("calibSlabPanel"+fNameTag+".root","RECREATE")
    calibMeans = {}
    calibConstantsInterLayerSlabPanel = copy.deepcopy(calibConstantsInterLayer)
    for slabNum,layers in slabCalibrations.iteritems():
        calibHistosSlab[slabNum].Write()
        calibMeans[slabNum] = (calibHistosSlab[slabNum].GetMean()/0.625)*0.625
        calibConstantsInterLayerSlabPanel[slabNum] = -calibMeans[slabNum]
    for panelNum,layers in panelCalibrations.iteritems():
        calibHistosPanel[panelNum].Write()
        calibMeans[panelNum] = (calibHistosPanel[panelNum].GetMean()/0.625)*0.625
        calibConstantsInterLayerSlabPanel[panelNum] = -calibMeans[panelNum]

    return calibConstantsInterLayerSlabPanel
def upgradeCalibrationInterLayer(calibConstantsIntraLayer,allLayerPaths,layerExtraSelections):
    calibConstantsFinal = {}
    inputTree = inputFile.Get("t")
    layerToChannel = {1:(0,1,24,25,9),2:(6,7,16,17,12,13),3:(2,3,22,23,4,5)}
    calibHistos = {}
    for pathNum,layers in allLayerPaths.iteritems():
        for higherLayer in layers[1:]:
            calibHistos[higherLayer,layers[0]] = r.TH1D("chans_{0}_{1}".format(higherLayer,layers[0]),"",160,-50,50)
            calibHistos[higherLayer,layers[0]].SetDirectory(0)
    iE = 1
    nEvents = inputTree.GetEntries()
    for event in inputTree:
        if iE % int(nEvents/5) == 0: 
            print iE*1./nEvents
        if event.beam != beamOn:
            iE += 1
            continue
        chans = event.chan
        heights = event.height
        times = event.time
        layers = event.layer
        firstPulses = {}
        firstPulsesExtra = {}
        for layer,height,time,chan in zip(layers,heights,times,chans):
            if chan not in firstPulsesExtra and height > cosmicHeightSelections[chan]:
                firstPulsesExtra[chan] = time
            if chan not in calibConstantsIntraLayer: continue
            if layer not in firstPulses and height > cosmicHeightSelections[chan]:
                firstPulses[layer] = time+calibConstantsIntraLayer[chan]
        if set(layerExtraSelections).issubset(set(firstPulsesExtra.keys())):
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
            calibMeans[higherLayer,layers[0]] = (calibHistos[higherLayer,layers[0]].GetMean()/0.625)*0.625

    for layer,chans in layerToChannel.iteritems():
        for chan in chans:
            if layer == 2 or layer == 3:
                calibConstantsInterLayer[chan] -= calibMeans[2,1]
            if layer == 3:
                calibConstantsInterLayer[chan] -= calibMeans[3,2]
            calibConstantsInterLayer[chan] = round(calibConstantsInterLayer[chan]/0.625)*0.625

    return calibConstantsInterLayer
if __name__=="__main__":
    allSlices = {}
    #orig
    # allSlices["slicesStraight"] = {1:(0,8+b2Delta,8),2:(1,9+b2Delta,9),3:(6,0+b2Delta,12),4:(7,1+b2Delta,13),5:(2,6+b2Delta,4),6:(3,7+b2Delta,5)}
    # allSlices["slicesBent1"] = {1:(1,8+b2Delta,8),2:(0,9+b2Delta,9),3:(7,0+b2Delta,12),4:(6,1+b2Delta,13),5:(3,6+b2Delta,4),6:(2,7+b2Delta,5)}
    # allSlices["slicesBent2"] = {1:(1,9+b2Delta,8),2:(0,8+b2Delta,9),3:(7,1+b2Delta,12),4:(6,0+b2Delta,13),5:(3,7+b2Delta,4),6:(2,6+b2Delta,5)}
    # allSlices["slicesBent3"] = {1:(1,8+b2Delta,9+b2Delta,8),2:(0,8+b2Delta,9+b2Delta,9),3:(7,0+b2Delta,1+b2Delta,12),4:(6,0+b2Delta,1+b2Delta,13),5:(3,6+b2Delta,7+b2Delta,4),6:(2,6+b2Delta,7+b2Delta,5)}
    #using 10
    layerExtraSelections=[]#4+b2Delta,12+b2Delta]#2+b2Delta]#,4+b2Delta,12+b2Delta,5+b2Delta]
    allSlabs=[2+b2Delta,4+b2Delta,12+b2Delta,5+b2Delta]
    allPanels=[11+b2Delta,11,15+b2Delta,13+b2Delta,3+b2Delta,10+b2Delta,10,14+b2Delta,14]
    slabExtraSelections = {}
    for slab in allSlabs:
        slabExtraSelections[slab] = []
    panelExtraSelections = {}
    for panel in allPanels:
        panelExtraSelections[panel] = []
    # layerExtraSelections=[]
    ignoreChansForSlices = [2+b2Delta,4+b2Delta,12+b2Delta,5+b2Delta,11+b2Delta,11,15+b2Delta,13+b2Delta,3+b2Delta,10+b2Delta]
    sliceExtraSelections={1:[10],2:[10],3:[14+b2Delta],4:[14+b2Delta],5:[14],6:[14]}
    allSlices["slicesStraight"] = {1:[0,8+b2Delta],2:[1,9+b2Delta,9],3:[6,0+b2Delta,12],4:[7,1+b2Delta,13],5:[2,6+b2Delta,4],6:[3,7+b2Delta,5]}
    allSlices["slicesBent1"] = {1:[1,8+b2Delta],2:[0,9+b2Delta,9],3:[7,0+b2Delta,12],4:[6,1+b2Delta,13],5:[3,6+b2Delta,4],6:[2,7+b2Delta,5]}
    allSlices["slicesBent2"] = {1:[1,9+b2Delta],2:[0,8+b2Delta,9],3:[7,1+b2Delta,12],4:[6,0+b2Delta,13],5:[3,7+b2Delta,4],6:[2,6+b2Delta,5]}
    allSlices["slicesBent3"] = {1:[1,8+b2Delta,9+b2Delta],2:[0,8+b2Delta,9+b2Delta,9],3:[7,0+b2Delta,1+b2Delta,12],4:[6,0+b2Delta,1+b2Delta,13],5:[3,6+b2Delta,7+b2Delta,4],6:[2,6+b2Delta,7+b2Delta,5]}
    # allSlices["slicesBent3"] = {1:(1,2,3,4),2:(0,2,3,5),3:(7,12,13,8),4:(6,12,13,9)}
    allLayerPaths = {1:(1,2),2:(2,3),3:(1,3)}

    slabCalibrations={2+b2Delta:[1,2],4+b2Delta:[1,2],12+b2Delta:[2,3],5+b2Delta:[2,3]}
    panelCalibrations={11+b2Delta:[1],11:[2],15+b2Delta:[3],13+b2Delta:[1],3+b2Delta:[2],10+b2Delta:[3],10:[1],14+b2Delta:[2],14:[3]}
    slabExtraSelections=[]
    upgradeCalibrationIntraLayerPlots(allSlices,sliceExtraSelections,ignoreChansForSlices)
    print "Done intra slice"
    calibConstantsIntraLayer = upgradeCalibrationIntraLayerCalculateCalibration("calibIntraSlice"+fNameTag+".root",allSlices)
    print "Done inter slice"
    pickle.dump(calibConstantsIntraLayer,open("calibConstantsIntraLayer"+fNameTag+".pkl",'w'))
    calibConstantsInterLayer = upgradeCalibrationInterLayer(calibConstantsIntraLayer,allLayerPaths,layerExtraSelections)
    print "Done inter layer"
    pickle.dump(calibConstantsInterLayer,open("calibConstantsInterLayer"+fNameTag+".pkl",'w'))
    calibConstantsInterLayerSlabPanel = upgradeCalibrationSlabPanel(calibConstantsInterLayer,slabCalibrations,slabExtraSelections,panelExtraSelections)
    pickle.dump(calibConstantsInterLayerSlabPanel,open("calibConstantsInterLayerSlabPanel"+fNameTag+".pkl",'w'))
    print "Done panel/slabs"

    print calibConstantsIntraLayer
    print calibConstantsInterLayer
    print calibConstantsInterLayerSlabPanel

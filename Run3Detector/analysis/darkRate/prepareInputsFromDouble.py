import ROOT as r
r.gROOT.SetBatch()

from array import array
binsDeltaT = array("d",range(-50,60,2))
def makeDoubleTemplatesVsTimeDiff(inputTree,chans,heights):
    extraSel = ""
    pulseQual = ["!(height < 25. && duration < 4.6*(height-12.))",
    "!(height >= 25. && duration < 60.)",
    "!(0.001*area < 0.4 && duration < 150.*(0.001*area))",
    "!(0.001*area >= 0.4 && duration < 60.)",
    "!(height > 17. && 0.001*area < 0.04*(height-17.))"]
    pulseQual = "(1)"
    # pulseQual = "("+"&&".join(pulseQual)+")"
    # extraSel = "&&("+pulseQual+")"
    # extraSel += "&&MaxIf$(height,chan!={0}&&chan!=30&&chan!={1}&&chan!=15)<0.1&&MaxIf$(sideband_RMS,$Iteration!=15)<1.3".format(*chans)
    # extraSel += "&&Sum$(chan=={0})==1&&Sum$(chan=={1})==1".format(*chans)
    # extraSel += "&&Max$(height)<{0}".format(heights[-1])
    chanSorted = chans
    histName = "double_chans_{0}_{1}".format(chans[0],chans[1])
    outputHist = r.TH1D(histName,"",len(binsDeltaT)-1,binsDeltaT)
    inputTree.Draw("MinIf$(time,chan=={0}&&{2})-MinIf$(time,chan=={1}&&{2})>>".format(chanSorted[1],chanSorted[0],pulseQual)+histName,"abs(MinIf$(time,chan=={0}&&{2})-MinIf$(time,chan=={1}&&{2}))<100&&MinIf$(time,chan=={0}&&{2})>200&&MinIf$(time,chan=={1}&&{2})>200&&MinIf$(time,chan=={0}&&{2})<2000&&MinIf$(time,chan=={1}&&{2})<2000{3}".format(chanSorted[1],chanSorted[0],pulseQual,extraSel))
    nEntries = inputTree.GetEntries()
    totalTime = 2000E-9*nEntries
    outputHist.Scale(1./totalTime)
    return outputHist
def makeDoubleTemplatesVsNPE(inputTree,chans,heights):
    extraSel = ""
    # extraSel += "&&MaxIf$(height,chan!={0}&&chan!=30&&chan!={1}&&chan!=15)<0.1&&MaxIf$(sideband_RMS,Iteration$!=15)<1.3".format(*chans)
    # extraSel += "&&Sum$(chan=={0})==1&&Sum$(chan=={1})==1".format(*chans)
    # extraSel += "&&Max$(height)<{0}".format(heights[-1])
    # chanLayers = [chanToLayer[x] for x in chans]
    # chanSorted = [y for _,y in sorted(zip(chanLayers,chans))]
    chanSorted = chans
    histName = "double_chans_{0}_{1}".format(chans[0],chans[1])
    outputHist = r.TH1D(histName,"",len(heights)+0,array('d',heights+[heights[-1]+50]))
    inputTree.Draw("MinIf$(height,chan=={0}||chan=={1})>>".format(chanSorted[1],chanSorted[0])+histName,"abs(MinIf$(time,chan=={0})-MinIf$(time,chan=={1}))<50&&MinIf$(time,chan=={0})>200&&MinIf$(time,chan=={1})>200&&MinIf$(time,chan=={0})<2000&&MinIf$(time,chan=={1})<2000{2}".format(chanSorted[1],chanSorted[0],extraSel))
    nEntries = inputTree.GetEntries()
    totalTime = 2000E-9*nEntries
    outputHist.Scale(1./totalTime)
    return outputHist
def prepareInputsFromDouble(useSaved=False):
    # inputDict = makeInputDict('source.txt')
    outputHists= {}
    # if useSaved:
    #     outputFile = r.TFile("doubleTemplatesVsNPE.root")
    #     for chans in inputDict.keys():
    #         outputHists[chans] = outputFile.Get("double_chans_{0}_{1}".format(chans[0],chans[1]))
    #     return outputFile,outputHists
    # else:
    #     outputFile = r.TFile("doubleTemplatesVsNPE.root","RECREATE")
    # heights = binsNPE
    # inDir = "/Users/mcitron/milliqanOffline/milliqanScripts/dcRuns/"
    # pbar = ProgressBar()
    outputFile = r.TFile("doubleTemplatesVsNPEPulseRun490.root","RECREATE")
    chanPairs = [(x,(x+1)%64) for x in range(0,63,2)]
    print (chanPairs)
    # chanPairs = [(0,1),(16,17),(32,33)] 
    inputFile = r.TFile("/homes/milliqan/milliqanOffline/Run3Detector/outputRun3/MilliQan_Run490_default_v23_updateChanNumbering.root")
    inputTree = inputFile.Get("t")
    heights = [0,75,200,400,1000,10000]
    chanToLayer = {}
    for i in range(16): chanToLayer[i] = 0
    for i in range(16,32): chanToLayer[i] = 1
    for i in range(32,48): chanToLayer[i] = 2
    for i in range(48,64): chanToLayer[i] = 3
    for chans in chanPairs:
        outputHist = makeDoubleTemplatesVsTimeDiff(inputTree,chans,heights)
        outputFile.cd()
        outputHist.Write()
        outputHists[chans] = outputHist
    outputHistsPerLayer = {}
    for layer in range(4):
        histName = "double_layer_"+str(layer)
        outputHistsPerLayer[layer] = r.TH1D(histName,"",len(binsDeltaT)-1,binsDeltaT)
    for chan in outputHists.keys():
        outputHistsPerLayer[chanToLayer[chan[0]]].Add(outputHists[chan])
    for layer in range(4):
        outputHistsPerLayer[layer].Write()

    return outputFile,outputHists
 
def throwToysFromDouble():
    useSaved = False
    print ("Getting inputs from doubles")
    inputFileDoubles,inputHistsDoubles = prepareInputsFromDouble(useSaved)
    chanToLayer = {}
    # totalRatesSingles = getSinglesRates(r.TFile("heightValidationUnbiased.root"))
    # print "Running toys"
    # for i in pbar(range(1000)):
    #     maxDeltaT = 1000
    #     for path in paths:
    #         for iO,otherChan in enumerate(path):
    #             doubleChans = path[iO+1:]+path[:iO]
    #             histInput = outputHists[doubleChans]
    #             while abs(maxDeltaT) > 100:
    #                 test1 = rand.Uniform(-1000,1000)
    #                 maxDeltaT = max([test2-test1,test3-test2,test1-test3],key = lambda x:abs(x))
if __name__=="__main__":
    throwToysFromDouble()


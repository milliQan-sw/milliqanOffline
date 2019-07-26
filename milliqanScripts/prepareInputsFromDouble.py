import ROOT as r

from measureSingleRateFromDouble import makeInputDict
from measureBackgrounds import layers,binsNPE,binsDeltaT
from throwToysForTriple import chanToLayer
from progressbar import ProgressBar
from throwToysForTriple import getSinglesRates,channelCalibrations

def makeDoubleTemplatesVsNPE(inputTree,chans,nPEs):
    extraSel = ""
    extraSel += "&&MaxIf$(nPE,chan!={0}&&chan!=30&&chan!={1})<0.1&&Max$(sideband_RMS)<1.3".format(*chans)
    extraSel += "&&Sum$(chan=={0})==1&&Sum$(chan=={1})==1".format(*chans)
    extraSel += "&&Max$(nPE)<{0}".format(nPEs[-1])
    chanLayers = [chanToLayer[x] for x in chans]
    chanSorted = [y for _,y in sorted(zip(chanLayers,chans))]
    histName = "double_chans_{0}_{1}".format(chans[0],chans[1])
    outputHist = r.TH1D(histName,"",len(binsDeltaT)-1,binsDeltaT)
    inputTree.Draw("MinIf$(time,chan=={0})-MinIf$(time,chan=={1})>>".format(chanSorted[1],chanSorted[0])+histName,"abs(MinIf$(time,chan=={0})-MinIf$(time,chan=={1}))<100&&groupTDC_b1[0]==groupTDC_b0[0]&&MinIf$(time,chan=={0})>60&&MinIf$(time,chan=={1})>60{2}".format(chanSorted[1],chanSorted[0],extraSel))
    totalTime = inputTree.GetMaximum("event_time_fromTDC")-inputTree.GetMinimum("event_time_fromTDC")
    nEntries = inputTree.GetEntries()
    nEntriesEff = inputTree.Draw("","groupTDC_b1[0]==groupTDC_b0[0]","goff")
    totalTime *= nEntriesEff*1./nEntries
    outputHist.Scale(1./totalTime)
    return outputHist
def prepareInputsFromDouble(useSaved=False):
    inputDict = makeInputDict('source.txt')
    outputHists= {}
    if useSaved:
        outputFile = r.TFile("doubleTemplates.root")
        for chans in inputDict.keys():
            outputHists[chans] = outputFile.Get("double_chans_{0}_{1}".format(chans[0],chans[1]))
        return outputFile,outputHists
    else:
        outputFile = r.TFile("doubleTemplates.root","RECREATE")
    nPEs = binsNPE
    inDir = "/Users/mcitron/milliqanOffline/milliqanScripts/dcRuns/"
    pbar = ProgressBar()
    for chans in pbar(inputDict.keys()):
        inputFile = r.TFile(inDir+"/"+inputDict[chans])
        inputTree = inputFile.Get("t")
        outputHist = makeDoubleTemplatesVsNPE(inputTree,chans,nPEs)
        outputFile.cd()
        outputHist.Write()
        outputHists[chans] = outputHist
    return outputFile,outputHists
 
def throwToysFromDouble():
    useSaved = False
    print "Getting inputs from doubles"
    inputFileDoubles,inputHistsDoubles = prepareInputsFromDouble(useSaved)
    # totalRatesSingles = getSinglesRates(r.TFile("nPEValidationUnbiased.root"))
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


import ROOT as r
import bisect
import pickle 
r.gROOT.SetBatch()

minBinsMC = {"878":2,"ET":1,"7725":3}
minBinsData = {"878":3,"ET":1,"7725":4}
maxBinsMC = {"878":17,"ET":17,"7725":17}
maxBinsData = {"878":18,"ET":16,"7725":16}
def readTimeInputsPerSpecies(inputFileData,inputFileMC):
    #return time corrections from file (NB: should added to recorded time!)
    speciesList = ["878","ET","7725"]
    timeCorrections = {}
    for species in speciesList:
        areaBins = []
        profHist = inputFileMC.Get("hprof"+species)
        nBins = profHist.GetNbinsX()
        sigmasHist = inputFileData.Get("sigmas"+species)
        sigmas = []
        correctionsMC = []
        correctionsData = []
        for iBin in range(1,nBins+1):
            areaBins.append(profHist.GetBinLowEdge(iBin))
            projData = inputFileData.Get("AreaProj{0}_{1}".format(species,iBin))
            projMC = inputFileMC.Get("AreaProj{0}_{1}".format(species,iBin))
            if projData.GetBinContent(projData.GetMaximumBin()) < 20:
                projData.Rebin(2)
            if projData.GetBinContent(projData.GetMaximumBin()) < 20:
                projData.Rebin(2)
            # projData.Rebin(2)
            binWithMaxData = projData.GetMaximumBin()
            binWithMaxMC = projMC.GetMaximumBin()
            meanData,meanMC = 0,0
            weightData,weightMC = 0,0
            for iRange in range(-4,5):
                meanData += projData.GetBinCenter(binWithMaxData+iRange)*projData.GetBinContent(binWithMaxData+iRange)
                weightData += projData.GetBinContent(binWithMaxData+iRange)
                meanMC += projMC.GetBinCenter(binWithMaxMC+iRange)*projMC.GetBinContent(binWithMaxMC+iRange)
                weightMC += projMC.GetBinContent(binWithMaxMC+iRange)
            if weightData > 0:
                meanData /= weightData
            if weightMC > 0: 
                meanMC /= weightMC
            if iBin > maxBinsData[species]:
                correctionsData.append(correctionsData[-1])
            else:
                correctionsData.append(-meanData)
            if iBin > maxBinsMC[species]:
                correctionsMC.append(correctionsMC[-1])
            else:
                correctionsMC.append(-meanMC)
        for iBin in range(1,nBins+1):
            if iBin < minBinsMC[species]:
                correctionsMC[iBin-1] = correctionsMC[minBinsMC[species]-1]
            if iBin < minBinsData[species]:
                correctionsData[iBin-1] = correctionsData[minBinsData[species]-1]-(correctionsMC[minBinsData[species]-1]-correctionsMC[iBin-1])
                sigmas.append(sigmasHist.GetBinContent(minBinsData[species]))
            else:
                if iBin > maxBinsData[species]:
                    sigmas.append(sigmasHist.GetBinContent(maxBinsData[species]))
                else:
                    sigmas.append(sigmasHist.GetBinContent(iBin))
        timeCorrections["data",species] = (areaBins,correctionsData,[0]*len(sigmas))
        timeCorrections["signal",species] = (areaBins,correctionsMC,sigmas)
        print (species)
        for i in range(len(timeCorrections["data",species][0])):
            print (i+1,timeCorrections["data",species][0][i],timeCorrections["data",species][1][i],timeCorrections["signal",species][1][i],timeCorrections["signal",species][2][i])
    return timeCorrections
def readTimeInputs(inputFileDataAbs,inputFileMCAbs,inputFileDataRMS,inputFileMCRMS):
    #return time corrections from file (NB: should added to recorded time!)
    sigmas = {}
    sigmasHistData = inputFileDataRMS.Get("sigmas")
    sigmasHistMC = inputFileMCRMS.Get("sigmas")
    profData = inputFileDataAbs.Get("hprofX")
    profMC = inputFileMCAbs.Get("hprofX")
    areaBins,timeShiftsData,timeShiftsMC,sigmasData,sigmasMC,sigmasCorr = [],[],[],[],[],[]
    for iBin in range(1,profData.GetNbinsX()+1):
        areaBins.append(profData.GetBinLowEdge(iBin))
        timeShiftsData.append(profData.GetBinContent(iBin))
        timeShiftsMC.append(profMC.GetBinContent(iBin))
        sigmasData.append(sigmasHistData.GetBinContent(iBin))
        sigmasMC.append(sigmasHistMC.GetBinContent(iBin))
        sigmaCorr = 0 if sigmasData[-1] < sigmasMC[-1] else (sigmasData[-1]**2-sigmasMC[-1]**2)**0.5
        sigmasCorr.append(sigmaCorr)
    meanShiftData = sum(timeShiftsData)/len(timeShiftsData)
    meanShiftMC = sum(timeShiftsMC)/len(timeShiftsMC)
    for i in range(len(timeShiftsMC)):
        timeShiftsData[i] = -(timeShiftsData[i])# - meanShiftData)
        timeShiftsMC[i] = -(timeShiftsMC[i])# - meanShiftMC)
    timeCorrections = {}
    timeCorrections["data"] = (areaBins,timeShiftsData,[0]*len(timeShiftsData))
    timeCorrections["signal"] = (areaBins,timeShiftsMC,sigmasCorr)
    return timeCorrections
    
    
def getCorrections(inputDir=None,saveToPickle=False,readFromPickle=None):
    if readFromPickle:
        return pickle.load(open(readFromPickle,'rb'))
    else:
        if inputDir == None:
            inputDir = "./timeCorrectionsFiles_update/200324/"
            inputFileData = r.TFile(inputDir+"SmallPulseDelay_data_Sat_noCh4.root")
            inputFileMC = r.TFile(inputDir+"SmallPulseDelay_MC_Sat.root")
            allInputFiles = [inputFileData,inputFileMC]
            timeCorrections = readTimeInputsPerSpecies(inputFileData,inputFileMC)
        #old inputs
        # if inputDir == None:
        #     inputDir = "./timeCorrectionsFiles/"
        # inputFileDataAbs = r.TFile(inputDir+"SmallPulseDelay_data.root")
        # inputFileMCAbs = r.TFile(inputDir+"SmallPulseDelay_MC.root")
        # inputFileMCRMS = r.TFile(inputDir+"Area_Proj_MC.root")
        # inputFileDataRMS = r.TFile(inputDir+"Area_Proj_data.root")
        # allInputFiles = [inputFileDataAbs,inputFileMCAbs,inputFileDataRMS,inputFileMCRMS]
        # timeCorrections = readTimeInputs(inputFileDataAbs,inputFileMCAbs,inputFileDataRMS,inputFileMCRMS)
        for iFile in allInputFiles:
            iFile.Close()
    if saveToPickle:
        pickle.dump(timeCorrections,open(saveToPickle,"wb"))
    return timeCorrections

if __name__=="__main__":
    getCorrections(saveToPickle="timeCorrectionsPickle.pkl")



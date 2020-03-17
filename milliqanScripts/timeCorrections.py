import ROOT as r
import bisect
r.gROOT.SetBatch()

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
    
    

def getCorrections(inputDir=None):
    if inputDir == None:
        inputDir = "./timeCorrectionsFiles/"
    inputFileDataAbs = r.TFile(inputDir+"SmallPulseDelay_data.root")
    inputFileMCAbs = r.TFile(inputDir+"SmallPulseDelay_MC.root")
    inputFileMCRMS = r.TFile(inputDir+"Area_Proj_MC.root")
    inputFileDataRMS = r.TFile(inputDir+"Area_Proj_data.root")
    allInputFiles = [inputFileDataAbs,inputFileMCAbs,inputFileDataRMS,inputFileMCRMS]
    timeCorrections = readTimeInputs(inputFileDataAbs,inputFileMCAbs,inputFileDataRMS,inputFileMCRMS)
    for iFile in allInputFiles:
        iFile.Close()
    return timeCorrections

if __name__=="__main__":
    getCorrections()
    


import ROOT

#file = ROOT.TFile("/home/czheng/scratch0/cosmicExplore/milliqanOffline/Run3Detector/analysis/utilities/chanvsNPE_Nocut.root")

filewithPUBM = ROOT.TFile("/home/czheng/scratch0/cosmicExplore/milliqanOffline/Run3Detector/analysis/utilities/chanvsNPE_withcut.root")


#hist = file.Get("B ChanvsNPE")
#hist_P = file.Get("P ChanvsNPE")
histwithPUBM = filewithPUBM.Get("B ChanvsNPE")
#P is for panel, no p is for bar
histwithPUBM_p = filewithPUBM.Get("P ChanvsNPE")


#hist.Add(hist_P, 1)
histwithPUBM.Add(histwithPUBM_p, 1)


#ChanHist=hist.ProjectionX()
ChanHistwithPUBM=histwithPUBM.ProjectionX()



#ChanHist.SetXTitle("chan")
ChanHistwithPUBM.SetXTitle("chan")
#ChanHist.SetYTitle("number of pulses")
ChanHistwithPUBM.SetYTitle("number of pulses")


output_file = ROOT.TFile("Run1190ChandistwithPKBMcut.root", "RECREATE")
ChanHistwithPUBM.Write()

output_file.Close()
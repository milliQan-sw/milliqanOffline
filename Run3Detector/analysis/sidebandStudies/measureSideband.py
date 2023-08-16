import ROOT as r
r.gROOT.SetBatch()
pedestalsPrev = [-0.00,-0.40,0.50,1.20,0.0,-0.20,0.70,-0.30,0.70,0.20,0.40,-0.00,1.10,0.10,0.10,0.10,5.90,-0.70,-0.10,0.20,0.20,-0.00,0.10,0.40,0.10,-0.10,-0.00,0.20,-0.10,-0.20,0.20,0.10,1.90,-0.00,-0.00,0.00,0.30,-0.30,-0.10,0.20,0.10,-0.50,0.80,0.20,0.60,-0.10,0.10,0.10,0.60,1.00,0.30,-1.50,0.90,0.90,-1.10,0.10,-0.10,-0.50,0.30,-0.70,0.50,-0.40,0.10,0.40,-0.50,-0.20,0.70,0.10,0.40,-0.00,-0.40,-4.00,-0.20,-0.00,-14.80,-3.50,0.80,-0.30,-0.00,0.20]
inputFile = r.TFile("MilliQan_Run678_default_v29.root","READ")
inputTree = inputFile.Get("t")
hist2D = r.TH2D("sidebandHist","",80,-0.5,79.5,1000,-10,10)
inputTree.Draw("sidebandMean:Iteration$>>"+hist2D.GetName(),"sidebandRMS<1.2","colz")
outputPed = []
for iBin in range(1,hist2D.GetNbinsX()+1):
    chan = hist2D.GetXaxis().GetBinCenter(iBin)
    proj = hist2D.ProjectionY(str(chan),iBin,iBin)
    correction = proj.GetBinCenter(proj.GetMaximumBin())
    correction = round(correction/0.1)*0.1
    correctionTotal = correction+pedestalsPrev[iBin-1]
    outputPed.append(float("%.1f"%correctionTotal))
print (outputPed)

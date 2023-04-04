import ROOT as r
import glob

r.gStyle.SetOptStat(0)
# r.gROOT.SetBatch(1)

HVs = [1150, 1250, 1300, 1350, 1450]
# HVs = [1150, 1250, 1350, 1450]
hs = []

fout = r.TFile("tmp/pulse_area_hists.root", "RECREATE")
for HV in HVs:
    fid = r.TFile("r878_{0}V_1p56V_20ns_100Hz_100000evnts.root".format(HV))
    t = fid.Get("Events")
    hs.append(r.TH1D("h{0}".format(HV),";pulse area [pVs]", 175, -50, 300))
    t.Draw("area>>h{0}".format(HV),"","goff")
    hs[-1].SetDirectory(0)
    fout.cd()
    hs[-1].Write()
    fid.Close()
fout.Close()
exit(0)

cols = [r.kBlack, r.kRed, r.kBlue, r.kGreen+2, r.kMagenta+1]

c = r.TCanvas()
hdummy = hs[0].Clone("hdummy")
maxval = 0
for h in hs:
    maxval = max(maxval, h.GetMaximum())
hdummy.Reset()
hdummy.GetYaxis().SetRangeUser(0,maxval*1.2)
hdummy.Draw()
leg = r.TLegend(0.75, 0.70, 0.88, 0.88)
for i,HV in list(enumerate(HVs)):
    hs[i].SetLineColor(cols[i])
    hs[i].SetLineWidth(2)
    hs[i].Draw("HIST SAME")
    leg.AddEntry(hs[i], "{0} V".format(HV), 'l')

leg.Draw()

raw_input()


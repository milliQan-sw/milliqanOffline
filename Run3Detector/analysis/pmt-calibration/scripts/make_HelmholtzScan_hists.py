import ROOT as r
import glob

r.gStyle.SetOptStat(0)
# r.gROOT.SetBatch(1)

Is =[0.0,0.82,1.0,1.5]
names = ["0p0","0p82","1p0","1p5"]

hs = []

for name in names:
    fid = r.TFile("/nfs-7/userdata/bemarsh/milliqan/pmt_calib/processed/r878_Helm{0}A_1450V_1p92V_13ns_300Hz_50000evnts.root".format(name))
    t = fid.Get("Events")
    hs.append(r.TH1D("h{0}".format(name),";pulse area [pVs]", 175, -50, 300))
    t.Draw("area>>h{0}".format(name),"","goff")
    hs[-1].SetDirectory(0)
    fid.Close()

cols = [r.kBlack, r.kRed, r.kBlue, r.kGreen+2, r.kMagenta+1]

c = r.TCanvas()
hdummy = hs[0].Clone("hdummy")
maxval = 0
for h in hs:
    maxval = max(maxval, h.GetMaximum())
hdummy.Reset()
hdummy.SetMaximum(maxval*1.2)
hdummy.Draw()
leg = r.TLegend(0.75, 0.70, 0.88, 0.88)
for i,I in list(enumerate(Is)):
    hs[i].SetLineColor(cols[i])
    hs[i].SetLineWidth(2)
    hs[i].Draw("HIST SAME")
    leg.AddEntry(hs[i], "{0} A".format(I), 'l')

leg.Draw()

raw_input()


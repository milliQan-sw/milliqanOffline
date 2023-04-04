import ROOT as r
import numpy as np

r.gStyle.SetOptStat(0)
r.TH1.StatOverflows(1)

# name_s = "r878h_1450V_2p7V_20ns_300Hz_400000evnts_v2"
# name_b = "r878b_1450V_2p7V_20ns_300Hz_100000evnts"

# name_s = "r878_Helm0p0A_1450V_1p92V_13ns_300Hz_50000evnts"
# name_b = "r878b_Helm0p0A_1450V_1p92V_13ns_300Hz_50000evnts"

# name_s = "r878_Helm0p82A_1450V_1p92V_13ns_300Hz_50000evnts"
# name_b = "r878b_Helm0p82A_1450V_1p92V_13ns_300Hz_50000evnts"

# name_s = "r878_Helm1p0A_1450V_1p92V_13ns_300Hz_50000evnts"
# name_b = "r878b_Helm1p0A_1450V_1p92V_13ns_300Hz_50000evnts"

# name_s = "r878_Helm1p5A_1450V_1p92V_13ns_300Hz_50000evnts"
# name_b = "r878b_Helm1p5A_1450V_1p92V_13ns_300Hz_50000evnts"

# name_s = "r878_Helm0p0ALong_1450V_1p92V_13ns_300Hz_50000evnts"
# name_b = "r878b_Helm0p0ALong_1450V_1p92V_13ns_300Hz_50000evnts"

name_s = "r878_Helm1p5ALong_1450V_1p92V_13ns_300Hz_50000evnts"
name_b = "r878b_Helm1p5ALong_1450V_1p92V_13ns_300Hz_50000evnts"

# name_s = "r878h_1450V_2p5V_20ns_300Hz_50000evnts"
# name_b = "r878b_1450V_2p5V_20ns_300Hz_50000evnts"

# name_s = "r7725/r7725_1400V_1p91V_13ns_300Hz_200000evnts"
# name_b = "r7725/r7725b_1400V_1p91V_13ns_300Hz_50000evnts"

fs = r.TFile("/nfs-7/userdata/bemarsh/milliqan/pmt_calib/processed/{0}.root".format(name_s))
ts = fs.Get("Events")

fb = r.TFile("/nfs-7/userdata/bemarsh/milliqan/pmt_calib/processed/{0}.root".format(name_b))
tb = fb.Get("Events")

# for r878
hs = r.TH1D("hs","",125,-50,200)
hb = r.TH1D("hb","",125,-50,200)

# #for r7725
# hs = r.TH1D("hs","",625,-50,1200)
# hb = r.TH1D("hb","",625,-50,1200)

ts.Draw("area>>hs","","goff")
tb.Draw("area-0.8>>hb","","goff")

hb.Scale(hs.Integral(1,27)/hb.Integral(1,27))
htot = hs.Clone("ht")
htot.Add(hb, -1)

f = hb.Integral(0,-1)/hs.Integral(0,-1)
Npe = -np.log(f)
E = (hs.GetMean() - hb.GetMean()) / Npe
V = (hs.GetRMS()**2 - hb.GetRMS()**2) / Npe - E**2
print f, -np.log(f)
print E, np.sqrt(V)

# fit = r.TF1("fit","gaus",-50,30)
# fit.SetParameter(0,500)
# fit.SetParameter(1,0)
# fit.SetParameter(2,5)
# fit2 = r.TF1("fit2","gaus",-50,30)
# fit2.SetParameter(0,500)
# fit2.SetParameter(1,0)
# fit2.SetParameter(2,5)
# hs.Fit("fit","N","goff",-50,10)
# hb.Fit("fit2","N","goff",-50,30)

c = r.TCanvas()
# c.SetLogy(1)

# fit.SetLineColor(r.kBlue)

# hs.GetYaxis().SetRangeUser(50,10000)
hs.GetXaxis().SetTitle("Pulse Area [pVs]")

hb.SetLineColor(r.kRed)

htot.SetLineColor(r.kBlack)
htot.SetLineStyle(2)

hs.SetLineWidth(2)
hb.SetLineWidth(2)
htot.SetLineWidth(2)

hs.Draw("HIST")
hb.Draw("HIST SAME")
htot.Draw("HIST SAME")
# fit.Draw("SAME")
# fit2.Draw("SAME")

leg = r.TLegend(0.55,0.75,0.88,0.88)
leg.AddEntry(hs, "LED On @ 2.7 V", 'l')
leg.AddEntry(hb, "LED Blocked @ 2.7 V", 'l')
leg.Draw()

text = r.TLatex()
text.SetNDC(1)
text.SetTextFont(42)
text.SetTextSize(0.04)
text.DrawLatex(0.55, 0.65, "#scale[1.0]{{#LT}}N_{{PE}}#GT = {0:.2f}".format(-np.log(f)))
text.DrawLatex(0.55, 0.59, "E(SPE) = {0:.1f} pVs".format(E))
text.DrawLatex(0.55, 0.53, "#sigma(SPE) = {0:.1f} pVs".format(np.sqrt(V)))

line = r.TLine()
line.SetLineStyle(2)
line.SetLineWidth(2)
line.DrawLine(E,0,E,hs.GetMaximum())

# c.SaveAs("~/public_html/milliqan/pmt_calib/plots/r7725/sb_1400V_1p91V_pulse_area_calib.png")
c.SaveAs("~/public_html/milliqan/pmt_calib/plots/sb_Helm1p5ALong_1450V_1p92V_pulse_area_calib.png")

raw_input()

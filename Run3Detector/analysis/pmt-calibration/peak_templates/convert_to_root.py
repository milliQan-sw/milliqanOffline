import numpy as np
import ROOT as r
import pickle

# fname = "template_peak_70_75_2GHz.pkl"
fname = "template_peak_r7725_400_550_1GHz.pkl"
a = pickle.load(open(fname, 'rb'))
h = r.TH1D("temp","",a.size,0,a.size)
for i in range(a.size):
    h.SetBinContent(i+1, a[i])

fout = r.TFile(fname.replace(".pkl",".root"), "RECREATE")
h.Write()
fout.Close()

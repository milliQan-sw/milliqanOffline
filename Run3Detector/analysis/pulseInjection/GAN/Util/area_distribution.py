"""
Use to create a histogram of the area distribution for the waveforms
"""
import numpy as np
import uproot
import ROOT as r


WAVEFORM_BOUNDS = (1200, 1600)

input_file = uproot.open("/home/ryan/Documents/Data/MilliQan/outputWaveforms_812_2p5V.root")

histogram_names = input_file.keys()

histogram_dict = {}

area_canvas = r.TCanvas("area", "LED_Area")
output_file = r.TFile("areaWaveforms.root", "RECREATE")
area_hist = r.TH1D("area_hist", "LED Area Histogram", 200, -1000, 5000)
x = np.arange(0, 1024*2.5, 2.5)
waveform_indices = np.where((x >= 1200) & (x <=1600))

for name in histogram_names:
    histogram = input_file[name]
    if histogram.classname == "TH1D":
        data = histogram.values()
        area_hist.Fill(np.trapz(data[waveform_indices]))
area_hist.Draw()
area_canvas.Write()
output_file.Close()

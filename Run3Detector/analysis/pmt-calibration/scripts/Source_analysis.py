#Import the packages
import ROOT as r
import numpy as np
import os

#Switch Directories
os.chdir(r'../Source_Results/')
print(f'Changed directory to {os.getcwd()}')

#Set the cd109 energy peak which is resolved in KeV
cd109 = 22.1

#Set the files for analysis
Files = ['PMT_Cd109_CA3148_1600V.root', 'PMT_Cd109_CA3148_no_mount_1600V.root',
'PMT_Cd109_CA3148_no_mount_no_cover_1600V.root', 'PMT_Cd109_CA3148_no_cover_1600V.root']

#Set the PMT names if a comparison is not going to be made
PMTs = ['CA3148 standard', 'CA3148 no mount', 'CA3148 no mount and no cover', 'CA3148 no cover']

#Set the legends to be used and colors
Legend_entry = ['Standard', 'No mount', 'No mount and No cover', 'No Cover']
colors = [r.kBlack, r.kGreen, r.kRed, r.kBlue]

Comparison = input('Do you want to compare the file plots? Enter yes or no. ')

if Comparison=='yes':
	Area_hists = []
	Scaler_hists = []
	entries = []
	for file in Files:
		df = r.RDataFrame('Events', file)
		entries.append(df.Count().GetValue())
		hist_A = df.Histo1D((file, f'{file}; Pulse Area [mV ns]', 100, 0, 5.e3), 'area_3046_1')
		hist_F = df.Histo1D((file, f'{file}; Scaler',  100, 5.e3, 120.e3), 'scaler_3046_1')
		Area_hists.append(hist_A)
		Scaler_hists.append(hist_F)
	c = r.TCanvas()	
	legend = r.TLegend(0.6, 0.7, 0.8, 0.8)
	legend.SetTextSize(0.03)
	for histo in Area_hists:
		idx = Area_hists.index(histo)
		c.cd()
		c.SetLogy()
		histo.SetTitle('Pulse Area Distributions of PMT Detector with Cd-109')
		histo.SetStats(0)
		histo.GetXaxis().SetTitle('Pulse Area [mV ns]')
		histo.GetYaxis().SetTitle('Counts')
		histo.SetLineColor(colors[idx])
		if Area_hists.index(histo)==0:
			histo.Draw('h')
		elif Area_hists.index(histo)!=0:
			histo.Draw('h, SAME')
		legend.AddEntry(histo.GetPtr(), Legend_entry[idx])
	legend.SetLineWidth(0)
	legend.Draw('same')
	latex = r.TLatex()
	latex.SetTextSize(0.03)
	latex.SetNDC()
	Same_pmt = input('Are we comparing the same PMT? Enter yes or no. ')
	if Same_pmt=='yes':
		PMT = input('Enter the PMT ID: ')
		latex.DrawText(0.6, 0.58, PMT)
	latex.DrawText(0.6, 0.55, 'Cd-109 and Scintillator')
	c.SaveAs(f'{PMT}_Area_comp.png')
	c2 = r.TCanvas()
	c2.cd()
	c2.SetLogy()
	legend2 = r.TLegend(0.15, 0.6, 0.2, 0.8)
	legend2.SetTextSize(0.03)
	for histo in Scaler_hists:
		idx = Scaler_hists.index(histo)
		c2.cd()
		histo.SetTitle('Frequency Distributions of PMT Detector with Cd-109')
		histo.SetStats(0)
		histo.GetXaxis().SetTitle('Frequency [Hz]')
		histo.GetYaxis().SetTitle('Counts')
		histo.SetLineColor(colors[idx])
		if Scaler_hists.index(histo)==0:
			histo.Draw('h')
		elif Scaler_hists.index(histo)!=0:
			histo.Draw('h, SAME')
		legend2.AddEntry(histo.GetPtr(), Legend_entry[idx])
	legend2.SetLineWidth(0)
	legend2.Draw('same')
	latex2 = r.TLatex()
	latex2.SetNDC()
	latex2.SetTextSize(0.03)
	latex.DrawText(0.15, 0.5, PMT)
	latex.DrawText(0.15, 0.45, 'Cd-109 and Scintillator')
	c2.SaveAs(f'{PMT}_Freq_comp.png')

if Comparison=='no':
	for file in Files:
		gaus1 = r.TF1('gaus', 'gaus', 1000, 3000)
		gaus2 = r.TF1('gaus2', 'gaus', 50, 500)
		idx = Files.index(file)
		PMT = PMTs[idx]
		df = r.RDataFrame('Events', file)
		hist_A = df.Histo1D((file, f'{file}; Pulse Area [mV ns]', 100, 0, 5.e3), 'area_3046_1')
		hist_F = df.Histo1D((file, f'{file}; Scaler',  100, 5.e3, 120.e3), 'scaler_3046_1')
		c = r.TCanvas()	
		legend = r.TLegend(0.6, 0.7, 0.8, 0.8)
		legend.SetTextSize(0.03)
		c.cd()
	#	c.SetLogy()
		hist_A.SetTitle('Pulse Area Distributions of PMT Detector with Cd-109')
		hist_A.Fit(gaus1, 'R+')
		hist_A.Fit(gaus2, 'R+')
		NPE = (gaus1.GetParameter(1)/gaus2.GetParameter(1))/cd109
		hist_A.SetStats(0)
		hist_A.GetXaxis().SetTitle('Pulse Area [mV ns]')
		hist_A.GetYaxis().SetTitle('Counts')
		hist_A.Draw()
		legend.AddEntry(hist_A.GetPtr(), Legend_entry[idx])
		legend.SetLineWidth(0)
		legend.Draw('same')
		latex = r.TLatex()
		latex.SetTextSize(0.03)
		latex.SetNDC()
		latex.DrawText(0.6, 0.58, PMT)
		latex.DrawText(0.6, 0.55, 'Cd-109 and Scintillator')
		latex.DrawText(0.6, 0.5, 'NPE/KeV = %.2f'%(NPE))
		c.SaveAs(f'{PMT}_Area.png')
		c2 = r.TCanvas()
		c2.cd()
		c2.SetLogy()
		legend2 = r.TLegend(0.15, 0.6, 0.2, 0.8)
		legend2.SetTextSize(0.03)
		c2.cd()
		hist_F.SetTitle('Frequency Distributions of PMT Detector with Cd-109')
		hist_F.SetStats(0)
		hist_F.GetXaxis().SetTitle('Frequency [Hz]')
		hist_F.GetYaxis().SetTitle('Counts')
		hist_F.Draw('h')
		legend2.AddEntry(hist_F.GetPtr(), Legend_entry[idx])
		legend2.SetLineWidth(0)
		legend2.Draw('same')
		latex2 = r.TLatex()
		latex2.SetNDC()
		latex2.SetTextSize(0.03)
		latex.DrawText(0.15, 0.5, PMT)
		latex.DrawText(0.15, 0.45, 'Cd-109 and Scintillator')
		c2.SaveAs(f'{PMT}_Freq.png')

#import necessary packages

import ROOT as r
import os
import glob
import numpy as np

#ignore a fitting warning (not sure why it exists but should not affect anything)
r.gROOT.SetBatch(r.kTRUE)

#Set the directory to the processed root output

os.chdir('../../drsProcessing/PMT_no_source_testing/')

print(f'Currently in {os.getcwd()}')

#Find all of the root files from testing and processing

Files = glob.glob('*.root')

#Set the serial numbers to name the PMT results appropriately; SERIAL NO. MUST BE IN THE ROOT FILE NAME

serial_numbers = ['CA2967', 'UCSB']

#Set the serial numbers for the PMT's you want to compare as well as the different stylistic choices to differentiate them on the plot; THESE MUST ALSO BE IN THE serial_numbers LIST ABOVE

compare = ['CA2967', 'UCSB']

compare_marker_style = [32, 21]

compare_color = [r.kBlue, r.kRed]

#hold the height means for each PMT test at various bias

height_means = {}

#height_errors holds the error of log(pulse height)

height_errors = {}

#hold the area means for each PMT test at various bias 

area_means = {}

#area_errors holds the error of the log(area)

area_errors = {}

#typical range of bias voltage testing

bias_voltages = [1400, 1450, 1500, 1550, 1600]

#Sort the PMT data according to their bias at testing to pre-sort the data

PMTS = {}

sorted_files = {}

for j in serial_numbers:
		
	PMTS[j] = []

for i in Files:

	for j in serial_numbers:
			
		if j in i:
			
			PMTS[j].append(i)

print(PMTS)

#Fit the data distributions and obtain the mean pulse height/area

for key in PMTS.keys():
	
	sorted_files[key] = []
	
	for i in range(len(bias_voltages)):
		
		v = bias_voltages[i]

		for file in PMTS[key]:
			
			if str(v) in file:
				
				sorted_files[key].append(file)

print(sorted_files)

#define the fitting range; obtained in testing while watching the PMT or by using the TTree; write them in order of increasing bias

bias_voltage_bounds_area = [[100, 300], [125, 400], [175, 400], [200, 575], [300, 650]]

bias_voltage_bounds_height = [[20, 40], [20, 55], [30, 75], [45, 100], [60, 135]]

j = 0

for key in sorted_files.keys():

	height_means[key] = []

	height_errors[key] = []

	area_means[key] = []

	area_errors[key] = []

	for file in range(len(sorted_files[key])):
		
		print(sorted_files[key][file])

		df = r.RDataFrame("Events", sorted_files[key][file])
	
		height = df.AsNumpy(['vMax_3046_1'])['vMax_3046_1']

		area = df.AsNumpy(['area_3046_1'])['area_3046_1']

		hist = df.Histo1D((f'{bias_voltages[file]} V', 'Counts; Pulse height',50, 0, 200), 'vMax_3046_1')
 
		histA = df.Histo1D((f'{bias_voltages[file]} V', 'Counts; Pulse Area', 100, 0, 2000), 'area_3046_1')

		Gauss = r.TF1('Gauss Fit Height', 'gaus', bias_voltage_bounds_height[file][0], bias_voltage_bounds_height[file][1])

		GaussA = r.TF1('Gauss Fit Area', 'gaus', bias_voltage_bounds_area[file][0], bias_voltage_bounds_area[file][1])

		hist.Fit(Gauss, 'ER')

		histA.Fit(GaussA, 'ER')

		mean = Gauss.GetParameter(1)

		meanerr = Gauss.GetParErrors()[1]

		meanA = GaussA.GetParameter(1)

		meanAerr = GaussA.GetParErrors()[1]

		height_means[key].append(mean)

		height_errors[key].append(meanerr/mean)

		area_means[key].append(meanA)

		area_errors[key].append(meanAerr/meanA)

		

		C = r.TCanvas()

		C.cd()
		
		hist.GetYaxis().SetTitle('Counts')

		hist.GetXaxis().SetTitle('Pulse height')

		hist.SetTitle(f'Pulse Height Distribution for {bias_voltages[file]}V Bias')

		hist.Draw('h')

		latex = r.TLatex()

		latex.SetNDC()

		latex.SetTextSize(0.03)

		latex.DrawText(0.8, 0.75, f'{bias_voltages[file]}V')

		C.SaveAs(f'{bias_voltages[file]}V_pulse_height_{serial_numbers[j]}.png')



		CA = r.TCanvas()

		CA.cd()

		histA.GetYaxis().SetTitle('Counts')

		histA.GetXaxis().SetTitle('Pulse Area')

		histA.SetTitle(f'Pulse Area Distribution for {bias_voltages[file]}V Bias')

		histA.Draw('h')

		latex = r.TLatex()

		latex.SetNDC()

		latex.SetTextSize(0.03)

		latex.DrawText(0.8, 0.75, f'{bias_voltages[file]}V')

		CA.SaveAs(f'{bias_voltages[file]}V_pulse_area_{serial_numbers[j]}.png')

	j+=1

print(height_means)

print(area_means)

#Do a log-log plot of the pulse characteristics and bias fitting them to a linear function

for key in sorted_files.keys():
	
	c = r.TCanvas()
	
	c.cd()
	
	linear = r.TF1('line', '[0]+[1]*x', min([np.log(i) for i in bias_voltages]), max([np.log(i) for i in bias_voltages]))

	linear.Clear()

	Graph = r.TGraphErrors(len(bias_voltages), np.asarray([np.log(i) for i in bias_voltages], 'd'), np.asarray([np.log(j) for j in height_means[key]], 'd'), np.zeros(len(bias_voltages)), np.asarray([k for k in height_errors[key]], 'd'))

	Graph.Fit(linear, 'ER')

	Graph.GetYaxis().SetTitle('log(Pulse Height)')

	Graph.GetXaxis().SetTitle('log(V_{bias})')
	
	Graph.SetTitle('Log(Pulse Height) Evolution with Bias Voltage')

	Graph.SetMarkerStyle(21)

	Graph.Draw('AP')
	
	legend = r.TLegend(0.2, 0.55, 0.3, 0.65)

	legend.SetTextSize(0.04)

	legend.SetLineWidth(0)

	legend.AddEntry(Graph, 'Data')	

	legend.AddEntry(linear, 'Fit')

	legend.Draw()

	latex = r.TLatex()

	latex.SetNDC()

	latex.SetTextSize(0.03)
	
	latex.DrawText(0.2, 0.75, f'{key}: 1400-1600V')

	c.Update()	

	c.SaveAs(f'{key}_height.png')


	ca = r.TCanvas()

	ca.cd()

	linearA = r.TF1('line', '[0]+[1]*x', min([np.log(i) for i in bias_voltages]), max([np.log(i) for i in bias_voltages]))

	linearA.Clear()

	GraphA = r.TGraphErrors(len(bias_voltages), np.asarray([np.log(i) for i in bias_voltages], 'd'), np.asarray([np.log(j) for j in area_means[key]], 'd'), np.zeros(len(bias_voltages)), np.asarray([k for k in area_errors[key]], 'd'))

	GraphA.Fit(linearA, 'ER')

	GraphA.GetYaxis().SetTitle('log(Pulse Area)')

	GraphA.GetXaxis().SetTitle('log(V_{bias})')

	GraphA.SetTitle('Log(Pulse Area) Evolution with Bias Voltage')

	GraphA.SetMarkerStyle(21)

	GraphA.Draw('AP')

	legendA = r.TLegend(0.2, 0.55, 0.3, 0.65)

	legendA.SetTextSize(0.04)

	legendA.SetLineWidth(0)

	legendA.AddEntry(GraphA, 'Data')

	legendA.AddEntry(linearA, 'Fit')

	legendA.Draw()

	latexA = r.TLatex()

	latexA.SetNDC()

	latexA.SetTextSize(0.03)

	latexA.DrawText(0.2, 0.75, f'{key}: 1400-1600V')

	ca.Update()

	ca.SaveAs(f'{key}_area.png')



print(len(area_errors['CA2967']), len(area_errors['UCSB']))

#Compare the PMT's declared earlier

Comparison = r.TCanvas()

ypos = 0.75

latex_comp = r.TLatex()

latex_comp.SetNDC()

latex_comp.SetTextSize(0.03)

for index, PMT in enumerate(compare):

	ypos -= 0.05

	Graph = r.TGraphErrors(len(bias_voltages), np.asarray([np.log(i) for i in bias_voltages], 'd'), np.asarray([np.log(j) for j in area_means[PMT]], 'd'), np.zeros(len(bias_voltages)), np.asarray([k for k in area_errors[PMT]], 'd'))	

	Graph.GetListOfFunctions().Remove(linear)

	Graph.SetMarkerStyle(compare_marker_style[index])

	Graph.SetMarkerColor(compare_color[index])

	Graph.SetTitle('PMT Linearity Comparison')

	Graph.GetXaxis().SetTitle('log(V_{bias})')

	Graph.GetYaxis().SetTitle('log(Pulse Area)')

	if index==0:

		Graph.DrawClone('AP')
		
	if index!=0:

		Graph.DrawClone('P SAME')

	latex_comp.DrawText(0.2, ypos, PMT)

	marker = r.TMarker(0.15, ypos+0.01, compare_marker_style[index])

	marker.SetNDC()
	
	marker.SetMarkerColor(compare_color[index])

	marker.SetMarkerSize(1)

	marker.DrawClone()
	
Comparison.Update()

Comparison.SaveAs('Comparison.png')

import ROOT as r
import numpy as np

#Make the script start quicker
r.gROOT.SetBatch(1)

#Set the File path
#path = '/net/cms26/cms26r0/milliqan/testCorrectionsRun3Hadd/v32_testCorrections/'
#path = '/net/cms26/cms26r0/milliqan/outputRun3Hadd/v32/'
path = '/net/cms2/cms2r0/neha/hadd_files_Aug8/'

#Run_nums = ['1006', '1031', '1032', '1035', '1038', '1039']
Run_nums = ['1006', '1031', '1038', '1039']

#add the full file path for each data set to a list 
Runs = []
for i in Run_nums:
	Run = path+f'MilliQan_Run{i}_default_v32_testCorrectionsV2.root'
	#Run = path+f'MilliQan_Run{i}_default_v32.root'	
	Runs.append(Run)
	print(f'Added Run {i}')

#make a chain and add the relevant files
chain = r.TChain('t')
for Run in Runs:
	chain.Add(Run)

#Set the combination of layer differences we want
combos = [3, 2, 1]

#Set cuts and the time branch to be used
layerhcut = 1000
layerAcut = 570.e3
slabAcuts = [[320.e3, 150.e3]]
slabH = 1200

#set the channels to be used as the endcap slabs
slabs = [[71, 75]]

#set the time variable to be used
t = 'timeFit_module_calibrated'

#make the dataframe
df = r.RDataFrame(chain)

#Create a list of histogram objects for drawing in a loop
histos = []
skew = [17.4, 25.9, 18.7, 2.8]
#start the loop of filters and making histogram objects
for pair in slabs:
	#Define the cuts for the slabs
	front = pair[0]
	back = pair[-1]
	A1 = slabAcuts[slabs.index(pair)][0]
	A2 = slabAcuts[slabs.index(pair)][-1]
	#Filter the dataframe for through going saturating hits
	df_slab_cuts = df.Filter(f'Sum(height[chan=={front}&&ipulse==0]>{slabH}&&area[chan=={front}&&ipulse==0]>{A1})').Filter(f'Sum(height[chan=={back}&&ipulse==0]>{slabH}&&area[chan=={back}&&ipulse==0]>{A2})')
	#Define the time of each channel (slabs)
	df_slab_peaks = df_slab_cuts.Define('Front_time', f'{t}[chan=={front}&&ipulse==0&&riseSamples>2]')
	df_slab_peaks = df_slab_peaks.Define('Back_time', f'{t}[chan=={back}&&ipulse==0&&riseSamples>2]')
	#Define the time difference in the two slab times
	df_slab_peaks = df_slab_peaks.Define(f'T_Diff_{front}_{back}', 'Back_time-Front_time')
	hist = df_slab_peaks.Histo1D(('temp', 'Time Difference Measured by Slab Detectors; \Delta t [ns]', 20, -32, 40), f'T_Diff_{front}_{back}')
	histos.append(hist)
	#now filter for layer hits and high layer saturation
	df_layer_hits = df_slab_cuts.Filter('Sum(layer==0&&ipulse==0)').Filter('Sum(layer==1&&ipulse==0)').Filter('Sum(layer==2&&ipulse==0)').Filter('Sum(layer==3&&ipulse==0)')
	df_layer_sat = df_layer_hits.Filter(f'Sum(height[layer==0&&ipulse==0]>{layerhcut}&&area[layer==0&&ipulse==0]>{layerAcut})').Filter(f'Sum(height[layer==1&&ipulse==0]>{layerhcut}&&area[layer==1&&ipulse==0]>{layerAcut})').Filter(f'Sum(height[layer==2&&ipulse==0]>{layerhcut}&&area[layer==2&&ipulse==0]>{layerAcut})').Filter(f'Sum(height[layer==3&&ipulse==0]>{layerhcut}&&area[layer==3&&ipulse==0]>{layerAcut})')
	#Make the time difference columns
	
	for num in range(4):
		if num==0:
			df_layer_sat = df_layer_sat.Define('Front_time', f'{t}[chan=={front}&&ipulse==0&&riseSamples>2]')
			df_layer_sat = df_layer_sat.Define('Back_time', f'{t}[chan=={back}&&ipulse==0&&riseSamples>2]')
			df_layer_sat = df_layer_sat.Define(f'Skew_{front}_{back}', f'{skew[num]}')
			df_layer_sat = df_layer_sat.Define(f'TDiff_{front}_{back}', f'Back_time-Front_time-Skew_{front}_{back}')
			hist1 = df_layer_sat.Histo1D(('temp', 'temp; \Delta t [ns]', 18, -35, 15), f'TDiff_{front}_{back}')
			histos.append(hist1)
		if num!=0:
			l2 = combos[num-1]
			df_layer_sat = df_layer_sat.Define(f'TDiff_0_{l2}_unskew', f'Min({t}[layer=={l2}&&ipulse==0&&riseSamples>2])-Min({t}[layer==0&&ipulse==0&&riseSamples>2])')
			df_layer_sat = df_layer_sat.Define(f'Skew_{0}_{l2}', f'{skew[num]}')
			df_layer_sat = df_layer_sat.Define(f'TDiff_0_{l2}', f'TDiff_0_{l2}_unskew-Skew_{0}_{l2}')
			if num==1:
				hist2 = df_layer_sat.Histo1D(('temp', 'temp; \Delta t [ns]', 20, -35, 15), f'TDiff_0_{l2}')
				histos.append(hist2)
			
			elif num==2:
				hist2 = df_layer_sat.Histo1D(('temp', 'temp; \Delta t [ns]', 20, -35, 15), f'TDiff_0_{l2}')
				histos.append(hist2)
			elif num==3:
				hist2 = df_layer_sat.Histo1D(('temp', 'temp; \Delta t [ns]', 35, -35, 15), f'TDiff_0_{l2}')
				histos.append(hist2)

print(f'Have {len(histos)} histograms to draw')


layer_distances = []

layer_dist_error = []

#Set the names for files to be saved
names = ['Endcap_timing_test.png', 'Endcap_timing_layer_hits.png', 'Layer0_Layer3.png', 'Layer0_Layer2.png', 'Layer0_Layer1.png']
#Set the titles for each plot
titles = ['Time Difference Measured by Endcaps', 'Time Difference Measured by Endcaps', 'Time Difference Measured by Layers 0 and 3', 'Time Difference Measured by Layers 0 and 2', 'Time Difference Measured by Layers 0 and 1']
#Set the plot message to indicate how differences are done
plot_message = ['Front panel - back panel', 'Back panel - Front panel', 'Layer3 - Layer0', 'Layer2 - Layer0', 'Layer1 - Layer0']

for hist in histos:
	c = r.TCanvas()
	c.cd()
	#Define the fitting function
	DGauss = "[0]*exp(-0.5*((x-[1])/[2])^2) +[3]*exp(-0.5*((x-[4])/[5])^2)"
	#Define the fitting range
	if histos.index(hist)==0:
		gaussFit = r.TF1('gaussfit', DGauss, -32, 40)
		gaussFit.SetParameters(60, 16, 2, 10, -10, 2)
	if histos.index(hist)==1:
		gaussFit = r.TF1('gaussfit', DGauss, -35,15 )
		gaussFit.SetParameters(60, 0, 2, 10, -26, 2)
	if histos.index(hist)==2:
		gaussFit = r.TF1('gaussfit', DGauss, -23, 10)
		gaussFit.SetParameters(40, 0, 2, 10, -16, 2)
	if histos.index(hist)==3:
		gaussFit = r.TF1('gaussfit', DGauss, -15, 10)
		gaussFit.SetParameters(40, 0, 2, 10, -11.3, 2)
	if histos.index(hist)==4:
		gaussFit = r.TF1('gaussfit', DGauss, -10, 10)
		gaussFit.SetParameters(40, 0, 2, 10, -6, 2)
	c.UseCurrentStyle()
	#stylize the plot
	hist.SetStats(0)
	hist.SetTitle(titles[histos.index(hist)])
	hist.GetYaxis().SetTitle('Counts')
	hist.GetXaxis().SetTitle('\Delta t  [ns]')
	hist.SetMarkerStyle(20)
	hist.SetLineWidth(3)
	#Fitting the hist with Log likelihood
	hist.Fit(gaussFit, 'LR')
	hist.DrawCopy('e1')
	#Getting the normalized Chi-square and the parameters
	mean1 = gaussFit.GetParameter(1)
	mean2 = gaussFit.GetParameter(4)
	mean1Err = gaussFit.GetParError(1)
	mean2Err = gaussFit.GetParError(4)
	std1 = gaussFit.GetParameter(2)
	std2 = gaussFit.GetParameter(5)
	if histos.index(hist)!=0:
		layer_distances.append(abs(mean1-mean2)*0.3/2)
		layer_dist_error.append(np.sqrt(mean1Err**2+mean2Err**2))
	#Setting up legends and labels
	legend = r.TLegend(0.15, 0.75,0.25, 0.8)
	legend.SetTextSize(0.03)
	legend.AddEntry(hist.GetPtr(), 'Data')
	legend.AddEntry(gaussFit, 'Fit')
	legend.SetLineWidth(0)
	legend.Draw('same')
	latex = r.TLatex()
	latex.SetNDC()
	latex.SetTextSize(0.03)
	latex.DrawText(0.12, 0.50,"t(Beam, Cosmic) = %.1f, %.1f ns"%(mean1, mean2))
	latex.DrawText(0.12, 0.45,"sigma(Beam, Cosmic) = %.1f, %.1f ns"%(std1, std2))
	latex.DrawText(0.3, 0.8, 'MilliQan Preliminary 2023')
	latex.DrawText(0.3, 0.75, 'Time difference of muon hits')
	latex.DrawText(0.3, 0.7, plot_message[histos.index(hist)])
	c.SaveAs(names[histos.index(hist)])



Distances = np.array([i for i in layer_distances])

errors = np.array([0.15*i for i in layer_dist_error])

print(Distances)
print(errors)

layer_dist_ref = np.array([0.86, 1.72, 2.58, 4.02])

print(layer_dist_ref)


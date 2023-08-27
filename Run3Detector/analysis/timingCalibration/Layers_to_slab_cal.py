import ROOT as r
import numpy as np

#Make the script start quicker
r.gROOT.SetBatch(1)

#Set the File path
path = '/net/cms2/cms2r0/neha/hadd_files_Aug8/'

Run_nums = ['1006', '1031', '1038', '1039']

#add the full file path for each data set to a list 
Runs = []
for i in Run_nums:
	Run = path+f'MilliQan_Run{i}_default_v32_testCorrectionsV2.root'
	Runs.append(Run)
	print(f'Added Run {i}')

#make a chain and add the relevant files
chain = r.TChain('t')
for Run in Runs:
	chain.Add(Run)

#Make an outfile
outfile = r.TFile('Layers_to_slabs.root', 'RECREATE')

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

#Hold the means of each beam muon population

Means = []

#start the loop of filters and making histogram objects
for pair in slabs:
	#Define the cuts for the slabs
	front = pair[0]
	back = pair[-1]
	A1 = slabAcuts[slabs.index(pair)][0]
	A2 = slabAcuts[slabs.index(pair)][-1]
	#Filter the dataframe for through going saturating hits
	df_slab_cuts = df.Filter(f'Sum(height[chan=={front}&&ipulse==0]>{slabH}&&area[chan=={front}&&ipulse==0]>{A1})').Filter(f'Sum(height[chan=={back}&&ipulse==0]>{slabH}&&area[chan=={back}&&ipulse==0]>{A2})')
	#Apply the condition for layer hits
	df_layer_hits = df_slab_cuts.Filter('Sum(layer==0&&ipulse==0)').Filter('Sum(layer==1&&ipulse==0)').Filter('Sum(layer==2&&ipulse==0)').Filter('Sum(layer==3&&ipulse==0)')
	#Apply the saturation requirements in each layer
	df_layer_sat = df_layer_hits.Filter(f'Sum(height[layer==0&&ipulse==0]>{layerhcut}&&area[layer==0&&ipulse==0]>{layerAcut})').Filter(f'Sum(height[layer==1&&ipulse==0]>{layerhcut}&&area[layer==1&&ipulse==0]>{layerAcut})').Filter(f'Sum(height[layer==2&&ipulse==0]>{layerhcut}&&area[layer==2&&ipulse==0]>{layerAcut})').Filter(f'Sum(height[layer==3&&ipulse==0]>{layerhcut}&&area[layer==3&&ipulse==0]>{layerAcut})')
	#Make the columns for each layers time
	for num in range(4):
		#Define the time for the bottom facing slab
		df_layer_sat = df_layer_sat.Define(f'Front_time_{num}', f'Min({t}[chan==71&&ipulse==0&&riseSamples>2])')
		df_layer_sat = df_layer_sat.Define(f'Layer_{num}', f'Min({t}[layer=={num}&&ipulse==0&&riseSamples>2])')
		df_layer_sat_time_cut = df_layer_sat.Define(f'TDiff_{front}_Layer{num}', f'Layer_{num}-Front_time_{num}').Filter(f'TDiff_{front}_Layer{num}>-13')
		if num==0 or num==1:
			if num==0:
				gauss = r.TF1('gaus', 'gaus',-15 ,5 )
			if num==1:
				gauss = r.TF1('gaus', 'gaus', -12, 5)
			hist = df_layer_sat_time_cut.Histo1D((f'Layer{num}', f'Layer_{num}; time', 25, -32, 40), f'TDiff_{front}_Layer{num}')
			hist.Fit(gauss, 'LR')
			Means.append(gauss.GetParameter(1))
		if num==2 or num==3:
			gauss = r.TF1('gaus', 'gaus',0 ,20 )
			hist = df_layer_sat_time_cut.Histo1D((f'Layer{num}', f'Layer_{num}; time', 25, -32, 40), f'TDiff_{front}_Layer{num}')
			hist.Fit(gauss, 'LR')
			Means.append(gauss.GetParameter(1))
		outfile.cd()
		hist.Write()

print(Means)

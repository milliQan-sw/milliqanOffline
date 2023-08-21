#NEED TO GENERALIZE

#to generalize for n runNumber cuts filter and add to list then Concat the dataFrames

import ROOT as r
import json
import numpy as np

r.gROOT.SetBatch(1)


#Read in the json data to ammend the calibration constants

calibrate = {}

calibrate['timing'] = []

with open('Calibration_Values.json', 'r') as file_name:
	json_data = json.load(file_name)
	for key in json_data:
		for item in json_data[key]:
			calibrate['timing'].append(item)

print('The original json corrections: ', calibrate, '\n')

Layers = {}

Layers['0'] = []

Layers['1'] = []

Layers['2'] = []

Layers['3'] = []

#Setting the path to collected data

#path = '/net/cms26/cms26r0/milliqan/outputRun3Hadd/v32/'

#path = '/net/cms26/cms26r0/milliqan/testCorrectionsRun3Hadd/v32_testCorrections/'

path = '/net/cms2/cms2r0/neha/hadd_files_Aug8/'

#set the run numbers for analysis

#Run_nums = ['1006', '1031', '1032','1035', '1038', '1039']

Run_nums = ['1006', '1031', '1038', '1039']

#Run_nums = ['1114', '1116', '1117']

#add the full file path for each data set to a list 

Runs = []

for i in Run_nums:
	#Run = path+f'MilliQan_Run{i}_default_v32.root'
	Run = path+f'MilliQan_Run{i}_default_v32_testCorrectionsV2.root'
	Runs.append(Run)
	print(f'Added Run {i}')

#time variable to be used

t = 'timeFit_module_calibrated'

#Create the chain for tree name 't' and add the files for analysis

chain = r.TChain('t')

for Run in Runs:
        chain.Add(Run)


#Make relevant filters


#make an outfile 

outfile = r.TFile('Cross_Column_check_Corrections.root', 'RECREATE')

#make data frame

df = r.RDataFrame(chain)

#List of leading channel pairs used in cross columns

#IF these channels change between Runs append all channel pairs to the original list

front_Pan_chan_pairs = [[0,1], [1, 4], [4, 5], [16, 17], [17, 20], [20,21]]

back_Pan_chan_pairs = [[32, 33], [33, 36], [36, 37], [48, 49], [49, 52], [52,53]]

#Make list of top pannels

Panel_num = [68, 72]

#Define the corrections for the bottom channels according to their position withrespect to the IP; i.e., Forward means channels under the first top panel; no need to fix last channel in column 0 or column 15

Forward_bottom_fix = [0, 0, 0, 0, 0, 0]

#Forward_bottom_fix = [-0.5062, -0.7975, 7.4964, -4.172, 2.4938, -1.1074] 

#Forward_bottom_fix = [-0.1827, 5.583, 1.173, -5.014, 0.497, 2.153]

Backward_bottom_fix = [0, 0, 0, 0, 0, 0]

#Backward_bottom_fix = [-0.5018, 5.2619, 0.1610, 5.9325, -4.3056, -0.6305]

#Backward_bottom_fix = [-1.776, 4.733, 4.146, 3.97, 8.708, -4.035]

#Defined Area cuts for each channel pair in the defined region

A_pan68 = [[620.e3, 615.e3], [615.e3, 620.e3], [530.e3, 620.e3],[608.e3, 620.e3], [610.e3, 610.e3], [520.e3, 608.e3]]

A_pan72 = [[610.e3, 610.e3], [600.e3, 600.e3], [610.e3, 610.e3], [610.e3, 605.e3], [610.e3, 615.e3], [530.e3, 615.e3]]

#Define the area cuts for the possible path analysis

#These are according to the pattern: i+2, i+8, i+10, j, j+2, j+8 for i and j being the left and right leading channels of their respective column

A_pan68_paths = [[618.e3, 618.e3, 615.e3, 615.e3, 610.e3, 620.e3], [610.e3, 620.e3, 615.e3, 530.e3, 535.e3, 620.e3], [535.e3, 620.e3, 620.e3, 525.e3, 540.e3, 600.e3], [600.e3, 610.e3, 610.e3, 610.e3, 520.e3, 610.e3], [520.e3, 610.e3, 620.e3, 520.e3, 525.e3, 610.e3], [525.e3, 610.e3, 610.e3, 519.e3, 525.e3, 620.e3]]

A_pan72_paths = [[610.e3, 610.e3, 520.e3, 600.e3, 610.e3, 610.e3], [610.e3, 610.e3, 610.e3, 610.e3, 520.e3, 608.e3], [520.e3, 608.e3, 600.e3, 520.e3, 520.e3, 600.e3], [610.e3, 600.e3, 610.e3, 610.e3, 610.e3, 610.e3], [610.e3, 610.e3, 605.e3, 530.e3, 535.e3, 615.e3], [535.e3, 615.e3, 615.e3, 618.e3, 535.e3, 620.e3]]

frontPan = df.Filter('Sum(height[chan==68&&ipulse==0]>1000)')

backPan = df.Filter('Sum(height[chan==72&&ipulse==0]>1000)')

for pairs in range(len(front_Pan_chan_pairs)):

	fit_front = r.TF1('gaus', 'gaus', -25, 25)

	fit_back = r.TF1('gaus', 'gaus', -25, 25)

	fix_front = Forward_bottom_fix[pairs]	

	fix_back = Backward_bottom_fix[pairs]

	ChanFpair = front_Pan_chan_pairs[pairs]

	ChanBpair = back_Pan_chan_pairs[pairs]	

	#set the area cuts for the channels under the front panel

	A1F, A2F = A_pan68[pairs][0], A_pan68[pairs][-1]

	A1B, A2B = A_pan72[pairs][0], A_pan72[pairs][-1]

	#every bottom channel of interest is the last channel in the pair+10

	jump = 10

	#Define the data frames to be filtered at each level and correct the relevant channel times

	frontPan = frontPan.Define(f'TimeFit_Chan{str(ChanFpair[-1]+jump)}', f'Max({t}[chan=={ChanFpair[-1]+jump}])')

	frontPan = frontPan.Define(f'T_Ref{str(ChanFpair[0])}', f'Max({t}[chan=={ChanFpair[0]}])')

	frontPan = frontPan.Define(f'Correction_time_{str(ChanFpair[-1]+jump)}', f'{str(fix_front)}')

	frontPan = frontPan.Define(f'TimeFit_Chan{str(ChanFpair[-1]+jump)}_Fixed', f'TimeFit_Chan{str(ChanFpair[-1]+jump)}+Correction_time_{str(ChanFpair[-1]+jump)}')



	backPan = backPan.Define(f'TimeFit_Chan{str(ChanBpair[-1]+jump)}', f'Max({t}[chan=={ChanBpair[-1]+jump}])')

	backPan = backPan.Define(f'T_Ref{str(ChanBpair[0])}', f'Max({t}[chan=={ChanBpair[0]}])')
	
	backPan = backPan.Define(f'Correction_time_{str(ChanBpair[-1]+jump)}', f'{str(fix_back)}')	
	
	backPan = backPan.Define(f'TimeFit_Chan{str(ChanBpair[-1]+jump)}_Fixed', f'TimeFit_Chan{str(ChanBpair[-1]+jump)}+Correction_time_{str(ChanBpair[-1]+jump)}')
	


	#Filter the data Frames; require saturated hit in the intermediary ROWS and the leading and bottom channels

	frontPanFilt = frontPan.Filter('Sum(height[row==1&&ipulse==0]>1000)').Filter('Sum(height[row==2&&ipulse==0]>1000)').Filter(f'Sum(area[chan=={ChanFpair[0]}&&ipulse==0]>{A1F})').Filter(f'Sum(area[chan=={ChanFpair[-1]+jump}&&ipulse==0]>{A2F})').Filter(f'Sum(height[chan=={ChanFpair[0]}&&ipulse==0]>1000)').Filter(f'Sum(height[chan=={ChanFpair[-1]}&&ipulse==0]>1000)')
	
	backPanFilt = backPan.Filter('Sum(height[row==1&&ipulse==0])>1000').Filter('Sum(height[row==2&&ipulse==0]>1000)').Filter(f'Sum(area[chan=={ChanBpair[0]}&&ipulse==0]>{A1B})').Filter(f'Sum(area[chan=={ChanBpair[-1]+jump}&&ipulse==0]>{A2B})').Filter(f'Sum(height[chan=={ChanBpair[0]}&&ipulse==0]>1000)').Filter(f'Sum(height[chan=={ChanBpair[-1]}&&ipulse==0]>1000)')
	

	frontPanFilt_DFs = {}

	backPanFilt_DFs = {}

	#Set the area cuts for this column pair in the left hand side of the detector

	FL2, FL8, FL10, FR, FR2, FR8  = A_pan68_paths[pairs][0], A_pan68_paths[pairs][1], A_pan68_paths[pairs][2], A_pan68_paths[pairs][3], A_pan68_paths[pairs][4], A_pan68_paths[pairs][5]

	BL2, BL8, BL10, BR, BR2, BR8  = A_pan72_paths[pairs][0], A_pan72_paths[pairs][1], A_pan72_paths[pairs][2], A_pan72_paths[pairs][3], A_pan72_paths[pairs][4], A_pan72_paths[pairs][5]
	
	print('Area cuts for front half of the detector: ', FL2, FL8, FL10, FR, FR2, FR8)	

	print('Area cuts for the back half of the detector: ', BL2, BL8, BL10, BR, BR2, BR8 )

	print(f'\n Working on the following column pair: {ChanBpair}')

		
	B1 = backPanFilt.Filter(f'Sum(area[chan=={ChanBpair[-1]}&&ipulse==0]>{BR})').Filter(f'Sum(area[chan=={ChanBpair[-1]+2}&&ipulse==0]>{BR2})').Filter(f'Sum(area[chan=={ChanBpair[-1]+8}&&ipulse==0]>{BR8})')

		
	backPanFilt_DFs['DataFrames'] = [B1]

	backPanFilt_DFs['Arrays'] = []

	for DF in backPanFilt_DFs['DataFrames']:


		DF = DF.Define(f'TDiff_{str(ChanBpair[0])}_{str(ChanBpair[-1]+jump)}', f'TimeFit_Chan{str(ChanBpair[-1]+jump)}_Fixed-T_Ref{str(ChanBpair[0])}').Filter(f'Sum(riseSamples[chan=={ChanBpair[0]}&&ipulse==0]>2)').Filter(f'Sum(riseSamples[chan=={ChanBpair[-1]+jump}&&ipulse==0]>2)')
	
		array = np.array(DF.AsNumpy([f'TDiff_{str(ChanBpair[0])}_{str(ChanBpair[-1]+jump)}'])[f'TDiff_{str(ChanBpair[0])}_{str(ChanBpair[-1]+jump)}'])	
		
		backPanFilt_DFs['Arrays'].append(array)

		print(f'Added {len(array)} events to array storage')

	
	histB = r.TH1F(f'TDiff_{str(ChanBpair[0])}_{str(ChanBpair[-1]+jump)}', f'TDiff_{str(ChanBpair[0])}_{str(ChanBpair[-1]+jump)}; \Delta t; Counts', 20, -26.25, 26.25)

	for array in backPanFilt_DFs['Arrays']:

		print(array)		

		for entry in array:
			
			histB.Fill(entry)

	
	print(f'Filled TDiff_{str(ChanBpair[0])}_{str(ChanBpair[-1]+jump)}')

	histB.Fit(fit_back, 'L')

	if 32<=ChanBpair[0]<=37:
		Layers['2'].append(fit_back.GetParameter(1))
	elif 37<ChanBpair[0]:
		Layers['3'].append(fit_back.GetParameter(1))

	histB.Write()
	
	
	if 17 not in front_Pan_chan_pairs[pairs]:
	
		print(f'\n Working on the following column pair: {ChanFpair}')
		
		F1 = frontPanFilt.Filter(f'Sum(area[chan=={ChanFpair[-1]}&&ipulse==0]>{FR})').Filter(f'Sum(area[chan=={ChanFpair[-1]+2}&&ipulse==0]>{FR2})').Filter(f'Sum(area[chan=={ChanFpair[-1]+8}&&ipulse==0]>{FR8})')


		frontPanFilt_DFs['DataFrames'] = [F1]

		frontPanFilt_DFs['Arrays'] = []

		for DF in frontPanFilt_DFs['DataFrames']:

			DF = DF.Define(f'TDiff_{str(ChanFpair[0])}_{str(ChanFpair[-1]+jump)}', f'TimeFit_Chan{str(ChanFpair[-1]+jump)}_Fixed-T_Ref{str(ChanFpair[0])}').Filter(f'Sum(riseSamples[chan=={ChanFpair[0]}&&ipulse==0]>2)').Filter(f'Sum(riseSamples[chan=={ChanFpair[-1]+jump}&&ipulse==0]>2)')
		
			array = np.array(DF.AsNumpy([f'TDiff_{str(ChanFpair[0])}_{str(ChanFpair[-1]+jump)}'])[f'TDiff_{str(ChanFpair[0])}_{str(ChanFpair[-1]+jump)}'])

			frontPanFilt_DFs['Arrays'].append(array)

			print(f'Added {len(array)} events to array storage')
		
			print(array)

		histF = r.TH1F(f'TDiff_{str(ChanFpair[0])}_{str(ChanFpair[-1]+jump)}', f'TDiff_{str(ChanFpair[0])}_{str(ChanFpair[-1]+jump)}; \Delta t; Counts', 20, -26.25, 26.25)

		for array in frontPanFilt_DFs['Arrays']:

			print(array)
                
			for entry in array:
                        
				histF.Fill(entry)
		
		print(f'Filled TDiff_{str(ChanFpair[0])}_{str(ChanFpair[-1]+jump)}')

		histF.Fit(fit_front, 'L')

		if ChanFpair[0]<16:
			Layers['0'].append(fit_front.GetParameter(1))
		elif 16<=ChanFpair[0]<=32:
			Layers['1'].append(fit_front.GetParameter(1))
			
		histF.Write()


	elif [16,17]==front_Pan_chan_pairs[pairs]:
			
		
		print(f'\n Working on the following column pair: {ChanFpair}')

		F1 = frontPanFilt.Filter(f'Sum(area[chan=={ChanFpair[-1]}&&ipulse==0]>{FR})').Filter(f'Sum(area[chan=={ChanFpair[-1]+2}&&ipulse==0]>{FR2})').Filter(f'Sum(area[chan=={ChanFpair[-1]+8+54}&&ipulse==0]>{FR8})')

		frontPanFilt_DFs['DataFrames'] = [F1]

		frontPanFilt_DFs['Arrays'] = []

		for DF in frontPanFilt_DFs['DataFrames']:

		
			DF = DF.Define(f'TDiff_{str(ChanFpair[0])}_{str(ChanFpair[-1]+jump)}', f'TimeFit_Chan{str(ChanFpair[-1]+jump)}_Fixed-T_Ref{str(ChanFpair[0])}').Filter(f'Sum(riseSamples[chan=={ChanFpair[0]}&&ipulse==0]>2)').Filter(f'Sum(riseSamples[chan=={ChanFpair[-1]+jump}&&ipulse==0]>2)')

			array = np.array(DF.AsNumpy([f'TDiff_{str(ChanFpair[0])}_{str(ChanFpair[-1]+jump)}'])[f'TDiff_{str(ChanFpair[0])}_{str(ChanFpair[-1]+jump)}'])

			frontPanFilt_DFs['Arrays'].append(array)

			print(f'Added {len(array)} events to array storage')

			print(array)	
			
		histF = r.TH1F(f'TDiff_{str(ChanFpair[0])}_{str(ChanFpair[-1]+jump)}', f'TDiff_{str(ChanFpair[0])}_{str(ChanFpair[-1]+jump)}; \Delta t; Counts', 20, -26.25, 26.25)

		for array in frontPanFilt_DFs['Arrays']:

			print(array)

			for entry in array:
                        
				histF.Fill(entry)	
		
		print(f'Filled TDiff_{str(ChanFpair[0])}_{str(ChanFpair[-1]+jump)}')
	
		histF.Fit(fit_front, 'L')
                
		if ChanFpair[0]<16:
			Layers['0'].append(fit_front.GetParameter(1))
		elif 16<=ChanFpair[0]<=32:
			Layers['1'].append(fit_front.GetParameter(1))

		histF.Write()

	elif 17 in front_Pan_chan_pairs[pairs]:
		
		print(f'\n Working on the following column pair: {ChanFpair}')

		
		F1 = frontPanFilt.Filter(f'Sum(area[chan=={ChanFpair[-1]}&&ipulse==0]>{FR})').Filter(f'Sum(area[chan=={ChanFpair[-1]+2}&&ipulse==0]>{FR2})').Filter(f'Sum(area[chan=={ChanFpair[-1]+8}&&ipulse==0]>{FR8})')

		frontPanFilt_DFs['DataFrames'] = [F1]

		frontPanFilt_DFs['Arrays'] = []

		for DF in frontPanFilt_DFs['DataFrames']:

		
			DF = DF.Define(f'TDiff_{str(ChanFpair[0])}_{str(ChanFpair[-1]+jump)}', f'TimeFit_Chan{str(ChanFpair[-1]+jump)}_Fixed-T_Ref{str(ChanFpair[0])}').Filter(f'Sum(riseSamples[chan=={ChanFpair[0]}&&ipulse==0]>2)').Filter(f'Sum(riseSamples[chan=={ChanFpair[-1]+jump}&&ipulse==0]>2)')

			array = np.array(DF.AsNumpy([f'TDiff_{str(ChanFpair[0])}_{str(ChanFpair[-1]+jump)}'])[f'TDiff_{str(ChanFpair[0])}_{str(ChanFpair[-1]+jump)}'])

			frontPanFilt_DFs['Arrays'].append(array)

			print(f'Added {len(array)} events to array storage')

			print(array)
	
			
		histF = r.TH1F(f'TDiff_{str(ChanFpair[0])}_{str(ChanFpair[-1]+jump)}', f'TDiff_{str(ChanFpair[0])}_{str(ChanFpair[-1]+jump)}; \Delta t; Counts', 20, -26.25, 26.25)

		for array in frontPanFilt_DFs['Arrays']:

			print(array)

			for entry in array:

				histF.Fill(entry)


		print(f'Filled TDiff_{str(ChanFpair[0])}_{str(ChanFpair[-1]+jump)}')

		histF.Fit(fit_front, 'L')
                
		if ChanFpair[0]<16:
			Layers['0'].append(fit_front.GetParameter(1))
		elif 16<=ChanFpair[0]<=32:
			Layers['1'].append(fit_front.GetParameter(1))
		
		histF.Write()	
		
		
print('Code works')


outfile.Close()

Column_corrections = []

for key in Layers:
	temp = []
	for i in range(len(Layers[key])):
		if i==0:
			temp.append(Layers[key][0])
		if i==1:
			temp.append(Layers[key][0]+Layers[key][1])
		elif i==2:
			temp.append(np.sum(Layers[key]))	

	Column_corrections.append(temp)

print(Column_corrections)

Leading = [[1, 4, 5],[17, 20 , 21], [33, 36, 37], [49, 52, 53]]

Columns = []

for leads in Leading:
	channels = []
	for lead in leads:
		channels.append([lead, lead+2, lead+8, lead+10])
	Columns.append(channels)


for layer in Columns:
	for column in layer:
		correction = Column_corrections[Columns.index(layer)][layer.index(column)]
		for channel in column:
			if channel!=25:
				calibrate['timing'][channel]+=correction
			elif channel==25:
				calibrate['timing'][channel]+=correction
				calibrate['timing'][channel+54]+=correction

'''with open('Channel_Calibrations.json', 'w') as filename:
	json.dump(calibrate, filename)'''

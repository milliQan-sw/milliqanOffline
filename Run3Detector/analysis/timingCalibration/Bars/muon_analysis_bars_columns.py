import ROOT as r
import json
import numpy as np

r.gROOT.SetBatch(1)

#optionally rewrite json

rewrite = input('Rewrite the Json file of corrections? Enter yes or no. ')

data = {}

calibrations = np.zeros(80).tolist()

#Setting the path to collected data

#path = '/net/cms26/cms26r0/milliqan/outputRun3Hadd/v32/'

#path = '/net/cms26/cms26r0/milliqan/testCorrectionsRun3Hadd/v32_testCorrections/'

path = '/net/cms2/cms2r0/neha/hadd_files_Aug8/'

#set the run numbers for analysis

Run_nums = ['1006', '1031', '1038', '1039']

#Run_nums = ['1114', '1116', '1117']


#add the full file path for each data set to a list 

Runs = []

for i in Run_nums:
#	Run = path+f'MilliQan_Run{i}_default_v32.root'
	Run = path+f'MilliQan_Run{i}_default_v32_testCorrectionsV2.root'
	Runs.append(Run)
	print(f'Added Run {i}')

#Create the chain for tree name 't' and add the files for analysis

chain = r.TChain('t')

for Run in Runs:
	chain.Add(Run)

#timing column name

#t = 'timeFit'

t = 'timeFit_module_calibrated'

#make data frame

df = r.RDataFrame(chain)

#Make an output file for the histogram objects

outfile = r.TFile('Layer_Check_columns.root', 'RECREATE')

#List of channels under the associated panels

topbars_pan68 = [0, 1, 4, 5, 16, 17, 20, 21]

topbars_pan72 = [32, 33, 36, 37, 48, 49, 52, 53]

#Set the pattern to jump to the next channel in the column

chanNxt = [2, 8, 10]

#Set the area cuts for each bar

A_pan68 = [[620.e3, 600.e3], [615.e3, 615.e3], [530.e3, 620.e3], [525.e3, 620.e3], [608.e3, 600.e3], [610.e3, 600.e3], [520.e3, 600.e3], [519.e3, 600.e3]]

A_pan68_mid = [[618.e3, 618.e3], [610.e3, 620.e3], [535.e3, 620.e3], [540.e3, 600.e3], [608.e3, 500.e3], [520.e3, 610.e3], [525.e3, 610.e3], [525.e3, 620.e3]]

A_pan72 = [[610.e3, 520.e3], [600.e3, 610.e3], [610.e3, 610.e3], [520.e3, 600.e3], [610.e3, 600.e3], [610.e3, 610.e3], [530.e3, 610.e3], [618.e3, 600.e3]] 

A_pan72_mid = [[610.e3, 610.e3], [610.e3, 610.e3], [520.e3, 608.e3], [520.e3, 600.e3], [610.e3, 600.e3], [610.e3, 610.e3], [535.e3, 615.e3], [535.e3, 620.e3]]

#set the corrections for each subset of channels; [chan+2, chan+8, chan+10]

#fix_pan68 = [[1.561, 0.093, 1.878, 7.547, 0.227, 1.488, 1.777, -2.811], [-0.783, -0.115, -7.299, 5.497, -7.369, -5.685, 1.214, -0.269], [0.349, -0.509, -0.806, 7.487, -6.692, -4.202, 2.407, -1.135]]

fix_pan68 = []

#fix_pan72 = [[0.518, 0.896, 4.411, 1.284, 0.281, -0.233, -0.964, 3.418], [-2.302, -0.404, 1.777, -0.553, -0.857, -0.574, -3.953, -0.353], [0.562, -0.557, 5.279, 0.259, 3.351, 5.945, -4.173, -0.634]]

fix_pan72 = []

for i in range(3):
	zeros = [0,0,0,0,0,0,0,0]
	fix_pan72.append(zeros)
	fix_pan68.append(zeros)
#Filter for events in columnar fashion but through panel 68; height cutoff is 1000 mV

#Split the detector in two

Panel_68_large = df.Filter('Sum(height[chan==68&&ipulse==0]>1000)')

Panel_72_large = df.Filter('Sum(height[chan==72&&ipulse==0]>1000)')

################################################################################

#Make the corrections for each channel in a column using the top as reference

for i in topbars_pan68:	

	#Make a column for reference times, i.e. the time stamp from the leading columns

	Panel_68_large =  Panel_68_large.Define(f'Time{str(i)}_ref',f'Max({t}[chan=={i}&&ipulse==0])')

#Loop through the data frame and correct the times of non-leading channels as well as find the time difference

for num in range(3):

	#define the "jump" to the next channel of interest in the column

	n = chanNxt[num]

	if n!=8:

		for i in topbars_pan68:	

			fit = r.TF1('gaus', 'gaus', -25, 25)
	
			Area1 = A_pan68[topbars_pan68.index(i)][0]

			Area2 = A_pan68[topbars_pan68.index(i)][-1]				
			
			AreaM1 = A_pan68_mid[topbars_pan68.index(i)][0]

			AreaM2 = A_pan68_mid[topbars_pan68.index(i)][-1]

			#Make a column for the comparison channels  time

			Panel_68_large =  Panel_68_large.Define(f'Time{str(i+n)}',f'Max({t}[chan=={i+n}&&ipulse==0])')

	
			#Now a column for the corrections

			Panel_68_large = Panel_68_large.Define(f'Correction_{str(i+n)}', f'{str(fix_pan68[num][topbars_pan68.index(i)])}')

			#Make column for the corrected times

			Panel_68_large = Panel_68_large.Define(f'Corrected_Time_{str(i+n)}', f'Time{str(i+n)}+Correction_{str(i+n)}')

			#Find the elapsed time	


			if i!=16 and i!=17:	

				Panel_68_large_ = Panel_68_large.Define(f'TimeDiff_Bars{str(i)}_{str(i+n)}', f'Corrected_Time_{str(i+n)} - Time{str(i)}_ref').Filter(f'Sum(height[chan=={i}&&ipulse==0]>1000)').Filter(f'Sum(height[chan=={i+10}&&ipulse==0]>1000)').Filter(f'Sum({Area1}<area[chan=={i}&&ipulse==0])').Filter(f'Sum({Area2}<area[chan=={i+10}&&ipulse==0])').Filter(f'Sum(riseSamples[chan=={i}]>2)').Filter(f'Sum(riseSamples[chan=={i+n}]>2)').Filter(f'Sum({AreaM1}<area[chan=={i+2}&&ipulse==0])').Filter(f'Sum(height[chan=={i+2}&&ipulse==0]>1000)').Filter(f'Sum({AreaM2}<area[chan=={i+8}&&ipulse==0])').Filter(f'Sum(height[chan=={i+8}&&ipulse==0]>1000)')

			elif i==16 or i==17:
				
				 Panel_68_large_ = Panel_68_large.Define(f'TimeDiff_Bars{str(i)}_{str(i+n)}', f'Corrected_Time_{str(i+n)} - Time{str(i)}_ref').Filter(f'Sum(height[chan=={i}&&ipulse==0]>1000)').Filter(f'Sum(height[chan=={i+10}&&ipulse==0]>1000)').Filter(f'Sum({Area1}<area[chan=={i}&&ipulse==0])').Filter(f'Sum({Area2}<area[chan=={i+10}&&ipulse==0])').Filter(f'Sum(riseSamples[chan=={i}]>2)').Filter(f'Sum(riseSamples[chan=={i+n}]>2)').Filter(f'Sum({AreaM1}<area[chan=={i+2}&&ipulse==0])').Filter(f'Sum(height[chan=={i+2}&&ipulse==0]>1000)').Filter(f'Sum({AreaM2}<area[chan=={i+8+54}&&ipulse==0])').Filter(f'Sum(height[chan=={i+8+54}&&ipulse==0]>1000)')


			print(f'Writing Bars_{str(i)}_{str(i+n)} histogram to outfile')

			diffHisto = Panel_68_large_.Histo1D((f'Corrected_diff_Bars{str(i)}_{str(i+n)}', 'Timing; time', 40,  -26.25, 26.25),f'TimeDiff_Bars{str(i)}_{str(i+n)}')

			diffHisto.Fit(fit, 'L')

			calibrations[i+n] = fit.GetParameter(1)

			outfile.cd()

			diffHisto.Write()

	elif n==8:


		for i in topbars_pan68:	
	
			fit = r.TF1('gaus', 'gaus', -25, 25)
			
			Area1 = A_pan68[topbars_pan68.index(i)][0]

			Area2 = A_pan68[topbars_pan68.index(i)][-1]			
			
			AreaM1 = A_pan68_mid[topbars_pan68.index(i)][0]

			AreaM2 = A_pan68_mid[topbars_pan68.index(i)][-1]

			if i!=16 and i!=17:	

				#Make a column for the comparison channels  time

				Panel_68_large =  Panel_68_large.Define(f'Time{str(i+n)}',f'Max({t}[chan=={i+n}&&ipulse==0])')

	
				#Now a column for the corrections

				Panel_68_large = Panel_68_large.Define(f'Correction_{str(i+n)}', f'{str(fix_pan68[num][topbars_pan68.index(i)])}')

				#Make column for the corrected times

				Panel_68_large = Panel_68_large.Define(f'Corrected_Time_{str(i+n)}', f'Time{str(i+n)}+Correction_{str(i+n)}')

				#Find the elapsed time	

				Panel_68_large_ = Panel_68_large.Define(f'TimeDiff_Bars{str(i)}_{str(i+n)}', f'Corrected_Time_{str(i+n)} - Time{str(i)}_ref').Filter(f'Sum(height[chan=={i}&&ipulse==0]>1000)').Filter(f'Sum(height[chan=={i+10}&&ipulse==0]>1000)').Filter(f'Sum({Area1}<area[chan=={i}&&ipulse==0])').Filter(f'Sum({Area2}<area[chan=={i+10}&&ipulse==0])').Filter(f'Sum(riseSamples[chan=={i}]>2)').Filter(f'Sum(riseSamples[chan=={i+n}]>2)').Filter(f'Sum({AreaM1}<area[chan=={i+2}&&ipulse==0])').Filter(f'Sum({AreaM2}<area[chan=={i+8}&&ipulse==0])').Filter(f'Sum(height[chan=={i+2}&&ipulse==0]>1000)').Filter(f'Sum(height[chan=={i+8}&&ipulse==0]>1000)')

				print(f'Writing Bars_{str(i)}_{str(i+n)} histogram to outfile')

				diffHisto = Panel_68_large_.Histo1D((f'Corrected_diff_Bars{str(i)}_{str(i+n)}', 'Timing; time', 40,  -26.25, 26.25),f'TimeDiff_Bars{str(i)}_{str(i+n)}')

				diffHisto.Fit(fit, 'L')

				calibrations[i+n] = fit.GetParameter(1)

				outfile.cd()


				diffHisto.Write()

			if i==16 or i==17:	
	
	
				#Make a column for the comparison channels  time

				Panel_68_large =  Panel_68_large.Define(f'Time{str(i+n+54)}',f'Max({t}[chan=={i+n+54}&&ipulse==0])')

	
				#Now a column for the corrections

				Panel_68_large = Panel_68_large.Define(f'Correction_{str(i+n+54)}', f'{str(fix_pan68[num][topbars_pan68.index(i)])}')

				#Make column for the corrected times

				Panel_68_large = Panel_68_large.Define(f'Corrected_Time_{str(i+n+54)}', f'Time{str(i+n+54)}+Correction_{str(i+n+54)}')

				#Find the elapsed time	

				Panel_68_large_ = Panel_68_large.Define(f'TimeDiff_Bars{str(i)}_{str(i+n+54)}', f'Corrected_Time_{str(i+n+54)} - Time{str(i)}_ref').Filter(f'Sum(height[chan=={i}&&ipulse==0]>1000)').Filter(f'Sum(height[chan=={i+n+54}&&ipulse==0]>1000)').Filter(f'Sum({Area1}<area[chan=={i}&&ipulse==0])').Filter(f'Sum({Area2}<area[chan=={i+10}&&ipulse==0])').Filter(f'Sum(riseSamples[chan=={i}]>2)').Filter(f'Sum(riseSamples[chan=={i+n+54}]>2)').Filter(f'Sum({AreaM1}<area[chan=={i+2}&&ipulse==0])').Filter(f'Sum({AreaM2}<area[chan=={i+n+54}&&ipulse==0])').Filter(f'Sum(height[chan=={i+2}&&ipulse==0]>1000)').Filter(f'Sum(height[chan=={i+10}&&ipulse==0]>1000)')

				print(f'Writing Bars_{str(i)}_{str(i+n+54)} histogram to outfile')

				diffHisto = Panel_68_large_.Histo1D((f'Corrected_diff_Bars{str(i)}_{str(i+n+54)}', 'Timing; time', 40,  -26.25, 26.25),f'TimeDiff_Bars{str(i)}_{str(i+n+54)}')

				diffHisto.Fit(fit, 'L')

				calibrations[i+n] = fit.GetParameter(1)

				calibrations[i+n+54] = fit.GetParameter(1)

				outfile.cd()


				diffHisto.Write()


for i in topbars_pan72:

	#Make a column for reference times, i.e. the time stamp from the leading columns

	Panel_72_large =  Panel_72_large.Define(f'Time{str(i)}_ref',f'Max({t}[chan=={i}&&ipulse==0])')
	
	
for num in range(3):

	n = chanNxt[num]

	for i in topbars_pan72:
		
		fit = r.TF1('gaus', 'gaus', -25, 25)

		Area1 = A_pan72[topbars_pan72.index(i)][0]

		Area2 = A_pan72[topbars_pan72.index(i)][-1]			

		AreaM1 = A_pan68_mid[topbars_pan72.index(i)][0]

		AreaM2 = A_pan72_mid[topbars_pan72.index(i)][-1]
		
		#Make a column for the comparison channels  time

		Panel_72_large =  Panel_72_large.Define(f'Time{str(i+n)}',f'Max({t}[chan=={i+n}&&ipulse==0])')

	
		#Now a column for the corrections

		Panel_72_large = Panel_72_large.Define(f'Correction_{str(i+n)}', f'{str(fix_pan72[num][topbars_pan72.index(i)])}')

		#Make column for the corrected times

		Panel_72_large = Panel_72_large.Define(f'Corrected_Time_{str(i+n)}', f'Time{str(i+n)}+Correction_{str(i+n)}')

		#Find the elapsed time	

		Panel_72_large_ = Panel_72_large.Define(f'TimeDiff_Bars{str(i)}_{str(i+n)}', f'Corrected_Time_{str(i+n)} - Time{str(i)}_ref').Filter(f'Sum(height[chan=={i}&&ipulse==0]>1000)').Filter(f'Sum(height[chan=={i+10}&&ipulse==0]>1000)').Filter(f'Sum({Area1}<area[chan=={i}&&ipulse==0])').Filter(f'Sum({Area2}<area[chan=={i+10}&&ipulse==0])').Filter(f'Sum(riseSamples[chan=={i}]>2)').Filter(f'Sum(riseSamples[chan=={i+n}]>2)').Filter(f'Sum({AreaM1}<area[chan=={i+2}&&ipulse==0])').Filter(f'Sum({AreaM2}<area[chan=={i+8}&&ipulse==0])').Filter(f'Sum(height[chan=={i+2}&&ipulse==0]>1000)').Filter(f'Sum(height[chan=={i+8}&&ipulse==0]>1000)')


		print(f'Writing Bars_{str(i)}_{str(i+n)} histogram to outfile')

		diffHisto = Panel_72_large_.Histo1D((f'Corrected_diff_Bars{str(i)}_{str(i+n)}', 'Timing; time', 40,  -26.25, 26.25),f'TimeDiff_Bars{str(i)}_{str(i+n)}')

		diffHisto.Fit(fit, 'L')

		calibrations[i+n] = fit.GetParameter(1)

		outfile.cd()

		diffHisto.Write()

###############################################################################

#Close the output file

outfile.Close()

print(calibrations)

data['timing_Calibration'] = calibrations

if rewrite=='yes':
	with open('Calibration_Values.json', 'w') as calibration:
		json.dump(data, calibration)

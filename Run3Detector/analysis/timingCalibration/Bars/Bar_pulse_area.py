import ROOT as r

r.gROOT.SetBatch(1)

path = '/net/cms26/cms26r0/milliqan/outputRun3Hadd/v32/'

#set the run numbers for analysis

Run_nums = ['1006', '1031', '1032','1035', '1038', '1039']

#add the full file path for each data set to a list 

Runs = []

for i in Run_nums:
        Run = path+f'MilliQan_Run{i}_default_v32.root'
        Runs.append(Run)
        print(f'Added Run {i}')

#Create the chain for tree name 't' and add the files for analysis

chain = r.TChain('t')

for Run in Runs:
        chain.Add(Run)

#make data frame

df = r.RDataFrame(chain)

#Split the detector into two based on top panel coverage                                          
Panel_68_pulses = df.Define('Panel68', f'height[chan==68&&ipulse==0]').Filter('Sum(ipulse==0&&chan==68)')

Panel_72_pulses = df.Define('Panel72', f'height[chan==72&&ipulse==0]').Filter('Sum(ipulse==0&&chan==72)')

#make an output file for hists

outfile = r.TFile('Bar_pulse_area.root', 'RECREATE')

#List of leading channels under the associated panels

topbars_pan68 = [0, 1, 4, 5, 16, 17, 20, 21]

topbars_pan72 = [32, 33, 36, 37, 48, 49, 52, 53]

#Set the pattern jump to next channels

n = [0, 2, 8, 10]

#Filter for events in columnar fashion but through panel 68; height cutoff is 1000 mV

Panel_68_large = Panel_68_pulses.Filter('Sum(height[chan==68]>1000)')

Panel_72_large = Panel_72_pulses.Filter('Sum(height[chan==72]>1000)')

for num in range(4):

	k = n[num]
	
	if k!=8:

		for i in topbars_pan68:

			columndiff = Panel_68_large.Define(f'Bars{str(i)}_{str(i+k)}',f'Max(area[chan=={i+k}&&ipulse==0])').Filter(f'Sum(height[chan=={i}&&ipulse==0]>1000)').Filter(f'Sum(height[chan=={i+10}&&ipulse==0]>1000)')


			column_Histo = columndiff.Histo1D((f'Bar{str(i+k)}', 'Pulse_area;Area', 100, 50.e3, 800.e3), f'Bars{str(i)}_{str(i+k)}')

			outfile.cd()

			column_Histo.Write()

			print(f'Finished writing Bar{str(i+k)}')

	if k==8:
		
		for i in topbars_pan68:

			if i!=16 and i!=17:

				columndiff = Panel_68_large.Define(f'Bars{str(i)}_{str(i+k)}',f'Max(area[chan=={i+k}&&ipulse==0])').Filter(f'Sum(ipulse[chan=={i}]==0&&height[chan=={i}]>1000)').Filter(f'Sum(ipulse[chan=={i+10}]==0&&height[chan=={i+10}]>1000)')


				column_Histo = columndiff.Histo1D((f'Bar{str(i+k)}', 'Pulse_area;Area', 100, 50.e3, 800.e3), f'Bars{str(i)}_{str(i+k)}')

				outfile.cd()

				column_Histo.Write()
			
				print(f'Finished writing Bar{str(i+k)}')

			if i==16 or i==17:


				columndiff = Panel_68_large.Define(f'Bars{str(i)}_{str(i+k+54)}',f'Max(area[chan=={i+k+54}&&ipulse==0])').Filter(f'Sum(ipulse[chan=={i}]==0&&height[chan=={i}]>1000)').Filter(f'Sum(ipulse[chan=={i+10}]==0&&height[chan=={i+10}]>1000)')


				column_Histo = columndiff.Histo1D((f'Bar{str(i+k+54)}', 'Pulse_area;Area', 100, 50.e3, 800.e3), f'Bars{str(i)}_{str(i+k+54)}')

				outfile.cd()
				
				column_Histo.Write()

				print(f'Finished writing Bar{str(i+k+54)}')

	for i in topbars_pan72:
	
		columndiff = Panel_72_large.Define(f'Bars{str(i)}_{str(i+k)}',f'Max(area[chan=={i+k}&&ipulse==0])').Filter(f'Sum(height[chan=={i}&&ipulse==0]>1000)').Filter(f'Sum(height[chan=={i+10}&&ipulse==0]>1000)')

		column_Histo = columndiff.Histo1D((f'Bar{str(i+k)}', 'Pulse_area; Area', 100, 50.e3, 800.e3), f'Bars{str(i)}_{str(i+k)}')

		outfile.cd()

		column_Histo.Write()
		
		print(f'Finished writing Bar{str(i+k)}')

outfile.Close()

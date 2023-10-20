"""
rewrite dataCuts.py into uproot version based on triggerRates.py
remove the display method from triggerRates.py

to-do
merge multiple panda table from same run
duration cut + area cut
2d histogram Npulse vs height(done)

9-6 adding openMergedFileV2

10-9 
start doing pick up noise investigationb
comment out some code at at line 122 for doing the analysis with pickup flag
Now I only interest about pickupFlagTight


10-17
attempt to get pedestel value for height < 1000mV and duration > 1000ns, but fail. it seems something is wrong in panda dataframe 
"""


import numpy as np
import pandas as pd
import ROOT as r
import os 
import sys
import time
import uproot 
from functools import partial
from triggerConstants import *



class triggerChecker():


	#function to open the input root file
	def openFile(self, dataIn):
		self.input_file = dataIn
		self.runNum = int(dataIn.split('Run')[-1].split('.')[0])
		self.fileNum = int(dataIn.split('.')[1].split('_')[0])
		fin = uproot.open(dataIn)
		tree = fin['t']
		self.myarray = tree.arrays(uprootInputs, library='pd')
		#self.setTimes()
		#self.defineTrigCols()
	
	#openMergedFile("MilliQan_Run1026","/store/user/milliqan/trees/v31/")
	#don't use this one, if there are many files and you need to do a complicated cut
	def openMergedFile(self, base_name,directory):
		similar_files = []
    
		for filename in os.listdir(directory):
			if filename.startswith(base_name) and filename.endswith(".root"):
				similar_files.append(directory+filename)

		data = []
		for file in similar_files:
			fin = uproot.open(file)
			tree = fin['t']
			myarray = tree.arrays(uprootInputs, library='pd')
			data.append(myarray)
		merged_data = pd.concat(data, ignore_index=True)
		self.myarray=merged_data

	#make 2D histogram N pulse vs height using cut 3
	# for height and npulse get the max and min value and put them into 10 bins
	


	#Maybe I should create a general input method for 2DHist if needed
	def createHist(self):
		HistogramTitle = "npulse vs Height"
		self.hist = r.TH2D("histogram", "npulse vs Height;npulse;Height", 50, 0, 50, 20, 0, 1400) #in the order of pulse,height
		self.hist.SetTitle(HistogramTitle)
		self.hist.GetXaxis().SetTitle("Npulse")
		self.hist.GetYaxis().SetTitle("Height")
		self.ChanDuration = r.TH2D("chan vs duration", "chan vs duration above 1k mV;chan;duration", 80, 0, 80, 25, 0, 2500)
		self.chanHist = r.TH2D("chan vs hight","title;chan;Height",80,0,80,140, 0, 1400)
		self.npeHist = r.TH2D("chan vs npe","title;chan;npe",80,0,80,70, 0, 700000)
		self.areaHist = r.TH2D("chan vs area","title;chan;area",80,0,80,70, 0, 700000)
		self.timeHist = r.TH2D("chan vs Time","data above 1000mV",80,0,80,100,0,2500)
		self.BoardChanHist = r.TH2D("chan vs board","chan vs board",80,0,80,6,0,6)
		self.BoardChanHist.GetXaxis().SetTitle("chan")
		self.BoardChanHist.GetYaxis().SetTitle("board")
		self.timeHist.GetXaxis().SetTitle("chan")
		self.timeHist.GetYaxis().SetTitle("time")
		self.ChanPE = r.TH1D("chan NPE larger than 1", "chan : NPE > 1",80,0,80)

		#making special histogram for explore pulse with duration larger than 1000ns and height is less than 1000mV
		self.specialChan = r.TH1D("special chan", "chan : dureation > 1k ns and height < 1000m V",80,0,80)
		self.specialArea = r.TH1D("special area", "area : dureation > 1k ns and height < 1000m V",70, 0, 700000)
		self.specialTime = r.TH1D("special time", "time : dureation > 1k ns and height < 1000m V",100,0,2500)
		self.specialNpulse = r.TH1D("special Npulse", "Npulse : dureation > 1k ns and height < 1000m V", 50, 0, 50,)
		self.specialChanHeight = r.TH2D("special chan vs height","chan vs height:  dureation > 1k ns and height < 1000m V",80,0,80,280, 0, 1400)
		self.specialHeight = r.TH1D("special height", " height : dureation > 1k ns and height < 1000m V",40, 0, 1400)
		self.specialPedastal = r.TH2D("special chan vs pedastal","chan vs pedastal:  dureation > 1k ns and height < 1000m V",80,0,80,280, 0, 1400)
		self.specialuncorrectedHeightChan = r.TH2D("Special Chan vs Uncorrected height","chan vs height:  dureation > 1k ns and height < 1000m V",80,0,80, 280, 0, 1400)
		self.specialpedastalDistribution = r.TH1D("special pedestal distribution", "pedestal : dureation > 1k ns and height < 1000m V",280, 0, 1400)
		self.specialuncorrectedHeight = r.TH1D("special uncorrected height distribution", "uncorrected height : dureation > 1k ns and height < 1000m V",280, 0, 1400)
		self.specialuncorrectedHeight.GetXaxis().SetTitle("mV")
		self.specialuncorrectedHeight.GetYaxis().SetTitle("# of pulses")
		self.specialpedastalDistribution.GetXaxis().SetTitle("mV")
		self.specialpedastalDistribution.GetYaxis().SetTitle("# of event")

		self.specialPedastal.GetXaxis().SetTitle("chan")
		self.specialPedastal.GetYaxis().SetTitle("pedestal (mV)")
		self.specialuncorrectedHeightChan.GetXaxis().SetTitle("chan")
		self.specialuncorrectedHeightChan.GetYaxis().SetTitle("uncorrected height (mV)")
		#making histogram for pulse at 22600-79000 area region
		self.AreaSpecialChan = r.TH1D("Area SpecialChan", "chan : 22600-79000 area",80,0,80)
		self.AreaSpecialChanHeight = r.TH2D("Area Special Chan height","chan vs height:  22600-79000 area",80,0,80,140, 0, 1400)


		

	
	#the following method come with channel hist, might to need to separate them
	def heightvsPulseHist(self,data,pedestalData,CpanelVeot=False):

		
		NumEvent=data["event"].max() + 1 #NumEvent=data["even4t"].max() + 1 TypeError: tuple indices must be integers or slices, not str

		if np.isnan(NumEvent): return
		#collect the event channel pair for extract the pedestal data
		EventChanPair=[]
		for event in range(NumEvent): #event based
			selected_data = data[data["event"] == event]
			pickupFlagList = selected_data["pickupFlag"]
			#pickupTightFlagList = selected_data["pickupFlagTight"]
			DurationList = selected_data["duration"]
			height_list=selected_data["height"]
			pulse_list =selected_data["npulses"]
			chan_list = selected_data["chan"]
			npe_list = selected_data["nPE"]
			area_list = selected_data["area"]
			board_list = selected_data["board"]
			time_list = selected_data["time_module_calibrated"]	
			npe_list = selected_data["nPE"]
			#dynamicPedestal_list = selected_data["dynamicPedestal"]
			count = 0
			if CpanelVeot == True:
				for chan in chan_list:
					
					#after june 29, eg run 1118, 74 and 75 become front/back panels
					#"""
					if chan >= 68 and chan <= 73:
						count += 1
						break

					#"""
					#used for run 1020-1030, 71 and 75 are front/back panels
					"""
					if chan >= 72 and chan <= 74:  
						count += 1
						break
					if chan >= 68 and chan <= 70:
						count += 1
						break
					"""
			if count == 0:
				#for pickUp, height, npulse,chan,npe,area,time,duration, board, dynamicPedestal in zip(pickupFlagList,height_list,pulse_list,chan_list,npe_list,area_list,time_list,DurationList,board_list,dynamicPedestal_list):
				for pickUp, height, npulse,chan,npe,area,time,duration, board in zip(pickupFlagList,height_list,pulse_list,chan_list,npe_list,area_list,time_list,DurationList,board_list):
				#for pickUp, height, npulse,chan,npe,area,time,duration in zip(pickupTightFlagList,height_list,pulse_list,chan_list,npe_list,area_list,time_list,DurationList):
					if pickUp==False:
						self.hist.Fill(npulse,height)
						self.chanHist.Fill(chan,height)
						self.npeHist.Fill(chan,npe)
						self.areaHist.Fill(chan,area)
						self.BoardChanHist.Fill(chan,board)
						if npe > 1:
							self.ChanPE.Fill(chan)

						if area > 22600 and area < 79000:
							self.AreaSpecialChan.Fill(chan)
							self.AreaSpecialChanHeight.Fill(chan,height)



						if duration > 1000 and height < 1000:
							self.specialChan.Fill(chan)
							self.specialArea.Fill(area)
							self.specialTime.Fill(time)
							self.specialNpulse.Fill(npulse)
							self.specialChanHeight.Fill(chan,height)
							self.specialHeight.Fill(height)
							pedastalValue = pedestalData["event" == event]["dynamicPedestal"][chan]
							self.specialuncorrectedHeightChan.Fill(chan,height-pedastalValue)
							self.specialuncorrectedHeight.Fill(height-pedastalValue)

							EventChanPair.append([event,chan])


						if height>=1000:
							self.timeHist.Fill(chan,time)
							self.ChanDuration.Fill(chan,duration)
							

				#cut front and back panel need to reach 1000mV
				"""
				chanCheck = []
				for pickUp, height, chan in zip(pickupFlagList,height_list,chan_list):
					if pickUp==False:
						if height > 1000:
							chanCheck.append(chan)

				if 74 in chanCheck:
					if 75 in chanCheck:
						for pickUp, height, npulse,chan,npe,area,time in zip(pickupFlagList,height_list,pulse_list,chan_list,npe_list,area_list,time_list):
							if pickUp==False:
								
								self.hist.Fill(npulse,height)
								self.chanHist.Fill(chan,height)
								self.npeHist.Fill(chan,npe)
								self.areaHist.Fill(chan,area)
								if height>=1000:
									self.timeHist.Fill(chan,time)

				"""
		#check if EventChanPair is empty
		if not EventChanPair:
			pass
		else:
			# Convert the list of lists into a set of tuples
			EventChanPair_set = set(tuple(sublist) for sublist in EventChanPair)
			for event, chan in EventChanPair_set:
				#print(chan,event)
				#print(pedestalData["event" == event]["dynamicPedestal"])
				dynamicPedestalValue=pedestalData["event" == event]["dynamicPedestal"][chan]
				self.specialPedastal.Fill(chan,dynamicPedestalValue)
				self.specialpedastalDistribution.Fill(dynamicPedestalValue)
				



	#mergedFileV2: it can process the selected files from the same run, but not merge them into big root file.
	def openMergedFileV2(self, base_name,directory):
		similar_files = []

		self.createHist()#create histogram

		for filename in os.listdir(directory):
			if filename.startswith(base_name) and filename.endswith(".root"):
				similar_files.append(directory+filename)
		NumnberOfTotalFiles = len(similar_files)
		processFileCount = 0
		data = []
		firstF=similar_files[0:15]
		#lastTen=similar_files[-2:]
		


		#for file in firstF:
		for file in similar_files:
			fin = uproot.open(file)
			tree = fin['t']
			data = tree.arrays(uprootInputs, library='pd')
			pedestalData = tree.arrays(["event","dynamicPedestal"])
			#print(type(data))
			#self.heightvsPulseHist(data,True) #ture for enable cosmic panel veto
			if type(data) == tuple:
				self.heightvsPulseHist(data[0],pedestalData)
			else:
				self.heightvsPulseHist(data,pedestalData)
			processFileCount += 1
			progress =processFileCount/NumnberOfTotalFiles*100
			print("progress:"+str(progress)+"%")
		
		self.hist.Write()
		self.chanHist.Write()
		self.npeHist.Write()
		self.areaHist.Write()
		self.timeHist.Write()
		self.ChanDuration.Write()
		self.BoardChanHist.Write()
		self.specialChan.Write()
		self.specialArea.Write()
		self.specialTime.Write()
		self.specialNpulse.Write()
		self.specialChanHeight.Write()
		self.specialHeight.Write()
		self.AreaSpecialChan.Write()
		self.AreaSpecialChanHeight.Write()
		self.ChanPE.Write()
		self.specialPedastal.Write()
		self.specialuncorrectedHeightChan.Write()
		self.specialuncorrectedHeight.Write()
		self.specialpedastalDistribution.Write()




	

if __name__ == "__main__":

	r.gROOT.SetBatch(1)

	Run_num = 1026

	#run1025 has issue
	#RunList = [1020,1021,1022,1023,1024,1025,1026,1027,1028,1029,1030]
	#for Run_num in RunList:
	mychecker = triggerChecker()
	print(f"run:{Run_num} start" )
	fileName = f"run{Run_num}_manyplots_more_bins.root"
	#fileName = f"run{Run_num}_heightVSPulse_cosPanelVeto.root"
	output_file = r.TFile(fileName, "RECREATE")

	mychecker.openMergedFileV2(f"MilliQan_Run{Run_num}","/store/user/milliqan/trees/v33/")
	output_file.Close()
	

	



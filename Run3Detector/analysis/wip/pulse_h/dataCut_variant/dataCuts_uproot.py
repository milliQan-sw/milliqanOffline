"""
rewrite dataCuts.py into uproot version based on triggerRates.py
remove the display method from triggerRates.py

to-do
merge multiple panda table from same run
duration cut + area cut
2d histogram Npulse vs height(done)

9-6 adding openMergedFileV2
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
	
	
	def heightvsPulseHist(self,data,CpanelVeot=False):


		NumEvent=data["event"].max() + 1
		if np.isnan(NumEvent): return

		for event in range(NumEvent): #event based
			selected_data = data[data["event"] == event]
			pickupFlagList = selected_data["pickupFlag"]
			height_list=selected_data["height"]
			pulse_list =selected_data["npulses"]
			chan_list = selected_data["chan"]
			count = 0
			if CpanelVeot == True:
				for chan in chan_list:
					
					#after june 29, eg run 1118 74 and 75 become front/back panels
					"""
					if chan >= 68 and chan <= 73:
						count += 1
						break

					"""
					#beaware run 1020-1030, 71 and 75 are front/back panels
					#"""
					if chan >= 72 and chan <= 74:  
						count += 1
						break
					if chan >= 68 and chan <= 70:
						count += 1
						break
					#"""
			if count == 0:
				for pickUp, height, npulse,chan in zip(pickupFlagList,height_list,pulse_list,chan_list):
					if pickUp==False:
						self.hist.Fill(npulse,height)

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
		firstF=similar_files[0:9]
		#lastTen=similar_files[-2:]
		
		#for file in firstF:
		for file in similar_files:
			fin = uproot.open(file)
			tree = fin['t']
			data = tree.arrays(uprootInputs, library='pd')
			#self.heightvsPulseHist(data,True) #ture for enable cosmic panel veto
			self.heightvsPulseHist(data)
			processFileCount += 1
			progress =processFileCount/NumnberOfTotalFiles*100
			print("progress:"+str(progress)+"%")
		
		self.hist.Write()



	

if __name__ == "__main__":

	r.gROOT.SetBatch(1)

	#Run_num = 1022
	#run1025 has issue
	RunList = [1025,1026,1027,1028,1029,1030]
	for Run_num in RunList:
		mychecker = triggerChecker()
		print(f"run:{Run_num} start" )
		fileName = f"run{Run_num}_heightVSPulse.root"
		#fileName = f"run{Run_num}_heightVSPulse_cosPanelVeto.root"
		output_file = r.TFile(fileName, "RECREATE")

		mychecker.openMergedFileV2(f"MilliQan_Run{Run_num}","/store/user/milliqan/trees/v33/")#new code


		output_file.Close()
	

	



import ROOT as r
from DetectorGeometry import *
from triggerConstants import *
import os
import numpy as np
import pandas as pd
import sys
import time
import uproot 
from functools import partial
from triggerConstants import *

class DataHandler():
	def __init__(self, dataPath,run,debug=False):

		self.debug = debug
		self.initializeData(dataPath,run)



	def initializeData(self, datapath,run):
		filesOfsameRun=[]
		self.pandasFiles = []
		base_name = f"MilliQan_Run{run}"
		
		for filename in os.listdir(datapath):
			if filename.startswith(base_name) and filename.endswith(".root"):
				filesOfsameRun.append(datapath+filename)
		
		if self.debug == True:
			print(filesOfsameRun)

		for file in filesOfsameRun:
			fin = uproot.open(file)
			tree = fin['t']
			singleData = tree.arrays(uprootInputs, library='pd')
			self.pandasFiles.append(singleData)
			#applyCuts(self.cuts,singleData)
		
	def plotCTHist(self,selected_data):
		TimeList = selected_data["timeFit"]
		LayerList = selected_data["layer"]
		TypeList = selected_data["type"]
		NPEList = selected_data["nPE"]
		for time,layer,type,npe in zip(TimeList,LayerList,TypeList,NPEList):
			if type == 0 and npe > 1:
				if layer == 0:
					CorrectedTime = time
					layer1CTHist.Fill(CorrectedTime)
				if layer == 1:
					CorrectedTime = time - 3.96
					layer2CTHist.Fill(CorrectedTime)
				if layer == 2:
					CorrectedTime = time - 3.96*2
					layer3CTHist.Fill(CorrectedTime)
				if layer == 3:
					CorrectedTime = time - 3.96 * 3
					layer4CTHist.Fill(CorrectedTime)

	def plotTHist(self,selected_data):
		TimeList = selected_data["timeFit"]
		LayerList = selected_data["layer"]
		TypeList = selected_data["type"]
		NPEList = selected_data["nPE"]
		for time,layer,type,npe in zip(TimeList,LayerList,TypeList,NPEList):
			if type == 0 and npe > 1:
				THistNoCorrect.Fill(time)
				if layer == 0:
					layer1THist.Fill(time)
				if layer == 1:
					layer2THist.Fill(time)
				if layer == 2:
					layer3THist.Fill(time)
				if layer == 3:
					layer4THist.Fill(time)
	

	

	def applyCuts(self,cuts):
		final_cutData = [] #save the event that pass the cuts with DaqNumber as identication.
		#resultList = []
		for singleData in self.pandasFiles:
			#lc=len(cuts)
			
			#None_check = []
			#select a specifc event
			NumEvent=singleData["event"].max() + 1
			#quit if there is no data in the file
			if np.isnan(NumEvent): continue
			#start the event based analysis
			for event in range(NumEvent):
				selected_data = singleData[(singleData["event"] == event) & (singleData["pickupFlag"] == False)] #select the data with specified event number and filter out those with tag "pickupFlag" == False
				self.plotTHist(selected_data)
				
				DQ = set(selected_data["DAQEventNumber"])
				emptySet = set()
				if DQ == emptySet: #it means currents event is empty
					continue
				event_cutData = []
				event_result = []
				for cut in cuts:
					result,DaqNum= cut(selected_data)
					if self.debug == True:
						print(str(result)+ " " +str(DaqNum))
					#if result == 0: #this means current event can't pass a specific cut, so move to the next event.
					#    break 
					event_cutData.append(DaqNum) #it should add to event based list.
					event_result.append(result)   #it should add to event based list.
				#if a single event pass all the cuts, then move the thing from file based(we have multiple files from a same run) list to run based list
				event_result = set(event_result)
				if 0 in event_result:
					continue
				else:
					#assuming each event has an unique DaqNum.
					final_cutData.append(DaqNum)
					self.plotCTHist(selected_data)


		return final_cutData
		
	#3.96 is the time for particle travel straight through a bar dectector and the air gap.
	def correctedTimeCut(self,selected_data):
		CorrectedTimeList = []
		TimeList = selected_data["timeFit"]
		LayerList = selected_data["layer"]
		TypeList = selected_data["type"]
		NPEList = selected_data["nPE"]
		DQ = set(selected_data["DAQEventNumber"])
		for time,layer,type,NPE in zip(TimeList,LayerList,TypeList,NPEList):
			if type == 0 and NPE > 1:  #bar
				if layer == 0:
					CorrectedTime = time
				if layer == 1:
					CorrectedTime = time - 3.96
				if layer == 2:
					CorrectedTime = time - 3.96*2
				if layer == 3:
					CorrectedTime = time - 3.96 * 3
				CorrectedTimeList.append(CorrectedTime)
		if CorrectedTimeList == []: return 0, None
		TimeDiff = max(CorrectedTimeList) - min(CorrectedTimeList)
		#15.02 is the time for particle travel through four bar detectector and the ajacent air gap.
		if TimeDiff < 15.02:
			return 1,DQ
			
		else:
			return 0, None

	

	
	
	




		

		





	#exactly one hit per layer cut
	#need to exclude the panels
	def exOneHit(self,selected_data):
		chanList = selected_data["chan"]
		layerList=selected_data["layer"]
		DQ = set(selected_data["DAQEventNumber"])
		emptySet = set()

		newLayerList = [] #need to exclude hits on the panels
		for chan,layer in zip(chanList,layerList):
			if chan >= 68 and chan <=75:
				continue
			else:
			   newLayerList.append(layer) 

		if self.debug:
			print("DQ:" + str(DQ))
		if self.debug:
			print("layerList:"+str(layerList))
		#DAQEventNumber = DQ[0]
		if len(set(newLayerList)) != len(newLayerList):
			return 0, None
		
		return 1,DQ


	#might need to add a new version flag for panel swaping after June
	def cosmicPanelVeto(self,selected_data):
		chanList = selected_data["chan"]
		DQ = set(selected_data["DAQEventNumber"])
		for chan in chanList:
			if (chan >= 68 and chan <=70) or (chan >=72 and chan <=74):
				return 0, None
		return 1,DQ




if __name__ == "__main__":

	Run_num = 1026
	fileName = f"run{Run_num}_TimeFitdistributionEX1Hit.root"
	output_file  = r.TFile(fileName, "RECREATE")
	layer1CTHist = r.TH1D("layer 0 corrected time","layer 0 corrected time",2500,0,2500)
	layer2CTHist = r.TH1D("layer 1 corrected time","layer 1 corrected time",2500,0,2500)
	layer3CTHist = r.TH1D("layer 2 corrected time","layer 2 corrected time",2500,0,2500)
	layer4CTHist = r.TH1D("layer 3 corrected time","layer 3 corrected time",2500,0,2500)
	layer1THist = r.TH1D("layer 0  time","layer 0 time",2500,0,2500)
	layer2THist = r.TH1D("layer 1  time","layer 1 time",2500,0,2500)
	layer3THist = r.TH1D("layer 2  time","layer 2 time",2500,0,2500)
	layer4THist = r.TH1D("layer 3  time","layer 3 time",2500,0,2500)
	THistNoCorrect = r.TH1D("default time","default time",2500,0,2500)#over time distribution histogram for bar detector 
	data = DataHandler("/store/user/milliqan/trees/v33/bar/",Run_num)
	#cutData=data.applyCuts([data.exOneHit,data.cosmicPanelVeto])
	cutData=data.applyCuts([data.correctedTimeCut,data.exOneHit])
	#cutData=data.applyCuts([data.cosmicPanelVeto])
	#print(cutData)
	THistNoCorrect.Write()
	layer1CTHist.Write()
	layer2CTHist.Write()
	layer3CTHist.Write()
	layer4CTHist.Write()
	layer1THist.Write()
	layer2THist.Write()
	layer3THist.Write()
	layer4THist.Write()
	output_file.Close()



		
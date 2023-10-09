"""
rewrite dataCuts.py into uproot version based on triggerRates.py
remove the display method from triggerRates.py

to-do
merge multiple panda table from same run
duration cut + area cut
2d histogram Npulse vs height

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
from histogramMerged import *



class triggerChecker():

	def __init__(self):
		self.defineFunctions()

	def checkNPulses(self, x, nHits=4):
		if len((x.unique()<64)) >= nHits: return True
		return False
	
	#check for NLayers hits in window
	def checkNLayers(self, x, nLayers=4):
		if len(x) < nLayers: return False
		unique = x.unique()
		layers = np.where((unique >= 0) & (unique < 4))
		return layers[0].size >= nLayers

	#return value of column (for debugging)
	def returnValue(self, x):
		return x.values[0]

	#check for separate layers in window
	def checkSeparate(self, x):
		hit = (np.array([np.in1d(combo, x) for combo in separateCombos]).all(1)).any()
		return hit

	#check for adjacent layers in window
	def checkAdjacent(self, x):
		hit = (np.array([np.in1d(combo, x) for combo in adjacentCombos]).all(1)).any()
		return hit
	
	#check for top panels trigger in window
	def checkTopPanels(self, x, bot=False):
		hit = np.array([np.in1d(panel, x) for panel in topPanels]).any()
		if not bot: return hit    
		extra = np.array([np.in1d(chan, x) for chan in bottomBars]).any()
		return extra*hit
	
	#check for front+back panels in window
	def checkThroughGoing(self, x):
		hit = np.array([np.in1d(panel, x) for panel in frontBack]).all()
		return hit
		
	#check for 3 in row trigger in window
	def checkThreeInRow(self, x):
		passed = np.array([np.count_nonzero([np.in1d(path, x) for path in line]) >= 3 for line in straightPaths]).any()
		return passed

	#define columns replaced by trigger finding
	def defineTrigCols(self):
		self.myarray['fourLayers'] = self.myarray['layer']
		self.myarray['threeInRow'] = self.myarray['chan']
		self.myarray['separateLayers'] = self.myarray['layer']
		self.myarray['adjacentLayers'] = self.myarray['layer']
		self.myarray['nLayers'] = self.myarray['layer']
		self.myarray['nHits'] = self.myarray['layer']
		self.myarray['topPanels'] = self.myarray['chan']
		self.myarray['topBotPanels'] = self.myarray['chan']
		self.myarray['panelsCleaned'] = np.where((self.myarray['height'] >= panelThreshold), self.myarray['chan'], False)
		self.myarray['frontBack'] = self.myarray['panelsCleaned']

	#function to open the input root file
	def openFile(self, dataIn):
		self.input_file = dataIn
		self.runNum = int(dataIn.split('Run')[-1].split('.')[0])
		self.fileNum = int(dataIn.split('.')[1].split('_')[0])
		fin = uproot.open(dataIn)
		tree = fin['t']
		self.myarray = tree.arrays(uprootInputs, library='pd')
		self.setTimes()
		self.defineTrigCols()
	
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


	#cut base on pulse and height
	def PHECut(self,height_threshold,pulse_threshold):
		eventList = []
		arrays = self.myarray
		numberOFevents = arrays["event"].max()
		for event in range(numberOFevents):

			pulse_count = 0 # count the number of pulse above height_threshold in an event
			#get the heightList in an event
			heightList= data[data["event"] == event]["height"]
			for height in heightList:
				if height >= height_threshold:
					pulse_count += 1
			if pulse_count >= pulse_threshold:
				eventList.append(event)
		
		return event


	#use datetime to create times of hits to be used in rolling window
	def setTimes(self):
		self.myarray['fake_time'] = pd.to_datetime((self.myarray['time']+self.myarray['event']*86400), unit='s')  
		self.myarray = self.myarray.sort_values(by=['entry', 'time'], ascending=True)

	#define specific trigger functions from generic functions
	def defineFunctions(self):
		self.thisNLayers = partial(self.checkNLayers, nLayers=nLayers)
		self.thisNPulses = partial(self.checkNPulses, nHits=nHits)
		self.topBotPanels = partial(self.checkTopPanels, bot=True)
		self.this4Layers = partial(self.checkNLayers, nLayers=4)

	#find the triggers in offline data
	def findTriggersOffline(self):
		#use a rolling window to find the triggers that should pass
		self.myarray[offlineTrigNames] = self.myarray.rolling(window='{}s'.format(trigWindow), on="fake_time", axis=0).agg({"fourLayers": self.this4Layers, "threeInRow": self.checkThreeInRow, "separateLayers": self.checkSeparate, "adjacentLayers": self.checkAdjacent, 'nLayers': self.thisNLayers, 'nHits': self.thisNPulses, 'topPanels': self.checkTopPanels, 'topBotPanels': self.topBotPanels, 'frontBack': self.checkThroughGoing})

	#convert all triggers to binary
	def convertTriggers(self, df):
		trig = format(int(df), '#016b').split("b")[-1]
		trig = trig[::-1]
		return trig

	#get value of specific trigger bit
	def getTriggerBit(self, df, bit):
		return int(df[bit])

	#get triggers passed online
	def getOnlineTriggers(self):
		self.myarray['triggerString'] = self.myarray.apply(lambda row: self.convertTriggers(row.tTrigger), axis=1)
		for i in range(13):
			self.myarray['trig{}'.format(i)] = self.myarray.apply(lambda row: self.getTriggerBit(row.triggerString, i), axis=1)

	#open the output file for plots
	def openOutputFile(self):
		outputFilename = os.getcwd() + '/triggerRates_Run{0}.{1}.root'.format(self.runNum, self.fileNum)
		self.file_out = r.TFile.Open(outputFilename, 'recreate')




	#height cut
	#dataCu:data used for cut
	#dataCo:data that I need to collect. 
	#outputList:output the corresponded list
	#pulse-based cut
	
	#cut0: collect the data before applied the cut
	def cut0(self,dataCo):
		outputList = []
		for specificData in self.myarray[(self.myarray["pickupFlag"] == False) & (self.myarray["type"] == 0)][dataCo]:
			if dataCo == "type" and specificData>0:
				print("something is wrong") 
			outputList.append(specificData)
		return outputList

	
	def cut1(self,dataCu,cutValue,dataCo):
		outputList = []
		for specificData in self.myarray[(self.myarray[dataCu] >= cutValue) & (self.myarray["pickupFlag"] == False) & (self.myarray["type"] == 0)][dataCo]:
			outputList.append(specificData)
		return outputList
	

	def cut2(self,dataCu,cutValue,dataCo):
		outputList = []
		for specificData in self.myarray[(self.myarray[dataCu] <= cutValue) & (self.myarray["pickupFlag"] == False) & (self.myarray["type"] == 0)][dataCo]:
			outputList.append(specificData)
		return outputList
	
	def cut3(self,dataCu,cutValue1,cutValue2,dataCo):
		outputList = []
		data=self.myarray
		for specificData in data[(self.myarray[dataCu] <= cutValue2) & (self.myarray[dataCu] >= cutValue1) & (self.myarray["pickupFlag"] == False) & (self.myarray["type"] == 0)][dataCo]:
			outputList.append(specificData)
		return outputList

	#cut4 is made for creating the 2D histogram.
	def cut4(self,dataCu1,cutValue1,cutValue2,datacut2,cutValue3,cutValue4):
		
		data=self.myarray
		#extract an event based data, let's use time
		data1 = data[(self.myarray[dataCu1] <= cutValue2) & (self.myarray[dataCu1] >= cutValue1) & (self.myarray[datacut2] >= cutValue3) & (self.myarray[datacut2] <= cutValue4) & (self.myarray["pickupFlag"] == False) & (self.myarray["type"] == 0)]["time"]
		
		Num_event = len(data1)
		return Num_event


	#event-based cut
	#use pulse cut(event-based) to get pulse based data? what?
	
	def pulseCount(self,dataCo,heightCut = 0):
		outputList = []
		#grab the number of event in a file
		eventList=set(data["event"])
		Num_event = len(eventList)
		for specific_event in eventList:
			pulse_count = data[data["height"] > heightCut]["event"]==specific_event
			num = pulse_count.sum() #the number of pulse that pass height cut

if __name__ == "__main__":

	"""
	r.gROOT.SetBatch(1)
	
	
	#height cut
	#runList = [1020,1021,1022,1023,1024,1025,1026,1027,1028,1029,1030]
	#for Run_num in runList:
	Run_num = 1026
	mychecker = triggerChecker()
	#mychecker.openFile(filename)
	mychecker.openMergedFile(f"MilliQan_Run{Run_num}","/store/user/milliqan/trees/v33/bar/")

	dataList = ["time","area","type","duration","column","layer","board","pickupFlag","npulses"] #column name that I selected for data collection
	timeList = []
	areaList = []
	typeList = []
	durationList = []
	columnList = []
	layerList = []
	heightList = []
	pickupFlagList = []
	boardList = []
	pulseList = []
	#ignore sideband's data and max so far

	#outputdataList=[timeList,heightList,areaList,typeList,duration]
	outputdataList=[timeList,areaList,typeList,durationList,columnList,layerList,boardList,pickupFlagList,pulseList] #output data for height cut



	for CollectData,OutputLIST in zip(dataList,outputdataList):
		#adding the extra histogram that no cut is applied.
		DataNoCut = mychecker.cut0(CollectData)
		OutputLIST.append(DataNoCut)

		for i in range(11):
			height_threshold = 100 + i * 100
			#print("CollectData:"+CollectData)
			ExtractedData = mychecker.cut2("height",height_threshold,CollectData)
			OutputLIST.append(ExtractedData)
	
	def pulse_histogram_noCuts(xtitle,data,nBins, xMin, xMax):
		HistogramTitleWithOutCut = f"{xtitle} without cut"
		hist0 = r.TH1D(f"data before applying the cut :{xtitle}", "My Histogram", nBins, xMin, xMax+(xMax-xMin)/nBins)
		hist0.SetTitle(HistogramTitleWithOutCut)
		hist0.GetXaxis().SetTitle(xtitle)
		for d in data:
			hist0.Fill(d)
		maxBinContent = hist0.GetMaximum()
		hist0.GetYaxis().SetRangeUser(0, 1.2 * maxBinContent)
		#hist0.Draw()
		hist0.Write()
	
	#plot the data with T hisogram
	def height_histogram(height,xtitle,data,nBins, xMin, xMax):
		HistogramTitle = f"{xtitle} with above {height}mV cut "
		hist = r.TH1D(f"above {height}mV data:{xtitle}", "My Histogram", nBins, xMin, xMax+(xMax-xMin)/nBins)
		hist.SetTitle(HistogramTitle)
		hist.GetXaxis().SetTitle(xtitle)
		for d in data:
			hist.Fill(d)
		#hist.Scale(1.0 / hist.GetEntries()) 
		canvas = r.TCanvas("canvas", "Canvas Title", 800, 600)
		hist.Draw()
		hist.Write()

	fileName = f"run{Run_num}_heightBelowcut.root"
	output_file = r.TFile(fileName, "RECREATE")


	for index1,subList in enumerate(outputdataList):
		for index2,subData in enumerate(subList):
			if index2 == 0:
				if subData == None: continue
				if subData == []: continue
				pulse_histogram_noCuts(dataList[index1],subData,100, min(subData), max(subData))
			else:
				if subData == None: continue
				height = 100 + (index2-1) * 100
				#print(min(subData))
				#print(max(subData))
				if subData == []: continue
				height_histogram(height,dataList[index1],subData,100, min(subData), max(subData))
	
	output_file.Close()
	HistMerge(fileName)
	
	#end of height cut
	"""
	

	"""
	#start the pulse(branch) cut (0-20 with increment value 2)
	Run_num = 1026
	fileName = f"run{Run_num}_Below_Npulsecut.root"
	output_file = r.TFile(fileName, "RECREATE")
	mychecker = triggerChecker()
	mychecker.openMergedFile(f"MilliQan_Run{Run_num}","/store/user/milliqan/trees/v33/bar/")


	#clear the data
	timeList = []
	areaList = []
	typeList = []
	durationList = []
	columnList = []
	layerList = []
	heightList = []
	pickupFlagList = []
	boardList = []
	pulseList = []
	dataList = ["time","area","type","duration","column","layer","board","pickupFlag","height"]
	outputdataList=[timeList,areaList,typeList,durationList,columnList,layerList,boardList,pickupFlagList,heightList]

	for CollectData,OutputLIST in zip(dataList,outputdataList):
		#adding the extra histogram that no cut is applied.
		DataNoCut = mychecker.cut0(CollectData)
		OutputLIST.append(DataNoCut)

		for i in range(11):
			pulse_threshold = 0 + i * 2
			#print("CollectData:"+CollectData)
			ExtractedData = mychecker.cut2("npulses",pulse_threshold,CollectData)
			OutputLIST.append(ExtractedData)

	
	def pulse_histogram(pulse_value,xtitle,data,nBins, xMin, xMax):
		
		HistogramTitle = f"{xtitle} with below {pulse_value} pulses cut "
		hist = r.TH1D(f"below {pulse_value}pulses data:{xtitle}", "My Histogram", nBins, xMin, xMax+(xMax-xMin)/nBins)
		hist.SetTitle(HistogramTitle)
		hist.GetXaxis().SetTitle(xtitle)
		for d in data:
			hist.Fill(d)
		#hist.Scale(1.0 / hist.GetEntries()) 
		#canvas = r.TCanvas("canvas", "Canvas Title", 800, 600)
		maxBinContent = hist.GetMaximum()
		hist.GetYaxis().SetRangeUser(0, 1.2 * maxBinContent)
		#hist.Draw()
		hist.Write()
	
	def pulse_histogram_noCuts(pulse_value,xtitle,data,nBins, xMin, xMax):
		HistogramTitleWithOutCut = f"{xtitle} without cut"
		hist0 = r.TH1D(f"data before applying the cut :{xtitle}", "My Histogram", nBins, xMin, xMax+(xMax-xMin)/nBins)
		hist0.SetTitle(HistogramTitleWithOutCut)
		hist0.GetXaxis().SetTitle(xtitle)
		for d in data:
			hist0.Fill(d)
		maxBinContent = hist0.GetMaximum()
		hist0.GetYaxis().SetRangeUser(0, 1.2 * maxBinContent)
		#hist0.Draw()
		hist0.Write()

	
	for index1,subList in enumerate(outputdataList):

		for index2,subData in enumerate(subList):
			if index2 == 0:
				if subData == None: continue
				if subData == []: continue
				pulse_histogram_noCuts(pulse_threshold,dataList[index1],subData,100, min(subData), max(subData))
			else:	
				if subData == None: continue
				pulse_threshold = 0 + (index2-1) * 2
				if subData == []: continue
				pulse_histogram(pulse_threshold,dataList[index1],subData,100, min(subData), max(subData))
	output_file.Close()
	HistMerge(fileName)
	#end of pulse analysis
	"""
	
	
	#for both area cut and duration cut, they need to be in cut 3
	#area cut
	# clean up the outputdataList
	Run_num = 1026
	fileName = f"run{Run_num}_areacut.root"
	output_file  = r.TFile(fileName, "RECREATE")
	mychecker = triggerChecker()
	mychecker.openMergedFile(f"MilliQan_Run{Run_num}","/store/user/milliqan/trees/v33/bar/")
	
	timeList = []
	areaList = []
	typeList = []
	durationList = []
	columnList = []
	layerList = []
	heightList = []
	pickupFlagList = []
	boardList = []
	pulseList = []

	dataList = ["time","type","duration","column","layer","board","pickupFlag","height"]
	outputdataList=[timeList,typeList,durationList,columnList,layerList,boardList,pickupFlagList,heightList]
	#areaLowerBound = [0,200,1200,3000,5000,7000,10000,20000,60000]
	#areaUpperBound = [200,1200,3000,5000,7000,10000,20000,60000,100000]
	areaLowerBound = [0,22530,78818,123848,180135,405285,506603,652950,810556]
	areaUpperBound = [22530,78818,123848,180135,405285,506603,652950,810556,1125766]

	loopOverNum = len(areaUpperBound)

	for CollectData,OutputLIST in zip(dataList,outputdataList):
		NoCutData = mychecker.cut0(CollectData)
		OutputLIST.append(NoCutData)
		for index in range(loopOverNum):
			LB = areaLowerBound[index]
			UB = areaUpperBound[index]
			ExtractedData = mychecker.cut3("area",LB,UB,CollectData)
			#hard code 5 different bins

			OutputLIST.append(ExtractedData)



	def areaCut_histogram(LB,UB,xtitle,data,nBins, xMin, xMax):
		HistogramTitle = f"{xtitle} with {LB}-{UB} area cut "
		hist = r.TH1D(f"{LB}-{UB} area cut:{xtitle}", "My Histogram", nBins, xMin, xMax+(xMax-xMin)/nBins)
		hist.SetTitle(HistogramTitle)
		hist.GetXaxis().SetTitle(xtitle)
		for d in data:
			hist.Fill(d)
		#hist.Scale(1.0 / hist.GetEntries()) 
		maxBinContent = hist.GetMaximum()
		hist.GetYaxis().SetRangeUser(0, 1.2 * maxBinContent)
		hist.Write()
	
	def NoCut_histogram(xtitle,data,nBins, xMin, xMax):
		HistogramTitle = f"{xtitle} with no area cut"
		hist = r.TH1D(f"no area cut:{xtitle}", "My Histogram", nBins, xMin, xMax+(xMax-xMin)/nBins)
		hist.SetTitle(HistogramTitle)
		hist.GetXaxis().SetTitle(xtitle)
		for d in data:
			hist.Fill(d)
		#hist.Scale(1.0 / hist.GetEntries()) 
		maxBinContent = hist.GetMaximum()
		hist.GetYaxis().SetRangeUser(0, 1.2 * maxBinContent)
		hist.Write()



	
	#ajust the max and min bin number be one in no cut histogram
	minBin = -1
	maxBin = 0
	for index1,subList in enumerate(outputdataList):
		for index2,subData in enumerate(subList):
			if index2 == 0:
				if dataList[index1] == "column" or dataList[index1] == "layer" or dataList[index1] == "board":
					NoCut_histogram(dataList[index1],subData,10, min(subData), max(subData))
				else:
					NoCut_histogram(dataList[index1],subData,100, min(subData), max(subData))
				minBin = min(subData)
				maxBin = max(subData)
			else:	
				if subData == None: continue
				areaLB = areaLowerBound[index2-1]
				areaHB = areaUpperBound[index2-1]
				if subData == []: continue
				if subData == None: continue
				#areaCut_histogram(areaLB,areaHB,dataList[index1],subData,1000, min(subData), max(subData)) #original code.
				if dataList[index1] == "column" or dataList[index1] == "layer" or dataList[index1] == "board":
					areaCut_histogram(areaLB,areaHB,dataList[index1],subData,10, minBin, maxBin)
				else:
					print(dataList[index1])
					print(minBin)
					print(maxBin)
					areaCut_histogram(areaLB,areaHB,dataList[index1],subData,100, minBin, maxBin)
	output_file.Close()
	HistMerge(fileName)
	
	

	"""
	#duration cut
	
	Run_num = 1026

	fileName = f"run{Run_num}_durationcut.root"
	output_file = r.TFile(fileName, "RECREATE")
	mychecker = triggerChecker()
	mychecker.openMergedFile(f"MilliQan_Run{Run_num}","/store/user/milliqan/trees/v33/bar/")
	
	timeList = []
	areaList = []
	typeList = []
	columnList = []
	layerList = []
	heightList = []
	pickupFlagList = []
	boardList = []
	pulseList = []

	dataList = ["time","type","area","column","layer","board","pickupFlag","height","npulses"]
	outputdataList=[timeList,typeList,areaList,columnList,layerList,boardList,pickupFlagList,heightList,pulseList]
	durationLowerBound = [0,192,317,568,745,1072,1223,1349,1425,1601,1879,2104,2331]
	durationUpperBound = [192,317,568,745,1072,1223,1329,1425,1601,1879,2104,2331,2500]
	DataLen=len(durationUpperBound)

	for CollectData,OutputLIST in zip(dataList,outputdataList):
		DataNoCut = mychecker.cut0(CollectData)
		OutputLIST.append(DataNoCut)

		for index in range(DataLen):
			LB = durationLowerBound[index]
			UB = durationUpperBound[index]
			ExtractedData = mychecker.cut3("duration",LB,UB,CollectData)
			OutputLIST.append(ExtractedData)


	#in the future change kev in unit input argument
	def pulse_histogram(LB,UB,xtitle,data,nBins, xMin, xMax):
		HistogramTitle = f"{xtitle} with {LB}-{UB} duration cut "
		hist = r.TH1D(f"{LB}-{UB} duration cut:{xtitle}", "My Histogram", nBins, xMin, xMax+(xMax-xMin)/nBins)
		hist.SetTitle(HistogramTitle)
		hist.GetXaxis().SetTitle(xtitle)
		for d in data:
			hist.Fill(d)
		#hist.Scale(1.0 / hist.GetEntries()) 
		canvas = r.TCanvas("canvas", "Canvas Title", 800, 600)
		hist.Draw()
		hist.Write()
	
	def pulse_histogram_noCuts(xtitle,data,nBins, xMin, xMax):
		HistogramTitleWithOutCut = f"{xtitle} without cut"
		hist0 = r.TH1D(f"data before applying the cut :{xtitle}", "My Histogram", nBins, xMin, xMax+(xMax-xMin)/nBins)
		hist0.SetTitle(HistogramTitleWithOutCut)
		hist0.GetXaxis().SetTitle(xtitle)
		for d in data:
			hist0.Fill(d)
		maxBinContent = hist0.GetMaximum()
		hist0.GetYaxis().SetRangeUser(0, 1.2 * maxBinContent)
		#hist0.Draw()
		hist0.Write()
	
	#ajust the max and min bin number be one in no cut histogram
	minBin = -1
	maxBin = 0
	for index1,subList in enumerate(outputdataList):
		print("index1" + str(type(index1))) #debug
		for index2,subData in enumerate(subList):
			if index2 == 0:
				if subData == None: continue
				if subData == []: continue
				if dataList[index1] == "column" or dataList[index1] == "layer" or dataList[index1] == "board":
					pulse_histogram_noCuts(dataList[index1],subData,10, min(subData), max(subData))
				else:
					pulse_histogram_noCuts(dataList[index1],subData,100, min(subData), max(subData))
				minBin = min(subData)
				maxBin = max(subData)

			else:
				if subData == None: continue
				if subData == []: continue
				DLB = durationLowerBound[index2-1]
				DHB = durationUpperBound[index2-1]
				if dataList[index1] == "column" or dataList[index1] == "layer" or dataList[index1] == "board":
					pulse_histogram_noCuts(dataList[index1],subData,10, min(subData), max(subData))
				else:
					pulse_histogram(DLB,DHB,dataList[index1],subData,100, minBin, maxBin)
	HistMerge(fileName)
	output_file.Close()
	"""
	
	
	
	
	




	

	



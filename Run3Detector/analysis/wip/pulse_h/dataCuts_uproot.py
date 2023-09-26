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
	


	def cut1(self,dataCu,cutValue,dataCo):
		outputList = []
		for specificData in self.myarray[(self.myarray[dataCu] >= cutValue) & (self.myarray["pickupFlag"] == False)][dataCo]:
			outputList.append(specificData)
		return outputList
	
	def cut2(self,dataCu,cutValue,dataCo):
		outputList = []
		for specificData in self.myarray[(self.myarray[dataCu] <= cutValue) & (self.myarray["pickupFlag"] == False)][dataCo]:
			outputList.append(specificData)
		return outputList
	
	def cut3(self,dataCu,cutValue1,cutValue2,dataCo):
		outputList = []
		data=self.myarray
		for specificData in data[(self.myarray[dataCu] <= cutValue2) & (self.myarray[dataCu] >= cutValue1) & (self.myarray["pickupFlag"] == True)][dataCo]:
			outputList.append(specificData)
		return outputList

	#cut4 is made for creating the 2D histogram.
	def cut4(self,dataCu1,cutValue1,cutValue2,datacut2,cutValue3,cutValue4):
		
		data=self.myarray
		#extract an event based data, let's use time
		data1 = data[(self.myarray[dataCu1] <= cutValue2) & (self.myarray[dataCu1] >= cutValue1) & (self.myarray[datacut2] >= cutValue3) & (self.myarray[datacut2] <= cutValue4) & (self.myarray["pickupFlag"] == False)][time]
		
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

	r.gROOT.SetBatch(1)
	

	#height cut
	runList = [1020,1021,1022,1023,1024,1025,1026,1027,1028,1029,1030]
	for Run_num in runList:
		#Run_num = 1026
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
			for i in range(11):
				height_threshold = 100 + i * 100
				#print("CollectData:"+CollectData)
				ExtractedData = mychecker.cut1("height",height_threshold,CollectData)
				OutputLIST.append(ExtractedData)
		
		
		#plot the data with T hisogram
		def height_histogram(height,xtitle,data,nBins, xMin, xMax):
			HistogramTitle = f"{xtitle} with above {height}mV cut "
			hist = r.TH1D(f"above {height}mV data:{xtitle}", "My Histogram", nBins, xMin, xMax)
			hist.SetTitle(HistogramTitle)
			hist.GetXaxis().SetTitle(xtitle)
			for d in data:
				hist.Fill(d)
			#hist.Scale(1.0 / hist.GetEntries()) 
			canvas = r.TCanvas("canvas", "Canvas Title", 800, 600)
			hist.Draw()
			hist.Write()

		fileName = f"run{Run_num}_heightcut.root"
		output_file = r.TFile(fileName, "RECREATE")


		for index1,subList in enumerate(outputdataList):
			for index2,subData in enumerate(subList):
				if subData == None: continue
				height = 100 + index2 * 100
				#print(min(subData))
				#print(max(subData))
				if subData == []: continue
				height_histogram(height,dataList[index1],subData,100, min(subData), max(subData))
		
		output_file.Close()
	
	#end of height cut
	

	"""
	#start the pulse(branch) cut (0-20 with increment value 2)
	Run_num = 1026
	fileName = f"run{Run_num}_pulsecut_pickupFlag.root"
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
		for i in range(11):
			pulse_threshold = 0 + i * 2
			#print("CollectData:"+CollectData)
			ExtractedData = mychecker.cut1("npulses",pulse_threshold,CollectData)
			OutputLIST.append(ExtractedData)

	
	def pulse_histogram(pulse_value,xtitle,data,nBins, xMin, xMax):
		HistogramTitle = f"{xtitle} with {pulse_value} pulses cut "
		hist = r.TH1D(f"{pulse_value}pulses data:{xtitle}", "My Histogram", nBins, xMin, xMax)
		hist.SetTitle(HistogramTitle)
		hist.GetXaxis().SetTitle(xtitle)
		for d in data:
			hist.Fill(d)
		#hist.Scale(1.0 / hist.GetEntries()) 
		canvas = r.TCanvas("canvas", "Canvas Title", 800, 600)
		hist.Draw()
		hist.Write()
	
	for index1,subList in enumerate(outputdataList):
		print("index1" + str(type(index1))) #debug
		for index2,subData in enumerate(subList):
			if subData == None: continue
			pulse_threshold = 0 + index2 * 2
			pulse_histogram(pulse_threshold,dataList[index1],subData,100, min(subData), max(subData))
	output_file.Close()
	#end of pulse analysis
	"""


	"""
	#cut N pulse(not branch) above height->get of events
	for i in range(11):
		height_threshold = 100 + i * 100
		for i in range(11):
			pulse_threshold = 0 + i * 2	
			EventList = mychecker.PHECut(height_threshold,pulse_threshold)
			numberOFevents = len(EventList)
	"""

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
	areaLowerBound = [0,200,1200,3000,5000,7000]
	areaUpperBound = [200,1200,3000,5000,7000,10000]

	for CollectData,OutputLIST in zip(dataList,outputdataList):
		for index in range(6):
			LB = areaLowerBound[index]
			UB = areaUpperBound[index]
			ExtractedData = mychecker.cut3("area",LB,UB,CollectData)
			#hard code 5 different bins

			OutputLIST.append(ExtractedData)


	#in the future change kev in unit input argument
	def pulse_histogram(LB,UB,xtitle,data,nBins, xMin, xMax):
		HistogramTitle = f"{xtitle} with {LB}-{UB} area cut "
		hist = r.TH1D(f"{LB}-{UB} area cut:{xtitle}", "My Histogram", nBins, xMin, xMax)
		hist.SetTitle(HistogramTitle)
		hist.GetXaxis().SetTitle(xtitle)
		for d in data:
			hist.Fill(d)
		#hist.Scale(1.0 / hist.GetEntries()) 
		canvas = r.TCanvas("canvas", "Canvas Title", 800, 600)
		hist.Draw()
		hist.Write()
	
	for index1,subList in enumerate(outputdataList):
		print("index1" + str(type(index1))) #debug
		for index2,subData in enumerate(subList):
			if subData == None: continue
			#height = 100 + index2 * 100
			#print(min(subData))
			#print(max(subData))
			areaLB = areaLowerBound[index2]
			areaHB = areaUpperBound[index2]
			pulse_histogram(areaLB,areaHB,dataList[index1],subData,100, min(subData), max(subData))
	"""	

	"""
	#duration cut
	
	Run_num = 1026

	fileName = f"run{Run_num}_durationcut_pickup.root"
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
	durationLowerBound = [1,131,190,293,600,1000]
	durationUpperBound = [131,190,293,600,1000,1400]

	for CollectData,OutputLIST in zip(dataList,outputdataList):
		for index in range(6):
			LB = durationLowerBound[index]
			UB = durationUpperBound[index]
			ExtractedData = mychecker.cut3("duration",LB,UB,CollectData)
			OutputLIST.append(ExtractedData)


	#in the future change kev in unit input argument
	def pulse_histogram(LB,UB,xtitle,data,nBins, xMin, xMax):
		HistogramTitle = f"{xtitle} with {LB}-{UB} duration cut "
		hist = r.TH1D(f"{LB}-{UB} duration cut:{xtitle}", "My Histogram", nBins, xMin, xMax)
		hist.SetTitle(HistogramTitle)
		hist.GetXaxis().SetTitle(xtitle)
		for d in data:
			hist.Fill(d)
		#hist.Scale(1.0 / hist.GetEntries()) 
		canvas = r.TCanvas("canvas", "Canvas Title", 800, 600)
		hist.Draw()
		hist.Write()
	
	for index1,subList in enumerate(outputdataList):
		print("index1" + str(type(index1))) #debug
		for index2,subData in enumerate(subList):
			if subData == None: continue
			#height = 100 + index2 * 100
			#print(min(subData))
			#print(max(subData))
			DLB = durationLowerBound[index2]
			DHB = durationUpperBound[index2]
			pulse_histogram(DLB,DHB,dataList[index1],subData,100, min(subData), max(subData))
	"""




	

	



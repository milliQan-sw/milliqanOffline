"""
rewrite dataCuts.py into uproot version based on triggerRates.py
remove the display method from triggerRates.py

merge data with Tchain and then load the data with uproot
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

	#check for nHits pulses in window
	#Q: what does (x.unique() < 64) do?
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


	def cut1(self,dataCu,cutValue,dataCo):
		outputList = []
		for specificData in self.myarray[self.myarray[dataCu] >= cutValue][dataCo]:
			outputList.append(specificData)
		return outputList
	
	def cut2(self,dataCu,cutValue,dataCo):
		outputList = []
		for specificData in self.myarray[self.myarray[dataCu] <= cutValue][dataCo]:
			outputList.append(specificData)
		return outputList



if __name__ == "__main__":

	r.gROOT.SetBatch(1)

	Run_num = 1031
	filename = f'/store/user/milliqan/trees/v31/MilliQan_Run{Run_num}.1_v31_firstPedestals.root'
	mychecker = triggerChecker()
	mychecker.openFile(filename)
	#print(mychecker.myarray)
	#print(type(mychecker.myarray))
	# Specify the file path for the text file
	#txt_file_path = 'output_data.txt'

	# Export the DataFrame to a text file
	#mychecker.myarray.to_csv(txt_file_path, index=False, sep='\t') 
	#dataList = ["time","height","area","type","duration"] #feed into cut1/2 dataCo
	dataList = ["time","area","type","duration"]
	timeList = []
	#heightList = []
	areaList = []
	typeList = []
	duration = []
	#outputdataList=[timeList,heightList,areaList,typeList,duration]
	outputdataList=[timeList,areaList,typeList,duration]
	#test for extracting the data
	"""
	areaList1 = []
	areaList1 = mychecker.cut1("height",200,"area",areaList1)
	"""
	#clean the data

	for CollectData,OutputLIST in zip(dataList,outputdataList):
		for i in range(11):
			height_threshold = 100 + i * 100
			#print("CollectData:"+CollectData)
			ExtractedData = mychecker.cut1("height",height_threshold,CollectData)
			OutputLIST.append(ExtractedData)
	
	#debug
	print("len(OutputLIST)" + str(len(outputdataList[0])))
	
	#plot the data with T hisogram
	def height_histogram(height,xtitle,data,nBins, xMin, xMax):
		HistogramTitle = f"{xtitle} with {height}kev cut "
		#hisarea = r.TH1D(f"{height}kev", "My Histogram", nBins, xMin, xMax)
		hist = r.TH1D(f"{height}kev data:{xtitle}", "My Histogram", nBins, xMin, xMax)
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

	#subList
	#subData: is float, it has bug
	for index1,subList in enumerate(outputdataList):
		print("index1" + str(type(index1))) #debug
		for index2,subData in enumerate(subList):
			if subData == None: continue
			height = 100 + index2 * 100
			print(min(subData))
			print(max(subData))
			height_histogram(height,dataList[index1],subData,100, min(subData), max(subData))
	

	



	# clean up the outputdataList

	

	



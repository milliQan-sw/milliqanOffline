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

	#create plots of the online/offline triggers passed
	def plotTriggers(self):
		self.openOutputFile()
		h_triggers = r.TH1F("h_triggers", "Recorded Triggers", 13, 0, 13)
		h_offline = r.TH1F("h_offline", "Offline Triggers Found", 13, 0, 13)
		c1 = r.TCanvas("c1", "c1", 800, 800)

		onlineTrigs = []
		for i in range(13):
			events = np.unique(self.myarray['event'].loc[self.myarray['trig{}'.format(i)] == True].to_numpy())
			onlineTrigs.append(len(events))
			h_triggers.Fill(i, len(events))

		offlineTrigs = np.zeros(13)
		for itrig, trig in enumerate(offlineTrigArray):
			events = np.unique(self.myarray['event'].loc[self.myarray[trig[0]] == True].to_numpy())
			offlineTrigs[trig[1]] = len(events)
			h_offline.Fill(trig[1], len(events))

		print("-----------------------Trigger Counts-------------------------")
		print("{0:<30} {1:>8} {2:>15}".format("Trigger", "Online Triggers", "Offline Triggers"))
		print("{0:<30} {1:>8} {2:>15}".format('Trigger 1: FourLayers:', onlineTrigs[0], offlineTrigs[0]))
		print("{0:<30} {1:>8} {2:>15}".format('Trigger 2: 3InRow', onlineTrigs[1], offlineTrigs[1]))
		print("{0:<30} {1:>8} {2:>15}".format('Trigger 3: separateLayers ', onlineTrigs[2], offlineTrigs[2]))
		print("{0:<30} {1:>8} {2:>15}".format('Trigger 4: adjacentLayers', onlineTrigs[3], offlineTrigs[3]))
		print("{0:<30} {1:>8} {2:>15}".format('Trigger 5: NLayers', onlineTrigs[4], offlineTrigs[4]))
		print("{0:<30} {1:>8} {2:>15}".format('Trigger 6: External', onlineTrigs[5], offlineTrigs[5]))
		print("{0:<30} {1:>8} {2:>15}".format('Trigger 7: NHits', onlineTrigs[6], offlineTrigs[6]))
		print("{0:<30} {1:>8} {2:>15}".format('Trigger 8: Internal', onlineTrigs[7], offlineTrigs[7]))
		print("{0:<30} {1:>8} {2:>15}".format('Trigger 9: TopPanels', onlineTrigs[8], offlineTrigs[8]))
		print("{0:<30} {1:>8} {2:>15}".format('Trigger 10: TopPanelBotBar', onlineTrigs[9], offlineTrigs[9]))
		print("{0:<30} {1:>8} {2:>15}".format('Trigger 11: FrontBackPanel', onlineTrigs[10], offlineTrigs[10]))
		print("{0:<30} {1:>8} {2:>15}".format('Trigger 12: SParticle', onlineTrigs[11], offlineTrigs[11]))
		print("{0:<30} {1:>8} {2:>15}".format('Trigger 13: ZeroBias', onlineTrigs[12], offlineTrigs[12]))
		print("---------------------------------------------------------------")

		c1.cd()
		h_offline.SetLineColor(2)
		h_offline.Draw("hist text")
		h_triggers.Draw("hist text same")
		l1 = r.TLegend(0.6, 0.5, 0.8, 0.6)
		l1.AddEntry(h_offline)
		l1.AddEntry(h_triggers)
		l1.Draw("same")
		self.file_out.cd()
		c1.Write()
		h_offline.Write()
		h_triggers.Write()


if __name__ == "__main__":

	r.gROOT.SetBatch(1)

	filename = '~/scratch0/milliQan/MilliQan_Run1114.1_test.root'

	mychecker = triggerChecker()
	mychecker.openFile(filename)
	mychecker.findTriggersOffline()
	mychecker.getOnlineTriggers()
	mychecker.plotTriggers()




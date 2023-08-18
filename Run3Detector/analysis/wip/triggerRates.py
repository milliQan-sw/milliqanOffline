import numpy as np
import pandas as pd
import ROOT as r
import os 
import sys
import time
import uproot 
from functools import partial
from triggerConstants import *
from pandas.api.indexers import BaseIndexer

class CustomIndexer(BaseIndexer):
    
    def get_window_bounds(self, num_values, min_periods, center, closed):
        
        start = np.arange(num_values, dtype='int64')
        end = np.arange(num_values, dtype='int64')
        endTimes = self.time + self.duration

        for i in range(num_values):
            for j in range(i+1, num_values):
                if self.event[i] != self.event[j]: break
                if (self.time[j] - endTimes[i]) > self.threshold: break
                else: end[i] = j+1

        return start, end 

class triggerChecker():

	def __init__(self):
		self.defineFunctions()
		#self.pedestalCorrections = np.array(pedestalCorrections) #deals with static pedestal corrections from config (not used?)

	def setDynamicPedestals(self):
		self.pedestals = self.tree.arrays(['event', 'chan', 'dynamicPedestal'], library='ak')
		self.corrections = [x.dynamicPedestal[x.chan].to_list() for x in self.pedestals]
		self.corrections = [item for sublist in self.corrections for item in sublist]

	#check for nHits pulses in window
	def checkNPulses(self, x, nHits=4):
		if len((x.unique()<64)) >= nHits: return True
		return False
	
	#check for NLayers hits in window
	def checkNLayers(self, x, nLayers=4):
		#if len(x) < nLayers: return False
		unique = x.unique()
		layers = np.where((unique >= 0) & (unique < 4))
		#print(layers)
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
		#passed = np.array([np.count_nonzero([np.in1d(path, x) for path in line]) >= 3 for line in straightPaths]).any()
		for line in straightPaths:
			hits = []
			for i, path in enumerate(line):
				if np.in1d(path,x).any():
					hits.append(i)
			if len(np.unique(np.array(hits))) >=3: 
				return True
		return False

	#define columns replaced by trigger finding
	def defineTrigCols(self, pedestalCorrection=False):
		if pedestalCorrection: 
			self.setDynamicPedestals()
			self.myarray = self.myarray.assign(pedestalCorrection=lambda x: self.corrections)
			#self.myarray = self.myarray.assign(pedestalCorrection=lambda x: self.pedestalCorrections[x.chan]) #this adds static pedestal correction from config files (not used?)
			self.myarray['correctedHeight'] = np.where((self.myarray['height'] + self.myarray['pedestalCorrection'] >= 15), True, False)
			self.myarray = self.myarray.loc[self.myarray['correctedHeight'] == True]
		self.myarray['fourLayers'] = np.where((self.myarray['type'] == 0), self.myarray['layer'], -1)
		self.myarray['threeInRow'] = self.myarray['chan']
		self.myarray['separateLayers'] = np.where((self.myarray['type'] == 0), self.myarray['layer'], -1)
		self.myarray['adjacentLayers'] = np.where((self.myarray['type'] == 0), self.myarray['layer'], -1)
		self.myarray['nLayers'] = np.where((self.myarray['type'] == 0), self.myarray['layer'], -1)
		self.myarray['nHits'] = np.where((self.myarray['type'] == 0), self.myarray['layer'], -1)
		self.myarray['topPanels'] = self.myarray['chan']
		self.myarray['topBotPanels'] = self.myarray['chan']
		self.myarray['panelsCleaned'] = np.where((self.myarray['height'] >= panelThreshold), self.myarray['chan'], False)
		self.myarray['frontBack'] = self.myarray['panelsCleaned']

	#function to open the input root file
	def openFile(self, dataIn, evtNum=-1, pedestalCorrection=False):
		self.input_file = dataIn
		self.runNum = int(dataIn.split('Run')[-1].split('.')[0])
		self.fileNum = int(dataIn.split('.')[1].split('_')[0])
		self.fin = uproot.open(dataIn)
		self.tree = self.fin['t']
		if evtNum!=-1:
			self.myarray = self.tree.arrays(uprootInputs, library='pd', entry_start=evtNum, entry_stop=evtNum+1)
		else:
                        self.myarray = self.tree.arrays(uprootInputs, library='pd')
		self.defineTrigCols(pedestalCorrection)
		self.setTimes()

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
	def findTriggersOffline(self, trigWindow = 160, debug=False):
		time = self.myarray['time'].to_numpy()
		duration = self.myarray['duration'].to_numpy()
		event = self.myarray['event'].to_numpy()
		indexer = CustomIndexer(time=self.myarray['time'].to_numpy(), duration=self.myarray['duration'].to_numpy(), event=self.myarray['event'].to_numpy(), threshold=trigWindow)
		#use a rolling window to find the triggers that should pass
		if debug:
			self.myarray[offlineTrigNames] = self.myarray.loc[self.myarray['event'] == 0].rolling(window='{}s'.format(trigWindow), on="fake_time", axis=0).agg({"fourLayers": self.this4Layers, "threeInRow": self.checkThreeInRow, "separateLayers": self.checkSeparate, "adjacentLayers": self.checkAdjacent, 'nLayers': self.thisNLayers, 'nHits': self.thisNPulses, 'topPanels': self.checkTopPanels, 'topBotPanels': self.topBotPanels, 'frontBack': self.checkThroughGoing})
		else:
			self.myarray[offlineTrigNames] = self.myarray.rolling(indexer, axis=0).agg({"fourLayers": self.this4Layers, "threeInRow": self.checkThreeInRow, "separateLayers": self.checkSeparate, "adjacentLayers": self.checkAdjacent, 'nLayers': self.thisNLayers, 'nHits': self.thisNPulses, 'topPanels': self.checkTopPanels, 'topBotPanels': self.topBotPanels, 'frontBack': self.checkThroughGoing})

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

		checkTrigger = 0
		onlineCheck = []
		offlineCheck = []
		onlyOnline = []
		onlyOffline = []

		onlineTrigs = []
		for i in range(13):
			events = np.unique(self.myarray['event'].loc[self.myarray['trig{}'.format(i)] == True].to_numpy())
			onlineTrigs.append(len(events))
			h_triggers.Fill(i, len(events))
			onlineCheck.append(events)

		offlineTrigs = np.zeros(13)
		for itrig, trig in enumerate(offlineTrigArray):
			events = np.unique(self.myarray['event'].loc[self.myarray[trig[0]] == True].to_numpy())
			offlineTrigs[trig[1]] = len(events)
			h_offline.Fill(trig[1], len(events))
			offlineCheck.append(events)

			onlyOnline.append([x for x in onlineCheck[itrig] if x not in offlineCheck[itrig]])
			onlyOffline.append([x for x in offlineCheck[itrig] if x not in onlineCheck[itrig]])

			print("Trigger {} non matching events".format(trig[0]))
			print("\tOnline only: ", ''.join(str(onlyOnline[itrig])))
			print("\tOffline only: ", ''.join(str(onlyOffline[itrig])))

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

	#filename = '/home/milliqan/scratch0/processTrees/milliqanOffline/Run3Detector/MilliQan_Run1116.1_matched.root'
	filename = '~/dump/MilliQan_Run1116.1_default_v32.root'


	mychecker = triggerChecker()
	mychecker.openFile(filename, evtNum=-1, pedestalCorrection=True)
	mychecker.findTriggersOffline(trigWindow=160, debug=False)
	mychecker.getOnlineTriggers()
	mychecker.plotTriggers()




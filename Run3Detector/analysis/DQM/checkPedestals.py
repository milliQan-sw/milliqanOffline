import ROOT as r
from ROOT import TH1F
import os
import sys
import numpy as np

def main():

	f_out = r.TFile.Open('hotChannels.root', 'recreate')

	firstRun = 490
	lastRun = 554

	h_hotChannels = []
	
	for ihist in range(80):
		name = 'h_channel' + str(ihist)
		title = 'Events Channel ' + str(ihist) + " is Hot"
		h = TH1F(name, title, lastRun-firstRun+10, firstRun, lastRun+10)
		h_hotChannels.append(h)

	for run in range(firstRun, lastRun):
		#highChannels = checkChannels(run)
		#for hc in highChannels:
		#	h_hotChannels[hc].Fill(run)
		allChannels = checkAllChannels(run)
		for ich, ch in enumerate(allChannels):
			h_hotChannels[ich].Fill(run, ch)	

	
	f_out.cd()
	for hc in h_hotChannels:
		hc.Write()

	f_out.Close()

def checkChannels(runNum):


	percentCut = 0.8

	highChannels = []

	dataDir = '/store/user/mcarrigan/trees/'

	mychain = r.TChain('t')
	
	for filename in os.listdir(dataDir):
		if 'MilliQan_Run'+str(runNum) not in filename: continue
		mychain.Add(dataDir + filename)

	totalEvents = mychain.GetEntries()
	print(totalEvents)

	numHits = np.zeros(80)

	for event in mychain:
		for chan in event.chan:
			numHits[chan] += 1

	print("Run {0} hot channels".format(runNum))
	for ichan, channel in enumerate(numHits):
		#print("Channel {0} number of hits {1}".format(ichan, numHits[ichan]))
		if numHits[ichan] / totalEvents > percentCut:
			print("Channel {0} number of hits {1}, fraction of events {2}".format(ichan, numHits[ichan], numHits[ichan]/totalEvents))
			highChannels.append(ichan)
	print('-----------------------------------------------------------------------------------------------')

	return highChannels
	
def checkAllChannels(runNum):

	channelRates = []

	dataDir = '/store/user/mcarrigan/trees/'

	mychain = r.TChain('t')
	
	for filename in os.listdir(dataDir):
		if 'MilliQan_Run'+str(runNum) not in filename: continue
		mychain.Add(dataDir + filename)

	totalEvents = mychain.GetEntries()
	print(totalEvents)

	numHits = np.zeros(80)

	for event in mychain:
		chanHit = np.zeros(80)
		for chan in event.chan:
			if chanHit[chan]==0:
				numHits[chan] += 1
				chanHit[chan] = 1

	print("Run {0} hot channels".format(runNum))
	for ichan, channel in enumerate(numHits):
		if totalEvents == 0 or numHits[ichan] == 0: channelRates.append(0)
		else:
			channelRates.append(numHits[ichan] / totalEvents)

	return channelRates



if __name__ == "__main__":

	main()

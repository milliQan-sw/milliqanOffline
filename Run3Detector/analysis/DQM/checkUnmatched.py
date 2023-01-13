import ROOT as r
import os
import sys
import numpy as np
from collections import Counter

def main():

	matched = r.TChain("matchedTrigEvents")
	unmatched = r.TChain("unmatchedTriggerBoardEvents")

	matched.Add("/store/user/milliqan/run3/MatchedEvents_Run591.*.root")
	unmatched.Add("/store/user/milliqan/run3/MatchedEvents_Run591*.root")

	fout = r.TFile("checkUnmatched.root", "recreate")

	h_timeDiff = r.TH1F("h_timeDiff", "Difference in Clock Cycles", 6500, 0, 6500)
	h_timeDiffAll = r.TH1F("h_timeDiffAll", "Difference in Clock Cycles", 10000, 0, 50000000)
	#h_timeDiffAll = r.TH1F("h_timeDiffAll", "Difference in Clock Cycles", 1.e4, 0, 5.e7)
	h_indexDiff = r.TH1F("h_indexDiff", "Difference in Trigger Board Event Number", 2000, -1000, 1000)

	#events = unmatched.GetEntries()
	#print(events)

	unmatchedTimes = np.array([])
	unmatchedTBEvents = np.array([])
	unmatchedTrigger = np.array([])

	matchedTBEvents = np.array([])
	matchedDAQEvents = np.array([])

	timeDiff = 44
	closeEvents = 0

	for ievent, event in enumerate(unmatched):
		unmatchedTimes = np.append(unmatchedTimes, [event.clockCycles])
		unmatchedTBEvents = np.append(unmatchedTBEvents, [event.tbEvent])
		unmatchedTrigger = np.append(unmatchedTrigger, [event.trigger])

	print(unmatchedTrigger.shape, unmatchedTBEvents.shape)

	for ievent, event in enumerate(matched):
		#if ievent%1==0: print("Working on event {0}".format(ievent))

		#if event.tbEvent in matchedTBEvents and event.tbEvent != -1: 
		#	index = np.where(matchedTBEvents == event.tbEvent)
		#	print("Trigger Board Event {0} has been matched multiple times, DAQEventNumbers {1}, and {2}".format(event.tbEvent, event.DAQEventNumber, matchedDAQEvents[index][0]))

		matchedTBEvents = np.append(matchedTBEvents, [event.tbEvent])
		matchedDAQEvents = np.append(matchedDAQEvents, [event.DAQEventNumber])

		diff = np.subtract(unmatchedTimes, event.clockCycles)

		diff = np.absolute(diff)
	
		minTime = np.amin(diff)

		index = np.where(diff == minTime)
		unmatchedIndex = unmatchedTBEvents[index][0]
		trigger = unmatchedTrigger[index][0]

		if minTime < timeDiff:
			print("Close times, DAQ event {0}, matched TB event {1} trigger {2}, unmatched TB event {3} trigger {4}, time {5} diff {6}".format(event.DAQEventNumber, event.tbEvent, event.trigger, unmatchedIndex, trigger, event.clockCycles, minTime))
			closeEvents += 1
		h_timeDiff.Fill(minTime)
		h_timeDiffAll.Fill(minTime)
		h_indexDiff.Fill(event.tbEvent-unmatchedIndex)

	print("Number of events within {0}, {1}".format(timeDiff, closeEvents))

	unique = np.unique(matchedTBEvents)
	num_unique = len(unique)
	repeats = [item for item, count in Counter(matchedTBEvents).items() if count > 1]
	print(repeats)
	print("Number of unique trigger board event numbers: {0}, number repeated {1}".format(num_unique, len(matchedTBEvents)-num_unique))

	fout.cd()
	h_timeDiff.Write()
	h_timeDiffAll.Write()
	h_indexDiff.Write()
	fout.Close()

if __name__ == "__main__":

	main()

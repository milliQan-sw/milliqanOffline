#!/usr/bin/env python
import os, sys, re
import ROOT
import glob
import math
from subprocess import call

def main(run,cuts,nevents):

	ROOT.PyConfig.IgnoreCommandLineOptions = True # avoid bizarre crash when constructing TChain
	t = ROOT.TChain("t")
	treeList=glob.glob("/net/cms6/cms6r0/milliqan/milliqanOffline/trees/Run"+run+"*/*.root")
	for f in treeList: 
		t.Add(f)

	t.SetEstimate(nevents) # limit how many events are read to memory
	#use Draw to generate table and store in memory
	# goff = graphics off
	t.Draw("run:file:event",cuts,"goff")
	selected = t.GetSelectedRows() #get how many events were found(can be larger than nevents)
	
	nsel = min(nevents,selected)

	cuts = cuts.replace(">=","ge").replace("<=","le").replace(">","gt").replace("<","lt").replace("==","e")
	cuts = cuts.replace("&&","_").replace("||","_").replace("$","_of").replace("(","_").replace(")","_")
	outFileName = "/net/cms6/cms6r0/milliqan/milliqanOffline/eventLists/eventList_Run%s_n%s_%s.txt" % (run,nevents,cuts)

	outFile = open(outFileName,"w")
	runs=t.GetV1()
	files=t.GetV2()
	events=t.GetV3()
	table = []
	for i in range(nsel):
		table.append([int(runs[i]),int(files[i]),int(events[i])])
		row = "%s %s %s\n" % (str(int(runs[i])),str(int(files[i])),str(int(events[i])))
		outFile.write(row)
	outFile.close()
	print "Wrote list to",outFileName
	return table


if __name__ == "__main__":
	print "This script was called by hand."
	if len(sys.argv)<4:
		print "Usage: ./findEvents.py runNumber selection nEvents"
		print "If you call this script from bash and use the symbol $ in selection, you must use single quotes or backslash to escape."
	else: main(sys.argv[1],sys.argv[2],int(sys.argv[3]))

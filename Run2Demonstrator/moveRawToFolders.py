#!/usr/bin/env python
import os, sys, re
#import ROOT
import glob
import math
from subprocess import call
import shutil
import config as cfg

def main():
	#runList = set(["Run"+"_".join([x.split("Run")[1].split(".")[0],x.split("Run")[1].split("_")[1].split(".root")[0]]) for x in glob.glob("/net/cms6/cms6r0/milliqan/MilliQan_Run*.root")])
	runList = set(["Run"+"_".join([x.split("Run")[1].split(".")[0],x.split("Run")[1].split("_")[1].split(".root")[0]]) for x in glob.glob(cfg.rawDir + "MilliQan_Run*.root")])
	if runList == set():
		print "No need to reorganize raw files."
	else: 
		print "Organizing files for the following runs:"
		print runList
	for i in runList:
	#	MilliQan_Run115.2867_TripleCoincidence.root
		runDir = cfg.rawDir+i
		if not os.path.exists(runDir):
			os.makedirs(runDir)

		runNum= i.split("_")[0]
		#print runNum
		moveList = glob.glob(cfg.rawDir+"MilliQan_"+runNum+".*.root")
		#print moveList
		for m in moveList:
			shutil.move(m,runDir)

if __name__ == "__main__":
	main()
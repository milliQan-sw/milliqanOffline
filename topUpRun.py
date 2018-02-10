#!/usr/bin/env python
import os, sys, re
#import ROOT
import glob
import math
from subprocess import call
import moveRawToFolders
import config as cfg


#### This script will submit jobs to process any raw files that don't have a corresponding tree

def main(arg1):
	run = str(arg1)

	filesPerJob=10.
	rawFileNumList=[ x.split("MilliQan_Run%s."%run)[1].split("_")[0] for x in glob.glob(cfg.rawDir+"Run"+run+"_*/*.root")]
	processedFileNumList=[ x.split("MilliQan_Run%s."%run)[1].split("_")[0] for x in glob.glob(cfg.offlineDir+"trees/Run"+run+"_*/*.root")]
	#glob.glob("/net/cms26/cms26r0/milliqan/UX5/Run"+run+"_*/*.root")
	
	missingFilenumbers= set(rawFileNumList) - set(processedFileNumList)
	
	nFiles=len(missingFilenumbers)

	if nFiles > 0: 
		print "Processing %i missing files from Run %s" % (nFiles,run)
		iFile=0
		nJobs= int(math.ceil(nFiles/filesPerJob))
		rawLocation = glob.glob(cfg.rawDir+"Run"+run+"_*")[0]
		fileList = [glob.glob(rawLocation+"/MilliQan_Run"+run+"."+x+"_*.root")[0] for x in missingFilenumbers]

		#print fileList

		runDir =cfg.offlineDir+"run/Run"+run+"_topUp"
		previousTopUps =[ int(x.split("_topUp")[1]) for x in glob.glob(runDir+"*")]
		if previousTopUps != []:
			thisIteration = max(previousTopUps)+1
		else: thisIteration=1
		runDir = runDir+str(thisIteration)+"/"
		
		if not os.path.exists(runDir):
			os.makedirs(runDir)

		for iJob in range(nJobs):
			scriptName= runDir+"Job"+str(iJob)+".sh"
			script = open(scriptName,"w")
			script.write("#!/bin/bash\n")
			for i in range(15):
				if iFile>=nFiles: break
				script.write("make_tree_v7 "+fileList[iFile]+"\n")
				iFile = iFile+1

			script.close()
			os.chmod(scriptName,0777)
			#print ["JobSubmit.csh","wrapper.sh",scriptName]
			#need full path for cron environment
			call(["/net/cms2/cms2r0/Job/JobSubmit.csh","/homes/milliqan/bin/wrapper.sh",scriptName])



if __name__ == "__main__":
	main(sys.argv[1])



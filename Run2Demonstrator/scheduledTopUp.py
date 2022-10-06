#!/usr/bin/env python
import os, sys, re
#import ROOT
import glob
import math
from subprocess import call
import moveRawToFolders
import config as cfg
import topUpRun

def main():
	
	## Count batch jobs running, waiting, or in queue
	nCurrentBatchJobs = sum(1 for line in open('/net/cms2/cms2r0/milliqan/jobs/running.list')) + sum(1 for line in open('/net/cms2/cms2r0/milliqan/jobs/ready.list')) + sum(1 for line in open('/net/cms2/cms2r0/milliqan/jobs/queued.list'))

	### exit if there are any jobs
	if nCurrentBatchJobs > 0: 
		print "Batch system occupied; try later."
		return

	moveRawToFolders.main()

	runList = [x.split("Run")[1].split("_")[0] for x in glob.glob(cfg.rawDir + "Run*")]
	#print runList
	for run in runList:
		topUpRun.main(run)



if __name__ == "__main__":
	main()
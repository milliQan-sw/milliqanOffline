#!/usr/bin/env python
import os, sys, re
import ROOT
import glob
import math
from subprocess import call
import moveRawToFolders
import config as cfg


#### This script will submit jobs to reprocess a run and overwrite existing files. ####

def main(arg1,arg2=None):
	run = str(arg1)
        if arg2 == None:
            make_tree_script = "simple_macro"
        else:
            make_tree_script = str(arg2)


	moveRawToFolders.main()

	filesPerJob=15.
	fileList=glob.glob(cfg.rawDir+"Run"+run+"_*/*.root")
	nFiles=len(fileList)
	iFile=0
	nJobs= int(math.ceil(nFiles/filesPerJob))
	runDir =cfg.offlineDir+"run/Run"+run
	if not os.path.exists(runDir):
		os.makedirs(runDir)
#	if not os.path.exists("/net/cms26/cms26r0/milliqan/milliqanOffline/run/Run"+run):
#	    os.makedirs("/net/cms26/cms26r0/milliqan/milliqanOffline/run/Run"+run)

	for iJob in range(nJobs):
		scriptName= runDir+"/Job"+str(iJob)+".sh"
		script = open(scriptName,"w")
		script.write("#!/bin/bash\n")
		script.write("cd /home/milliqan/milliqanOffline\n")
		for i in range(15):
			if iFile>=nFiles: break
			#script.write("root -b -q 'make_tree.C+(\""+fileList[iFile]+"\""")'\n")
			script.write(make_tree_script+" "+fileList[iFile]+"\n")
			iFile = iFile+1

		script.close()
		os.chmod(scriptName,0777)
		#print ["JobSubmit.csh","wrapper.sh",scriptName]
		call(["JobSubmit.csh","wrapper.sh",scriptName])



if __name__ == "__main__":
    if len(sys.argv) == 2:
	main(sys.argv[1])
    else:
	main(sys.argv[1],sys.argv[2])



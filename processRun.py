#!/usr/bin/env python
import os, sys, re
import ROOT
import glob
import math
from subprocess import call


def main(arg1):
	run = str(arg1)

	filesPerJob=15.
	fileList=glob.glob("/net/cms26/cms26r0/milliqan/UX5/*"+run+".*.root")
	nFiles=len(fileList)
	iFile=0
	nJobs= int(math.ceil(nFiles/filesPerJob))
	if not os.path.exists("run/Run"+run):
	    os.makedirs("run/Run"+run)

	for iJob in range(nJobs):
		scriptName= "run/Run"+run+"/Job"+str(iJob)+".sh"
		script = open(scriptName,"w")
		script.write("#!/bin/bash\n")
		for i in range(15):
			if iFile>=nFiles: break
			#script.write("root -b -q 'make_tree.C+(\""+fileList[iFile]+"\""")'\n")
			script.write("make_tree "+fileList[iFile]+"\n")
			iFile = iFile+1

		script.close()
		os.chmod(scriptName,0777)
		call(["JobSubmit.csh","./wrapper.sh",scriptName])



if __name__ == "__main__":
	print "This script was called by hand."
	main(sys.argv[1])



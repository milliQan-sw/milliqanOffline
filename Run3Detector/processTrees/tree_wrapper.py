import os
import sys
import subprocess

runNum = -1
fileNum = -1

if len(sys.argv) < 3:
	print("Need to give process number, version, and input data directory")
	sys.exit()

fileList = open("filelist.txt", "r")

info = fileList.readlines()

print("Python trying to run process {0}, file list has {1} entries".format(sys.argv[1], len(info)))

line = info[int(sys.argv[1])]
runNum = str(int(float(line.split()[0])))
fileNum = str(int(float(line.split()[1])))
subName = str(sys.argv[3])

inFile = sys.argv[2] + 'MilliQan_Run{0}.{1}_default.root'.format(runNum,fileNum)
outFile = 'MilliQan_Run{0}.{1}_{2}.root'.format(runNum,fileNum, subName)
triggerFile = sys.argv[2] + "MatchedEvents_Run{0}.{1}.root".format(runNum, fileNum)

print("In tree wrapper calling subprocess")
subprocess.call('source $PWD/setup.sh && python3 $PWD/scripts/runOfflineFactory.py --inputFile {0} --outputFile {1} -m {2} --exe ./run.exe'.format(inFile, outFile, triggerFile), shell=True)
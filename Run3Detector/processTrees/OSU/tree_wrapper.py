import os
import sys
import subprocess
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--process', type=str, default='-1', help='Process number to be run')
    parser.add_argument('-i', '--inputDir', type=str, help='Input data directory', required=True)
    parser.add_argument('-v', '--version', type=str, default='v31_firstPedestals', help='Set the version of offline trees')
    parser.add_argument('-s', '--singleRun', type=str, default='-1', help='Single run number if running only one job')
    args = parser.parse_args()
    return args

def singleJob():
    print("Running single file")
    inFile = args.inputDir + 'MilliQan_Run{0}_default.root'.format(args.singleRun)
    outFile = 'MilliQan_Run{0}_{1}.root'.format(args.singleRun, args.version)
    triggerFile = args.inputDir + 'MatchedEvents_Run{0}.root'.format(args.singleRun)

    print("Input file is {0}\nTrigger File is {1}\nOutput File is {2}".format(inFile, triggerFile, outFile))

    if os.path.exists(triggerFile):
        print("In tree wrapper calling subprocess, with matched trigger file")
        subprocess.call('source $PWD/setup.sh && python3 $PWD/scripts/runOfflineFactory.py --inputFile {0} --outputFile {1} -m {2} --exe ./run.exe --publish'.format(inFile, outFile, triggerFile), shell=True)
    else:
        print("In tree wrapper calling subprocess, no matched trigger file")
        subprocess.call('source $PWD/setup.sh && python3 $PWD/scripts/runOfflineFactory.py --inputFile {0} --outputFile {1} --exe ./run.exe --publish'.format(inFile, outFile), shell=True)

def main():
    runNum = -1
    fileNum = -1

    #if len(sys.argv) < 3:
    #    print("Need to give process number, version, and input data directory")
    #    sys.exit(1)

    if args.process == '-1':
        print("Need to provide process number, exiting")
        sys.exit(1)

    fileList = open("filelist.txt", "r")

    info = fileList.readlines()

    print("Python trying to run process {0}, file list has {1} entries".format(args.process, len(info)))

    line = info[int(args.process)]
    runNum = str(int(float(line.split()[0])))
    fileNum = str(int(float(line.split()[1])))
    subName = str(args.version)

    inFile = args.inputDir + 'MilliQan_Run{0}.{1}_default.root'.format(runNum,fileNum)
    outFile = 'MilliQan_Run{0}.{1}_{2}.root'.format(runNum,fileNum, subName)
    triggerFile = args.inputDir + "MatchedEvents_Run{0}.{1}.root".format(runNum, fileNum)

    print("Input file is {0}\nTrigger File is {1}\nOutput File is {2}".format(inFile, triggerFile, outFile))


    if os.path.exists(triggerFile):
        print("In tree wrapper calling subprocess, with matched trigger file")
        subprocess.call('source $PWD/setup.sh && python3 $PWD/scripts/runOfflineFactory.py --inputFile {0} --outputFile {1} -m {2} --exe ./run.exe --publish'.format(inFile, outFile, triggerFile), shell=True)
    else:
        print("In tree wrapper calling subprocess, no matched trigger file")
        subprocess.call('source $PWD/setup.sh && python3 $PWD/scripts/runOfflineFactory.py --inputFile {0} --outputFile {1} --exe ./run.exe --publish'.format(inFile, outFile), shell=True)

if __name__ == "__main__":

    args = parse_args()

    if args.singleRun != "-1":
        singleJob()
    else:
        main()

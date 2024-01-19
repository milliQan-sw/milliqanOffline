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
    parser.add_argument('--slab', action='store_true', help='Process slab data')
    args = parser.parse_args()
    return args

def singleJob():
    print("Running single file")
    if args.slab:
        inFile = args.inputDir + 'MilliQanSlab_Run{0}_default.root'.format(args.singleRun)
        triggerFile = args.inputDir + 'MatchedEventsSlab_Run{0}_rematch.root'.format(args.singleRun)
        outFile = 'MilliQanSlab_Run{0}_{1}.root'.format(args.singleRun, args.version)
    else: 
        inFile = args.inputDir + 'MilliQan_Run{0}_default.root'.format(args.singleRun)
        triggerFile = args.inputDir + 'MatchedEvents_Run{0}_rematch.root'.format(args.singleRun)
        outFile = 'MilliQan_Run{0}_{1}.root'.format(args.singleRun, args.version)

    print("Input file is {0}\nTrigger File is {1}\nOutput File is {2}".format(inFile, triggerFile, outFile))

    cmd = 'source $PWD/setup.sh && python3 $PWD/scripts/runOfflineFactory.py --inputFile {0} --outputFile {1} --exe ./run.exe --publish'.format(inFile, outFile)

    if os.path.exists(triggerFile):
        cmd = '{0} -m {1}'.format(cmd, triggerFile)
    else:
        print("Trigger file {} does not exist".format(triggerFile))

    if args.slab:
        print("Processing slab detector data")
        cmd = '{0} --slab'.format(cmd)

    subprocess.call(cmd, shell=True)

    '''if os.path.exists(triggerFile):
        print("In tree wrapper calling subprocess, with matched trigger file")
        subprocess.call('source $PWD/setup.sh && python3 $PWD/scripts/runOfflineFactory.py --inputFile {0} --outputFile {1} -m {2} --exe ./run.exe --publish'.format(inFile, outFile, triggerFile), shell=True)
    else:
        print("In tree wrapper calling subprocess, no matched trigger file")
        subprocess.call('source $PWD/setup.sh && python3 $PWD/scripts/runOfflineFactory.py --inputFile {0} --outputFile {1} --exe ./run.exe --publish'.format(inFile, outFile), shell=True)'''

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

    if args.slab:
        inFile = args.inputDir + 'MilliQanSlab_Run{0}.{1}_default.root'.format(runNum,fileNum)
        outFile = 'MilliQanSlab_Run{0}.{1}_{2}.root'.format(runNum,fileNum, subName)
        triggerFile = args.inputDir + "MatchedEventsSlab_Run{0}.{1}_rematch.root".format(runNum, fileNum)
    else:
        inFile = args.inputDir + 'MilliQan_Run{0}.{1}_default.root'.format(runNum,fileNum)
        outFile = 'MilliQan_Run{0}.{1}_{2}.root'.format(runNum,fileNum, subName)
        triggerFile = args.inputDir + "MatchedEvents_Run{0}.{1}_rematch.root".format(runNum, fileNum)

    print("Input file is {0}\nTrigger File is {1}\nOutput File is {2}".format(inFile, triggerFile, outFile))

    cmd = 'source $PWD/setup.sh && python3 $PWD/scripts/runOfflineFactory.py --inputFile {0} --outputFile {1} --exe ./run.exe --publish'.format(inFile, outFile)

    if os.path.exists(triggerFile):
        cmd = '{0} -m {1}'.format(cmd, triggerFile)
    else:
        print("Trigger file {} does not exist".format(triggerFile))

    if args.slab:
        print("Processing slab detector data")
        cmd = '{0} --slab'.format(cmd)

    subprocess.call(cmd, shell=True)

    '''if os.path.exists(triggerFile):
        print("In tree wrapper calling subprocess, with matched trigger file")
        subprocess.call('source $PWD/setup.sh && python3 $PWD/scripts/runOfflineFactory.py --inputFile {0} --outputFile {1} -m {2} --exe ./run.exe --publish'.format(inFile, outFile, triggerFile), shell=True)
    else:
        print("In tree wrapper calling subprocess, no matched trigger file")
        subprocess.call('source $PWD/setup.sh && python3 $PWD/scripts/runOfflineFactory.py --inputFile {0} --outputFile {1} --exe ./run.exe --publish'.format(inFile, outFile), shell=True)'''

if __name__ == "__main__":

    args = parse_args()

    if args.singleRun != "-1":
        singleJob()
    else:
        main()

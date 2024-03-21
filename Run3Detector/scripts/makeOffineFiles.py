import time
import os
import sys

def getFileInfo(filename):
    runNum = int(filename.split('.')[0].split('Run')[-1])
    fileNum = int(filename.split('.')[1].split('_')[0])
    return runNum, fileNum

def triggerFileExists(dataDir, runNum, fileNum):
    trigFile = "{0}TriggerBoard_Run{1}.{2}.root".format(dataDir, runNum, fileNum)
    return os.path.exists(trigFile)

def matchFiles(dataDir, runNum):
    workDir = '/home/milliqan/MilliDAQ/'
    cmd = "python3 /home/milliqan/Run3/MilliDAQ/test/runCombineFiles.py -r {0} -d {1} -w {2} --standalone".format(runNum, dataDir, workDir)
    os.system(cmd)
    cmd = "mv {0}/MatchedEvents*.root {1}".format(workDir, dataDir)
    os.system(cmd)

def processFile(inputFile, outputFile, matchedFile):
    if matchedFile != "":
        cmd = "python3 scripts/runOfflineFactory.py --inputFile {0} --outputFile {1} -m {2} --exe ./run.exe".format(inputFile, outputFile, matchedFile)
    else:
        cmd = "python3 scripts/runOfflineFactory.py --inputFile {0} --outputFile {1} --exe ./run.exe".format(inputFile, outputFile)
    os.system(cmd)

def checkRunning():
    fin = open('/home/milliqan/log/processingFiles.log', 'r+')
    #fin.seek(0)
    running = fin.readlines()[0]
    print(running)
    if '1' in running:
        print("Already processing files, exiting...")
        fin.close()
        sys.exit(0)
    if '0' in running:
        fin.truncate(0)
        fin.write('1')
        fin.close()
        print("Processing files...")

if __name__ == "__main__":

    checkRunning()
    dataDir = '/home/milliqan/run3Data/'
    outputDir = '/home/milliqan/offlineFiles/'
    for filename in os.listdir(dataDir):
        if not filename.startswith('MilliQan'): continue
        runNum, fileNum = getFileInfo(filename)
        if runNum < 1041: continue #temporary for now to not take up too much disk
        outputFileName = "{0}MilliQan_Run{1}.{2}_v32.root".format(outputDir, runNum, fileNum)
        if os.path.exists(outputFileName): continue
        triggerFile = "{0}TriggerBoard_Run{1}.{2}.root".format(dataDir, runNum, fileNum)
        matchedFile = "{0}MatchedEvents_Run{1}.{2}.root".format(dataDir, runNum, fileNum)
        if os.path.exists(triggerFile) and not os.path.exists(matchedFile):
            matchFiles(dataDir, runNum)
        if not os.path.exists(matchedFile): matchedFile = ""
        processFile(dataDir+filename, outputFileName, matchedFile)
        break
    fin = open('/home/milliqan/log/processingFiles.log', 'w')
    fin.truncate()
    fin.write('0')


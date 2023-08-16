import os
import ROOT as r



def getRunFile(filename):
    runNum = filename.split('Run')[-1].split('.')[0]
    fileNum = filename.split('.')[1].split('_')[0]
    return runNum, fileNum

def printFileCounts():
    fout = open('fileCounts.csv', 'w')
    print("{0:<10} {1:>8} {2:>8} {3:>8}".format('Run Number', 'DAQ Files', 'Trigger Files', 'Matched Files'))
    for key, value in daqFiles.items():
        numDAQ = len(daqFiles[key])
        numTrig = 0
        numMatched = 0
        missing = ''
        if key in trigFiles.keys(): numTrig = len(trigFiles[key])
        if key in matchedFiles.keys(): numMatched = len(matchedFiles[key])
        if numDAQ != numMatched: missing = 'x'
        print("{0:<10} {1:>8} {2:>8} {3:>8} {4:>8}".format(key, numDAQ, numTrig, numMatched, missing))
        fout.write('{0},{1},{2},{3},{4}\n'.format(key, numDAQ, numTrig, numMatched, missing))
    fout.close()



if __name__ == "__main__":

    path = '/store/user/milliqan/run3/'
    directories = ['1000']
    subdirectories = ['0000', '0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009']

    daqFiles = {}
    trigFiles = {}
    matchedFiles = {}

    for directory in directories:
        for sub in subdirectories:
            fullPath = path+directory+'/'+sub
            for filename in os.listdir(fullPath):
                if not filename.endswith('.root'): continue
                if filename.startswith('MilliQan'):
                    runNum, fileNum = getRunFile(filename)
                    if runNum in daqFiles:
                        daqFiles[runNum].append(fileNum)
                    else:
                        daqFiles[runNum] = [fileNum]
                elif filename.startswith('TriggerBoard'):
                    runNum, fileNum = getRunFile(filename)
                    if runNum in trigFiles:
                        trigFiles[runNum].append(fileNum)
                    else:
                        trigFiles[runNum] = [fileNum]
                elif filename.startswith('MatchedEvents'):
                    if not 'rematch' in filename: continue
                    runNum, fileNum = getRunFile(filename)
                    if runNum in matchedFiles:
                        matchedFiles[runNum].append(fileNum)
                    else:
                        matchedFiles[runNum] = [fileNum]
                 

    
    printFileCounts()

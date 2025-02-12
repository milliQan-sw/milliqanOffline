import os
import sys

def getFileList(runs, dataDir='/eos/experiment/milliqan/trees/v35/1900/'):

    fileList = []
    for run in runs:
        
        for file in os.listdir(dataDir):

            runNum = int(file.split('_')[1].split('.')[0].replace('Run', ''))
            if runNum != run: continue

            fileList.append('/'.join([dataDir, file]))

    return fileList
        


if __name__ == "__main__":

    hvRuns = {1450:[1966], 1400:[1967], 1350:[1968], 1300:[1969], 1250:[1970], 900:[1971], 
            850:[1972], 800:[1973], 750:[1974], 700:[1975, 1980], 650:[1982, 1983, 1984, 1985], 
            600:[1986, 1987], 550:[1988, 1989], 500:[1990]}

    for irun, (hv, runs) in enumerate(hvRuns.items()):

        #if irun > 0: break
        if hv != 900: continue
            
        files = getFileList(runs)
        print(hv, runs, files)


        beam = False
        skim = True
        sim = False
        outputFile = f'backgroundPanelAnalysis_HV{hv}_v4.root'
        qualityLevel = 'override'
        fileList = ','.join(files)
        maxEvents = None

        cmdString = f'python3 backgroundPanelAnalysis.py {beam} {skim} {sim} {outputFile} {qualityLevel} {fileList} {maxEvents}'
        
        os.system(cmdString)
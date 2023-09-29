import ROOT as r
import os
import argparse
import sys
import math
from IPython import display

class quickPlot():
    
    def __init__(self):

        self.checkRunDir()

        self.args = self.parse_args()
        '''if len(self.args) > 1:
            if not self.args.events:
                print("Need to give event numbers to plot")
                sys.exit(1)
            if not self.args.fileName and (not self.args.run or not self.args.fileNumber):
                print("Need to give either a run and file number or a filename as input")
                sys.exit(1)
        '''    
        self.offlineDir = '/share/scratch0/mcarrigan/milliQan/processTrees/milliqanOffline/Run3Detector/'
        self.dataDir = '/store/user/milliqan/run3/1100/0001/'
        self.fileName = ''
        self.fileNum = -1
        self.runNum = -1
        self.events = -1

        if self.args.fileName: self.fileName = self.args.fileName
        if self.args.run: self.runNum = self.args.runNum
        if self.args.fileNumber: self.fileNum = self.args.fileNum
        if self.args.events: self.events = self.args.events

        print(self.args.run, self.args.fileNumber, self.args.fileName)
        if (self.args.run and self.args.fileNumber):
            self.parseInputFile()
            self.callSingularity()
            self.copyDisplays()
        #self.loadFile()
        #self.plotEvents()
        #r.gSystem.Load('~/scratch0/milliQan/processTrees/MilliDAQ/libMilliDAQ.so')
    
    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-r', '--run', default=None, type=int, help='run number of input file')
        parser.add_argument('-n', '--fileNumber', default=None, type=int, help='file number of input file')
        parser.add_argument('-f', '--fileName', default='', type=str, help='input file name')
        parser.add_argument('-e', '--events', default=None, nargs='+', type=str, help='events to plot')
        args = parser.parse_args()
        return args

    def checkRunDir(self):
        if not os.getcwd().startswith('/share/scratch0'):
            print("Need to be in scratch0 directory to run this command")
            sys.exit()
    
    def parseInputFile(self):
        if self.runNum and self.fileNum:
            #self.runNum = self.args.run
            #self.fileNum = self.args.fileNumber
            self.fileName = '{0}MilliQan_Run{1}.{2}_default.root'.format(self.dataDir, str(self.runNum), str(self.fileNum))
        elif self.fileName:
            #self.fileName = self.args.fileName
            self.runNum = int(self.fileName.split('Run')[-1].split('.')[0])
            self.fileNum = int(self.fileName.split('.')[1].split('_')[0])
        else:
            print("Need to provide either the run and file number or the file name")
            sys.exit(1)
        #self.dataDir += math.floor(self.runNum)
        print("Input file:", self.fileName)
            
    def callSingularity(self):
        bindDirs = '/store/user/milliqan/,/share/scratch0/mcarrigan/milliQan/processTrees/milliqanOffline'
        sif = '/share/scratch0/mcarrigan/milliQan/processTrees/offline.sif'
        outputFile = os.getcwd() + '/test.root'
        exe = './run.exe'
        home = self.offlineDir+':/home'
        if isinstance(self.events, list): 
            commands = 'singularity/makeDisplays.sh {0} {1} {2} {3}'.format(self.fileName, outputFile, exe, ' '.join(self.events))
        else:
            commands = 'singularity/makeDisplays.sh {0} {1} {2} {3}'.format(self.fileName, outputFile, exe, self.events)
        print(commands)
        cmd = 'singularity exec --home {0} -B {1} {2} {3}'.format(home, bindDirs, sif, commands)
        os.system(cmd)
        
    def copyDisplays(self):
        displayDir = self.offlineDir + '/displays/Run' + str(self.runNum) + '/'
        os.system('cp -r {0} {1}'.format(displayDir, os.getcwd()))

    def showPlots(self, plotName):
        display.Image(plotName)        
            
if __name__ == "__main__":
        
    quickPlot()

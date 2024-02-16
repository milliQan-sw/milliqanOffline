import os
import sys


from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *






#------------------------------------------customized function--------------------------------------
#plotting function for makind N-bars got hits when it pass four layer cut

nbars=r.TH1F("nbars","nbars;number of bars",32,0,32)
#based on previous study nPE collected from cosmic muon hitting  on bar can reach up 30k(cosmic muon travel staight through) - 2.5k(
#cosmic travel transvererly through the bar).   
WideNPEh = r.TH1F("bar NPE","bar NPE histogram;bar NPE; events",25000,0,50000)
NPERatio = r.TH1F("bar NPE ratio", "bar NPE ratio;max bar Npe / min bar Npe;events",40,0,200) 
pulseNpeh = r.TH1F("pulse NPE","pulse NPE histogram;pulse NPE; events",25000,0,50000)
CorrectedTimeDist = r.TH1F("D T max", "D T max;dT max;events",40,-30,50)

#unfinished
def CorrectTimeDt(TimeArray,layerArray):
    arraylen = len(TimeArray)
    for index in range(arraylen):
        n = 80
        #find the time for the first hit of each channel 
        timeDict = {}
        for time,chan in zip(TimeArray[index],ChanArray[index]):
            if chan in timeDict:
                pass

            else:
                timeDict[chan] =[time]    
        
def remove_non_zero(lst):
    return [x for x in lst if x > 0]


#function for making the plot
def NHitsPlot(events):
    #print(ak.to_pandas(events))
    #events = events[events.fourLayerCut]
    if len(events) == 0:return  #quit if the current file is empty
    ChanArray = (ak.to_list(events.chan))
    NpeArray = (ak.to_list(events.nPE))
    #TimeArray = (ak.to_list(events.timeFit_module_calibrated))
    #layerArray = (ak.to_list(events.layer))
    n = 80  # Number of zeros you want
    #print(ChanArray)
    #print(NpeArray)
    arraylen = len(ChanArray)
    #print(arraylen)
    for index in range(arraylen):
        Npe_list = [0] * n
        for nPE, chan in zip(NpeArray[index],ChanArray[index]):
            Npe_list[chan] += nPE
        #print(Npe_list)    
        #NonezeroNpelist = remove_non_zero(Npe_list)
        #maxNPE = max(NonezeroNpelist)
        #minNPE = min(NonezeroNpelist)  #FIXME: I want the non-zero minimum. I need to fix it.
        #print(minNPE)
        #print(Npe_list)
        #if minNPE > 0:
        #    NPERatio.Fill(maxNPE/minNPE)
        for npe in Npe_list:
            if npe > 0:
                WideNPEh.Fill(npe)

    uniqueBarsCount = [len(set(inner_list)) for inner_list in ChanArray]
    #print(uniqueBarsCount)
    for count in uniqueBarsCount:
        nbars.Fill(count)
    #nbars.FillN(len(uniqueBarsCount), uniqueBarsCount, np.ones(len(uniqueBarsCount)))
    #FIXME: FillN has weird bug
    


#extra function for trim down the size of event
def NPEtrim(self,cutName=None, NPEcut = 1):
    for branch in branches:
        if branch == 'boardsMatched': continue
        self.events[branch] = self.events[branch][self.events['nPE']>=NPEcut]
    


def bartrim(self,cutName=None):
    for branch in branches:
        if branch == 'boardsMatched': continue
        self.events[branch] = self.events[branch][self.events['type']==0]
    

mycuts = milliqanCuts()

setattr(milliqanCuts, 'bartrim', bartrim)

setattr(milliqanCuts, 'NPEtrim', NPEtrim)



#------------------------------------------start of main function----------------------------------------------------------

#filelist =['/mnt/hadoop/se/store/user/milliqan/trees/v34/MilliQan_Run1190.4_v34.root:t']

#"""
filelist = []

def appendRun(filelist,run):
    #directory = "/mnt/hadoop/se/store/user/milliqan/trees/v34/1000/"
    directory = "/mnt/hadoop/se/store/user/milliqan/trees/v34/1100/"
    for filename in os.listdir(directory):
        if filename.startswith(f"MilliQan_Run{run}") and filename.endswith(".root"):
            filelist.append(directory+filename+":t")
cosmicGoodRun = [1163]


for run in cosmicGoodRun:
    appendRun(filelist,run)
#"""

branches = ['boardsMatched', 'nPE', 'layer','type','chan','pickupFlag','timeFit_module_calibrated']


pickupCut = mycuts.getCut(mycuts.pickupCut, 'pickupCut', cut=True, branches=branches)


boardMatchCut = mycuts.getCut(mycuts.boardsMatched, 'boardMatchCut', cut=True, branches=branches)




#cutflow = [boardMatchCut,pickupCut,mycuts.bartrim,mycuts.fourLayerCut]
cutflow = [boardMatchCut,pickupCut,mycuts.bartrim]
#cutflow = [boardMatchCut,pickupCut,mycuts.fourLayerCut,mycuts.bartrim]
#cutflow = [boardMatchCut,pickupCut,mycuts.bartrim]

myschedule = milliQanScheduler(cutflow, mycuts)


myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts)

myiterator.setCustomFunction(NHitsPlot)

myiterator.run()


output_file = r.TFile("test1163.root", "RECREATE")
nbars.Write()
WideNPEh.Write()
NPERatio.Write()
output_file.Close()

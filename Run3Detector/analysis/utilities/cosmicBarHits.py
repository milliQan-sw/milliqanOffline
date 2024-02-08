import os
import sys


from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *






#------------------------------------------customized function--------------------------------------
#plotting function for makind N-bars got hits when it pass four layer cut

#nbars=r.TH1("nbars","nbars",32,0,32)

#function for making the plot
def NHitsPlot(events):
    print(ak.to_pandas(events))
    events = events[events.fourLayerCut]
    if len(events) == 0:return
    ChanArray = (ak.to_list(events.chan))
    uniqueBarsCount = [len(set(inner_list)) for inner_list in ChanArray]
    print(uniqueBarsCount)
    #unfinished


#extra function for trim down the size of event
def NPEtrim(self,cutName=None, NPEcut = 1):
    slimmedEvents = self.events[self.events['nPE']>=NPEcut]
    return slimmedEvents


def bartrim(self,cutName=None):
    slimmedEvents = self.events[self.events['type']==0]
    return slimmedEvents

mycuts = milliqanCuts()

setattr(milliqanCuts, 'bartrim', bartrim)

setattr(milliqanCuts, 'NPEtrim', NPEtrim)



#------------------------------------------start of main function----------------------------------------------------------

filelist =['/mnt/hadoop/se/store/user/milliqan/trees/v34/MilliQan_Run1190.155_v34.root:t']

"""
filelist = []

def appendRun(filelist,run):
    #directory = "/mnt/hadoop/se/store/user/milliqan/trees/v34/1000/"
    directory = "/mnt/hadoop/se/store/user/milliqan/trees/v34/"
    for filename in os.listdir(directory):
        if filename.startswith(f"MilliQan_Run{run}") and filename.endswith(".root"):
            filelist.append(directory+filename+":t")
cosmicGoodRun = [1190]


for run in cosmicGoodRun:
    appendRun(filelist,run)
"""

branches = ['boardsMatched', 'nPE', 'layer','type','chan','pickupFlag']


pickupCut = mycuts.getCut(mycuts.pickupCut, 'pickupCut', cut=True, branches=branches)


boardMatchCut = mycuts.getCut(mycuts.boardsMatched, 'boardMatchCut', cut=True, branches=branches)




cutflow = [boardMatchCut,pickupCut,mycuts.bartrim,mycuts.NPEtrim,mycuts.fourLayerCut]


myschedule = milliQanScheduler(cutflow, mycuts)


myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts)

myiterator.setCustomFunction(NHitsPlot)

myiterator.run()

import os
import sys

sys.path.append("/share/scratch0/czheng/MyMilliqnofflineWorking/milliqanOffline/Run3Detector/analysis/utilities")

from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *

filelist =['/mnt/hadoop/se/store/user/milliqan/trees/v34/1100/MilliQan_Run1190.155_v34.root:t']

branches = ['nPE','layer','type','chan']

mycuts = milliqanCuts()

def OLDoneHitPerLayerCut(self, cutName=None, cut=False):
    self.events['oneHitPerLayerCut'] =((ak.count(self.events.layer==0, axis=1)==1) & 
                                        (ak.count(self.events.layer==1, axis=1)==1) & 
                                        (ak.count(self.events.layer==2, axis=1)==1) &
                                        (ak.count(self.events.layer==3, axis=1)==1))


def barTrim(self, cutName=None):
    self.events = self.events[self.events['type'] == 0]


def printEvents(self,cutName=None):
    print(ak.to_pandas(self.events))
    print(ak.to_pandas(self.events[self.events.oneHitPerLayerCut]))
    
def evensizeTrim(self,cutName=None):
    sizeCuts=(ak.count(self.events.layer==0, axis=1)==1) #extract the events that only has 1 pulse
    self.events = self.events[sizeCuts]

setattr(milliqanCuts, 'evensizeTrim',evensizeTrim)

setattr(milliqanCuts, 'barTrim', barTrim)

setattr(milliqanCuts, 'OLDoneHitPerLayerCut', OLDoneHitPerLayerCut)

setattr(milliqanCuts, 'printEvents', printEvents)

#cutflow that create the mask for the old one 1 hit per layer cut

#cutflow = [mycuts.barTrim,mycuts.evensizeTrim,mycuts.OLDoneHitPerLayerCut,mycuts.printEvents]

#cutflow that create the mask for the new one 1 hit per layer cut
cutflow = [mycuts.barTrim,mycuts.fourLayerCut,mycuts.oneHitPerLayerCut,mycuts.printEvents]

myschedule = milliQanScheduler(cutflow, mycuts)


myschedule.printSchedule()

myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts)

myiterator.run()

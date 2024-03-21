import os
import sys

sys.path.append("/share/scratch0/czheng/MyMilliqnofflineWorking/milliqanOffline/Run3Detector/analysis/utilities")

from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *

filelist =['/mnt/hadoop/se/store/user/milliqan/trees/v34/MilliQan_Run1190.155_v34.root:t']

branches = ['height']

mycuts = milliqanCuts()



heightCut = mycuts.getCut(mycuts.heightCut, 'heightCut', cut=36)

eventCuts = mycuts.getCut(mycuts.combineCuts, 'eventCuts', ['heightCut'])




cutflow = [heightCut,eventCuts]

myschedule = milliQanScheduler(cutflow, mycuts)


myschedule.printSchedule()


#in the demo mycuts, myplotter arguements are useless now
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts)

myiterator.run()
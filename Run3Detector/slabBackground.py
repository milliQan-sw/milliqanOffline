import os
import sys

sys.path.append(os.getcwd() + '/analysis/utilities/')

from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *

filelist = ['output_97.root:t','output_98.root:t','output_99.root:t']
branches = ['event','column','row','layer','time','nPE']

mycuts = milliqanCuts()


neverCut = mycuts.getCut(mycuts.neverCut, 'neverCut', cut=True)

fourLayerCut = mycuts.getCut(mycuts.fourLayerCut, 'fourLayerCut', cut=True)
oneHitPerLayerCut = mycuts.getCut(mycuts.oneHitPerLayerCut, 'oneHitPerLayerCut', cut=True)
muonCut = mycuts.getCut(mycuts.muonCut, 'muonCut', cut=True)
#straightLineCut = mycuts.getCut(mycuts.straightLineCut, allowedMove=False)
nPERatioCut = mycuts.getCut(mycuts.nPERatioCut, 'nPERatioCut', cut=True)

getMaxHitTimeDiff = mycuts.getCut(mycuts.getMaxHitTimeDiff, 'getMaxHitTimeDiff')
smallTimeDiffCut = mycuts.getCut(mycuts.smallTimeDiffCut, 'smallTimeDiffCut', cut=True)
largeTimeDiffCut = mycuts.getCut(mycuts.largeTimeDiffCut, 'largeTimeDiffCut', cut=True)

myplotter = milliqanPlotter()

cutflow = [neverCut, muonCut, nPERatioCut, getMaxHitTimeDiff, smallTimeDiffCut, mycuts.getCutflowCounts]
#cutflow = [neverCut, fourLayerCut, oneHitPerLayerCut, muonCut, getMaxHitTimeDiff, mycuts.getCutflowCounts]
#cutflow = [neverCut, fourLayerCut, oneHitPerLayerCut, muonCut, nPERatioCut, mycuts.getCutflowCounts]
#cutflow = [fourLayerCut, oneHitPerLayerCut, muonCut, straightLineCut, mycuts.getCutflowCounts]

myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

myschedule.printSchedule()

myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter, 100)

myiterator.run()


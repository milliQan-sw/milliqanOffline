import ROOT as r
from collections import defaultdict

r.gROOT.SetBatch(True)
r.PyConfig.IgnoreCommandLineOptions = True
from collections import OrderedDict as odict

typeOrder = ["ET", "R7725", "R878"]

runToHV = odict()
runToHV[27] = (1400,1400,1250)
runToHV[28] = (1400,1450,1300)
runToHV[29] = (1500,1500,1350)
runToHV[30] = (1500,1550,1400)
runToHV[31] = (1300, 1300, 1150)
runToHV[32] = ( 1200, 1250, 1100)
runToHV[33] = ( 1200, 1200, 1050)
runToHV[34] = ( 1100, 1150, 1000)
runToHV[35] = ( 1100, 1100, 950 )
runToHV[36] = ( 1000, 1050, 900 )
runToHV[37] = ( 1000,1000, 850  )
runToHV[38] = ( 900,950, 800    )
runToHV[39] = ( 900,900, 750    )
runToHV[40] = ( 800,850,700     )
runToHV[41] = ( 800,800,650     )
runToHV[42] = ( 700, 700, 600   )
runToHV[43] = ( 600, 600, 550   )
runToHV[44] = ( 1700, 1700, 1500)
runToHV[45] = ( 1700, 1650, 1475)
runToHV[46] = ( 1600, 1600, 1450)
typeDict = {}
for iTyp,typ in enumerate(typeOrder):
    HVToRun = defaultdict(list)
    for run in runToHV:
        HVToRun[runToHV[run][iTyp]].append(run)
    typeDict[typ] = HVToRun

channelDict = {}
channelDict["ET"] = [0,1,2,3,7]
channelDict["R878"] = [4,5,6,12,13,14,15]
channelDict["R7725"] = [8,9,10,11]

channelToHVToRun = {}
for typ,channelList in channelDict.iteritems():
    #unique so ok
    for channel in channelList:
        channelToHVToRun[channel] = typeDict[typ]
print channelToHVToRun[0]

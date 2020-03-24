import pandas as pd
import math
import os
import importlib.util
import json




parentDir = "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[:-1]) 
spec = importlib.util.spec_from_file_location("config", parentDir+"/config.py")
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

tag =config.tag

oneBin = False

def makeCardOneChannel(bkg,sig,label):
    cardString = """imax *
jmax *
kmax * 
--------------------
shapes * {2} FAKE
--------------------
bin {2}
observation {0}
--------------------
bin {2} {2}
process	sig bkg
process	    0 1 
rate	{1} {0} 
--------------------

sigSyst lnN 1.1 - 
bkgSyst lnN - 1.1 """.format(bkg,sig,label)
    return(cardString)

def makeCard(paths,labelDict,bkg,sig):
    rate = ""
    obs = ""
    labels = ""
    binLabels = ""
    for path in paths:
        obs += "%.0f"%(bkg[path])+" "
        rate += "%.2f"%sig[path]+" "+"%.2f"%bkg[path]+" "
        labels += labelDict[path]+" "
        binLabels += labelDict[path]+" "+labelDict[path]+" "
    cardString = """imax *
jmax *
kmax * 
--------------------
shapes * * FAKE
--------------------
bin {0}
observation {1}
--------------------
bin {2}
process	{3}
process	    {4}
rate	{5}
--------------------

""".format(labels,obs,binLabels,"sig bkg "*len(paths),"0 1 "*len(paths),rate)
    return(cardString)

def addGammaLines(paths,bkg,sig):
    gammaLines = ""
    for iP,path in enumerate(paths):
        weightLine = ["-"]*len(paths)*2
        weightLine[iP*2+1] = "%.4f" % (bkg[path]/bkg[path+"Gamma"])
        line = "predUnc_"+path+" gmN %.0f "%(bkg[path+"Gamma"])+" ".join(weightLine)
        gammaLines += line +"\n"

        if (sig[path+"Gamma"] == 0):
            continue
        weightLine = ["-"]*len(paths)*2
        weightLine[iP*2] = "%.4f" % (sig[path]/sig[path+"Gamma"])
        line = "predUncSig_"+path+" gmN %.0f "%(sig[path+"Gamma"])+" ".join(weightLine)
        gammaLines += line +"\n"

    return gammaLines
def addSystematicsLines(paths,systematicsPerModel):
    systLines = ""
    for syst in systematicsPerModel:
        systLineTemp = systematicsPerModel[syst]
        if len(systLineTemp) == 2:
            if (abs(systLineTemp[0]) < 0.01 and abs(systLineTemp[1]) < 0.01): continue
            systLine = syst+" lnN "+("{1}/{0} - ".format("%.2f" % (1+systLineTemp[0]),"%.2f" % (1+systLineTemp[1])))*len(paths)
        else:
            if len(systLineTemp) != len(paths):
                raise "Don't know what to do with syst: {0}!".format(syst)
            systLine = syst+" lnN "
            for systInBin in systLineTemp:
                if abs(systInBin) > 0.01:
                    systLine += "{0} - ".format("%.2f" % (1+systInBin))
                else:
                    systLine += "- - "
            if not any(char.isdigit() for char in systLine.split("lnN")[1]):
                continue
        systLines += systLine+"\n"

    return systLines

paths = ["StraightYieldLow","StraightYieldHigh","StraightPlusSlabYieldLow","StraightPlusSlabYieldHigh","StraightPlusTwoOrMoreSlabsYieldLow"]

labelDict = {"StraightYieldLow":"straight_low","StraightYieldHigh":"straight_high",
        "StraightPlusSlabYieldLow":"straightPlusSlab_low","StraightPlusSlabYieldHigh":"straightPlusSlab_high",
        "StraightPlusTwoOrMoreSlabsYieldLow":"straightPlusAtLeastTwoSlabs"}
dfSig = pd.read_csv("../signalYields_{0}.csv".format(tag))
dfBkg = pd.read_csv("../backgroundYields_{0}.csv".format(tag))

outputDir = "statsCardOutput_{0}/cards_mcp".format(tag)
if not os.path.exists(outputDir):
    os.makedirs(outputDir)

bkg = dfBkg.iloc[0]
with open('v8_v1_save2m.json') as f:
  systematics = json.load(f)
for index, row in dfSig.iterrows():
    mass = row["mass"]
    charge = round(row["charge"],6)
    cardName = "signalCardMass{0}Charge{1}.txt".format(str(mass).replace(".","p"),str(charge).replace(".","p"))
    if oneBin:
        bkgY = 0
        sig = 0
        sens = -1
        labelFinal = ""
        for label in ["StraightYieldLow","StraightYieldHigh","StraightPlusSlabYieldLow","StraightPlusSlabYieldHigh","StraightPlusTwoOrMoreSlabsYieldLow"]:
            bkgTemp = bkg[label]
            sigTemp = row[label]
            sensTemp = (2*(bkgTemp+sigTemp)*math.log(1+sigTemp/bkgTemp)-sigTemp)**0.5
            if sensTemp > sens:
                bkgY = bkgTemp*1
                sig = sigTemp*1
                sens = sensTemp
                labelFinal = label
        card = makeCardOneChannel(bkgY,sig,labelDict[labelFinal])
    else:
        card = makeCard(paths,labelDict,bkg,row)
        card += addGammaLines(paths,bkg,row)
        systematicsPerModel = systematics["q_"+str(charge).replace(".","p")]["m_"+str(mass).replace(".","p")]
        card += addSystematicsLines(paths,systematicsPerModel)
    with open(outputDir+"/"+cardName,'w') as f:
        f.write(card)

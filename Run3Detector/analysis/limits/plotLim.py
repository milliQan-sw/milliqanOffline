import os
import csv
import numpy as np
import math
from collections import OrderedDict as odict
from collections import defaultdict
import glob,pickle
import argparse
#from config_2018 import configs
from array import array
import ROOT as r
r.gStyle.SetOptStat(0)
r.gROOT.SetBatch(True)
import ctypes
def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-i","--inDir",help="input directory",type=str)
    parser.add_argument("-a","--asymp",help="asymptotic limits",action="store_true")
    parser.add_argument("-m","--model",help="model name to run",type=str)
    parser.add_argument("-o","--outFile",help="output file name",type=str)
    parser.add_argument("-q","--quants",help="quantiles",type=float,nargs='+',default=[0.5])
    parser.add_argument("-f","--femto",help="lim on xs in fb",action="store_true")
    args = parser.parse_args()
    return args
def convert_graph_to_exponentials(graph, base=math.e):
    """
    Converts the x and y values of a ROOT TGraph to their exponentials: base^x and base^y.

    Args:
        graph (ROOT.TGraph): The input ROOT graph.
        base (float): The base for the exponential transformation (default is e).

    Returns:
        ROOT.TGraph: A new TGraph with exponentiated x and y values.
    """
    n_points = graph.GetN()
    new_graph = r.TGraph()

    for i in range(n_points):
        x, y = ctypes.c_double(1.),ctypes.c_double(1.)
        graph.GetPoint(i, x, y)

        exp_x = base ** x.value
        exp_y = base ** y.value
        new_graph.SetPoint(new_graph.GetN(), exp_x, exp_y)

    return new_graph
def tgraph_to_csv(graph, output_csv):

    # Open the CSV file for writing
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['x', 'y'])  # header

        for i in range(graph.GetN()):
            x = ctypes.c_double(1.0)
            y = ctypes.c_double(1.0)
            graph.GetPoint(i, x, y)
            writer.writerow([x.value, y.value])

    print(f"Successfully written TGraph data to '{output_csv}'")




def isRootFileOk(fileName):
    isOK = False
    if os.path.exists(os.path.abspath(fileName)):
        # r.gErrorIgnoreLevel=r.kError
        r.gErrorIgnoreLevel=r.kSysError
        tf = r.TFile(os.path.abspath(fileName),"READ")
        if not (tf.IsZombie() or tf.TestBit(r.TFile.kRecovered)): isOK = True
        tf.Close()

    return isOK
def getContour(graph):
    graph.GetHistogram().SetContour(1,array('d',[1.0]))
    graph.Draw("cont list")
    contourList = []
    contLevel = graph.GetContourList(1.)
    if contLevel and contLevel.GetSize()>0:
        for i in range(0,contLevel.GetSize()):
            contourTemp = contLevel[i].Clone()
            if type(contourTemp) != int: contourTemp.SetName(graph.GetName()+"_r1Contour")
            else: continue
        contourList.append(contourTemp)
        contourList = sorted(contourList,key = lambda contour: contour.GetN())[::-1]
        return contourList[0]
    else:
        return None
def plotLim1D(inDir,model,outFile,quants,femto,asymp):
    #cfg = configs[model]
    #xsDict = pickle.load(open(cfg.xsDict,"r"))
    tFileOut = r.TFile(outFile.replace(".root","_1D.root"),"RECREATE")
    dictOutFull = {}
    for quant in quants:
        lims = defaultdict(dict)
        if quant >= 0:
            if asymp:
                inFiles = glob.glob(inDir+"/higgsCombinetestCard*_"+model+"_*Asymptotic*")
                inFiles = [x for x in inFiles if "Obs.Asymptotic" not in x]
            else:
                inFiles = glob.glob(inDir+"/higgsCombinetestCard*_"+model+"_*"+"quant"+str(quant)+"*")
        else:
            if asymp:
                inFiles = glob.glob(inDir+"/higgsCombinetestCard*_"+model+"_*Obs.Asymptotic*")
            else:
                inFiles = glob.glob(inDir+"/higgsCombinetestCard*_"+model+"_*mH120.root")
        if len(inFiles) == 0:
            print("WARNING no input files for quant {0}!".format(quant))
        for inFile in inFiles:
            if not isRootFileOk(inFile): continue
            tFile = r.TFile(inFile)
            #keyNameSplit=inFile.split("_")
            keyNameSplit=inFile.split(".")
            if model == "gluinoGMSB":
                print(keyNameSplit)
                mSusy = int(inFile.split("gluinoGMSB_M")[1].split("_")[0])
                ctau0 = int(inFile.split("ctau")[1].split("p")[0])
                # mSusy = int(keyNameSplit[keyNameSplit.index("mGluino")+1])
                mLsp = 1
                # ctau0 = int(keyNameSplit[keyNameSplit.index("ctau0")+1].split(".")[0])
            elif model == "zPrime" or model == "zPrimeLLInv":
                signalSplit = inFile.split("_")
                mSusy = int(signalSplit[signalSplit.index("mZ")+1])
                mLsp = int(signalSplit[signalSplit.index("mX")+1])
                ctau0 = int(signalSplit[signalSplit.index("ctau")+1])
            else:
                #mSusy = int(keyNameSplit[keyNameSplit.index("mSUSY")+1])
                #mLsp = int(keyNameSplit[keyNameSplit.index("mLSP")+1])
                #ctau0 = int(float((signalSplit[2].split("ctau")[1]).replace("p",".")))
                mMCP = float(keyNameSplit[0].split("Mass")[1].split("Charge")[0].replace("p","."))
                charge = float(keyNameSplit[0].split("Mass")[1].split("Charge")[1].replace("p","."))
            tTree = tFile.Get("limit")
            if not tTree:continue
            if asymp and quant > 0:
                if tTree.GetEntries() != 5: continue
            else:
                #if tTree.GetEntries() != 1: continue
                if (tTree.GetEntries() != 6) & (tTree.GetEntries() != 5): continue
            entryDict = {0.025:0,0.16:1,0.5:2,0.84:3,0.975:4,-1:5}
            if asymp:
                if quant <= 0:
                     #lims[(mSusy,mLsp)][ctau0] = tTree.GetMaximum("limit")
                     if tTree.GetEntry(entryDict[quant]) > 1000: continue
                     lims[(mMCP)][charge] = tTree.GetEntry(entryDict[quant])
                else:
                    #tTree.GetEntry(entryDict[quant])
                    if tTree.GetEntry(entryDict[quant]) > 1000: continue
                    #lims[(mSusy,mLsp)][ctau0] = tTree.limit
                    lims[(mMCP)][charge] = tTree.GetEntry(entryDict[quant])
            else:
                lims[(mSusy,mLsp)][ctau0] = tTree.GetMaximum("limit")
            #if femto:
            #    lims[(mSusy,mLsp)][ctau0]*=xsDict[mSusy][0]
        dictOutFull["quant"+str(quant)] = lims
    for name,dictOut in dictOutFull.items():
        outputDir = tFileOut.mkdir(name)
        outputDir.cd()
        #for (mSusy,mLsp) in dictOut:
        for (mMCP,charge) in dictOut:
            #outputGraph = r.TGraph(len(dictOut[(mSusy,mLsp)]))
            #outputGraph.SetName(model+"_"+str(mSusy)+"_"+str(mLsp)+"_graph")
            outputGraph = r.TGraph(len(dictOut[(mMCP)]))
            outputGraph.SetName(model+"_"+str(mMCP)+"_"+str(charge)+"_graph")
            outputGraph.SetTitle("")
            i = 0
            #ctau0s = []
            qs = []
            lims = []
            #for ctau0 in dictOut[(mSusy,mLsp)]:
            for q in dictOut[(mMCP)]:
                #ctau0s.append(ctau0)
                #lims.append(dictOut[(mSusy,mLsp)][ctau0])
                qs.append(q)
                lims.append(dictOut[(mSusy,mLsp)][ctau0])
            #lims = [x for _,x in sorted(zip(ctau0s,lims))]
            lims = [x for _,x in sorted(zip(qs,lims))]
            #ctau0s = sorted(ctau0s)
            qs = sorted(qs)
            #for ctau0,lim in zip(ctau0s,lims):
            for q,lim in zip(qs,lims):
                #outputGraph.SetPoint(i,ctau0,lim)
                outputGraph.SetPoint(i,q,lim)
                i += 1

            outputGraph.Write()
def plotLim(inDir,model,outFile,quants,femto,asymp):
    tFileOut = r.TFile(outFile,"RECREATE")
    #cfg = configs[model]
    #xsDict = pickle.load(open(cfg.xsDict,"r"))
    dictOutFull = {}
    for quant in quants:
        lims = defaultdict(dict)
        #if quant >= 0:
        #    inFiles = glob.glob(inDir+"/higgsCombinetestCard_*"+model+"*"+"quant"+str(quant)+"*")
        #else: #LOOK HERE
            #inFiles = glob.glob(inDir+"/higgsCombinetestCard_*"+model+"*mH120.root")
        inFiles = glob.glob(inDir+"/higgsCombinesignalCard*mH120.root")
        if len(inFiles) == 0:
            print("WARNING no input files for quant {0}!".format(quant))
        print("mass","charge","yield")
        for inFile in inFiles:
            if not isRootFileOk(inFile): continue
            tFile = r.TFile(inFile)
            #keyNameSplit=inFile.split("_")
            keyNameSplit=inFile.split(".")
            # mSusy = int(keyNameSplit[keyNameSplit.index("mSUSY")+1])
            # mLsp = int(keyNameSplit[keyNameSplit.index("mLSP")+1])
            # ctau0 = int(keyNameSplit[keyNameSplit.index("ctau0")+1].split(".")[0])
            if model == "gluinoGMSB":
                mSusy = int(inFile.split("gluinoGMSB_M")[1].split("_")[0])
                ctau0 = int(inFile.split("ctau")[1].split("p")[0])
                mLsp = 1
            elif model == "zPrime":
                mSusy = int(signalSplit[signalSplit.index("mZ")+1])
                mLsp = int(signalSplit[signalSplit.index("mX")+1])
                ctau0 = int(signalSplit[signalSplit.index("ctau")+1])
            else:
                #mSusy = int(keyNameSplit[keyNameSplit.index("mSUSY")+1])
                #mLsp = int(keyNameSplit[keyNameSplit.index("mLSP")+1])
                #ctau0 = int(float((signalSplit[2].split("ctau")[1]).replace("p",".")))
                mMCP = float(keyNameSplit[0].split("Mass")[1].split("Charge")[0].replace("p","."))
                charge = float(keyNameSplit[0].split("Mass")[1].split("Charge")[1].replace("p","."))
            entryDict = {0.025:0,0.16:1,0.5:2,0.84:3,0.975:4,-1:5}
            tTree = tFile.Get("limit")
            if not tTree:continue
            if (tTree.GetEntries() != 6) & (tTree.GetEntries() != 5): continue
            #if femto:
            #    lims[mLsp][(mSusy,ctau0)] = tTree.GetMaximum("limit")*xsDict[mSusy][0]
            else:
                #lims[mLsp][(mSusy,ctau0)] = tTree.GetMaximum("limit")
                tTree.GetEntry(entryDict[quant])
                if tTree.limit > 5: continue
                if tTree.limit < 0.01: continue
                if tTree.limit > 2 and tTree.limit < 2.1: continue
                print(mMCP,charge,tTree.limit)
                lims[(mMCP)][charge] = tTree.limit
        dictOutFull["quant"+str(quant)] = lims
    for name,dictOut in dictOutFull.items():
        outputDir = tFileOut.mkdir(name)
        outputDir.cd()
        
        outputGraph = r.TGraph2D(len(dictOut))
        i=0
        for mMCP in dictOut:
            for charge in dictOut[(mMCP)]:
                outputGraph.SetPoint(i,math.log(mMCP),math.log(charge),dictOut[(mMCP)][charge])
                i+=1
        contour = getContour(outputGraph)
        contour = convert_graph_to_exponentials(contour)

        if contour: 
            tgraph_to_csv(contour,outFile.replace("root","csv"))
            contour.Write()
            contour.SetTitle("Combined SR1+SR2 Limit")
            contour.GetXaxis().SetTitle("Mass[GeV]")
            contour.GetYaxis().SetTitle("Charge Q/e")
            #contour.SetLogx()
            #contour.SetLogy()
        outputGraph.Write()

        #for ctau0 in dictOut:
        '''
        for mMCP in dictOut:
            #ctauArray = np.logspace(2,5,15)
            massArray = np.logspace(-1,2,15)
            #outputHist = r.TH2D(model+"_"+str(ctau0),"",60,1050,3550,len(ctauArray)-1,array('d',ctauArray))
            outputHist = r.TH2D(model+"_"+str(mMCP),"",60,1050,3550,len(massArray)-1,array('d',massArray))
            #outputGraph = r.TGraph2D(len(dictOut[ctau0]))
            outputGraph = r.TGraph2D(len(dictOut[ctau0]))
            #outputGraph.SetName(model+"_"+str(ctau0)+"_graph")
            outputGraph.SetName(model+"_"+str(mMCP)+"_graph")
            outputGraph.SetTitle(model+" "+str(ctau0))
            i = 0
            print dictOut[ctau0]
            for (mSusy,mLsp) in dictOut[ctau0]:
                outputHist.Fill(mSusy,mLsp,dictOut[ctau0][mSusy,mLsp])
                outputGraph.SetPoint(i,mSusy,mLsp,dictOut[ctau0][mSusy,mLsp])
                i += 1
            interpHist = outputGraph.GetHistogram().Clone(outputGraph.GetName()+"interp")
            contour = getContour(outputGraph)
            if contour:
                contour.Write()
            outputHist.Write()
            outputGraph.Write()
            interpHist.Write()
            '''
    # for name,dictOut in dictOutFull.items():
    #     outputDir = tFileOut.mkdir(name)
    #     outputDir.cd()
    #     for ctau0 in dictOut:
    #         outputHist = r.TH2D(model+"_"+str(ctau0),"",30,1000,4000,100,0,30000)
    #         outputGraph = r.TGraph2D(len(dictOut[ctau0]))
    #         outputGraph.SetName(model+"_"+str(ctau0)+"_graph")
    #         outputGraph.SetTitle(model+" "+str(ctau0))
    #         i = 0
    #         for (mSusy,mLsp) in dictOut[ctau0]:
    #             outputHist.Fill(mSusy,mLsp,dictOut[ctau0][mSusy,mLsp])
    #             outputGraph.SetPoint(i,mSusy,mLsp,dictOut[ctau0][mSusy,mLsp])
    #             i += 1
    #         interpHist = outputGraph.GetHistogram().Clone(outputGraph.GetName()+"interp")
    #         contour = getContour(outputGraph)
    #         if contour:
    #             contour.Write()
    #         outputHist.Write()
    #         outputGraph.Write()
    #         interpHist.Write()

if __name__=="__main__":
    # plotLim1D(**vars(parse_args()))
    plotLim(**vars(parse_args()))

#ver 1.0
#1/12/2023 Collin Zheng  Zheng.1947@buckeyemail.osu.edu
#the code needs to be run with python2
#this code is for v29 runs on T3 only

import math
import ROOT as r
from ROOT import *
import numpy as np
import argparse


def initializeTree(runNum):

    chain = r.TChain("t")
    chain.Add('/store/user/mcarrigan/trees/v29/MilliQan_Run' + runNum + '.*_v29_firstPedestals.root')
    return chain

def counting_map(runNum):
    nx = 6
    ny = 21
    
    rowName = ["front pannel","1st row(layer one)","2nd row(layer one)","3rd row(layer one)", "4th row(layer one)","top pannel (layer1&2)","1st row(layer two)","2nd row(layer two)","3rd row(layer two)", "4th row(layer two)","empty","1st row(layer 3)","2nd row(layer 3)","3rd row(layer 3)", "4th row(layer 3)","top pannel (layer3&4)","1st row(layer 4)","2nd row(layer 4)","3rd row(layer 4)", "4th row(layer 4)","back pannel"]
    columnName = ["left pannel","1st column","2nd column","3rd column", "4th column", "right pannel"]
    c1 = TCanvas("c1","demo bin labels",10,10,600,600)
    c1.SetGrid()
    c1.SetLeftMargin(0.30)
    c1.SetRightMargin(0.30)
    c1.SetBottomMargin(0.30)
    h = TH2F("h","heatmap",nx,-1,nx-1,ny,0,ny)

    chain = initializeTree(runNum)
    entry = 0
    while entry < chain.GetEntries():

    
        chain.GetEvent(entry)
        #chain.GetEvent(306318)
        #if chain.event == 318:

        if nx < 7: # used for loop over all events
            columnlist = chain.column
            rowlist = chain.row
            layerList = chain.layer

            chanList = chain.chan
            nPEList = chain.nPE
            durationList = chain.duration
            heightList = chain.height
            #print(chain.chan)
            areaList = chain.area
            
            #j = 1
            for chainIndex, chan in enumerate(chanList):
                #filter condition
                if nPEList[chainIndex] > 40.0 and  heightList[chainIndex]>1200.0 and durationList[chainIndex]>200.0 and areaList[chainIndex]>200.0:
                #if j == 1: # take away filter condition
                    row = rowlist[chainIndex]
                    column = columnlist[chainIndex]
                    layer = layerList[chainIndex]
                    

                    if layer == -1: #back pannel 
                        h.Fill(column,row,1)
                        #print(column,row,layer)
                    if layer == 0: #layer one
                        h.Fill(column,row+1,1)
                        #print(column,row,layer)  
                    if layer == 1: #layer two
                        h.Fill(column,row+6,1)
                        #print(column,row,layer)
                    if layer == 2: #layer three
                        h.Fill(column,row+11,1)
                        #print(column,row,layer)
                    if layer == 3: #layer four
                        h.Fill(column,row+16,1)
                        #print(column,row,layer)
                    if layer == 4: #back pannel
                        h.Fill(column,row+20,1)
                        #print(column,row,layer)

            h.LabelsDeflate("X")
            h.LabelsDeflate("Y")

            #h.LabelsOption("v")
            #let the axixs label in the expected order
            i = 1
            while i <= nx:
                h.GetXaxis().SetBinLabel(i,columnName[i-1])   
                i += 1

            k = 1
            while k <= ny:
                h.GetYaxis().SetBinLabel(k,rowName[k-1])   
                k += 1

                
        
        entry += 1

    h.Draw("text")  #DISPLAY THE BIN number

    c1.Draw()

    f=r.TFile.Open("counting_map.root","recreate")
    h.Write()
    c1.Write()
    f.Close()
    print("plot is save as counting_map.root ")

def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument('runNum',help ='provide run number in 3 digits. we only have runs from 560-591')
    args = parser.parse_args()
    runNum = args.runNum
    counting_map(runNum)

if __name__ == "__main__":
    Main()
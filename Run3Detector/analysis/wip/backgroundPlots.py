import ROOT as r
import math
import numpy as np
import os
import sys
import json
import shutil
sys.path.append('../utilities/')
from utilities import *
import argparse


def getFileList(inputFile):
    with open(inputFile, 'r') as fin:
        files = json.load(fin)
    fileList = []
    for k, v in files.items():
        fileList += v
    return fileList

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-d","--directory",help="Directory to get input file from",type=str)
    parser.add_argument("-t", "--tag", help="String to be appended to plot and directory names", type=str)
    args = parser.parse_args()
    return args



if __name__ == "__main__":

    r.gROOT.ProcessLine( "gErrorIgnoreLevel = 6001;")
    r.gROOT.ProcessLine( "gPrintViaErrorHandler = kTRUE;")
    r.gROOT.SetBatch(1)

    args = parse_args()

    if not args.directory:
        inputFile = '/abyss/users/mcarrigan/milliqan/backgroundAnalysis_1600_noBeamInFill_med/mergedOutput.root'
    else:
        inputFile = args.directory

    if not args.tag:
        tag = '1600_noBeamInFill'
    else:
        tag = args.tag

    #option to scale by activity in channels found in zero bias events
    scaleFactor = False

    if scaleFactor:
        #fin_sf = r.TFile.Open('/abyss/users/mcarrigan/milliqan/backgroundAnalysis_1700_noBeamInFillZB/mergedOutput.root', 'read')
        mychain = r.TChain('t')
        mychain.Add('/store/user/milliqan/trees/v35/bar/1600/MilliQan_Run164*.root')
        mychain.Draw("chan>>h_channel(80, 0, 80)", "!pickupFlagTight && tTrigger == 4096")
        h_channel = r.gDirectory.Get('h_channel')
        #h_channel = fin_sf.Get('h_channel')
        nEntries = h_channel.GetEntries()

        h_channelScaled = r.TH1F('h_channelScaled', 'Scaled Channel Counts', 80, 0, 80)
        h_channelFactors = r.TH1F('h_channelFactors', 'Channel Scale Factors', 80, 0, 80)

        sfs = pd.DataFrame([], columns=['channel', 'scaleFactor'])

        minBin = [-1, 10e5]
        for ibin in range(h_channel.GetNbinsX()):
            newVal = h_channel.GetBinContent(ibin+1) #/ nEntries
            h_channelScaled.Fill(ibin, newVal)
            if newVal < minBin[1] and newVal > 0 and h_channel.GetBinContent(ibin+1) > 0 and ibin < 64: 
                minBin[0] = ibin
                minBin[1] = newVal
            print("Bin {}, value {}, new val {}".format(ibin, h_channel.GetBinContent(ibin+1), newVal))

        for ibin in range(h_channelScaled.GetNbinsX()):
            newVal = h_channelScaled.GetBinContent(ibin+1) / minBin[1]
            h_channelFactors.Fill(ibin, newVal)
            sfs.loc[len(sfs)] = [ibin, newVal]

        #sfs['channel'].loc[sfs['channel'] == 78] = 24
        #sfs['channel'].loc[sfs['channel'] == 79] = 25
        sfs.loc[sfs['channel'] == 24, 'scaleFactor'] = sfs.loc[sfs['channel'] == 78, 'scaleFactor'].values
        sfs.loc[sfs['channel'] == 25, 'scaleFactor'] = sfs.loc[sfs['channel'] == 79, 'scaleFactor'].values

        #sfs['scaleFactor'].loc[sfs['channel'] == 24] = sfs['scaleFactor'].loc[sfs['channel'] == 78]
        #sfs['scaleFactor'].loc[sfs['channel'] == 25] = sfs['scaleFactor'].loc[sfs['channel'] == 79]

    fileList = '/'.join(inputFile.split('/')[:-1]) + '/filelist.json'
    inputFiles = getFileList(fileList)

    print("Run was over {} files".format(len(inputFiles)))

    totalLumi, runTime = getLumiofFileList(inputFiles)

    plotDir = 'plots_{}'.format(tag)
    if not os.path.isdir(plotDir):
        os.mkdir(plotDir)

    fin = r.TFile.Open(inputFile, 'read')

    fout = r.TFile.Open('{}/plots_{}.root'.format(plotDir, tag), 'recreate')

    countHistograms = []
    pathHistograms = []

    for key in fin.GetListOfKeys():
        #print(key.GetName())
        if key.GetName().startswith('h_threeInLineCountPath'): countHistograms.append(key.ReadObj())
        if key.GetName().startswith('h_threeInLinePath'): pathHistograms.append(key.ReadObj())

    counts = []

    for hist in countHistograms:
        failed = hist.GetBinContent(1)
        passing = hist.GetBinContent(2)
        counts.append([failed, passing])


    #plot the ratio of events with each 3 in line trigger

    h_ratio3InLine_L0 = r.TH1F('h_ratio3InLine_L0', "Ratio of Events with 3 In Line Triggers (Layer 0 Free)", 16, 0, 16)
    h_ratio3InLine_L1 = r.TH1F('h_ratio3InLine_L1', "Ratio of Events with 3 In Line Triggers (Layer 1 Free)", 16, 0, 16)
    h_ratio3InLine_L2 = r.TH1F('h_ratio3InLine_L2', "Ratio of Events with 3 In Line Triggers (Layer 2 Free)", 16, 0, 16)
    h_ratio3InLine_L3 = r.TH1F('h_ratio3InLine_L3', "Ratio of Events with 3 In Line Triggers (Layer 3 Free)", 16, 0, 16)

    h_counts3InLine_L0 = r.TH1F('h_counts3InLine_L0', "Number of Events with 3 In Line Triggers (Layer 0 Free)", 16, 0, 16)
    h_counts3InLine_L1 = r.TH1F('h_counts3InLine_L1', "Number of Events with 3 In Line Triggers (Layer 1 Free)", 16, 0, 16)
    h_counts3InLine_L2 = r.TH1F('h_counts3InLine_L2', "Number of Events with 3 In Line Triggers (Layer 2 Free)", 16, 0, 16)
    h_counts3InLine_L3 = r.TH1F('h_counts3InLine_L3', "Number of Events with 3 In Line Triggers (Layer 3 Free)", 16, 0, 16)

    h_counts3InLine = [h_counts3InLine_L0, h_counts3InLine_L1, h_counts3InLine_L2, h_counts3InLine_L3]
    h_ratio3InLine = [h_ratio3InLine_L0, h_ratio3InLine_L1, h_ratio3InLine_L2, h_ratio3InLine_L3]

    for ic, count in enumerate(counts):
        ratio = count[1] / (count[0] + count[1])
        error = 0
        if count[0]+count[1] > 0: 
            if count[1] == 0: count[1] = 1
            error = ratio * math.sqrt((math.sqrt(count[1])/count[1]**2) + (math.sqrt(count[1]+count[0])/(count[0]+count[1]))**2)
        errorC = 1
        if count[1] > 0: errorC = math.sqrt(count[1])

        h_ratio3InLine[ic//16].SetBinContent(ic%16+1, ratio)
        h_ratio3InLine[ic//16].SetBinError(ic%16+1, error)

        h_counts3InLine[ic//16].SetBinContent(ic%16+1, count[1])
        h_counts3InLine[ic//16].SetBinError(ic%16+1, errorC)

    c2 = r.TCanvas("c2", "c2", 800, 800)
    c2.Divide(1, 4)

    c2.cd(1)
    h_ratio3InLine_L0.Draw("E")
    c2.cd(2)
    h_ratio3InLine_L1.Draw("E")
    c2.cd(3)
    h_ratio3InLine[2].Draw("E")
    c2.cd(4)
    h_ratio3InLine_L3.Draw("E")
    c2.Draw()

    c2.SaveAs("{}/RatioThreeInLine_{}.pdf".format(plotDir, tag))

    fout.cd()
    c2.Write('RatioThreeInLine')

    c2.cd(1)
    h_counts3InLine_L0.Draw("E")
    c2.cd(2)
    h_counts3InLine_L1.Draw("E")
    c2.cd(3)
    h_counts3InLine_L2.Draw("E")
    c2.cd(4)
    h_counts3InLine_L3.Draw("E")
    c2.Draw()

    c2.SaveAs("{}/CountsThreeInLine_{}.pdf".format(plotDir, tag))
    c2.Write('CountsThreeInLine')


    #now get counts for each 4th layer channel

    fourthLayerCounts = []
    fourthLayerCountsRaw = []

    for i in range(64): #loop over plots
        total_counts = np.zeros((4, 4))
        total_countsRaw = np.zeros((4, 4))

        #if i > 0: continue
        hist = pathHistograms[i]
        for row in range(4): #loop over rows
            for col in range(4): #loop over columns
                counts_ = hist.GetBinContent(row+1, col+1)
                total_countsRaw[row][col] = counts_
                if scaleFactor:
                    sf = sfs.loc[sfs['channel'] == i, 'scaleFactor'].values[0]
                    print('channel {}, counts {}, scaleFactor {}'.format(i, counts_, sf))
                    #print(i, sf, counts_, counts_/sf)
                    if sf != 0: counts_ = counts_ / sf
                    else: 
                        print("scale factor is 0, counts are", counts_)
                total_counts[row][col] = counts_
        fourthLayerCounts.append(total_counts)
        fourthLayerCountsRaw.append(total_countsRaw)

    ratioFourthLayer = fourthLayerCounts.copy()
    
    #find ratio of total events that had 3 in line
    for i, (layer, total) in enumerate(zip(ratioFourthLayer, counts)):
        if not total[1] == 0: 
            ratioFourthLayer[i] = layer / total[1]


    #draw all 4th layer plots

    c3 = r.TCanvas("c3", "c3", 1000, 1000)
    c3.Divide(4, 4)
    c4 = r.TCanvas("c4", "c4", 1000, 1000)
    c4.Divide(4, 4)
    c5 = r.TCanvas("c5", "c5", 1000, 1000)
    c5.Divide(4, 4)
    c6 = r.TCanvas("c6", "c6", 1000, 1000)
    c6.Divide(4, 4)

    canvases = [c3, c4, c5, c6]

    for i in range(64):
        canvases[i//16].cd(i%16+1)
        #c3.cd(i+1)
        pathHistograms[i].Draw('colz text')

        #titles were saved wrong, need to fix
        path = pathHistograms[i].GetName().split('Path')[1].split('_')[0]
        name = pathHistograms[i].GetTitle().split()[:-1]
        name = ' '.join(name)
        name += (' ' + path)
        pathHistograms[i].SetTitle(name)
        
        pathHistograms[i].GetXaxis().SetTitle("Column")
        pathHistograms[i].GetYaxis().SetTitle("Row")
        pathHistograms[i].SetStats(False)
    #c3.Draw()

    c3.SaveAs('{}/fourthLayerCounts_L0_{}.pdf'.format(plotDir, tag))
    c4.SaveAs('{}/fourthLayerCounts_L1_{}.pdf'.format(plotDir, tag))
    c5.SaveAs('{}/fourthLayerCounts_L2_{}.pdf'.format(plotDir, tag))
    c6.SaveAs('{}/fourthLayerCounts_L3_{}.pdf'.format(plotDir, tag))
    
    c3.Write('fourthLayerCounts_L0')
    c4.Write('fourthLayerCounts_L1')
    c5.Write('fourthLayerCounts_L2')
    c6.Write('fourthLayerCounts_L3')


    #draw all 4th layer plot ratios

    c3 = r.TCanvas("c3", "c3", 1000, 1000)
    c3.Divide(4, 4)
    c4 = r.TCanvas("c4", "c4", 1000, 1000)
    c4.Divide(4, 4)
    c5 = r.TCanvas("c5", "c5", 1000, 1000)
    c5.Divide(4, 4)
    c6 = r.TCanvas("c6", "c6", 1000, 1000)
    c6.Divide(4, 4)

    canvases = [c3, c4, c5, c6]

    for i in range(64):
        canvases[i//16].cd(i%16+1)

        #print("Total 3 In line paths", counts[i][1])

        if counts[i][1] > 0: pathHistograms[i].Scale(1/counts[i][1]) #scale by total number of 3 in line paths
        pathHistograms[i].Draw('colz text')

        #titles were saved wrong, need to fix
        path = pathHistograms[i].GetName().split('Path')[1].split('_')[0]
        name = pathHistograms[i].GetTitle().split()[:-1]
        name = ' '.join(name)
        name += (' ' + path)
        pathHistograms[i].SetTitle(name)
        
        pathHistograms[i].GetXaxis().SetTitle("Column")
        pathHistograms[i].GetYaxis().SetTitle("Row")
        pathHistograms[i].SetStats(False)
    #c3.Draw()

    c3.SaveAs('{}/fourthLayerRatios_L0_{}.pdf'.format(plotDir, tag))
    c4.SaveAs('{}/fourthLayerRatios_L1_{}.pdf'.format(plotDir, tag))
    c5.SaveAs('{}/fourthLayerRatios_L2_{}.pdf'.format(plotDir, tag))
    c6.SaveAs('{}/fourthLayerRatios_L3_{}.pdf'.format(plotDir, tag))

    c3.Write('fourthLayerRatios_L0')
    c4.Write('fourthLayerRatios_L1')
    c5.Write('fourthLayerRatios_L2')
    c6.Write('fourthLayerRatios_L3')


    #draw all 4th layer plot ratios given hit in 4th layer

    c3 = r.TCanvas("c3", "c3", 1000, 1000)
    c3.Divide(4, 4)
    c4 = r.TCanvas("c4", "c4", 1000, 1000)
    c4.Divide(4, 4)
    c5 = r.TCanvas("c5", "c5", 1000, 1000)
    c5.Divide(4, 4)
    c6 = r.TCanvas("c6", "c6", 1000, 1000)
    c6.Divide(4, 4)

    canvases = [c3, c4, c5, c6]

    for i in range(64):
        canvases[i//16].cd(i%16+1)

        totalHits = np.sum(fourthLayerCounts[i])
        #print("Sum of hits", totalHits)

        if totalHits > 0: pathHistograms[i].Scale(1/totalHits) #scale by total number of 3 in line paths
        pathHistograms[i].Draw('colz text')

        #titles were saved wrong, need to fix
        path = pathHistograms[i].GetName().split('Path')[1].split('_')[0]
        name = pathHistograms[i].GetTitle().split()[:-1]
        name = ' '.join(name)
        name += (' ' + path)
        pathHistograms[i].SetTitle(name)
        
        pathHistograms[i].GetXaxis().SetTitle("Column")
        pathHistograms[i].GetYaxis().SetTitle("Row")
        pathHistograms[i].SetStats(False)
    #c3.Draw()

    c3.SaveAs('{}/fourthLayerRatios4thHit_L0_{}.pdf'.format(plotDir, tag))
    c4.SaveAs('{}/fourthLayerRatios4thHit_L1_{}.pdf'.format(plotDir, tag))
    c5.SaveAs('{}/fourthLayerRatios4thHit_L2_{}.pdf'.format(plotDir, tag))
    c6.SaveAs('{}/fourthLayerRatios4thHit_L3_{}.pdf'.format(plotDir, tag))

    c3.Write('fourthLayerRatios4thHit_L0')
    c4.Write('fourthLayerRatios4thHit_L1')
    c5.Write('fourthLayerRatios4thHit_L2')
    c6.Write('fourthLayerRatios4thHit_L3')

    #plot distance from straight line path

    c1 = r.TCanvas("c1", "c1", 800, 600)

    h_movementTotal = r.TH2F('h_movementTotal', 'Movement from Straight Line Path', 7, -3, 4, 7, -3, 4)

    h_movementL0 = r.TH2F('h_movementL0', 'Movement from Straight Line Path L0 Free', 7, -3, 4, 7, -3, 4)
    h_movementL1 = r.TH2F('h_movementL1', 'Movement from Straight Line Path L1 Free', 7, -3, 4, 7, -3, 4)
    h_movementL2 = r.TH2F('h_movementL2', 'Movement from Straight Line Path L2 Free', 7, -3, 4, 7, -3, 4)
    h_movementL3 = r.TH2F('h_movementL3', 'Movement from Straight Line Path L3 Free', 7, -3, 4, 7, -3, 4)
    h_normalization = r.TH2F('h_normalization', 'Normalization Histogram', 7, -3, 4, 7, -3, 4)

    h_movementAbsDistance = r.TH1F('h_movementAbsDistance', 'Distance from Straight Line Path', 28, 0, 7)
    h_movementAbsSum = r.TH1F('h_movementAbsSum', 'Sum of Movement from Straight Line Path', 28, 0, 7)
    h_movementAbsMax = r.TH1F('h_movementAbsMax', 'Max of Movement from Straight Line Path', 28, 0, 7)

    h_movementAbsDistanceCount = r.TH1F('h_movementAbsDistanceCount', 'Distance from Sraight Line Path Counts', 28, 0, 7)

    h_normalizationAbsDistance = r.TH1F('h_normalizationAbsDistance', 'Normalization Histogram', 28, 0, 7)
    h_normalizationAbsSum = r.TH1F('h_normalizationAbsSum', 'Normalization Histogram', 28, 0, 7)
    h_normalizationAbsMax = r.TH1F('h_normalizationAbsMax', 'Normalization Histogram', 28, 0, 7)

    layer_hists = [h_movementL0, h_movementL1, h_movementL2, h_movementL3]

    for ipath, (path, pathRaw) in enumerate(zip(fourthLayerCounts,fourthLayerCountsRaw)):
        #print(path)
        freelayer = ipath//16
        s_row = (ipath - freelayer*16)//4
        s_col = ipath%4
        for irow, row in enumerate(path):
            for icol, col in enumerate(row):
                deltaRow = s_row - irow
                deltaCol = s_col - icol

                value = 0
                totalHits = counts[ipath][1]
                if totalHits > 0:
                    value = col / totalHits #counts[ipath][1]
                #print("path {}, totalHits {}, value {}, deltaRow {}".format(ipath, totalHits, value))
                #if freelayer == 3 and deltaRow == -3 and deltaCol == 2: 
                #    print("Path {}, path row {}, this row {}, delta row {}, Path col {}, this col {}, delta col {}, totalHits {}, value {}".format(ipath, s_row, irow, deltaRow, s_col, icol, deltaCol, totalHits, value))
                h_movementTotal.Fill(deltaCol, deltaRow, value)
                h_normalization.Fill(deltaCol, deltaRow)

                movement = math.sqrt((abs(deltaCol)**2) + (abs(deltaRow)**2))
                h_movementAbsDistance.Fill(movement, value)
                h_movementAbsDistanceCount.Fill(movement, pathRaw[irow][icol])
                h_normalizationAbsDistance.Fill(movement)

                h_movementAbsSum.Fill(deltaRow+deltaCol, value)
                h_normalizationAbsSum.Fill(deltaRow+deltaCol)

                max_d = max([deltaRow, deltaCol])
                h_movementAbsMax.Fill(max_d, value)
                h_normalizationAbsMax.Fill(max_d)

                layer_hists[freelayer].Fill(deltaCol, deltaRow, value)


    h_movementTotal.Divide(h_normalization)
    h_movementAbsDistance.Divide(h_normalizationAbsDistance)
    h_movementAbsSum.Divide(h_normalizationAbsSum)
    h_movementAbsMax.Divide(h_normalizationAbsMax)

    h_normalization.Scale(1./4)
    for h in layer_hists:
        h.Divide(h_normalization)

    fout.cd()
    h_movementTotal.Write()
    h_normalization.Write()
    h_movementL0.Write()
    h_movementL1.Write()
    h_movementL2.Write()
    h_movementL3.Write()
    h_movementAbsDistance.Write()
    h_movementAbsDistanceCount.Write()
    h_normalizationAbsDistance.Write()
    h_movementAbsSum.Write()
    h_normalizationAbsSum.Write()
    h_movementAbsMax.Write()
    h_normalizationAbsMax.Write()

    c1 = r.TCanvas("c1", "c1", 1000, 600)
    c1.cd()

    total  = h_movementTotal.Integral()
    h_movementTotal.Scale(1. / total)

    h_movementTotal.Draw('colz text')
    h_movementTotal.SetStats(False)
    h_movementTotal.GetYaxis().SetTitle('\Delta Row')
    h_movementTotal.GetXaxis().SetTitle('\Delta Column')
    c1.Write("h_movementTotalScaled")


    #get the rate
    numStraight = h_movementAbsDistanceCount.GetBinContent(1)
    totalTime = runTime.total_seconds()

    rate = numStraight / totalTime

    print("There are {} events over {}s giving a rate of {}/s".format(numStraight, totalTime, rate))

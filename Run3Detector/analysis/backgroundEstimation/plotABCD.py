import ROOT as r
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
import sys
import math
import argparse
from array import array
import cmsstyle as cms

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-i", "--inputFile", help="Input root file containing ABCD plot", type=str, required=True)
    parser.add_argument("-u", "--unblind", help="Option to unblind the results and show signal region", action='store_true')
    parser.add_argument("--SR", help="Give signal region of interest to get background estimates (current options SR1 and SR2)", type=int)
    parser.add_argument('-o', '--outputFile', help='Output file to save plots if unblinded', type=str, default=None)
    args = parser.parse_args()
    return args

def getPoissonErr(val, sigma=1):
    if val > 0:
        return np.sqrt(val), np.sqrt(val)
    else:
        beta = r.Math.erf(sigma / np.sqrt(2.0))
        alpha = (1 - beta)
        if val == 0:
            val = 1e-10
        lower = r.Math.gamma_quantile(alpha / 2., val , 1.0)
        upper = r.Math.gamma_quantile_c(alpha / 2., val + 1, 1.0)
    return lower, upper

def modifyPlot(h_ABCD):
    # Create edges for X and Y axes
    edgesX = []
    edgesY = []
    
    nbinsX = h_ABCD.GetNbinsX()
    nbinsY = h_ABCD.GetNbinsY()
    
    # Extract bin edges (1-indexed in ROOT)
    for b in range(1, nbinsX + 1):
        edgesX.append(h_ABCD.GetXaxis().GetBinLowEdge(b))
    edgesX.append(h_ABCD.GetXaxis().GetBinUpEdge(nbinsX))
    
    for b in range(1, nbinsY + 1):
        edgesY.append(h_ABCD.GetYaxis().GetBinLowEdge(b))
    edgesY.append(h_ABCD.GetYaxis().GetBinUpEdge(nbinsY))
    
    # Shift the first edge to 0.1 (to hide true zero)
    edgesX[0] = 1
    
    # Convert to array
    edgesX = array('d', edgesX)
    edgesY = array('d', edgesY)
    
    # Create a new TH2F with modified binning
    h_ABCDMod = r.TH2F('h_ABCDMod', 'Max Panel NPE vs N Bars Hit;Max Panel NPE;N Bars Hit',
                        len(edgesX) - 1, edgesX,
                        len(edgesY) - 1, edgesY)
    
    # Copy bin content (including underflow/overflow bins)
    for xbin in range(0, nbinsX + 2):  # Include underflow (0) and overflow (nbinsX+1)
        for ybin in range(0, nbinsY + 2):
            content = h_ABCD.GetBinContent(xbin, ybin)
            h_ABCDMod.SetBinContent(xbin, ybin, content)

    return h_ABCDMod


def calculateABCD(h_ABCD, maxTime=20, unblind=False, fout=None):
    
    yval = h_ABCD.GetYaxis().FindFixBin(maxTime)
    xval = h_ABCD.GetXaxis().FindFixBin(1)
    
    x_low = 0
    x_high = h_ABCD.GetNbinsX()
    
    y_low = 0
    y_high = h_ABCD.GetNbinsY()

    A = -1
    err_A = -1
    if unblind:
        A = h_ABCD.Integral(xval, x_high+1, y_low, yval-1)
        err_A = np.sqrt(A)

    B = h_ABCD.Integral(x_low, xval-1, y_low, yval-1)
    C = h_ABCD.Integral(x_low, xval-1, yval, y_high+1)
    D = h_ABCD.Integral(xval, x_high+1, yval, y_high+1)
    
    err_B = getPoissonErr(B)
    err_C = getPoissonErr(C)
    err_D = getPoissonErr(D)

    if C == 0:
        estErrALow = np.inf
        estErrAHigh = np.inf
        print("Error calculating uncertainty")
    elif B == 0:
        estErrALow = D/C*err_B[0]
        estErrAHigh = D/C*err_B[1]
    elif D == 0:
        estErrALow = B/C*err_D[0]
        estErrAHigh = B/C*err_D[1]
    else:
        estErrALow = (B*D)/C*np.sqrt((err_B[0]/B)**2 + (err_D[0]/D)**2 + (err_C[0]/C)**2)
        estErrAHigh = (B*D)/C*np.sqrt((err_B[1]/B)**2 + (err_D[1]/D)**2 + (err_C[1]/C)**2)

    estErrA = [estErrALow, estErrAHigh]

    if C>0:
        estA = round(B*D/C, 3)
        BCRatio = round(B/C, 4)
        BCErrLow = round(B/C*np.sqrt((err_B[0]/B)**2 + (err_C[0]/C)**2), 4)
        BCErrHigh = round(B/C*np.sqrt((err_B[1]/B)**2 + (err_C[1]/C)**2), 4)
        DCRatio = round(D/C, 4)
        DCErrLow = round(D/C*np.sqrt((err_D[0]/D)**2 + (err_D[0]/C)**2), 4)
        DCErrHigh = round(D/C*np.sqrt((err_D[1]/D)**2 + (err_D[1]/C)**2), 4)
    else:
        BCRatio = np.inf
        DCRatio = np.inf
        estA = np.inf


    print(f"Ratio B/C {BCRatio} + {BCErrHigh} - {BCErrLow} and D/C {DCRatio} + {DCErrHigh} - {DCErrLow} for SR1")

    if fout is not None:
        #c1 = r.TCanvas("c1", "c1", 800, 600)
        c1 = cms.cmsCanvas('c1',1e-1,40,2e-2,3e-1,"Mass [GeV]","Charge (Q/e)",iPos=0, square=True)
        c1.SetLogy(1)
        c1.SetLogz(1)

        h_ABCD.SetTitle(";Straight Path;Max-Min Time (ns)")
        h_ABCD.Draw("colz")

        lx = r.TLine(x_low, h_ABCD.GetYaxis().GetBinLowEdge(yval+1), h_ABCD.GetXaxis().GetBinLowEdge(x_high+1), h_ABCD.GetYaxis().GetBinLowEdge(yval))
        ly = r.TLine(h_ABCD.GetXaxis().GetBinLowEdge(xval), y_low, h_ABCD.GetXaxis().GetBinLowEdge(xval), h_ABCD.GetYaxis().GetBinLowEdge(y_high+1))
        lx.SetLineColor(r.kRed)
        ly.SetLineColor(r.kRed)
        lx.SetLineStyle(7)
        ly.SetLineStyle(7)
        
        lx.Draw("same")
        ly.Draw("same")

        t_a = r.TLatex()
        t_b = r.TLatex()
        t_c = r.TLatex()
        t_d = r.TLatex()
        t_a.SetTextColor(r.kBlack)
        t_b.SetTextColor(r.kBlack)
        t_c.SetTextColor(r.kBlack)
        t_d.SetTextColor(r.kBlack)
        if unblind:
            t_a.DrawLatex(1.4, 2, f"A={A}")
        t_b.DrawLatex(0.2, 2, f"B={B}")
        t_c.DrawLatex(0.2, 60, f"C={C}")
        t_d.DrawLatex(1.4, 60, f"D={D}")

        sysErrA = f'#pm{round(estErrA[0], 2)}'
        if estErrA[0] != estErrA[1]:
            sysErrA = f'-{round(estErrA[0], 2)} +{round(estErrA[1], 2)}'
            
        statErrALow, statErrAHigh = getPoissonErr(estA)
        statErrA = f'#pm{round(statErrALow, 2)}'
        if statErrALow != statErrAHigh:
            statErrA = f'-{round(statErrALow, 2)} +{round(statErrAHigh, 2)}'

        output = 'A = #frac{BD}{C} = #frac{' + str(B) + '#times' + str(D) + '}{'+ str(C) + f'}} = {estA}{statErrA}{sysErrA}'
        
        t_results = r.TLatex()
        t_results.SetTextSize(0.02)
        t_results.SetTextColor(r.kBlack)
        t_results.DrawLatex(1.05, 10, output)

        expName = r.TLatex()
        expName.SetNDC()
        expName.SetTextSize(0.04);
        expName.SetTextFont(62)
        expName.DrawLatex(0.13, 0.94, "milliQan Preliminary");
        
        textRun = r.TLatex()
        textRun.SetNDC()
        textRun.SetTextSize(0.04)
        textRun.SetTextAlign(31)
        textRun.DrawLatex(0.97, 0.94, "186.3 d (13.6 TeV)");

        box = r.TBox(1, 0, 2, 20)  # Covers a section of the histogram
        box.SetFillColorAlpha(r.kBlack, 1)  # Semi-transparent red
        box.SetLineColor(r.kBlack)  # Red outline
        box.SetLineWidth(2)  # Thicker border
        if not unblind:
            box.Draw("same")

        cms.SetCMSPalette()
        
        f = r.TFile.Open(fout, 'Update')
        f.cd()
        c1.Write('ABCD_SR1')
        h_ABCD.Write("h_ABCD")
        f.Close()

        imgName = fout.replace('.root', '_SR1.png')
        c1.SaveAs(imgName)

    return A, estA, estErrA

def calculateABCDSR2(h_ABCD, nBars=4, panelNPE=50, unblind=False, fout=None):
    
    yval = h_ABCD.GetYaxis().FindFixBin(nBars)
    xval = h_ABCD.GetXaxis().FindFixBin(panelNPE)
    
    x_low = 0
    x_high = h_ABCD.GetNbinsX()
    
    y_low = 0
    y_high = h_ABCD.GetNbinsY()

    A = -1
    err_A = -1

    if unblind:
        A = h_ABCD.Integral(x_low, xval-1, y_low, yval)
        err_A = np.sqrt(A)

    B = h_ABCD.Integral(xval, x_high+1, y_low, yval)
    C = h_ABCD.Integral(xval, x_high+1, yval+1, y_high+1)
    D = h_ABCD.Integral(x_low, xval-1, yval+1, y_high+1)

    
    err_B = getPoissonErr(B)
    err_C = getPoissonErr(C)
    err_D = getPoissonErr(D)

    if C == 0:
        estErrALow = np.inf
        estErrAHigh = np.inf
        print("Error calculating uncertainty")
    elif B == 0:
        estErrALow = D/C*err_B[0]
        estErrAHigh = D/C*err_B[1]
    elif D == 0:
        estErrALow = B/C*err_D[0]
        estErrAHigh = B/C*err_D[1]
    else:
        estErrALow = (B*D)/C*np.sqrt((err_B[0]/B)**2 + (err_D[0]/D)**2 + (err_C[0]/C)**2)
        estErrAHigh = (B*D)/C*np.sqrt((err_B[1]/B)**2 + (err_D[1]/D)**2 + (err_C[1]/C)**2)

    estErrA = [estErrALow, estErrAHigh]
    if C == 0:
        estA = np.inf
        print("Error calculating estimate, C==0")
    else:
        estA = round(B*D/C, 3)

    if C>0:
        estA = round(B*D/C, 3)
        BCRatio = round(B/C, 3)
        BCErrLow = round(B/C*np.sqrt((err_B[0]/B)**2 + (err_C[0]/C)**2), 3)
        BCErrHigh = round(B/C*np.sqrt((err_B[1]/B)**2 + (err_C[1]/C)**2), 3)
        DCRatio = round(D/C, 3)
        if D==0:            
            DCErrLow = round(1/C*np.sqrt((err_D[0]/1)**2 + (err_D[0]/C)**2), 3)
            DCErrHigh = round(1/C*np.sqrt((err_D[1]/1)**2 + (err_D[1]/C)**2), 3)
        else:
            DCErrLow = round(D/C*np.sqrt((err_D[0]/D)**2 + (err_D[0]/C)**2), 3)
            DCErrHigh = round(D/C*np.sqrt((err_D[1]/D)**2 + (err_D[1]/C)**2), 3)            
    else:
        BCRatio = np.inf
        DCRatio = np.inf


    print(f"Ratio B/C {BCRatio} + {BCErrHigh} - {BCErrLow} and D/C {DCRatio} + {DCErrHigh} - {DCErrLow} for SR2")

    #make plots if unblinding
    if unblind and fout is not None:

        c1 = cms.cmsCanvas('c1',1e-1,40,2e-2,3e-1,"Mass [GeV]","Charge (Q/e)",iPos=0, square=True)
        c1.SetLogx(1)
        c1.SetLogz(1)

        h_ABCDMod = modifyPlot(h_ABCD)
        h_ABCDMod.SetTitle(";Max Panel NPE;# Bars Hit")
        h_ABCDMod.Draw("colz")

        h_ABCDMod.GetXaxis().SetTitleSize(0.05)
        h_ABCDMod.GetYaxis().SetTitleSize(0.05)
        h_ABCDMod.GetXaxis().SetTitleOffset(1.2)
        
        lx = r.TLine(x_low, h_ABCDMod.GetYaxis().GetBinLowEdge(yval+1), h_ABCDMod.GetXaxis().GetBinLowEdge(x_high+1), h_ABCDMod.GetYaxis().GetBinLowEdge(yval+1))
        ly = r.TLine(h_ABCDMod.GetXaxis().GetBinLowEdge(xval), y_low, h_ABCDMod.GetXaxis().GetBinLowEdge(xval), h_ABCDMod.GetYaxis().GetBinLowEdge(y_high+1))
        lx.SetLineColor(r.kRed)
        ly.SetLineColor(r.kRed)
        lx.SetLineStyle(7)
        ly.SetLineStyle(7)

        lx.Draw("same")
        ly.Draw("same")

        t_a = r.TLatex()
        t_b = r.TLatex()
        t_c = r.TLatex()
        t_d = r.TLatex()
        t_a.SetTextColor(r.kBlack)
        t_b.SetTextColor(r.kBlack)
        t_c.SetTextColor(r.kBlack)
        t_d.SetTextColor(r.kBlack)
        t_a.DrawLatex(5, 2, f"A={A}")
        t_b.DrawLatex(100, 2, f"B={B}")
        t_c.DrawLatex(100, 14, f"C={C}")
        t_d.DrawLatex(5, 14, f"D={D}")

        sysErrA = f'#pm{round(estErrA[0], 2)}'
        if estErrA[0] != estErrA[1]:
            sysErrA = f'-{round(estErrA[0], 2)} +{round(estErrA[1], 2)}'
            
        statErrALow, statErrAHigh = getPoissonErr(estA)
        statErrA = f'#pm{round(statErrALow, 2)}'
        if statErrALow != statErrAHigh:
            statErrA = f'-{round(statErrALow, 2)} +{round(statErrAHigh, 2)}'

        if statErrALow == 0 or sysErrALow == 0:
            errLow = f'-{round(statErrALow, 2)} - {round(estErrA[0], 2)}'
            errHigh = f'+{round(statErrAHigh, 2)} + {round(estErrA[1], 2)}'
            print(errLow, errHigh)
            output = 'A = #frac{BD}{C} = #frac{' + str(B) + '#times' + str(D) + '}{'+ str(C) + f'}} = {estA}^{{{errHigh}}}_{{{errLow}}}'
        else:
            output = 'A = #frac{BD}{C} = #frac{' + str(B) + '#times' + str(D) + '}{'+ str(C) + '} = ' + str(estA) + ' ' + str(statErrA) + ' ' + str(sysErrA)

        t_results = r.TLatex()
        t_results.SetTextSize(0.02)
        t_results.SetTextColor(r.kBlack)
        t_results.DrawLatex(1.9, 10, output)

        expName = r.TLatex()
        expName.SetNDC()
        expName.SetTextSize(0.04);
        expName.SetTextFont(62)
        expName.DrawLatex(0.13, 0.94, "milliQan Preliminary");
        
        textRun = r.TLatex()
        textRun.SetNDC()
        textRun.SetTextSize(0.04)
        textRun.SetTextAlign(31)
        textRun.DrawLatex(0.97, 0.94, "186.3 d (13.6 TeV)");

        f = r.TFile.Open(fout, 'Update')
        f.cd()
        c1.Write('ABCD_SR2')
        h_ABCDMod.Write("h_ABCD2")
        f.Close()

        imgName = fout.replace('.root', '_SR2.png')
        c1.SaveAs(imgName)

    return A, estA, estErrA


#used for closure tests to compare measurements from different ABCD cuts
def plotAllABCD(dataDir=os.getcwd(), outputFile='abcdPlots.root'):
    g_ABCD = r.TGraphErrors()
    g_ABCD.SetTitle("ABCD Measured vs Estimated;Measured;Estimated")
    h_sigma = r.TH1F('h_sigma', '#sigma ABCD;#sigma(Estimate-Measured);', 50, -5, 5)
    c1 = r.TCanvas("c1", "c1", 800, 800)
    
    # Define the upper pad (larger)
    upper_pad = r.TPad("upper_pad", "Upper Pad", 0.0, 0.4, 1.0, 1.0)  # xlow, ylow, xup, yup
    upper_pad.SetBottomMargin(0.1)  # Reduce bottom margin
    upper_pad.Draw()
    
    # Define the lower pad (smaller)
    lower_pad = r.TPad("lower_pad", "Lower Pad", 0.0, 0.0, 1.0, 0.35)  # xlow, ylow, xup, yup
    lower_pad.SetTopMargin(0.05)    # Reduce top margin
    lower_pad.SetBottomMargin(0.3) # Increase bottom margin for labels
    lower_pad.Draw()

    max = 0
    for i, filename in enumerate(os.listdir(dataDir)):
        if not filename.endswith('root') or not filename.startswith('bgCutFlow'): continue
    
        fin = r.TFile.Open(filename)
        h_ABCD = fin.Get('h_ABCD')
        A, estA, estErrA = calculateABCD(h_ABCD)
        errA = round(np.sqrt(A), 2)
        g_ABCD.SetPoint(i, A, estA)
        g_ABCD.SetPointError(i, errA, estErrA)
        diff = estErrA - A
        if estErrA == 0:
            sigma = 0
        else:
            sigma = diff/estErrA
        h_sigma.Fill(sigma)
        print(f'file {filename}, A: {A}+-{errA}, estA: {estA}+-{estErrA}')
        if A > max: max = A
        if estA > max: max = estA

    max = math.ceil(max*1.1)
    r.gStyle.SetOptStat(0)
    upper_pad.cd()
    print("Setting the axes from", 0, max)
    #g_ABCD.GetXaxis().SetLimits(0, max)
    g_ABCD.SetMinimum(0)
    g_ABCD.SetMaximum(max)
    g_ABCD.Draw("P")

    l1 = r.TLine(0, 0, max, max)
    l1.SetLineColor(r.kRed)
    l1.Draw("same")
    lower_pad.cd()
    r.gStyle.SetOptStat(0)
    h_sigma.Draw()

    fout = r.TFile.Open(outputFile, 'RECREATE')
    fout.cd()
    c1.Write('ABCD_Measured_vs_Estimate')
    g_ABCD.Write('g_Measured_vs_Estimate')
    h_sigma.Write('sigma_Measured_vs_Estimate')

    


if __name__ == "__main__":

    r.gStyle.SetOptStat(0)
    
    #plotAllABCD()

    args = parse_args()

    if args.inputFile:

        fin = r.TFile.Open(args.inputFile, 'READ')

        h_ABCD = fin.Get('h_ABCD')
        A, estA, estErrA = calculateABCD(h_ABCD, unblind=args.unblind, fout=args.outputFile)
        
        sysErrA = f'+-{round(estErrA[0], 2)}'
        if estErrA[0] != estErrA[1]:
            sysErrA = f'-{round(estErrA[0], 2)} +{round(estErrA[1], 2)}'
            
        statErrALow, statErrAHigh = getPoissonErr(estA)
        statErrA = f'+-{round(statErrALow, 2)}'
        if statErrALow != statErrAHigh:
            statErrA = f'-{round(statErrALow, 2)} +{round(statErrAHigh, 2)}'
            
        print("---------------------------------------------------------------------------------------------")
        print(f"Estimated events in SR1: {estA} {statErrA} (stat) {sysErrA} (sys)")
        if args.unblind:
            print(f"Measured: {A} events in SR1")
        print("---------------------------------------------------------------------------------------------")

        if args.SR==2:

            h_ABCD = fin.Get('h_ABCD2')
            A, estA, estErrA = calculateABCDSR2(h_ABCD, unblind=args.unblind, fout=args.outputFile)

            sysErrA = f'+-{round(estErrA[0], 2)}'
            if estErrA[0] != estErrA[1]:
                sysErrA = f'-{round(estErrA[0], 2)} +{round(estErrA[1], 2)}'
                
            statErrALow, statErrAHigh = getPoissonErr(estA)
            statErrA = f'+-{round(statErrALow, 2)}'
            if statErrALow != statErrAHigh:
                statErrA = f'-{round(statErrALow, 2)} +{round(statErrAHigh, 2)}'
            print("---------------------------------------------------------------------------------------------")
            print(f"Estimated events in SR2: {estA} {statErrA} (stat) {sysErrA} (sys)")
            if args.unblind:
                print(f"Measured: {A} events in SR2")
            print("---------------------------------------------------------------------------------------------")








    
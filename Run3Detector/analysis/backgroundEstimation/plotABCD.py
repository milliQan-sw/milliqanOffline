import ROOT as r
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
import sys
import math

def calculateABCD(h_ABCD, maxTime=40):
    
    yval = h_ABCD.GetYaxis().FindFixBin(maxTime)
    xval = h_ABCD.GetXaxis().FindFixBin(1)
    
    x_low = 0
    x_high = h_ABCD.GetNbinsX()
    
    y_low = 0
    y_high = h_ABCD.GetNbinsY()
    
    A = h_ABCD.Integral(xval, x_high+1, y_low, yval)
    B = h_ABCD.Integral(x_low, xval, y_low, yval)
    C = h_ABCD.Integral(x_low, xval, yval, y_high+1)
    D = h_ABCD.Integral(xval, x_high+1, yval, y_high+1)
    
    err_A = np.sqrt(A)
    err_B = np.sqrt(B)
    err_C = np.sqrt(C)
    err_D = np.sqrt(D)

    estA = round(B*D/C,2)
    
    estErrA = (B*D)/C*np.sqrt(1/B + 1/D + 1/C)
    estErrA = round(estErrA, 2)

    return A, estA, estErrA


def plotAllABCD(dataDir=os.getcwd(), outputFile='abcdPlots.root'):
    g_ABCD = r.TGraphErrors()
    g_ABCD.SetTitle("ABCD Measured vs Estimated;Measured;Estimated")
    h_sigma = r.TH1F('h_sigma', '#sigma ABCD;#sigma(Estimate-Measured);', 50, -5, 5)
    c1 = r.TCanvas("c1", "c1", 800, 1200)
    
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

    plotAllABCD()
import ROOT as r
import numpy as np
from ctypes import c_double
import math

if __name__ == "__main__":

    fin = r.TFile.Open('triggerEfficiencyPlots8mv.root')

    fout = r.TFile.Open('combinedEfficiency.root', 'RECREATE')

    c1 = r.TCanvas("c1", "c1", 800, 600)
    c2 = r.TCanvas("c2", "c2", 800, 600)

    g_ratio = r.TGraphErrors()
    points = []
    totalTriple = []
    totalDouble = []

    timeTriple = fin.Get('channel0/hTimeTriple_0').GetBinContent(1)
    timeDouble = fin.Get('channel0/hTimeDouble_0').GetBinContent(1)

    for ichan in range(64):

        tripleCount3d = fin.Get(f'channel{ichan}/tripleCoincidenceCount')
        doubleCount3d = fin.Get(f'channel{ichan}/doubleCoincidenceCount')

        ymin = tripleCount3d.GetYaxis().FindBin(20)
        ymax = tripleCount3d.GetNbinsY()+1
        zmin = tripleCount3d.GetZaxis().FindBin(20)
        zmax = tripleCount3d.GetNbinsZ()+1

        tripleCount = tripleCount3d.ProjectionX("tripleCount", ymin, ymax, zmin, zmax)
        doubleCount = doubleCount3d.ProjectionX("doubleCount", ymin, ymax, zmin, zmax)

        for ibin in range(tripleCount.GetNbinsX()):

            t = tripleCount.GetBinContent(ibin)
            d = doubleCount.GetBinContent(ibin)

            if ichan==0:
                point = tripleCount.GetBinLowEdge(ibin)
                points.append(point)

                totalTriple.append(t)
                totalDouble.append(d)

            else:
                totalTriple[ibin] += t
                totalDouble[ibin] += d


        for ibin in range(len(points)):
            if totalDouble[ibin] == 0:
                print(f"ibin {ibin} is empty")
                continue
            val = totalTriple[ibin]/totalDouble[ibin] * timeDouble/timeTriple
            g_ratio.SetPoint(ibin, points[ibin], val)
            err = timeDouble/timeTriple*totalTriple[ibin]/totalDouble[ibin]*np.sqrt(1/totalTriple[ibin] + 1/totalDouble[ibin])
            g_ratio.SetPointError(ibin, 0, err)
            print(ibin, points[ibin], val)

    c1.cd()

    g_ratio.Draw("AP")
    g_ratio.SetMarkerStyle(8)
    g_ratio.SetTitle("Trigger Efficiency vs nPE")
    g_ratio.GetXaxis().SetTitle("nPE")
    g_ratio.GetYaxis().SetTitle("Efficiency")

    f2 = r.TF1("f2", "[0] * (0.5 * (1 + TMath::Erf((x - [1]) / ([2] * sqrt(2)))))", 0.001, 10)
    f2.SetParLimits(1, 0.0001, 20)
    f2.SetParLimits(2, 0.1, 10)
    f2.SetParLimits(0, 0.7, 1.3)
    f2.SetParameters(1, 1, 5)
    fitOut = g_ratio.Fit(f2, "SW", "", 0.2, 5)

    lamb = round(f2.GetParameter(0), 2)
    mu = round(f2.GetParameter(1), 2)
    sigma = round(f2.GetParameter(2), 2)
    chi = round(fitOut.Chi2() / fitOut.Ndf(), 2)

    text1 = r.TLatex()
    text1.SetTextSize(0.03);  
    text1.SetTextColor(r.kRed);  

    text2 = r.TLatex()
    text2.SetTextSize(0.03)
    text2.SetTextColor(r.kRed)

    text1.DrawLatex(2, 0.6, "#lambda: {}, #mu {}".format(lamb, mu))
    text2.DrawLatex(2, 0.5, "#sigma {}, #chi^2/ndof {}".format(sigma, chi))
    c1.SetLogx(0)

    g_ratio = r.TGraphErrors()
    
    
    points = []
    totalTriple = []
    totalDouble = []

    timeTriple = fin.Get('channel0/hTimeTriple_0').GetBinContent(1)
    timeDouble = fin.Get('channel0/hTimeDouble_0').GetBinContent(1)

    for ichan in range(64):

        tripleCount3d = fin.Get(f'channel{ichan}/hTripleHeight_{ichan}')
        doubleCount3d = fin.Get(f'channel{ichan}/hDoubleHeight_{ichan}')

        ymin = tripleCount3d.GetYaxis().FindBin(20)
        ymax = tripleCount3d.GetNbinsY()+1
        zmin = tripleCount3d.GetZaxis().FindBin(20)
        zmax = tripleCount3d.GetNbinsZ()+1

        tripleCount = tripleCount3d.ProjectionX("tripleCount", ymin, ymax, zmin, zmax)
        doubleCount = doubleCount3d.ProjectionX("doubleCount", ymin, ymax, zmin, zmax)

        for ibin in range(tripleCount.GetNbinsX()):

            t = tripleCount.GetBinContent(ibin)
            d = doubleCount.GetBinContent(ibin)

            if ichan==0:
                point = tripleCount.GetBinLowEdge(ibin)
                points.append(point)

                totalTriple.append(t)
                totalDouble.append(d)

            else:
                totalTriple[ibin] += t
                totalDouble[ibin] += d


    for ibin in range(len(points)):
        if totalDouble[ibin] == 0:
            print(f"ibin {ibin} is empty")
            continue
        val = totalTriple[ibin]/totalDouble[ibin] * timeDouble/timeTriple
        g_ratio.SetPoint(ibin, points[ibin], val)
        err = timeDouble/timeTriple*totalTriple[ibin]/totalDouble[ibin]*np.sqrt(1/totalTriple[ibin] + 1/totalDouble[ibin])
        g_ratio.SetPointError(ibin, 0, err)
        print(ibin, points[ibin], val)


    c2.cd()

    g_ratio.Draw("AP")
    g_ratio.SetMarkerStyle(8)
    g_ratio.SetTitle("Trigger Efficiency vs Height")
    g_ratio.GetXaxis().SetTitle("Height")
    g_ratio.GetYaxis().SetTitle("Efficiency")

    f2 = r.TF1("f2", "[0] * (0.5 * (1 + TMath::Erf((x - [1]) / ([2] * sqrt(2)))))", 0.001, 10)
    f2.SetParLimits(1, 0.0001, 20)
    f2.SetParLimits(2, 0.1, 10)
    f2.SetParLimits(0, 0.7, 1.3)
    f2.SetParameters(1, 1, 5)
    fitOut = g_ratio.Fit(f2, "SW", "", 8, 500)

    lamb = round(f2.GetParameter(0), 2)
    mu = round(f2.GetParameter(1), 2)
    sigma = round(f2.GetParameter(2), 2)
    chi = round(fitOut.Chi2() / fitOut.Ndf(), 2)

    text1 = r.TLatex()
    text1.SetTextSize(0.03);  
    text1.SetTextColor(r.kRed);  

    text2 = r.TLatex()
    text2.SetTextSize(0.03)
    text2.SetTextColor(r.kRed)

    text1.DrawLatex(100, 0.6, "#lambda: {}, #mu {}".format(lamb, mu))
    text2.DrawLatex(100, 0.5, "#sigma {}, #chi^2/ndof {}".format(sigma, chi))
    c2.SetLogx(1)

    fout.cd()
    c1.Write('efficiencyNPE_allChannels')
    c2.Write('efficiencyHeight_allChannels')
    fout.Close()
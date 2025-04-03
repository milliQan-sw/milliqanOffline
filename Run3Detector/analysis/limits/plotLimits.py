import ROOT as r
import numpy as np
from array import array
import mplhep as hep
from data_points import excluded_points
from data_points import projection_data
import cmsstyle as CMS
from ctypes import c_double as double

def getContour(graph):
    graph.GetHistogram().SetContour(1,array('d',[3.0])) 
    graph.Draw("cont list")
    contourList = []
    #contLevel = graph.GetContourList(3.)
    contLevel = graph.GetContourList(np.log(3.))
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


r.gROOT.SetBatch(1)

# Path to the input file
#input_file = "simYields.txt"
input_file1 = "weightsSR1.txt"
input_file2 = 'weightsSR2.txt'

# Load the data from the file, skipping the first line (header)
data1 = np.loadtxt(input_file1, skiprows=1)
data2 = np.loadtxt(input_file2, skiprows=1)

proj_m, proj_q = zip(*projection_data)
exclude_m, exclude_q = zip(*excluded_points)

exclude_m_filled = list(array('d',exclude_m)) + [exclude_m[-1],exclude_m[0]]
exclude_q_filled = list(array('d',exclude_q)) + [0.32,0.32]


# Assuming the file has three columns: mass, charge, efficiencies
mass = data1[:, 0]  # First column: mass values
charge = data1[:, 1]  # Second column: charge values
yields1 = data1[:, 2]  # Third column: yields (z values)

mass2 = data2[:, 0]  # First column: mass values
charge2 = data2[:, 1]  # Second column: charge values
yields2 = data2[:, 2]  # Third column: yields (z values)

yields = np.maximum(yields1, yields2)
yields = yields *0.88

yields = [1e-10 if x == 0 else x for x in yields]

#To compare with 200 fb^-1 projection, scale yields by 200/140
#We have 124.73 fb^-1 for our current analysis
lumi = 124.73
scale = lumi/140
yields = [x*scale for x in yields]

limit_charges = []
limit_masses = []
limit_yields = []

c1 = CMS.cmsCanvas('c1',1e-1,40,2e-2,3e-1,"Mass [GeV]","Charge (Q/e)",iPos=0, square=False)
#c1 = r.TCanvas()
c1.SetLogx()
c1.SetLogy()
c1.SetLogz()

projectionGraph = r.TGraph(len(proj_m),array('d',proj_m),array('d',proj_q))
projectionGraph.SetLineColor(r.kBlue)
projectionGraph.SetLineWidth(3)
projectionGraph.SetTitle(rf"MilliQan Run 3 Signal Sensitivity at L={str(lumi)} fb^{{-1}};Mass [GeV];Charge Q/e")

c1.GetFrame().SetBorderSize(12)
c1.SetFrameBorderMode(0)
projectionGraph.GetXaxis().CenterTitle(True)
projectionGraph.GetYaxis().CenterTitle(True)
projectionGraph.GetXaxis().SetTitleSize(0.03)
projectionGraph.GetYaxis().SetTitleSize(0.03)
projectionGraph.GetXaxis().SetTitleOffset(1.0)
projectionGraph.GetYaxis().SetTitleOffset(1.0)


#graph2D = r.TGraph2D(len(mass),array('d',mass),array('d',charge),array('d',yields))
graph2D = r.TGraph2D(len(mass),array('d',mass),array('d',charge),array('d',np.log(yields)))
#graph2D.Draw("surf1")
graph1D = getContour(graph2D)
graph1D.SetLineWidth(2)
graph1D.SetLineColor(r.kRed)

excludedGraph = r.TGraph(len(exclude_m),array('d',exclude_m),array('d',exclude_q))
excludedGraph.SetLineColor(r.kBlack)
excludedGraph.SetLineWidth(2)

exclusion_fill = r.TGraph(len(exclude_m_filled),array('d',exclude_m_filled),array('d',exclude_q_filled))
exclusion_fill.SetFillColor(r.kGray)
exclusion_fill.SetFillStyle(1001)

#create graph to fill in SR1/SR2
nBins = projectionGraph.GetN()
xVals1 = []
yVals1 = []
xVals2 = []
yVals2 = []

xd = double(0)
yd = double(0)

# Loop through the points in the first graph and add them to the xVals and yVals lists
for i in range(nBins):
    projectionGraph.GetPoint(i, xd, yd)
    if yd.value > 0.24: continue
    if round(xd.value, 1) == 1.5:
        xVals2.append(xd.value)
        yVals2.append(yd.value)    
        xVals1.append(xd.value)
        yVals1.append(yd.value)   
    elif xd.value>1.5:
        xVals2.append(xd.value)
        yVals2.append(yd.value)
    else:
        xVals1.append(xd.value)
        yVals1.append(yd.value)

# Loop through the points in the second graph and reverse the order for closing the shape
for j, i in enumerate(range(nBins - 1, -1, -1)):
    excludedGraph.GetPoint(i, xd, yd)
    if j==0:
        xVals2.append(xd.value+0.3)
        yVals2.append(yVals2[-1])
    if yd.value > 0.24: continue
    if round(xd.value, 2) == 1.53:
        xVals2.append(xd.value)
        yVals2.append(yd.value)    
        xVals1.append(xd.value)
        yVals1.append(yd.value)   
    elif xd.value > 1.5:
        xVals2.append(xd.value)
        yVals2.append(yd.value)
    else:
        xVals1.append(xd.value)
        yVals1.append(yd.value)       

sr1Graph = r.TGraph(len(xVals1))
for i in range(len(xVals1)):
    sr1Graph.SetPoint(i, xVals1[i], yVals1[i])

sr2Graph = r.TGraph(len(xVals2))
for i in range(len(xVals2)):
    sr2Graph.SetPoint(i, xVals2[i], yVals2[i])

sr1Graph.SetFillColorAlpha(r.kGreen, 0.3)
sr1Graph.SetLineWidth(0)

sr2Graph.SetFillColorAlpha(r.kRed, 0.3)
sr2Graph.SetLineWidth(0)


r.gStyle.SetLineWidth(2)
r.gStyle.SetFrameLineWidth(2)
projectionGraph.GetXaxis().SetTitleSize(0.05)
projectionGraph.GetXaxis().CenterTitle(False)
projectionGraph.GetXaxis().SetTitleOffset(1.18)
projectionGraph.GetYaxis().SetTitleSize(0.05)
projectionGraph.GetYaxis().CenterTitle(False)
projectionGraph.GetYaxis().SetTitleOffset(1.18)
r.gPad.SetLeftMargin(0.13)
projectionGraph.Draw("AL")
#graph1D.Draw("L same")
excludedGraph.Draw("L same")
exclusion_fill.Draw("F")
exclusion_fill.SetFillColorAlpha(r.kBlack, 0.2)
sr1Graph.Draw("F")
sr2Graph.Draw("F")

legend = r.TLegend(0.6, 0.2, 0.8, 0.4)  # x1, y1, x2, y2 (coordinates in the canvas)
#legend.SetHeader("Graphs", "C")  # Centered header
legend.SetTextSize(0.03)
#legend.AddEntry(graph1D, rf"Run 3 {str(lumi)} fb^{{-1}} Limit", "L")  # Add graph1D with line style
legend.AddEntry(projectionGraph, rf"200 fb^{{-1}} Projection", "L")  # Add projectionGraph with line style
legend.Draw()

CMS.SetLumi("")
CMS.SetEnergy("13.6 TeV")
CMS.SetExtraText("Preliminary")

latex = r.TLatex()
latex.SetTextSize(0.06)
latex.SetTextFont(62)
latex.SetTextAlign(13)
latex.DrawLatexNDC(0.15, 0.98, "milliQan Preliminary")

extra = r.TLatex()
latex.SetTextSize(0.05)
latex.SetTextFont(62)
latex.SetTextAlign(13)
#latex.DrawLatexNDC(0.27, 0.975, "Preliminary")

extra = r.TLatex()
latex.SetTextSize(0.05)
latex.SetTextFont(42)
latex.SetTextAlign(13)
latex.DrawLatexNDC(0.82, 0.985, "(13.6 TeV)")

sr1Text = r.TLatex()
sr1Text.SetTextColor(r.kGreen+2)
sr1Text.DrawLatexNDC(0.35, 0.3, 'SR 1')

sr2Text = r.TLatex()
sr2Text.SetTextColor(r.kRed)
sr2Text.DrawLatexNDC(0.7, 0.75, 'SR 2')

paperRef = r.TLatex()
paperRef.SetTextSize(0.025)
paperRef.SetTextFont(42)
paperRef.DrawLatexNDC(0.62, 0.25,'(2021PhRvD.104c2002B)')

c1.SaveAs("limitsLakeLouise.png")



import ROOT as r
from collections import defaultdict
from uncertainties import ufloat
r.gROOT.SetBatch()
r.gStyle.SetOptStat(0)

rangeDict = {}
rangeDict[1640] = 1 
rangeDict[1641] = 2 
rangeDict[1642] = 4 
rangeDict[1643] = 10 
rangeDict[1644] = 20
rangeDict[1645] = 30
rangeDict[1646] = 40 
rangeDict[1647] = 70 
rangeDict[1648] = 70 
rangeDict[1649] = 40 
rangeDict[1650] = 20 
rangeDict[1651] = 10 
rangeDict[1652] = 5 
rangeDict[1653] = 4 
rangeDict[1654] = 4 
rangeDict[1655] = 4 
rangeDict[1656] = 4 
rangeDict[1657] = 4 
rangeDict[1658] = 10 
rangeDict[1659] = 20 
rangeDict[1660] = 40 

rangeDict[1668] = 1
rangeDict[1669] = 10
rangeDict[1670] = 20
rangeDict[1671] = 30
rangeDict[1672] = 40
rangeDict[1673] = 40
rangeDict[1674] = 30
rangeDict[1675] = 10
rangeDict[1676] = 2
rangeDict[1677] = 2
rangeDict[1678] = 2
rangeDict[1679] = 10
rangeDict[1682] = 30
rangeDict[1683] = 40
rangeDict[1684] = 60
rangeDict[1685] = 60
rangeDict[1686] = 60

rangeDict[1687] = 20
rangeDict[1688] = 20
rangeDict[1689] = 20
rangeDict[1690] = 70
rangeDict[1691] = 70
rangeDict[1692] = 70
rangeDict[1692] = 70
rangeDict[1694] = 70

# end to end
# 1687 20cm 0.7hz
# 1688 20cm shielding 0.5hz
# 1689 20cm double shielding 0.5hz
# 1690 70cm 0.42hz
# 1691 70cm shielding 0.37hz
# 1692 70cm longer shielding, bigger solid angle 0.4hz
# 1693 70 cm - light on for few seconds at start
# 1693 70 cm - light off



shieldDict = {}
shieldDict[1640] = 0
shieldDict[1641] = 0 
shieldDict[1642] = 0  
shieldDict[1643] = 0 
shieldDict[1644] = 0
shieldDict[1645] = 0
shieldDict[1646] = 0 
shieldDict[1647] = 0 
shieldDict[1648] = 1 
shieldDict[1649] = 1 
shieldDict[1650] = 1 
shieldDict[1651] = 1 
shieldDict[1652] = 1 
shieldDict[1653] = 1 
shieldDict[1654] = 0 
shieldDict[1655] = 1 
shieldDict[1656] = 0 
shieldDict[1657] = 2 
shieldDict[1658] = 2
shieldDict[1659] = 2 
shieldDict[1660] = 2 

shieldDict[1668] = 0
shieldDict[1669] = 0
shieldDict[1670] = 0
shieldDict[1671] = 0
shieldDict[1672] = 0
shieldDict[1673] = 1
shieldDict[1674] = 1
shieldDict[1675] = 1
shieldDict[1676] = 1
shieldDict[1677] = 0
shieldDict[1678] = 2
shieldDict[1679] = 2
shieldDict[1682] = 2
shieldDict[1683] = 2
shieldDict[1684] = 2
shieldDict[1685] = 1
shieldDict[1686] = 0

shieldDict[1687] = -1
shieldDict[1688] = -2
shieldDict[1689] = -3
# shieldDict[1690] = -1
shieldDict[1691] = -2
shieldDict[1692] = -3
shieldDict[1694] = -1
outHistsAll = {}
outHistsAll["Rate"] = {}
outHistsAll["Height_Ch29"] = {}
outHistsAll["Height_Ch27"] = {}
outHistsAll["Height_Ch10"] = {}
outHistsAll["TD"]= {}
outHistsAll["TDCh10"]= {}
# matched="groupTDC_b0[0]-groupTDC_b1[0]==0"
matched="groupTDC_b0[0]!=-1E5"
rates = defaultdict(list)
meanTime = defaultdict(list)
rmsTime = defaultdict(list)
distances = defaultdict(list)
# heightThresh = 6
areaThresh = 60
chanSel = "area>{0}".format(areaThresh)
for run in range(1668,1695):
    if run not in shieldDict: continue
    inFile = r.TFile("RadiationRuns/Run{0}.root".format(run))
    inTree = inFile.Get("t")
    minTime = inTree.GetMinimum("event_time_fromTDC")
    entries = inTree.Draw("",matched+"&&"+"Sum$(chan==29&&"+chanSel+")>0&&Sum$(chan==27&&"+chanSel+")>0","goff")
    entries = ufloat(entries,entries**0.5)
    # entries = inTree.Draw("","","goff")
    timeDiffForMean = r.TH1D("Run{0}_timeDiffForMean".format(run),"",112,-30,40)
    inTree.Draw("MinIf$(time,chan==29&&"+chanSel+")-MinIf$(time,chan==27&&"+chanSel+")>>{0}".format(timeDiffForMean.GetName()),matched+"&&"+"Sum$(chan==29&&"+chanSel+")>0&&Sum$(chan==27&&"+chanSel+")>0")
    mean = timeDiffForMean.GetMean()
    meanErr = timeDiffForMean.GetMeanError()
    rms = timeDiffForMean.GetRMS()
    rmsErr = timeDiffForMean.GetRMSError()
    meanTime[shieldDict[run]].append(ufloat(mean,meanErr))
    rmsTime[shieldDict[run]].append(ufloat(rms,rmsErr))
    outHistsAll["Rate"][run] = r.TH1D("Run{0}".format(run),"",400,0,100)
    inTree.Draw("event_time_fromTDC-{0}>>{1}".format(minTime,outHistsAll["Rate"][run].GetName()),matched)
    outHistsAll["Rate"][run].SetDirectory(0)
    outHistsAll["TD"][run] = r.TH1D("Run{0}_timeDiff".format(run),"",160,-100,100)
    inTree.Draw("MinIf$(time,chan==29&&"+chanSel+")-MinIf$(time,chan==27&&"+chanSel+")>>{0}".format(outHistsAll["TD"][run].GetName()),matched+"&&"+"Sum$(chan==29&&"+chanSel+")>0&&Sum$(chan==27&&"+chanSel+")>0")
    outHistsAll["TD"][run].SetDirectory(0)
    outHistsAll["TDCh10"][run] = r.TH1D("Run{0}_timeDiffCh10".format(run),"",160,-100,100)
    inTree.Draw("MinIf$(time,chan==10&&"+chanSel+")-MinIf$(time,chan==27&&"+chanSel+")>>{0}".format(outHistsAll["TDCh10"][run].GetName()),matched+"&&"+"Sum$(chan==29&&"+chanSel+")>0&&Sum$(chan==27&&"+chanSel+")>0&&Sum$(chan==10&&"+chanSel+")")
    outHistsAll["TDCh10"][run].SetDirectory(0)
    outHistsAll["Height_Ch29"][run] = r.TH1D("Run{0}_Height_Ch29".format(run),"",100,0,100)
    inTree.Draw("MaxIf$(height,chan==29)>>"+outHistsAll["Height_Ch29"][run].GetName(),matched+"&&"+"Sum$(chan==29&&"+chanSel+")>0&&Sum$(chan==27&&"+chanSel+")>0")
    outHistsAll["Height_Ch29"][run].SetDirectory(0)
    outHistsAll["Height_Ch27"][run] = r.TH1D("Run{0}_Height_Ch27".format(run),"",100,0,100)
    inTree.Draw("MaxIf$(height,chan==27)>>"+outHistsAll["Height_Ch27"][run].GetName(),matched+"&&"+"Sum$(chan==29&&"+chanSel+")>0&&Sum$(chan==27&&"+chanSel+")>0")
    outHistsAll["Height_Ch27"][run].SetDirectory(0)
    outHistsAll["Height_Ch10"][run] = r.TH1D("Run{0}_Height_Ch10".format(run),"",100,0,100)
    inTree.Draw("MaxIf$(height,chan==10)>>"+outHistsAll["Height_Ch10"][run].GetName(),matched+"&&"+"Sum$(chan==29&&"+chanSel+")>0&&Sum$(chan==27&&"+chanSel+")>0")
    outHistsAll["Height_Ch10"][run].SetDirectory(0)
    rate = entries/(inTree.GetMaximum("event_time_fromTDC")-inTree.GetMinimum("event_time_fromTDC"))
    # print run,inTree.GetMaximum("event_time_fromTDC")-inTree.GetMinimum("event_time_fromTDC"),entries,rate
    rates[shieldDict[run]].append(rate)
    distances[shieldDict[run]].append(rangeDict[run])
outDir = "RadiationStudyOutput"
import os
if not os.path.exists(outDir):
    os.mkdir(outDir)
outFile = r.TFile(outDir+"/outFile.root","RECREATE")
outFile.cd()
for run in outHistsAll["Rate"]:
    if shieldDict[run] >= 0:
        shieldLabel = shieldDict[run]
    else:
        shieldLabel = -shieldDict[run]-1
    for plotType in outHistsAll:
        tC = r.TCanvas()
        outHistsAll[plotType][run].Draw()
        tC.SaveAs(outDir+"/{0}_{1}_{2}.pdf".format(outHistsAll[plotType][run].GetName(),rangeDict[run],shieldLabel))
        outHistsAll[plotType][run].Write()

import matplotlib.pyplot as plt
from array import array
outGraphs = []
tC = r.TCanvas()
# tC.SetLogy()
dummyHist = r.TH1D("dummy","",10,0,80)
legend = r.TLegend()
dummyHist.Draw()
colours = {0:r.kBlack,1:r.kBlue,2:r.kRed,-1:r.kBlack,-2:r.kRed,-3:r.kRed}
styles = {0:0,1:0,2:0,-1:2,-2:2,-3:2}
for shield in [-1,-2]:#[-3,-2,-1,0,1,2]:
    ratesN = array('d',[y.n for x,y in sorted(zip(distances[shield],rates[shield]))])
    ratesS = array('d',[y.s for x,y in sorted(zip(distances[shield],rates[shield]))])
    distancesSorted = [x for x in sorted(distances[shield])]

    outGraph = r.TGraphErrors(len(ratesN),array('d',distancesSorted),ratesN,array('d',[0]*len(ratesN)),ratesS)
    outGraph.SetLineColor(colours[shield])
    # print ratesN
    # print distances[shield]
    # plt.plot(distances[shield],rates[shield],label=str(shield))
    # if shield >= 0:
    #     legend.AddEntry(outGraph,"Side-by-side with shield level {0}".format(shield))
    # else:
    #     legend.AddEntry(outGraph,"End-to-end with shield level {0}".format(-(shield+1)))
    if shield == 0:
        legend.AddEntry(outGraph,"Side-by-side without shield")
    elif shield == -1:
        legend.AddEntry(outGraph,"End-to-end without shield")
    elif shield == -2:
        legend.AddEntry(outGraph,"End-to-end with shield")
    else:
        legend.AddEntry(outGraph,"Side-by-side with shield")
    outGraph.Draw("sameLP")
    outGraphs.append(outGraph)
dummyHist.SetMaximum(1)
dummyHist.SetMinimum(0.1)
legend.Draw("same")
tC.SaveAs("RadiationStudyOutput/overallRate.pdf")

dummyHist.Clear()
legend = r.TLegend()
dummyHist.Draw()

for shield in [-1,-2]:#[-3,-2,-1,0,1,2]:
    meanTimeN = array('d',[y.n for x,y in sorted(zip(distances[shield],meanTime[shield]))])
    meanTimeS = array('d',[y.s for x,y in sorted(zip(distances[shield],meanTime[shield]))])
    distancesSorted = [x for x in sorted(distances[shield])]
    outGraph = r.TGraphErrors(len(meanTimeN),array('d',distancesSorted),meanTimeN,array('d',[0]*len(meanTimeN)),meanTimeS)
    outGraph.SetLineColor(colours[shield])
    if shield == 0:
        legend.AddEntry(outGraph,"Side-by-side without shield")
    elif shield == -1:
        legend.AddEntry(outGraph,"End-to-end without shield")
    elif shield == -2:
        legend.AddEntry(outGraph,"End-to-end with shield")
    else:
        legend.AddEntry(outGraph,"Side-by-side with shield")
    outGraph.Draw("sameLP")
    outGraphs.append(outGraph)
tC.SetLogy(0)
dummyHist.SetMaximum(10)
dummyHist.SetMinimum(0)
legend.Draw("same")
tC.SaveAs("RadiationStudyOutput/overallMeans.pdf")

dummyHist.Clear()
legend = r.TLegend()
dummyHist.Draw()
for shield in [-1,-2]:#[-3,-2,-1,0,1,2]:
    rmsTimeN = array('d',[y.n for x,y in sorted(zip(distances[shield],rmsTime[shield]))])
    rmsTimeS = array('d',[y.s for x,y in sorted(zip(distances[shield],rmsTime[shield]))])
    distancesSorted = [x for x in sorted(distances[shield])]
    outGraph = r.TGraphErrors(len(rmsTimeN),array('d',distancesSorted),rmsTimeN,array('d',[0]*len(rmsTimeN)),rmsTimeS)
    outGraph.SetLineColor(colours[shield])
    if shield == 0:
        legend.AddEntry(outGraph,"Side-by-side without shield")
    elif shield == -1:
        legend.AddEntry(outGraph,"End-to-end without shield")
    elif shield == -2:
        legend.AddEntry(outGraph,"End-to-end with shield")
    else:
        legend.AddEntry(outGraph,"Side-by-side with shield")
    outGraph.Draw("sameLP")
    outGraphs.append(outGraph)

dummyHist.SetMaximum(20)
dummyHist.SetMinimum(0)
legend.Draw("same")
tC.SaveAs("RadiationStudyOutput/overallRMSs.pdf")
# plt.legend()
# plt.savefig("RadiationStudyOutput/overallRate.pdf")

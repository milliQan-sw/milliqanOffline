import ROOT as r
import sys
import pandas as pd
sys.path.append('../')
r.gROOT.SetBatch()
r.gStyle.SetOptStat(0)
from measureBackgroundsClean import totalRunTime
from config import tag as outtag
from uncertainties import ufloat

def getIntegralAndError(hist,low,high):
    error = r.Double(0)
    integral = hist.IntegralAndError(hist.FindBin(low),hist.FindBin(high-1E-3),error)
    return ufloat(integral,error)

outputFile = r.TFile("backgroundsSimple.root","RECREATE")
# if __name__=="__main__":
#     for lpf in ["LPFilter","NoLPFilter","LPFilter_try8"][-1:]:
#         makePulseInjectionStudies("pulseInjection{}.root".format(lpf),"{}PulseInjectionResults.root".format(lpf))
# inputFileNoBeam = r.TFile("../outputFileABCDnoBeamFull2018DatasetAll_VALIDATEMay19.root")
# inputFileBeam = r.TFile("../outputFileABCDnoBeamFull2018DatasetAll_VALIDATEMay19.root")

versionTag = "V19_finalForUnblindingMinNPEForVeto0p5"
inputFileNoBeam = r.TFile("../outputFileABCDnoBeam{0}_15ns.root".format(versionTag))
inputFileBeam = r.TFile("../outputFileABCDbeam{0}InvertPanel_15ns.root".format(versionTag))
# inputFileBeam = r.TFile("../outputFileABCDbeamRand10V19_finalForUnblindingMinNPEForVeto0p5_rand10ForBeam_15ns.root")
# inputFileBeam = r.TFile("../outputFileABCDBeamRand10{0}_15ns.root".format(versionTag))
# inputFileBeam = r.TFile("../outputFileABCDbeamBlind{0}_15ns.root".format(versionTag))
# inputFileBeam = r.TFile("../outputFileABCDbeamBlind{0}_15ns.root".format(versionTag))
# versionTag = "V16_finalForPreliminaryLimit"
# inputFileNoBeam = r.TFile("../outputFileABCDnoBeamsignalInjectionStudies191204{0}_15ns.root".format(versionTag))
# inputFileBeam = r.TFile("../outputFileABCDbeamBlindsignalInjectionStudies191204{0}_15ns.root".format(versionTag))
tag = "{0}_15ns".format(versionTag)

# inputFileNoBeam = r.TFile("../outputFileABCDnoBeamFull2018DatasetAll_VALIDATEMay1915ns.root")
# inputFileBeam = r.TFile("../outputFileABCDnoBeamFull2018DatasetAll_VALIDATEMay1915ns.root")
scaleToString = "beam"
npeThreshDict = {"":[2.,20.],"PlusSlab":[5.,30.],"PlusTwoOrMoreSlabs":[0.5,1E6]}
outputDict = {}
data = {'mass':[-1],'charge':[-1],'StraightYieldLow':[],'StraightYieldLowGamma':[],'StraightYieldLowNoBeamSyst':[],'StraightYieldHigh':[],'StraightYieldHighGamma':[],'StraightYieldHighNoBeamSyst':[],'StraightPlusTwoOrMoreSlabsYieldLow':[],'StraightPlusTwoOrMoreSlabsYieldLowGamma':[],'StraightPlusTwoOrMoreSlabsYieldLowNoBeamSyst':[],'StraightPlusSlabYieldLow':[],'StraightPlusSlabYieldLowGamma':[],'StraightPlusSlabYieldLowNoBeamSyst':[],'StraightPlusSlabYieldHigh':[],'StraightPlusSlabYieldHighGamma':[],'StraightPlusSlabYieldHighNoBeamSyst':[]}
for plusSlab in ["","PlusSlab","PlusTwoOrMoreSlabs"]:
    if plusSlab == "":
        plusSlabString = "NoSlab"
    else:
        plusSlabString = plusSlab
    for npe in ["Min","MinCorr"][-1:]:
        for pulseSel in ["NoOtherPulse","NoPrePulse","NoPrePulsePlusPanelHit"][-1:]:
            inputHistNoBeamA = inputFileNoBeam.Get("{2}/max/NPE{0}/All{1}/A".format(npe,plusSlab,pulseSel))
            inputHistNoBeamB = inputFileNoBeam.Get("{2}/max/NPE{0}/All{1}/D".format(npe,plusSlab,pulseSel))
            inputHistNoBeamC = inputFileNoBeam.Get("{2}/max/NPE{0}/All{1}/B".format(npe,plusSlab,pulseSel))
            inputHistNoBeamD = inputFileNoBeam.Get("{2}/max/NPE{0}/All{1}/C".format(npe,plusSlab,pulseSel))
            # for iBin in range(1,inputHistNoBeamA.GetNbinsX()+1):
            #     print (inputHistNoBeamA.GetBinLowEdge(iBin))

            inputHistBeamA = inputFileBeam.Get("{2}/max/NPE{0}/All{1}/A".format(npe,plusSlab,pulseSel))
            inputHistBeamB = inputFileBeam.Get("{2}/max/NPE{0}/All{1}/D".format(npe,plusSlab,pulseSel))
            inputHistBeamC = inputFileBeam.Get("{2}/max/NPE{0}/All{1}/B".format(npe,plusSlab,pulseSel))
            inputHistBeamD = inputFileBeam.Get("{2}/max/NPE{0}/All{1}/C".format(npe,plusSlab,pulseSel))

            hists = [inputHistNoBeamB,inputHistNoBeamC,inputHistNoBeamD,inputHistBeamB,inputHistBeamC,inputHistBeamD]
            for hist in hists: hist.Scale(totalRunTime[scaleToString]/3600.)

            inputHistNoBeamAPred = inputFileNoBeam.Get("{2}/max/NPE{0}/All{1}/APred".format(npe,plusSlab,pulseSel))
            inputHistBeamAPred = inputFileBeam.Get("{2}/max/NPE{0}/All{1}/APred".format(npe,plusSlab,pulseSel))
            inputHistBeamAPred.Scale(totalRunTime[scaleToString]/3600.)
            inputHistNoBeamA.Scale(totalRunTime[scaleToString]/3600.)
            inputHistNoBeamAPred.Scale(totalRunTime[scaleToString]/3600.)
            if plusSlab == "":
                inputHistNoBeamAPred.SetMinimum(0.1)
                inputHistNoBeamAPred.SetMaximum(500)
                inputHistNoBeamA.SetMinimum(0.1)
                inputHistNoBeamA.SetMaximum(500)
                inputHistBeamAPred.SetMinimum(0.1)
                inputHistBeamAPred.SetMaximum(500)
            else:
                inputHistNoBeamAPred.SetMinimum(0.1)
                inputHistNoBeamAPred.SetMaximum(20)
                inputHistNoBeamA.SetMinimum(0.1)
                inputHistNoBeamA.SetMaximum(20)
                inputHistBeamAPred.SetMinimum(0.1)
                inputHistBeamAPred.SetMaximum(20)
            # inputHistBeamA.SetMinimum(0.1)
            # inputHistBeamA.SetMaximum(200)
            leg = r.TLegend(0.6,0.65,0.89,0.89)
            leg.SetBorderSize(0)

            tempC = r.TCanvas()
            tempC.SetLogx()
            tempC.SetLogy()
            inputHistNoBeamA.GetXaxis().SetTitle("{0}(NPE)".format(npe))
            inputHistNoBeamA.GetYaxis().SetTitle("Total background")
            inputHistNoBeamA.GetYaxis().SetTitleSize(0.05)
            inputHistNoBeamA.GetYaxis().SetTitleOffset(0.9)
            inputHistNoBeamAPred.SetTitle("")
            inputHistNoBeamA.GetXaxis().SetTitleSize(0.05)
            # inputHistNoBeamA.GetXaxis().SetTitleOffset(1.1)
            inputHistNoBeamAPred.Draw("")
            inputHistNoBeamAPred.GetXaxis().SetRangeUser(0.5,1E4)
            maxVal = inputHistNoBeamA.GetMaximum()
            inputHistNoBeamAPred.SetLineColor(r.kRed)
            inputHistNoBeamA.Draw("same")
            if "Min" in npe:
                # print ("No Beam D")
                # print (inputHistNoBeamD.Integral(0,-1))
                # print ("Beam D")
                # print (inputHistBeamD.Integral(0,-1))
                print (pulseSel,plusSlabString)
                print ("No Beam")
                obsL = getIntegralAndError(inputHistNoBeamA,npeThreshDict[plusSlab][0],npeThreshDict[plusSlab][1])
                yieldLB = getIntegralAndError(inputHistNoBeamB,npeThreshDict[plusSlab][0],npeThreshDict[plusSlab][1])
                yieldLC = getIntegralAndError(inputHistNoBeamC,npeThreshDict[plusSlab][0],npeThreshDict[plusSlab][1])
                yieldLD = getIntegralAndError(inputHistNoBeamD,npeThreshDict[plusSlab][0],npeThreshDict[plusSlab][1])
                print (yieldLB,yieldLC,yieldLD)
                if yieldLD > 0:
                    predL = yieldLB*yieldLC/yieldLD
                else:
                    predL = ufloat(0,0)

                obsH = getIntegralAndError(inputHistNoBeamA,npeThreshDict[plusSlab][1],1E6)
                yieldHB = getIntegralAndError(inputHistNoBeamB,npeThreshDict[plusSlab][1],1E6)
                yieldHC = getIntegralAndError(inputHistNoBeamC,npeThreshDict[plusSlab][1],1E6)
                yieldHD = getIntegralAndError(inputHistNoBeamD,npeThreshDict[plusSlab][1],1E6)
                if yieldHD > 0:
                    predH = yieldHB*yieldHC/yieldHD
                else:
                    predH = ufloat(0,0)
                print (yieldHB,yieldHC,yieldHD)

                print ("Low NPE pred:","%.2f ± %.2f" % (predL.n,predL.s),"obs:","%.2f" % obsL.n)
                print ("High NPE pred:","%.2f ± %.2f" % (predH.n,predH.s), "obs:","%.2f" % obsH.n)

                if predL.n > 0 and obsL.n > 0:
                    data["Straight"+plusSlab+"YieldLowNoBeamSyst"].append(obsL.n/predL.n)
                else:
                    data["Straight"+plusSlab+"YieldLowNoBeamSyst"].append(2)
                if plusSlab != "PlusTwoOrMoreSlabs":
                    if predH.n > 0 and obsH.n > 0:
                        data["Straight"+plusSlab+"YieldHighNoBeamSyst"].append(obsH.n/predH.n)
                    else:
                        data["Straight"+plusSlab+"YieldHighNoBeamSyst"].append(2)

                print ("Beam")
                obsL = getIntegralAndError(inputHistBeamA,npeThreshDict[plusSlab][0],npeThreshDict[plusSlab][1])
                yieldLB = getIntegralAndError(inputHistBeamB,npeThreshDict[plusSlab][0],npeThreshDict[plusSlab][1])
                yieldLC = getIntegralAndError(inputHistBeamC,npeThreshDict[plusSlab][0],npeThreshDict[plusSlab][1])
                yieldLD = getIntegralAndError(inputHistBeamD,npeThreshDict[plusSlab][0],npeThreshDict[plusSlab][1])
                print (yieldLB,yieldLC,yieldLD)
                if yieldLD > 0:
                    predL = yieldLB*yieldLC/yieldLD
                else:
                    predL = ufloat(0,0)

                obsH = getIntegralAndError(inputHistBeamA,npeThreshDict[plusSlab][1],1E6)
                yieldHB = getIntegralAndError(inputHistBeamB,npeThreshDict[plusSlab][1],1E6)
                yieldHC = getIntegralAndError(inputHistBeamC,npeThreshDict[plusSlab][1],1E6)
                yieldHD = getIntegralAndError(inputHistBeamD,npeThreshDict[plusSlab][1],1E6)
                if yieldHD > 0:
                    predH = yieldHB*yieldHC/yieldHD
                else:
                    predH = ufloat(0,0)

                print (yieldHB,yieldHC,yieldHD)
                print ("Low NPE pred:","%.2f ± %.2f" % (predL.n,predL.s),"obs:","%.2f" % obsL.n)
                print ("High NPE pred:","%.2f ± %.2f" % (predH.n,predH.s),"%.2f" % obsH.n)
                data["Straight"+plusSlab+"YieldLow"].append(predL.n) 
                if predL.n > 0:
                    data["Straight"+plusSlab+"YieldLowGamma"].append(round((predL.n/predL.s)**2)) 
                else:
                    if yieldLD > 0:
                        data["Straight"+plusSlab+"YieldLowGamma"].append(yieldLB.n/yieldLD.n) 
                    else:
                        data["Straight"+plusSlab+"YieldLowGamma"].append(0) 
                if plusSlab != "PlusTwoOrMoreSlabs":
                    data["Straight"+plusSlab+"YieldHigh"].append(predH.n) 
                    if predH.n > 0:
                        data["Straight"+plusSlab+"YieldHighGamma"].append(round((predH.n/predH.s)**2)) 
                    else:
                        if yieldHD > 0:
                            data["Straight"+plusSlab+"YieldHighGamma"].append(yieldHC.n/yieldHD.n) 
                        else:
                            data["Straight"+plusSlab+"YieldHighGamma"].append(0) 

            leg.AddEntry(inputHistNoBeamA,"Observation")
            leg.AddEntry(inputHistNoBeamAPred,"ABCD Prediction")
            leg.Draw()
            tempC.SaveAs("backgroundYieldsNoBeam_15ns_{0}_{1}_{2}_{3}.pdf".format(npe,plusSlabString,tag,pulseSel))
            tempC.Clear()
            outputFile.cd()
            inputHistNoBeamA.SetName("backgroundPerNPENoBeamMeasurement")
            inputHistNoBeamA.Write()

            leg.Clear()
            inputHistBeamAPred.SetLineStyle(2)
            #inputHistNoBeamAPred.Scale(totalRunTime["beam"]/totalRunTime["noBeam"])
            leg.AddEntry(inputHistNoBeamAPred,"Prediction (no beam)")
            leg.AddEntry(inputHistBeamAPred,"Prediction (with beam)")
            inputHistBeamAPred.SetTitle("")
            inputHistBeamAPred.Draw("")
            inputHistBeamAPred.GetXaxis().SetRangeUser(0.5,1E4)
            inputHistNoBeamAPred.Draw("same")
            leg.Draw()
            tempC.SaveAs("backgroundYieldsWithBeam_15ns_{0}_{1}_{2}_{3}.pdf".format(npe,plusSlabString,tag,pulseSel))
            tempC.Clear()

            # perPathDir = inputFileNoBeam.Get("NoOtherPulse/max/NPE{0}/All/perPathRates".format(npe))
            # colours = [r.kRed,r.kBlue,r.kGreen,r.kYellow+1,r.kOrange,r.kCyan+1]
            # i = -1
            # legend = r.TLegend(0.6,0.7,0.89,0.89)
            # legend.SetBorderSize(0)
            # inputHistNoBeamA.SetLineColor(0)
            # inputHistNoBeamA.SetMarkerColor(0)
            # inputHistNoBeamA.Draw()
            # for key in perPathDir.GetListOfKeys():
            #     i += 1
            #     hist = key.ReadObj()
            #     hist.GetXaxis().SetRangeUser(1E-4,1E4)
            #     hist.SetLineColor(colours[i])
            #     hist.SetMarkerColor(colours[i])
            #     hist.Scale(totalRunTime["beam"]/3600.)
            #     if "_6"  in hist.GetName(): 
            #         hist.SetLineWidth(2)
            #     if i == 0:
            #         hist.Draw("same")
            #     else:
            #         hist.Draw("same")
            #     legend.AddEntry(hist,hist.GetName().replace("_"," "))
            # legend.Draw()
            # tempC.SaveAs("perPathPlotsNoBeam.pdf")
df = pd.DataFrame(data)
df.to_csv("backgroundYields_{0}.csv".format(outtag))
outputFile.Close()

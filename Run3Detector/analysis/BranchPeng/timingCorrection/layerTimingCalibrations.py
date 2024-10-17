import pandas as pd
import ROOT as r 

def getRunTime():

    #define the runs used in beam on/off data
    beamOnRuns = [1400, 1800]
    beamOffRuns = [1300, 1800]

    #open the lumi file
    lumis = pd.read_json('/share/scratch0/peng/CMSSW_12_4_11_patch3/src/milliqanOffline/Run3Detector/configuration/mqLumis.json', orient='split', compression='infer')

    #make sure start/stop are datetimes
    lumis['start'] = pd.to_datetime(lumis['start'])
    lumis['stop'] = pd.to_datetime(lumis['stop'])

    #get all beam on/off files in run ranges
    beamOn = lumis[(lumis['run'] >= beamOnRuns[0]) & (lumis['run'] < beamOnRuns[1]) & (lumis['beamInFill']==True)]
    beamOff = lumis[(lumis['run'] >= beamOffRuns[0]) & (lumis['run'] < beamOffRuns[1]) & (lumis['beamInFill']==False)]

    #calculate total lumi in beam on datasetc
    totalLumi = beamOn['lumiEst'].sum()

    #calculate total time of runs in seconds
    runTimeOn = (beamOn['stop'] - beamOn['start']).sum().total_seconds()
    runTimeOff = (beamOff['stop'] - beamOff['start']).sum().total_seconds()

    print("Beam on runs ran for {}s with lumi {}pb^-1".format(runTimeOn, totalLumi))
    print("Beam off runs ran for {}s".format(runTimeOff))

    scale = runTimeOff/runTimeOn

    print("Scale to normalize beam data {}".format(scale))

    return runTimeOn, runTimeOff

if __name__ == "__main__":

    #stop python from displaying canvases
    r.gROOT.SetBatch(1)

    #define output file to write out root plots
    fout = r.TFile.Open("timingCalibrationPlots.root", "RECREATE")

    #get the total run time for beam on/off
    runTimeOn, runTimeOff = getRunTime()

    #open the plots of time difference between front slab and each channel for beam on/off
    f_beamOn = r.TFile.Open('/data/users/mcarrigan/milliqan/timingCorrections/timingCorrection_beamOn.root', 'READ')
    f_beamOff = r.TFile.Open('/data/users/mcarrigan/milliqan/timingCorrections/timingCorrection_beamOff.root', 'READ')

    #create a TCanvas for plots of each layer
    c_l1 = r.TCanvas("c_l1", "Layer 1", 1400, 1400)
    c_l2 = r.TCanvas("c_l2", "Layer 2", 1400, 1400)
    c_l3 = r.TCanvas("c_l3", "Layer 3", 1400, 1400)
    c_l4 = r.TCanvas("c_l4", "Layer 4", 1400, 1400)

    #divide each canvas into 16 plots for each channel in a layer
    c_l1.Divide(4, 4)
    c_l2.Divide(4, 4)
    c_l3.Divide(4, 4)
    c_l4.Divide(4, 4)

    timeCanvases = [c_l1, c_l2, c_l3, c_l4]

    #create fit bounds for each channel in the beam on dataset
    boundsOn = [
        [-25, -13], [-40, 0], [-40, 0], [-20, -12], [-35, -22], [-25, -19], [-32, -21], [-40, 0],
        [-40, 0], [-25, -13], [-40, 0], [-40, 0], [-40, 0], [-35, -23], [-40, 0], [-40, 0],

        [-15, -9], [-20, -12], [-30, 10], [-30, 10], [-30, 10], [-25, -15], [-20, -13], [-30, 10],
        [-30, 10], [-30, 10], [-30, 10], [-30, 10], [-30, 10], [-30, 10], [-30, 10], [-30, 10],

        [-20, 20], [-20, 20], [-20, 20], [-20, 20], [-20, 20], [-20, 20], [-20, 20], [-20, 20],
        [-20, 20], [-20, 20], [-20, 20], [-20, 20], [-20, 20], [-20, 20], [-20, 20], [-20, 20],

        [-10, 30], [-10, 30], [-10, 30], [-10, 30], [-10, 30], [-10, 30], [-10, 30], [-10, 30],
        [-10, 30], [-10, 30], [-10, 30], [-10, 30], [-10, 30], [-10, 30], [-10, 30], [-7, 2]
    ]

    #create fit bounds for each channel in the beam off dataset
    boundsOff = [
        [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0],
        [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0],

        [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0],
        [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0],

        [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0],
        [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0],

        [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0],
        [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0]
    ]

    h_timeDiff_beamOn.Scale(1./runTimeOn)
    h_timeDiff_beamOff.Scale(1./runTimeOff)
    h_timeDiff_beamOn.Draw("hist")
    h_timeDiff_beamOn.SetTitle("Time Difference L3-L0")
    h_timeDiff_beamOn.GetXaxis().SetTitle("#Delta t (ns)")
    h_timeDiff_beamOn.GetYaxis().SetTitle("Events/s")
    h_timeDiff_beamOff.Draw("hist same")

    f_on = r.TF1('f_on', 'gaus', -20, 20)
    f_onMod = r.TF1('f_onMod', 'gaus', -20, 20)
    f_off = r.TF1('f_off', 'gaus', -40, 10)

    out_on = h_timeDiff_beamOn.Fit(f_on, "0", "", -20, 20)
    out_off = h_timeDiff_beamOff.Fit(f_off, "0", "", -40, 10)

    f_off.SetLineColor(2)
    f_on.SetLineColor(4)
    f_on.Draw("same")
    f_off.Draw("same")

    h_timeDiff_mod = h_timeDiff_beamOn.Clone()
    for ibin in range(h_timeDiff_beamOn.GetNbinsX()):
        center = h_timeDiff_beamOn.GetBinCenter(ibin)
        bkgd = f_off.Eval(center)
        if bkgd < 0: bkgd = 0
        beamOnVal = h_timeDiff_beamOn.GetBinContent(ibin)
        fillVal = beamOnVal - bkgd
        print(f"beam val {beamOnVal}, background {bkgd}, fill {fillVal}")
        h_timeDiff_mod.SetBinContent(ibin, fillVal)

    out_onMod = h_timeDiff_mod.Fit(f_onMod, "0", "", -20, 20)
    f_onMod.SetLineColor(1)
    h_timeDiff_mod.SetLineColor(1)
    f_onMod.Draw("same")
    h_timeDiff_mod.Draw("same")

    l1 = r.TLegend(0.2, 0.7, 0.4, 0.9)
    l1.AddEntry(h_timeDiff_beamOn, "Beam On #mu {}, #sigma {}".format(round(f_on.GetParameter(1), 2), round(f_on.GetParameter(2), 2)), "l")
    l1.AddEntry(h_timeDiff_beamOff, "Beam Off #mu {}, #sigma {}".format(round(f_off.GetParameter(1), 2), round(f_off.GetParameter(2), 2)), "l")
    l1.AddEntry(h_timeDiff_mod, "Beam On Mod #mu {}, #sigma {}".format(round(f_onMod.GetParameter(1), 2), round(f_onMod.GetParameter(2), 2)), "l")

    l1.Draw()
    c1.Draw()
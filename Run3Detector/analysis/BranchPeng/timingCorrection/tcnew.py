import pandas as pd
import ROOT as r 

def getRunTime():
    beamOnRuns = [1400, 1800]
    beamOffRuns = [1300, 1800]

    lumis = pd.read_json('/share/scratch0/peng/CMSSW_12_4_11_patch3/src/milliqanOffline/Run3Detector/configuration/mqLumis.json', orient='split', compression='infer')

    lumis['start'] = pd.to_datetime(lumis['start'])
    lumis['stop'] = pd.to_datetime(lumis['stop'])

    beamOn = lumis[(lumis['run'] >= beamOnRuns[0]) & (lumis['run'] < beamOnRuns[1]) & (lumis['beamInFill'] == True)]
    beamOff = lumis[(lumis['run'] >= beamOffRuns[0]) & (lumis['run'] < beamOffRuns[1]) & (lumis['beamInFill'] == False)]

    totalLumi = beamOn['lumiEst'].sum()

    runTimeOn = (beamOn['stop'] - beamOn['start']).sum().total_seconds()
    runTimeOff = (beamOff['stop'] - beamOff['start']).sum().total_seconds()

    print("Beam on runs ran for {}s with lumi {}pb^-1".format(runTimeOn, totalLumi))
    print("Beam off runs ran for {}s".format(runTimeOff))

    scale = runTimeOff / runTimeOn

    print("Scale to normalize beam data {}".format(scale))

    return runTimeOn, runTimeOff

if __name__ == "__main__":
    r.gROOT.SetBatch(1)

    fout = r.TFile.Open("timingCalibrationPlots.root", "RECREATE")

    runTimeOn, runTimeOff = getRunTime()

    f_beamOn = r.TFile.Open('/data/users/mcarrigan/milliqan/timingCorrections/timingCorrection_beamOn.root', 'READ')
    f_beamOff = r.TFile.Open('/data/users/mcarrigan/milliqan/timingCorrections/timingCorrection_beamOff.root', 'READ')

    c_l1 = r.TCanvas("c_l1", "Layer 1", 1400, 1400)
    c_l2 = r.TCanvas("c_l2", "Layer 2", 1400, 1400)
    c_l3 = r.TCanvas("c_l3", "Layer 3", 1400, 1400)
    c_l4 = r.TCanvas("c_l4", "Layer 4", 1400, 1400)

    c_l1.Divide(4, 4)
    c_l2.Divide(4, 4)
    c_l3.Divide(4, 4)
    c_l4.Divide(4, 4)

    timeCanvases = [c_l1, c_l2, c_l3, c_l4]

    boundsOn = [[-40, 0]] * 16 + [[-30, 10]] * 16 + [[-20, 20]] * 16 + [[-10, 30]] * 16
    boundsOff = [[-40, 0]] * 64

    for i in range(64):
        h_on = f_beamOn.Get(f'h_timeDiffFrontPanel{i}')
        h_off = f_beamOff.Get(f'h_timeDiffFrontPanel{i}')

        h_on.Scale(1. / runTimeOn)
        h_off.Scale(1. / runTimeOff)

        f_on = r.TF1('f_on', 'gaus', boundsOn[i][0], boundsOn[i][1])
        f_off = r.TF1('f_off', 'gaus', boundsOff[i][0], boundsOff[i][1])

        h_on.Fit(f_on, "0", "", boundsOn[i][0], boundsOn[i][1])
        h_off.Fit(f_off, "0", "", boundsOff[i][0], boundsOff[i][1])

        f_off.SetLineColor(2)
        f_on.SetLineColor(4)

        if i % 16 == 0:
            timeCanvases[i // 16].cd()
        timeCanvases[i // 16].cd(i % 16 + 1)

        h_on.Draw("hist")
        h_off.Draw("hist same")
        f_on.Draw("same")
        f_off.Draw("same")

        # Create and position TPaveText box for fit parameters
        stats = r.TPaveText(0.6, 0.6, 0.9, 0.9, "NDC")
        stats.SetTextAlign(12)
        stats.SetTextSize(0.03)
        stats.SetFillColor(0)

        # Add mean, stddev, and chi2/ndof for beamOn
        stats.AddText(f"Beam On (Blue):")
        stats.AddText(f"  Mean: {f_on.GetParameter(1):.2f}")
        stats.AddText(f"  StdDev: {f_on.GetParameter(2):.2f}")
        stats.AddText(f"  Chi2/NDOF: {f_on.GetChisquare()/f_on.GetNDF():.2f}")

        # Add mean, stddev, and chi2/ndof for beamOff
        stats.AddText(f"Beam Off (Red):")
        stats.AddText(f"  Mean: {f_off.GetParameter(1):.2f}")
        stats.AddText(f"  StdDev: {f_off.GetParameter(2):.2f}")
        stats.AddText(f"  Chi2/NDOF: {f_off.GetChisquare()/f_off.GetNDF():.2f}")

        stats.Draw()

    fout.cd()
    c_l1.Write("FitsL1")
    c_l2.Write("FitsL2")
    c_l3.Write("FitsL3")
    c_l4.Write("FitsL4")

    fout.Close()
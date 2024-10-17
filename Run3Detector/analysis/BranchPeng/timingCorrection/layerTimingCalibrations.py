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

    # Stop python from displaying canvases
    r.gROOT.SetBatch(1)

    # Define output file to write out root plots
    fout = r.TFile.Open("timingCalibrationPlots.root", "RECREATE")

    # Get the total run time for beam on/off
    runTimeOn, runTimeOff = getRunTime()

    # Open the plots of time difference between front slab and each channel for beam on/off
    f_beamOn = r.TFile.Open('/data/users/mcarrigan/milliqan/timingCorrections/timingCorrection_beamOn.root', 'READ')
    f_beamOff = r.TFile.Open('/data/users/mcarrigan/milliqan/timingCorrections/timingCorrection_beamOff.root', 'READ')

    # Create combined histograms for layers 3 and 0
    h_timeDiff_beamOn = f_beamOn.Get('h_timeDiffFrontPanel0').Clone("h_timeDiff_beamOn")
    h_timeDiff_beamOff = f_beamOff.Get('h_timeDiffFrontPanel0').Clone("h_timeDiff_beamOff")

    # Add histograms from other channels in layers 3 and 0 (16 channels each layer)
    for i in range(1, 16):
        h_timeDiff_beamOn.Add(f_beamOn.Get(f'h_timeDiffFrontPanel{i}'))
        h_timeDiff_beamOff.Add(f_beamOff.Get(f'h_timeDiffFrontPanel{i}'))

    # Normalize by run times
    h_timeDiff_beamOn.Scale(1. / runTimeOn)
    h_timeDiff_beamOff.Scale(1. / runTimeOff)

    # Set titles and labels
    h_timeDiff_beamOn.SetTitle("Time Difference L3-L0")
    h_timeDiff_beamOn.GetXaxis().SetTitle("#Delta t (ns)")
    h_timeDiff_beamOn.GetYaxis().SetTitle("Events/s")

    # Draw histograms
    c1 = r.TCanvas("c1", "Combined Time Difference", 800, 600)
    h_timeDiff_beamOn.Draw("hist")
    h_timeDiff_beamOff.Draw("hist same")

    # Perform fits on combined histograms
    f_on = r.TF1('f_on', 'gaus', -20, 20)
    f_off = r.TF1('f_off', 'gaus', -40, 10)
    h_timeDiff_beamOn.Fit(f_on, "0", "", -20, 20)
    h_timeDiff_beamOff.Fit(f_off, "0", "", -40, 10)

    f_off.SetLineColor(2)
    f_on.SetLineColor(4)
    f_on.Draw("same")
    f_off.Draw("same")

    # Subtract background and fit modified histogram
    h_timeDiff_mod = h_timeDiff_beamOn.Clone("h_timeDiff_mod")
    for ibin in range(h_timeDiff_beamOn.GetNbinsX()):
        center = h_timeDiff_beamOn.GetBinCenter(ibin)
        bkgd = f_off.Eval(center)
        bkgd = max(bkgd, 0)  # ensure no negative background
        fillVal = h_timeDiff_beamOn.GetBinContent(ibin) - bkgd
        h_timeDiff_mod.SetBinContent(ibin, fillVal)

    # Fit and draw modified histogram
    f_onMod = r.TF1('f_onMod', 'gaus', -20, 20)
    h_timeDiff_mod.Fit(f_onMod, "0", "", -20, 20)
    f_onMod.SetLineColor(1)
    h_timeDiff_mod.SetLineColor(1)
    h_timeDiff_mod.Draw("hist same")
    f_onMod.Draw("same")

    # Add legend and draw canvas
    l1 = r.TLegend(0.2, 0.7, 0.4, 0.9)
    l1.AddEntry(h_timeDiff_beamOn, f"Beam On #mu={f_on.GetParameter(1):.2f}, #sigma={f_on.GetParameter(2):.2f}", "l")
    l1.AddEntry(h_timeDiff_beamOff, f"Beam Off #mu={f_off.GetParameter(1):.2f}, #sigma={f_off.GetParameter(2):.2f}", "l")
    l1.AddEntry(h_timeDiff_mod, f"Beam On Mod #mu={f_onMod.GetParameter(1):.2f}, #sigma={f_onMod.GetParameter(2):.2f}", "l")
    l1.Draw()

    c1.Write()
    fout.Close()
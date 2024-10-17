import pandas as pd
import ROOT as r 

def getRunTime():
    # Define the runs used in beam on/off data
    beamOnRuns = [1400, 1800]
    beamOffRuns = [1300, 1800]

    # Open the lumi file
    lumis = pd.read_json('/share/scratch0/peng/CMSSW_12_4_11_patch3/src/milliqanOffline/Run3Detector/configuration/mqLumis.json', orient='split', compression='infer')

    # Ensure start/stop are datetime objects
    lumis['start'] = pd.to_datetime(lumis['start'])
    lumis['stop'] = pd.to_datetime(lumis['stop'])

    # Get all beam on/off files in run ranges
    beamOn = lumis[(lumis['run'] >= beamOnRuns[0]) & (lumis['run'] < beamOnRuns[1]) & (lumis['beamInFill']==True)]
    beamOff = lumis[(lumis['run'] >= beamOffRuns[0]) & (lumis['run'] < beamOffRuns[1]) & (lumis['beamInFill']==False)]

    # Calculate total lumi in beam on dataset
    totalLumi = beamOn['lumiEst'].sum()

    # Calculate total run time in seconds
    runTimeOn = (beamOn['stop'] - beamOn['start']).sum().total_seconds()
    runTimeOff = (beamOff['stop'] - beamOff['start']).sum().total_seconds()

    print("Beam on runs ran for {}s with lumi {}pb^-1".format(runTimeOn, totalLumi))
    print("Beam off runs ran for {}s".format(runTimeOff))

    scale = runTimeOff / runTimeOn

    print("Scale to normalize beam data {}".format(scale))

    return runTimeOn, runTimeOff

if __name__ == "__main__":
    # Stop Python from displaying canvases
    r.gROOT.SetBatch(1)

    # Define output file to write out ROOT plots
    fout = r.TFile.Open("timingCalibrationPlots.root", "RECREATE")

    # Get the total run time for beam on/off
    runTimeOn, runTimeOff = getRunTime()

    # Open the timing correction files for beam on/off
    f_beamOn = r.TFile.Open('/data/users/mcarrigan/milliqan/timingCorrections/timingCorrection_beamOn.root', 'READ')
    f_beamOff = r.TFile.Open('/data/users/mcarrigan/milliqan/timingCorrections/timingCorrection_beamOff.root', 'READ')

    # Create TCanvases for each layer
    c_l1 = r.TCanvas("c_l1", "Layer 1", 1400, 1400)
    c_l2 = r.TCanvas("c_l2", "Layer 2", 1400, 1400)
    c_l3 = r.TCanvas("c_l3", "Layer 3", 1400, 1400)
    c_l4 = r.TCanvas("c_l4", "Layer 4", 1400, 1400)

    # Divide each canvas into 16 plots for each channel in a layer
    c_l1.Divide(4, 4)
    c_l2.Divide(4, 4)
    c_l3.Divide(4, 4)
    c_l4.Divide(4, 4)

    timeCanvases = [c_l1, c_l2, c_l3, c_l4]

    # Define fit bounds for each channel in beam on and off datasets
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

    boundsOff = [
        [-40, 0]] * 64

    # Loop over all 64 channels
    for i in range(64):
        # Get the time difference histogram for beam on and beam off data
        h_on = f_beamOn.Get(f'h_timeDiffFrontPanel{i}')
        h_off = f_beamOff.Get(f'h_timeDiffFrontPanel{i}')

        # Scale each histogram by the total run time for normalization
        h_on.Scale(1. / runTimeOn)
        h_off.Scale(1. / runTimeOff)

        # Subtract beamOff data from beamOn data directly
        for bin in range(1, h_on.GetNbinsX() + 1):
            beamOn_value = h_on.GetBinContent(bin)
            beamOff_value = h_off.GetBinContent(bin)
            adjusted_value = beamOn_value - beamOff_value
            h_on.SetBinContent(bin, adjusted_value)

        # Create Gaussian functions for fitting
        f_on = r.TF1('f_on', 'gaus', boundsOn[i][0], boundsOn[i][1])
        f_off = r.TF1('f_off', 'gaus', boundsOff[i][0], boundsOff[i][1])

        # Fit the adjusted beamOn histogram and beamOff histogram
        h_on.Fit(f_on, "0", "", boundsOn[i][0], boundsOn[i][1])
        h_off.Fit(f_off, "0", "", boundsOff[i][0], boundsOff[i][1])

        # Set line colors for visualization
        f_off.SetLineColor(2)  # Red for beamOff
        f_on.SetLineColor(4)   # Blue for adjusted beamOn

        # Select the correct canvas and pad
        timeCanvases[i // 16].cd()
        timeCanvases[i // 16].cd(i % 16 + 1)

        # Draw histograms and fits on the canvas
        h_on.Draw("hist")
        h_off.Draw("hist same")
        f_on.Draw("same")
        f_off.Draw("same")

    # Write all canvases to the output file
    fout.cd()
    c_l1.Write("FitsL1")
    c_l2.Write("FitsL2")
    c_l3.Write("FitsL3")
    c_l4.Write("FitsL4")

    fout.Close()
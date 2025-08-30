import pandas as pd
import ROOT as r 


def getRunTime():

    #define the runs used in beam on/off data
    beamOnRuns=[1400, 1800]
    beamOffRuns=[1300, 1800]

    #open the lumi file
    lumis = pd.read_json('mqLumis.json', orient = 'split', compression = 'infer')

    #make sure start/stop are datetimes
    lumis['start'] = pd.to_datetime(lumis['start'])
    lumis['stop'] = pd.to_datetime(lumis['stop'])

    #get all beam on/off files in run ranges
    beamOn = lumis[(lumis['run'] >= beamOnRuns[0]) & (lumis['run'] < beamOnRuns[1]) & (lumis['beamInFill']==True)]
    beamOff = lumis[(lumis['run'] >= beamOffRuns[0]) & (lumis['run'] < beamOffRuns[1]) & (lumis['beamInFill']==False)]

    #calculate total lumi in beam on dataset
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
    f_beamOn = r.TFile.Open('timingCorrection_beamOn.root', 'READ')
    f_beamOff = r.TFile.Open('timingCorrection_beamOff.root', 'READ')

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
        [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0],
        [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0],

        [-20, 20], [-20, 20], [-20, 20], [-20, 20], [-20, 20], [-20, 20], [-20, 20], [-20, 20],
        [-20, 20], [-20, 20], [-20, 20], [-20, 20], [-20, 20], [-20, 20], [-20, 20], [-20, 20],

        [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0],
        [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0],

        [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0],
        [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0], [-40, 0]
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

    #loop over all 64 channels
    for i in range(64):

        #get the plot of time difference between front pannel and channel i 
        h_on = f_beamOn.Get(f'h_timeDiffFrontPanel{i}')
        h_off = f_beamOff.Get(f'h_timeDiffFrontPanel{i}')

        #scale each plot by the total run time so they are normalized
        h_on.Scale(1./runTimeOn)
        h_off.Scale(1./runTimeOff)

        h_off.SetLineColor(2)

        #create gaussian functions
        f_on = r.TF1('f_on', 'gaus', boundsOn[i][0], boundsOn[i][1])
        f_off = r.TF1('f_off', 'gaus', boundsOff[i][0], boundsOff[i][1])

        #optionally set fit parameter limits if fits need it
        '''f_off.SetParLimits(0, 1e-30, 1)
        f_off.SetParLimits(1, -40, -10)
        f_off.SetParLimits(2, 1e-2, 5)'''

        #fit plots
        h_on.Fit(f_on, "0", "", boundsOn[i][0], boundsOn[i][1])
        h_off.Fit(f_off, "0", "", boundsOff[i][0], boundsOff[i][1])

        f_off.SetLineColor(2)
        f_on.SetLineColor(4)

        #change to correct canvas
        if i%16 == 0:
            timeCanvases[i//16].cd()
        timeCanvases[i//16].cd(i%16+1)

        #draw plots on canvas
        h_on.Draw("hist")
        h_off.Draw("hist same")
        f_on.Draw("same")
        f_off.Draw("same")

    
    #write all plots to output file
    fout.cd()
    c_l1.Write("FitsL1")
    c_l2.Write("FitsL2")
    c_l3.Write("FitsL3")
    c_l4.Write("FitsL4")

    fout.Close()

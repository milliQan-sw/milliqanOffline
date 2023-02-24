import ROOT as r
import numpy as np


# Get list of histograms in ROOT file
def GetKeyNames(rootFile, dir = "" ):
    rootFile.cd(dir)
    return [key.GetName() for key in r.gDirectory.GetListOfKeys()]


# Load in ROOT file
pathToData = '/home/rsantos/Data/outputWaveforms_805_noLED.root'
dataFile = r.TFile(pathToData)
waveForm = dataFile.Get('Waves_4169')

areas = []
# Loop over all histograms in root file
for hist in GetKeyNames(dataFile):
    waveForm = dataFile.Get(hist)

    voltage = []
    # Loop over bins in histogram
    for i in range(waveForm.GetNbinsX()):
        voltage.append(waveForm.GetBinContent(i))
    # Assuming that the bin size is consistent throughout the histogram so we do not insert x values into trapz
    areas.append(np.trapz(voltage))

# Creating Canvas
print(areas)
c1 = r.TCanvas('c1', 'Voltage Area', 200, 10, 700, 500)
# Create ROOT file to store histogram
hfile = r.gROOT.FindObject('0-SPE.root')
if hfile:
    hfile.Close()

hfile = r.TFile('0-SPE.root', 'RECREATE', 'Volatage-Area')
harea = r.TH1F('Varea', 'Voltage Area No LED', 100, -50000, 100000)
for areaValue in areas:
    harea.Fill(areaValue)

harea.Draw()

hfile.Write()
    # Calculate area under curve based off trapezoid approx.

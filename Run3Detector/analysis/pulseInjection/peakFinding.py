from ROOT import TSpectrum, TFile, TString, TH1



def peakFinding( input_file:TFile, sigma: int = 2,
                 threshold: float = 0.1, max_peaks:int= 20):
    """
    Function to perform peak finding on a set of histograms
    Return location of peaks and estimated background
    """

    if not input_file.IsOpen():
        print("Could not open ROOT file")
        exit()
    keys = input_file.GetListOfKeys()
    print(len(keys))
    peak_locations = []
    for key in keys:
        
        obj = key.ReadObj()
        if isinstance(obj, TH1):
            spectrum = TSpectrum(max_peaks)

            # Find peaks that are 2 sigma above average, and exclude peaks that are less that 0.01 * max height of tallest peak
            peaks = spectrum.Search(obj, sigma, "", threshold) #
            peak_location = []
            for i in range(spectrum.GetNPeaks()):
                peak_location.append((spectrum.GetPositionX()[i], spectrum.GetPositionY()[i]))
            peak_locations.append(peak_location)
    return peak_locations

if __name__ == "__main__":
    input_file = TFile("/home/ryan/Documents/Data/MilliQan/outputWaveforms_805_noLED.root", "READ")
    print(peakFinding(input_file))





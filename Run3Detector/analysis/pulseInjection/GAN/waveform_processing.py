import numpy as np
import uproot

def extract_waveforms(input_file_path:str,
                      ns_per_measurement:float = 2.5,
                      number_of_measurements:int = 1024):
    input_file = uproot.open(input_file_path)
    histogram_names = input_file.keys()

    for name in histogram_names:
        histogram = input_file[name]
        if histogram.classname == "TH1D"
        data = histogram.values()
        # Remove trailing ;1 from names given by uproot
        self.histogram_dict[name[:name.rfind(";")]] = data

def background_estimation(input_file: str):
    input_file = TFile(input_file, "READ")
    all_noise = []
    for key in input_file.GetListOfKeys():
        obj = key.ReadObj()
        if isinstance(obj, TH1):
            spectrum = TSpectrum()
            background_hist = spectrum.Background(obj)
            background_values = [background_hist.GetBinContent(i)
                                 for i in range(background_hist.GetNbinsX())]
            all_noise.append(background_values)
    return np.mean(all_noise, axis=1)

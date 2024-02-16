from tensorflow.keras import layers
import numpy as np
from ROOT import TFile, TH1
import logging

class WaveformProcessor():
    def __init__(self, input_file:TFile):
        self.histogram_array = ROOT.TList() 
        for key in input_file.GetListOfKeys():
            obj = key.ReadObj()
            if isinstance(obj, ROOT.TH1):
                self.histogram_array.Add(obj)

        self.voltage_window = np.zeros(1024)

    def extract_waveforms(self):
        for hist in self.histogram_array:
            waveform_values = self.histogram_to_array(hist)
            waveform_bounds = self.find_waveform_bounds(hist)

    def histogram_to_array(self, waveform:TH1):
        # Extract noise level by taking a percentile of the voltages
        num_bins = waveform.GetNbinsX()
        bin_contents = np.zeros(num_bins)
        logging.debug(f"Number of bins in waveform histogram: {bin_contents}")
        # Fill the array with bin contents
        for i in range(1, num_bins + 1):
            bin_contents[i - 1] = waveform.GetBinContent(i)
        return bin_contents

    def find_waveform_bounds(self, hist_values, noise_percentile=20):
        # TODO This currently won't work, need to find way to find bounds
        noise = np.mean(np.percentile(hist_values, noise_percentile))
        waveform_bounds_total = np.empty(2)
        for i, value in enumerate(np.greater(hist_values, noise)):
            waveform_bounds = np.empty((2, 1))
            if value and not np.greater(hist_values,noise)[i-1]:
                print(f"Found start of waveform at {i}")
                waveform_bounds[0] = i
            if value and not(np.greater(hist_values, noise)[i+1]):
                print(f"Found end of waveform at {i}")
                waveform_bounds[1] = i
            
        return waveform_bounds

        
    
if __name__ == "__main__":
    led_file = TFile("/home/ryan/Documents/Data/MilliQan/"
                      "outputWaveforms_812_2p5V.root", "READ")
    processor = WaveformProcessor(led_file)

        

        
        
        

import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import uproot
import logging
import unittest

from ROOT import TSpectrum, TFile, TH1

logging.basicConfig(level="WARNING")

class WaveformProcessor():
    def __init__(self, input_file_path: str):
        input_file = uproot.open(input_file_path)
        histogram_names = input_file.keys()

        logging.debug(f"Input file: {input_file}")

        self.ns_per_measurement = 2.5
        self.number_of_measurements = 1024

        self.times = np.arange(0, self.number_of_measurements*self.ns_per_measurement,
                               self.ns_per_measurement)

        self.histogram_dict = {}

        for name in histogram_names:
            histogram = input_file[name]
            if histogram.classname == "TH1D":
                data = histogram.values()

                # Remove trailing ;1 from names given by uproot
                self.histogram_dict[name[:name.rfind(";")]] = data
        
        self.background_estimation(input_file_path) 
        logging.debug(f" Histograms: {self.histogram_dict}") 
        self.voltage_window = np.zeros(1024)


    def background_estimation(self, input_file: str):
        self.noise_dict = {} 
        input_file = TFile(input_file, "READ")
        for key in input_file.GetListOfKeys():
            obj = key.ReadObj()
            if isinstance(obj, TH1):
                spectrum = TSpectrum()
                background_hist = spectrum.Background(obj)
                background_values = [background_hist.GetBinContent(i)
                                     for i in range(background_hist.GetNbinsX())]

                background_array = np.array(background_values)

                self.noise_dict[key.GetName()] = np.mean(background_array)

        
    def find_waveform_bounds(self) -> None:
        self.peak_dictionary = {} 
        for key, value in self.histogram_dict.items():
            peak_positions, _ = find_peaks(value, distance=10)
            pulse_bounds = np.empty([len(peak_positions),2])

            for i, index in enumerate(peak_positions):
                start_index = index 
                while start_index > 0 and value[start_index] > self.noise_dict[key]:
                    start_index -= 1

                pulse_bounds[i][0] = value[start_index-1]

                stop_index = index
                while stop_index < len(value) and value[start_index] > self.noise_dict[key]:
                    stop_index += 1
                pulse_bounds[i][1] = value[stop_index-1]

            self.peak_dictionary[key] = pulse_bounds
        logging.debug(f"Peaks: {self.peak_dictionary}")

    def plot_waveforms(self, plotDirectory: str) -> None:
        if not os.path.exists(plotDirectory):
            os.mkdir(plotDirectory)
            
        for key, value in self.histogram_dict.items():
            plt.clf()
            plt.plot(self.times, value)
            for peak in self.peak_dictionary[key]: 
                plt.axvline(peak[0])
                plt.axvline(peak[1])

            plt.savefig("{0}/{1}.png".format(plotDirectory, key))
            
            
class TestWaveformProcessor(unittest.TestCase):
    def test_find_waveform_bounds(self):
        file = TFile("/home/ryan/Documents/Research/Data/MilliQanWaveforms/outputWaveforms_805_noLED.root")
        hist = file.Get("Waves_41")
        processor = WaveformProcessor(file)
        waveform_bounds = processor.find_waveform_bounds()


if __name__ == "__main__":
    processor = WaveformProcessor("/home/ryan/Documents/Data/MilliQan/outputWaveforms_805_noLED.root")
    bounds = processor.find_waveform_bounds()
    processor.plot_waveforms("Plots")


import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import uproot
import logging
import unittest
import keras.Model
from ROOT import TSpectrum, TFile, TH1

logging.basicConfig(level="DEBUG")

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
            peak_positions, _ = find_peaks(value, prominence=5, height=15)
            pulse_bounds = np.empty([len(peak_positions), 2])

            continue_flag = False
            for i, index in enumerate(peak_positions):
                start_index = index 
                while start_index > 0 and value[start_index] > self.noise_dict[key]:
                    start_index -= 1

                pulse_bounds[i][0] = start_index

                stop_index = index
                while stop_index < len(value) and value[stop_index] > self.noise_dict[key]:
                    stop_index += 1
                pulse_bounds[i][1] = stop_index

                # If the bounds of the waveform lie at the edge of the window, it's probably
                # a messy event so just dump it
                if stop_index == len(value) or start_index == 0:
                    continue_flag = True
                    break

            if continue_flag:
                continue
            self.peak_dictionary[key] = pulse_bounds

        logging.debug(f"Peaks: {self.peak_dictionary}")

    def isolate_waveforms(self) -> None:
        number_of_waves: int = sum([len(peak) for peak in self.peak_dictionary.values()])
        input_data = np.zeros((number_of_waves, 1024))

        index = 0
        for key, value in self.peak_dictionary.items():
            # Slice values in histogram_dict to just capture waveforms
            for waveform in value:
                logging.debug(f"Key: {key} \n"
                             f"Index: {waveform[0]}, {waveform[1]}\n")
                sliced_histogram_values = self.histogram_dict[key][int(waveform[0]):int(waveform[1]+1)]
                input_data[index][:len(sliced_histogram_values)] = sliced_histogram_values
                index += 1

    def calculate_npe(self, waveform, area_per_spe) -> int:
        waveform_area = np.trapz(waveform, dx=self.ns_per_measurement)
        return round(waveform_area / area_per_spe)


        
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
            

def build_waveform_generator(latent_dim, num_classes):    
    noise = layers.Input(shape=(latent_dim,))
    label = layer.Input(shape=(num_classes,))

    x = layers.Concatenate()([noise, label])
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dense(784, activation='sigmoid')(x)
    x = layers.Dense(1024, activation='sigmoid')(x)
    return Model([noise, label], x)

if __name__ == "__main__":
    processor = WaveformProcessor("/home/ryan/Documents/Data/MilliQan/outputWaveforms_805_noLED.root")
    bounds = processor.find_waveform_bounds()
    processor.isolate_waveforms()


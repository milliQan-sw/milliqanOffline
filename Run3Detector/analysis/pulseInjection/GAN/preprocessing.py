"""
Contains class to preprocess waveform data before being
sent into the GAN.

Methods:
background_estimation
find_waveform_bounds
isolate_waveforms
calculate_npe
plot_waveforms

"""

from typing import Dict, Union
import logging

import numpy.typing as npt
import numpy as np
import uproot
from ROOT import TFile, TH1, TSpectrum
from scipy.signal import find_peaks
import tensorflow as tf

logging.basicConfig(level=logging.ERROR)

def fix_imbalanced_data(input_data:npt.ArrayLike,
                        input_labels:npt.ArrayLike,
                        majority_label:int,
                        minority_label:int,
                        oversample_undersample:str,
                        shuffle_buffer_size:int = 100000,
                        batch_size=256
                        )-> Union[tf.data.Dataset, None]:

    dataset = tf.data.Dataset.from_tensor_slices((input_data,
                                                  input_labels))

    majority_dataset = dataset.filter(lambda data, label:
                                      label == majority_label).shuffle(shuffle_buffer_size)
    minority_dataset = dataset.filter(lambda data, label:
                                      label == minority_label).shuffle(shuffle_buffer_size)
    if oversample_undersample == "oversample":
        resampled_ds = tf.data.Dataset.sample_from_datasets([majority_dataset,
                                                             minority_dataset],
                                                            weights=[0.5,0.5])
        resampled_ds = resampled_ds.batch(batch_size).prefetch(2)
        return resampled_ds
    else:
        logging.warning("Only oversample is setup!")
        return

                                                            


class WaveformProcessor():
    ns_per_measurement = 2.5
    number_of_measurements = 1024

    def __init__(self, input_file_path: str):
        self.input_file_path = input_file_path
        self.input_file = uproot.open(input_file_path)
        histogram_names = self.input_file.keys()

        logging.debug(f"Input file: {self.input_file}")

        self.times = np.arange(0,
                               self.number_of_measurements *
                               self.ns_per_measurement,
                               self.ns_per_measurement)

        self.histogram_dict = {}

        for name in histogram_names:
            histogram = self.input_file[name]
            if histogram.classname == "TH1D":
                data = histogram.values()

                # Remove trailing ;1 from names given by uproot
                self.histogram_dict[name[:name.rfind(";")]] = data

        self.noise: Dict[str, float] = self.background_estimation()

        logging.debug(f" Histograms: {self.histogram_dict}")

    def background_estimation(self) -> Dict[str, float]:
        noise_dict = {}
        input_file = TFile.Open(self.input_file_path)
        for key in input_file.GetListOfKeys():
            obj = key.ReadObj()
            if isinstance(obj, TH1):
                spectrum = TSpectrum()
                background_hist = spectrum.Background(obj)
                background_values = [background_hist.GetBinContent(i)
                                     for i in range(background_hist.GetNbinsX())]

                background_array = np.array(background_values)

                noise_dict[key.GetName()] = np.mean(background_array)
        return noise_dict

    def find_waveform_bounds(self, n_peaks: int,
                             noise_dict: Dict[str, float],
                             peak_prominence: float = 50) -> Dict[str, npt.NDArray]:
        peak_dictionary = {}
        for key, value in self.histogram_dict.items():
            peak_positions, _ = find_peaks(value, distance=100, height=30)
            if len(peak_positions) > 1:
                continue

            print(f"Number of Peaks: {len(peak_positions)}")
            pulse_bounds = np.empty([len(peak_positions), 2])

            continue_flag = False
            for i, index in enumerate(peak_positions):
                start_index = index
                while (start_index > 0 and
                       value[start_index] > noise_dict[key]):
                    start_index -= 1

                pulse_bounds[i][0] = start_index

                stop_index = index
                while (stop_index < len(value) and
                       value[stop_index] > noise_dict[key]):
                    stop_index += 1
                pulse_bounds[i][1] = stop_index

                # If the bounds of the waveform lie at the edge of the window,
                # it's probably a messy event so just dump it
                if stop_index == len(value) or start_index == 0:
                    continue_flag = True
                    break
            if continue_flag:
                continue

            peak_dictionary[key] = pulse_bounds
        return peak_dictionary

    def isolate_waveforms(self, peak_dictionary: Dict[str, npt.NDArray]) -> npt.NDArray:
        number_of_waves: int = sum([len(peak) for peak in
                                    peak_dictionary.values()])
        logging.debug("Number of waves: {}".format(number_of_waves))

        # TODO The size of this array should be variable
        input_data = np.zeros((number_of_waves, 500))

        index = 0
        for key, value in peak_dictionary.items():
            # Slice values in histogram_dict to just capture waveforms
            for waveform in value:

                logging.debug(f"Key: {key} \n"
                              f"Index: {waveform[0]}, {waveform[1]}\n")

                sliced_histogram_values = (self.histogram_dict[key]
                                           [int(waveform[0]):int(waveform[1]+1)])

                logging.debug("input_data shape: {}".format(len(input_data)))
                logging.debug("sliced_histogram_values shape: {}"
                              .format(len(sliced_histogram_values)))

                input_data[index][:len(sliced_histogram_values)
                                  ] = sliced_histogram_values
                index += 1
        return input_data

    def calculate_npe(self, waveforms: np.ndarray, area_per_spe: float) -> int:
        waveform_area = np.trapz(waveforms)
        return np.round(np.divide(waveform_area, area_per_spe))

    def plot_waveforms(self, plotDirectory: str) -> None:
        if not os.path.exists(plotDirectory):
            os.mkdir(plotDirectory)
        for key, value in self.histogram_dict.items():
            try:
                plt.clf()
                plt.plot(self.times, value)
                for peak in self.peak_dictionary[key]:
                    plt.axvline(self.times[int(peak[0])], color='r')
                    plt.axvline(self.times[int(peak[1])], color='r')

                plt.savefig("{0}/{1}.png".format(plotDirectory, key))
            except KeyError:
                continue


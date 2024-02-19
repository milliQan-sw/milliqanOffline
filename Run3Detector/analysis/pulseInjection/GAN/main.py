import numpy as np
from scipy.signal import find_peaks
import uproot
import logging
import unittest


class WaveformProcessor():
    def __init__(self, input_file_path: str):
        input_file = uproot.open(input_file_path)
        histogram_names = input_file.keys()
        self.histogram_dict = {}
        for name in histogram_names:
            histogram = input_file[name]
            if histogram.classname == "TH1D":
                data = histogram.values()
                self.histogram_dict[name] = data

        self.voltage_window = np.zeros(1024)

    def extract_waveforms(self):
        for hist in self.histogram_array:
            waveform_values = self.histogram_to_array(hist)
            waveform_bounds = self.find_waveform_bounds(hist)

    # def histogram_to_array(self, waveform:TH1):
    #     # Extract noise level by taking a percentile of the voltages
    #     num_bins = waveform.GetNbinsX()
    #     bin_contents = np.zeros(num_bins)
    #     logging.debug(f"Number of bins in waveform histogram: {bin_contents}")
    #     # Fill the array with bin contents
    #     for i in range(1, num_bins + 1):
    #         bin_contents[i - 1] = waveform.GetBinContent(i)
    #     return bin_contents

    def find_waveform_bounds(self, noise_percentile=20):
        for key, value in self.histogram_dict.items():
            noise = np.percentile(value, noise_percentile)
            logging.info(f"Noise level for waveform is {noise}")

            peak_positions, _ = find_peaks(value, prominence=1, width=15)
            print(peak_positions)

        # spectrum = TSpectrum()
        # n_peaks = spectrum.Search(waveform)
        # logging.info(f"Found {n_peaks} peaks")
        # peak_positions = spectrum.GetPostionX()

        # x_axis = waveform.GetXaxis()
        # n_bins = waveform.GetNbinsX() + 1
        # waveform_bounds_total = np.array((-1, 2))
        # for peak_pos in peak_positions:
        #     peak_bin = x_axis.FindBin(peak_pos)
        #     waveform_bounds = np.array((1, 2))

        #     for bin in range(peak_bin, n_bins):
        #         bin_content = waveform.GetBinContent(bin)
        #         bin_center = x_axis.GetBinCenter(bin)
        #         if bin_content < noise[0]:
        #             waveform_bounds[-1] = bin_center
        #             break

        #     for bin in range(peak_bin, 0, -1):
        #         bin_content = waveform.GetBinContent(bin)
        #         bin_center = x_axis.GetBinCenter(bin)
        #         if bin_content < noise[0]:
        #             waveform_bounds[0] = bin_center
        #             break
        #     waveform_bounds_total.append(waveform_bounds)
        # return waveform_bounds


class TestWaveformProcessor(unittest.TestCase):
    def test_find_waveform_bounds(self):
        file = TFile("/home/ryan/Documents/Research/Data/MilliQanWaveforms/outputWaveforms_805_noLED.root")
        hist = file.Get("Waves_41")
        processor = WaveformProcessor(file)
        waveform_bounds = processor.find_waveform_bounds(hist, 90)


if __name__ == "__main__":
    processor = WaveformProcessor("/home/ryan/Documents/Research/Data/MilliQanWaveforms/outputWaveforms_805_noLED.root")
    processor.find_waveform_bounds()

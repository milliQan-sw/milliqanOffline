from typing import Dict
from preprocessing import WaveformProcessor
import numpy.typing as npt
import matplotlib.pyplot as plt

DATA_DIRECTORY: str = "/home/ryan/Documents/Data/MilliQan/"
N_PEAKS: int = 3
wp = WaveformProcessor(DATA_DIRECTORY + "outputWaveforms_805_noLED.root")

noise: Dict[str, float] = wp.background_estimation()
peak_dictionary: Dict[str,
                         npt.NDArray] = wp.find_waveform_bounds(N_PEAKS, noise)
isolated_waveforms = wp.isolate_waveforms(peak_dictionary)

for waveform in isolated_waveforms:
    plt.clf()
    plt.plot(waveform)
    plt.show()

import numpy as np
import ROOT as r
import matplotlib.pyplot as plt

import gan
from preprocessing import WaveformProcessor

# Bounds of wavefrom in ns
WAVEFORM_BOUNDS = (1200, 1600)
SPE_AREA = 480
SPE_TOLERANCE = 5.14921
NS_PER_MEASUREMENT = 2.5

# Preprocess Waveform Data
input_file = "/home/ryan/Documents/Data/MilliQan/outputWaveforms_812_2p5V.root"
processor = WaveformProcessor(input_file)



times = processor.times
# # Set static bounds for LED datset
static_bounds = {key: np.array([[np.where(times == WAVEFORM_BOUNDS[0])[0],
                                 np.where(times == WAVEFORM_BOUNDS[1])[0]]])
                 for key in processor.histogram_dict.keys()}

# Isolate Waveforms
isolated_peaks = processor.isolate_waveforms(static_bounds)
areas = [] 
for item in isolated_peaks:
    led_area_hist = TH1F("led_hist", "LED Area Histogram", 200, 0, 2000)
    for value in item:
        led_area_hist.fill(value)
    areas.append(led_area_hist.Integral())
#TODO Check
print(areas) 
# Only pick waveforms that could reasonably represent SPE peaks
area = np.trapz(isolated_peaks, dx=2.5)
print(area)
spe_waveform = area[(area < SPE_AREA + SPE_TOLERANCE)]
print(spe_waveform)
# Defining GAN
gan_creator = gan.GAN()
discriminator = gan_creator.define_discriminator()
generator = gan_creator.define_generator(1000)
gan = gan_creator.define_gan(generator, discriminator)

import numpy as np
import ROOT as r
import matplotlib.pyplot as plt

import gan
from preprocessing import WaveformProcessor

# Bounds of wavefrom in ns
WAVEFORM_BOUNDS = (1200, 1600)
SPE_AREA = 1000
SPE_TOLERANCE = 10
NS_PER_MEASUREMENT = 2.5
PLOT = False
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
# Only pick waveforms that could reasonably represent SPE peaks

area = np.trapz(isolated_peaks, dx=2.5)
indices = np.where((area < SPE_AREA + SPE_TOLERANCE) &
                   (area > SPE_AREA - SPE_TOLERANCE))
spe_waveform = isolated_peaks[(area < SPE_AREA + SPE_TOLERANCE) &
                              (area > SPE_AREA - SPE_TOLERANCE)]
print(f"Number of spe: {len(spe_waveform[0])}")
# Viewing waveforms

indices = np.array(indices)
if PLOT:
    for value in indices.flatten():
        print(f"Index: {value}")
        plt.clf()
        plt.plot(isolated_peaks[value])
        plt.show()

# Defining GAN
latent_dim = 1000
gan_creator = gan.GAN()
discriminator = gan_creator.define_discriminator(n_inputs=201)
generator = gan_creator.define_generator(1000, n_outputs=201)
gan = gan_creator.define_gan(generator, discriminator)
loss = gan_creator.train(generator, discriminator, gan,
                         latent_dim, spe_waveform, n_epochs=10)

discriminator.save("discriminator.keras")
generator.save("generator.keras")
gan.save("gan.keras")

plt.clf()
plt.plot(loss)
plt.show()

gen_x, gen_y = gan_creator.generate_fake_samples(generator, latent_dim, 5)


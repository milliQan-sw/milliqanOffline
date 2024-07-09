from tensorflow.keras.utils import plot_model
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import ROOT as r 
from Lib.preprocessing import WaveformProcessor

LATENT_DIM = 500
WAVEFORM_BOUNDS = (1200, 1600)
N_SAMPLES = 1000
SPE_AREA = 500

INPUT_FILE = "/home/ryan/Documents/Data/MilliQan/outputWaveforms_812_2p5V.root"
processor = WaveformProcessor(INPUT_FILE)


# # Set static bounds for LED datset
static_bounds = {key: np.array([[np.where(processor.times == WAVEFORM_BOUNDS[0])[0],
                                 np.where(processor.times == WAVEFORM_BOUNDS[1])[0]]])
                 for key in processor.histogram_dict}

# Isolate Waveforms
isolated_peaks = processor.isolate_waveforms(static_bounds)

npe = np.round(np.divide(np.trapz(isolated_peaks), SPE_AREA))



latent_points = np.random.normal(size=(N_SAMPLES , LATENT_DIM))
seed_class_label= np.ones(N_SAMPLES)

generator = tf.keras.models.load_model("TrainedModels/generator.keras")
plot_model(generator, to_file="model.jpg", rankdir="LR",
           show_layer_names=False)
noise = tf.random.normal([LATENT_DIM])
waveforms = generator.predict([latent_points, seed_class_label])

areas = np.trapz(waveforms, axis=1)

spe_waveform = isolated_peaks[np.round(np.divide(np.trapz(isolated_peaks), 500)) == 1]
plt.hist(np.trapz(spe_waveform, axis=1), bins=30, alpha=0.5, edgecolor='black')
plt.hist(areas, bins=30, alpha=0.5, edgecolor='black')
plt.xlabel("Area (pV s / 2.5)")
plt.title("Generated SPE  versus Real Waveform Area Distribution")

plt.show()

    




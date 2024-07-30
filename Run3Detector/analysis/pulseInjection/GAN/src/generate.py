import os
import datetime
import logging 
from tensorflow.keras.utils import plot_model
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import ROOT as r 

from preprocessing import WaveformProcessor
timestamp = datetime.datetime.now().replace(microsecond=0).isoformat().replace(":", "")

    
LATENT_DIM = 500
WAVEFORM_BOUNDS = (1200, 1600)
N_SAMPLES = 1000
SPE_AREA = 500
NPE_VALUES = (1, 2)

INPUT_FILE = "/home/ryan/Documents/Data/MilliQan/outputWaveforms_812_2p5V.root"
processor = WaveformProcessor(INPUT_FILE)


# # Set static bounds for LED datset
static_bounds = {key: np.array([[np.where(processor.times == WAVEFORM_BOUNDS[0])[0],
                                 np.where(processor.times == WAVEFORM_BOUNDS[1])[0]]])
                 for key in processor.histogram_dict}

# Isolate Waveforms
isolated_peaks = processor.isolate_waveforms(static_bounds)

npe = np.round(np.divide(np.trapz(isolated_peaks), SPE_AREA))


# Setup input to generator
latent_points = np.random.normal(size=(N_SAMPLES * len(NPE_VALUES) , LATENT_DIM))
arrays = []
for npe in NPE_VALUES:
    arrays.append(np.full(N_SAMPLES, npe, dtype=int))

seed_class_label = np.concatenate(arrays)
logging.info("Number of labels passed to generator: {}".format(len(seed_class_label)))     
generator = tf.keras.models.load_model("trained_models/generator_20240725-120437.keras")
plot_model(generator, to_file="model.jpg", rankdir="LR",
           show_layer_names=False)

waveforms = generator.predict([latent_points, seed_class_label])

areas = np.trapz(waveforms, axis=1)

if not os.path.isdir('plots'):
    os.mkdir('plots')
os.mkdir(f'plots/{timestamp}')

for i, npe in enumerate(NPE_VALUES): 
    spe_waveform = isolated_peaks[np.round(np.divide(np.trapz(isolated_peaks), 500)) == npe]
    plt.hist(np.trapz(spe_waveform, axis=1), bins=30, alpha=0.5, edgecolor='black', label=f"Real_{npe}")
    plt.hist(areas[:(i+1)*N_SAMPLES], bins=30, alpha=0.5, edgecolor='black', label=f"Generated_{npe}")

plt.legend()
plt.xlabel("Area (pV s / 2.5)")
plt.title("Generated SPE  versus Real Waveform Area Distribution")
plt.savefig(f'plots/{timestamp}/{npe}_npe_area.png', format='png')
plt.show()


    




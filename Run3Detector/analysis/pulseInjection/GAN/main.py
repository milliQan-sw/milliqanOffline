import time

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

import ganv2
from preprocessing import WaveformProcessor
from utilities import plot_loss

# Data Preprocessing Constants
WAVEFORM_BOUNDS = (1200, 1600)
SPE_AREA = 500
NS_PER_MEASUREMENT = 2.5

# Model Constants
LATENT_DIM = 500
BATCH_SIZE = 128
EPOCHS = 100000
EVAL_EPOCH = 2000  # How often you should get output during training

PLOT = False

# Preprocess Waveform Data
INPUT_FILE = "/home/ryan/Documents/Data/MilliQan/outputWaveforms_812_2p5V.root"
processor = WaveformProcessor(INPUT_FILE)


# Set static bounds for LED datset
static_bounds = {key: np.array([[np.where(processor.times == WAVEFORM_BOUNDS[0])[0],
                                 np.where(processor.times == WAVEFORM_BOUNDS[1])[0]]])
                 for key in processor.histogram_dict}

# Isolate Waveforms
isolated_peaks = processor.isolate_waveforms(static_bounds)

npe = np.round(np.divide(np.trapz(isolated_peaks), SPE_AREA))
num_classes = 12
#num_classes = len(tf.unique(npe)[0])

dataset = tf.data.Dataset.from_tensor_slices((isolated_peaks,
                                              npe))

dataset = dataset.filter(lambda data, label: tf.logical_and(label >=0, label <12))
dataset = dataset.shuffle(buffer_size=200)
dataset = dataset.batch(BATCH_SIZE).prefetch(buffer_size=tf.data.experimental.AUTOTUNE)

if PLOT:
    for i, value in enumerate(isolated_peaks):
        print(f"Index: {value}")
        plt.clf()
        plt.plot(value)
        plt.text(3, 6, f"NPE: {npe[i]}", fontsize=12, color='red')
        plt.show()
        plt.savefig(f"Plots/isolated_peak_{i}.png")

# # Defining GAN
discriminator = ganv2.build_discriminator(embed_dim=128, input_shape=201,
                                          num_classes=num_classes)

generator = ganv2.build_generator(LATENT_DIM, output_shape=201, embed_dim=16,
                                  num_classes=num_classes)

print(generator.summary())
# Train Models
generator_opt = tf.keras.optimizers.Adam()
disc_opt = tf.keras.optimizers.Adam()

d_loss_values = []
g_loss_values = [] 

start = time.time()
for epoch in range(EPOCHS):
    if (epoch % 100) == 0:
        print(f"On epoch {epoch}")
    d_loss = 0.0
    g_loss = 0.0

    i = 0
    assert dataset is not None, "Error in setting up dataset"
    for waveform_batch, label_batch in dataset:
        i+=1
        d_batch_loss, g_batch_loss = ganv2.train_step(waveform_batch, label_batch,
                                                      LATENT_DIM, num_classes,
                                                      generator, discriminator,
                                                      generator_opt, disc_opt)
        d_loss += d_batch_loss
        g_loss += g_batch_loss

    d_loss /= i
    g_loss /= i
    d_loss_values.append(d_loss)
    g_loss_values.append(g_loss)
end = time.time()

plot_loss(d_loss_values, g_loss_values, save_location=f"Plots/loss_{EPOCHS}.png")

print(f"Training took {end - start} seconds to complete.")
discriminator.save(f"TrainedModels/discriminator_{EPOCHS}.keras")
generator.save(f"TrainedModels/generator_{EPOCHS}.keras")

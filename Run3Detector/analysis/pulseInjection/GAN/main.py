import time
import logging
logging.basicConfig(level = logging.INFO)

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from preprocessing import WaveformProcessor, fix_imbalanced_data
import gan
import utilities

# Data Preprocessing Constants
WAVEFORM_BOUNDS = (1200, 1600)
SPE_AREA = 500
NS_PER_MEASUREMENT = 2.5

# Model Constants
LATENT_DIM = 500
BATCH_SIZE = 64
EPOCHS = 50
EVAL_EPOCH = 2000  # How often you should get output during training

PLOT = False

# Preprocess Waveform Data
INPUT_FILE = ("/home/ryan/Documents/Data/MilliQan/"
              "outputWaveforms_812_2p5V.root")
processor = WaveformProcessor(INPUT_FILE)


# Set static bounds for LED datset
static_bounds = {key: np.array([[np.where(processor.times == WAVEFORM_BOUNDS[0])[0],
                                 np.where(processor.times == WAVEFORM_BOUNDS[1])[0]]])
                 for key in processor.histogram_dict}

# Isolate Waveforms
isolated_peaks = processor.isolate_waveforms(static_bounds)
peak_heights = np.max(isolated_peaks, axis=1)
utilities.plot_histogram(peak_heights, 100, 0, 300,
                         write_to_existing_file=True,
                         file_path="height.root")


npe = np.round(np.divide(np.trapz(isolated_peaks), SPE_AREA))

NUM_CLASSES = 3
# num_classes = len(tf.unique(npe)[0])

balanced_dataset = fix_imbalanced_data(isolated_peaks, npe,
                                       1, 2, "oversample", batch_size=BATCH_SIZE)

# if balanced_dataset is not None:
#     for features, label in balanced_dataset.take(1):
#         logging.info("Mean of data labels: {}".format(label.numpy().mean()))

    
dataset = tf.data.Dataset.from_tensor_slices((isolated_peaks,
                                              npe))

dataset = dataset.filter(lambda data, label: tf.logical_and(label > 0,
                                                            label < NUM_CLASSES))
dataset = dataset.shuffle(buffer_size=200)
dataset = dataset.batch(BATCH_SIZE).prefetch(buffer_size=tf.data.experimental.
                                             AUTOTUNE)

if PLOT:
    for i, value in enumerate(isolated_peaks):
        print(f"Index: {value}")
        plt.clf()
        plt.plot(value)
        plt.text(3, 6, f"NPE: {npe[i]}", fontsize=12, color='red')
        plt.show()
        plt.savefig(f"Plots/isolated_peak_{i}.png")

# # Defining GAN
discriminator = gan.build_discriminator(embed_dim=128, input_shape=isolated_peaks.shape[1],
                                          num_classes=NUM_CLASSES+1, extra_info_shape=2)

generator = gan.build_generator(LATENT_DIM, output_shape=isolated_peaks.shape[1], embed_dim=16,
                                  num_classes=NUM_CLASSES+1)

# Train Models
generator_opt = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
disc_opt = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)

d_loss_values = np.zeros(EPOCHS)
g_loss_values = np.zeros(EPOCHS) 

start = time.time()
for epoch in range(EPOCHS):
    if (epoch % 100) == 0:
        logging.info(f"On epoch {epoch}")
    d_loss = 0.0
    g_loss = 0.0

    i = 0
    assert dataset is not None, "Error in setting up dataset"
    for waveform_batch, label_batch in dataset:
        i+=1
        d_batch_loss, g_batch_loss, generator_opt, disc_opt = gan.train_step(waveform_batch, label_batch,
                                                                             LATENT_DIM, NUM_CLASSES,
                                                                             generator, discriminator,
                                                                             generator_opt, disc_opt, BATCH_SIZE)
        d_loss += d_batch_loss
        g_loss += g_batch_loss

    d_loss /= i
    g_loss /= i
    d_loss_values[epoch] = d_loss
    g_loss_values[epoch] = g_loss
end = time.time()

utilities.plot_loss(d_loss_values, g_loss_values, save_location=f"Plots/loss_{EPOCHS}.png")

logging.info(f"Training took {end - start} seconds to complete.")
discriminator.save(f"TrainedModels/discriminator_{EPOCHS}.keras")
generator.save(f"TrainedModels/generator_{EPOCHS}.keras")

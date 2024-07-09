import time
import datetime
import sys
import os
import cProfile
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

tf.debugging.set_log_device_placement(True)
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
from Lib.preprocessing import WaveformProcessor
import Lib.gan 

tf.config.list_physical_devices('GPU')
# Data Preprocessing Constants
WAVEFORM_BOUNDS = (1200, 1600)
SPE_AREA = 500
NS_PER_MEASUREMENT = 2.5

# Model Constants
LATENT_DIM = 500
BATCH_SIZE = 128
EPOCHS = 100
EVAL_EPOCH = 10  # How often you should get output during training

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
#utilities.plot_histogram(peak_heights, 100, 0, 300,
#                         write_to_existing_file=True,
#                         file_path="height.root")

# Create Height Classification


npe = np.round(np.divide(np.trapz(isolated_peaks), SPE_AREA))

NUM_CLASSES = 3
# num_classes = len(tf.unique(npe)[0])

dataset = tf.data.Dataset.from_tensor_slices((isolated_peaks,
                                              npe))

dataset = dataset.filter(lambda data, label: tf.logical_and(label >= 0,
                                                            label <= NUM_CLASSES))
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
discriminator = gan.build_discriminator(embed_dim=128, input_shape=500,
                                          num_classes=NUM_CLASSES+1)

generator = gan.build_generator(LATENT_DIM, output_shape=500, embed_dim=16,
                                  num_classes=NUM_CLASSES+1)

print(generator.summary())
# Train Models
generator_opt = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
disc_opt = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)

d_loss_values = []
g_loss_values = [] 


# Create summaries for tensorboard
current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
train_log_dir = 'logs/gradient_tape/' + current_time + '/train'
train_summary_writer = tf.summary.create_file_writer(train_log_dir)

start = time.time()
for epoch in range(EPOCHS):
    # Monitoring of training
    if (epoch % 100) == 0:
        print(f"On epoch {epoch}")

    # Evaluation of model during training
    if (epoch % EVAL_EPOCH) == 0:
        waveform = gan.generate_waveforms(generator, [1])
        with train_summary_writer.as_default():
            tf.summary.histogram(f"output/{epoch}", waveform[0], step=epoch)

    d_loss = 0.0
    g_loss = 0.0

    i = 0
    assert dataset is not None, "Error in setting up dataset"
    for waveform_batch, label_batch in dataset:
        i+=1
        d_batch_loss, g_batch_loss = gan.train_step(waveform_batch, label_batch,
                                                    LATENT_DIM,
                                                    generator, discriminator,
                                                    generator_opt, disc_opt)
        d_loss += d_batch_loss
        g_loss += g_batch_loss

    d_loss /= i
    g_loss /= i
    d_loss_values.append(d_loss)
    g_loss_values.append(g_loss)

    with train_summary_writer.as_default():
        tf.summary.scalar('d_loss', d_loss, step=epoch)
        tf.summary.scalar('g_loss', g_loss, step=epoch)
            
end = time.time()

print(f"Training took {end - start} seconds to complete.")


from sys import _current_frames
import time
import datetime
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

import logging 
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

# Tensorflow setup
tf.debugging.set_log_device_placement(False)
logger.info("Num GPUs Available: {}".format(len(tf.config.experimental.list_physical_devices('GPU'))))
tf.config.list_physical_devices('GPU')

from preprocessing import WaveformProcessor
import gan as gan

# Data Preprocessing Constants
WAVEFORM_BOUNDS = (1200, 1600)
SPE_AREA = 500
NS_PER_MEASUREMENT = 2.5

# Model Constants
LATENT_DIM = 500
BATCH_SIZE = 32
EPOCHS = 10
NUM_CLASSES = 2
EVAL_EPOCH = 10  # How often you should get output during training

PLOT = False

# Preprocess Waveform Data
INPUT_FILE = ("/home/ryan/Documents/Data/MilliQan/outputWaveforms_812_2p5V.root")
processor = WaveformProcessor(INPUT_FILE)


# Set static bounds for LED datset
static_bounds = {key: np.array([[np.where(processor.times == WAVEFORM_BOUNDS[0])[0],
                                 np.where(processor.times == WAVEFORM_BOUNDS[1])[0]]])
                 for key in processor.histogram_dict}

# Isolate Waveforms
isolated_peaks = processor.isolate_waveforms(static_bounds)
peak_heights = np.max(isolated_peaks, axis=1)

# Create Height Classification
npe = np.round(np.divide(np.trapz(isolated_peaks), SPE_AREA))

# Normalize data
normalization = tf.keras.layers.Normalization()
normalization.adapt(isolated_peaks)

# Create dataset
dataset = tf.data.Dataset.from_tensor_slices((isolated_peaks,
                                              npe))

# Need to add back in data part to lambda function
dataset_1_npe = dataset.filter(lambda data, label: tf.math.equal(label, 1))
dataset_1_npe = dataset_1_npe.shuffle(100000).repeat(50)
dataset_2_npe = dataset.filter(lambda data, label: tf.math.equal(label, 2))
dataset_2_npe = dataset_2_npe.shuffle(100000).repeat(50)

for features, label in dataset_1_npe.take(10):
    logger.debug(f"1 npe features: {features.numpy()}")
    logger.debug(f" 1 npe labels: {label.numpy()}")

for features, label in dataset_2_npe.take(10):
    logger.debug(f"1 npe features: {features.numpy()}")
    logger.debug(f" 1 npe labels: {label.numpy()}")
#breakpoint()
dataset = tf.data.Dataset.sample_from_datasets([dataset_1_npe, dataset_2_npe], weights=[0.5, 0.5])
dataset = dataset.batch(BATCH_SIZE).prefetch(buffer_size=tf.data.experimental.
                                             AUTOTUNE)
# Get size of dataset
logger.debug("About to count size of dataset")
data_counter = 0 
for data in dataset:
    data_counter += 1
logger.debug(f"Size of Dataset: {data_counter}")
# Test that the datasets have been sampled correctly
for features, label in dataset.take(1):
  logger.debug(f"Mean value of dataset labels: {label.numpy().mean()}")

if PLOT:
    for i, value in enumerate(isolated_peaks):
        logger.debug(f"Index: {value}")
        plt.clf()
        plt.plot(value)
        plt.text(3, 6, f"NPE: {npe[i]}", fontsize=12, color='red')
        plt.show()
        plt.savefig(f"Plots/isolated_peak_{i}.png")


        
# Defining GAN
discriminator = gan.build_discriminator(embed_dim=128, input_shape=500,
                                        num_classes=NUM_CLASSES+1,
                                        normalization_layer=normalization)

generator = gan.build_generator(LATENT_DIM, output_shape=500, embed_dim=16,
                                  num_classes=NUM_CLASSES+1)

logger.info(generator.summary())
# Train Models
generator_opt = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
disc_opt = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)

d_loss_values = np.zeros(EPOCHS)
g_loss_values = np.zeros(EPOCHS) 


# Create summaries for tensorboard
current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
train_log_dir = 'logs/gradient_tape/' + current_time + '/train'
train_summary_writer = tf.summary.create_file_writer(train_log_dir)



start = time.time()
for epoch in range(EPOCHS):
    # Monitoring of training
    if (epoch % 10) == 0:
        logger.info(f"On epoch {epoch}")

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
    d_loss_values[epoch] = d_loss
    g_loss_values[epoch] = g_loss

    with train_summary_writer.as_default():
        tf.summary.scalar('d_loss', d_loss, step=epoch)
        tf.summary.scalar('g_loss', g_loss, step=epoch)
            
end = time.time()
logger.info(f"Training took {end - start} seconds to complete.")

generator.save("trained_models/generator_{}.keras".format(current_time))
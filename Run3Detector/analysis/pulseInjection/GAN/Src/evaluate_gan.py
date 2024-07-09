import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

batch_size = 100
latent_dim = 500

noise = tf.random.normal([batch_size, latent_dim])
labels = np.ones(batch_size)

generator = tf.keras.models.load_model("TrainedModels/generator_500.keras")
generated_waveforms = generator([noise, labels])
for waveform in generated_waveforms:
    plt.plot(waveform)

plt.show()


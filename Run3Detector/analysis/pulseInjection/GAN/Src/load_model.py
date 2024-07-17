"""
File to load in pretrained models and generate samples
"""
import tensorflow as tf
import matplotlib.pyplot as plt

import Lib.gan

LATENT_DIM = 1000
discriminator = tf.keras.models.load_model('TrainedModels/discriminator.keras')
gan_model = discriminator = tf.keras.models.load_model('TrainedModels/gan.keras')
generator = tf.keras.models.load_model('TrainedModels/generator.keras')


gan_creator = gan.GAN()
gen_x, gen_y = gan_creator.generate_fake_samples(generator, LATENT_DIM, 5)
print(gen_x)

plt.plot(gen_x[1])
plt.show()

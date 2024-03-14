from typing import Dict

from keras.models import Sequential
import matplotlib.pyplot as plt
from keras.layers import Dense
import numpy as np
import numpy.typing as npt


class GAN():

    def define_discriminator(self, n_inputs=100, optimizer='adam'):
        model = Sequential()
        model.add(Dense(25, activation='relu', kernel_initializer='he_uniform', input_dim=n_inputs))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        return model

    def define_generator(self, latent_dim, n_outputs=100):
        model = Sequential()
        model.add(Dense(500, activation = 'relu', kernel_initializer='he_uniform', input_dim=latent_dim))
        model.add(Dense(n_outputs, activation='linear'))
        return model

    def define_gan(self, generator, discriminator):
        discriminator.trainable = False
        model = Sequential()
        model.add(generator)
        model.add(discriminator)
        # This will compile the generator as well
        model.compile(loss='binary_crossentropy', optimizer='adam')
        return model

    def generate_real_samples(self, isolated_waveforms, number_of_samples: int):
        random_choices = np.random.randint(0, high=len(isolated_waveforms),
                                        size=number_of_samples)
        x_train = isolated_waveforms[random_choices]
        print(len(isolated_waveforms[0]))
        x_train = x_train.reshape(number_of_samples, len(isolated_waveforms[0]))
        y = np.ones((number_of_samples, 1))
        return x_train, y

    def generate_latent_points(self, latent_dim, n):
        x_input = np.random.randn(latent_dim, n)
        x_input = x_input.reshape(n, latent_dim)
        return x_input

    def generate_fake_samples(self, generator, latent_dim, n):
        x_input = self.generate_latent_points(latent_dim, n)
        gen_x = generator.predict(x_input)
        gen_y = np.zeros((n, 1))
        return gen_x, gen_y

    def summarize_performance(self, epoch, generator, discriminator, latent_dim, isolated_waveforms, n=100):

        x_real, y_real = self.generate_real_samples(isolated_waveforms, n)
        _, acc_real = discriminator.evaluate(x_real, y_real, verbose=0)
        x_fake, y_fake = self.generate_fake_samples(generator, latent_dim, n)
        _, acc_fake = discriminator.evaluate(x_fake, y_fake, verbose=0)
        print(epoch, acc_real, acc_fake)
        plt.plot(x_real[0], color='red')
        plt.plot(x_fake[0], color='blue')
        plt.show()

    def train(self, generator, discriminator,
              gan, latent_dim, input_data: Dict[str, npt.NDArray], n_epochs=10000,
            n_batch=32, n_eval=2000):

        half_batch = int(n_batch/2)
        for i in range(n_epochs):
            x_real, y_real = self.generate_real_samples(input_data, half_batch)
            x_fake, y_fake = self.generate_fake_samples(generator, latent_dim, half_batch)
            discriminator.train_on_batch(x_real, y_real)
            discriminator.train_on_batch(x_fake, y_fake)
            x_gan = self.generate_latent_points(latent_dim, n_batch)

            # You only train the discriminator during GAN training
            # Therefore, you want the generator to output data that passes as
            # real data

            y_gan = np.ones((n_batch, 1)) 
            gan.train_on_batch(x_gan, y_gan)
            if (i + 1) % n_eval == 0:
                self.summarize_performance(i, generator, discriminator, latent_dim, input_data)

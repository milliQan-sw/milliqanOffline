import tensorflow as tf
from tensorflow.keras.layers import (Input, Dense, LeakyReLU, Embedding, Flatten,
                                     Concatenate, Reshape, Activation)
from tensorflow.keras.models import Model

def build_generator(latent_dim, output_shape, embed_dim, num_classes):
    noise = Input((latent_dim), name="noise_input")
    x = Dense(256, name="gen_dense0")(noise)
    x = LeakyReLU(0.2, name="gen_relu0")(x)

def define_discriminator(n_inputs, num_classes):
    inputs = layers.Input(shape=n_inputs)
    labels = layers.Input(shape=(num_classes))
    concatenated = layers.Concatenate()([inputs, labels])
    x = Dense(25, activation='relu')(concatenated)
    output = Dense(1, activation='sigmoid')(x)
    model = keras.Model([inputs, labels], output)
    return model

def define_generator(self, latent_dim, n_outputs=100, num_classes=4):
    inputs = layers.Input(shape=(latent_dim,))
    labels = layers.Input(shape=(num_classes))
    concatenated = layers.Concatenate()([inputs, labels])
    x = layers.Dense(500, activation= 'relu')(concatenated)
    output = layers.Dense(n_outputs, activation='linear')(x)

    return keras.Model([inputs, labels], output)

class GAN():
    NUM_CLASSES = 4

    def define_discriminator(self, n_inputs=100, optimizer='adam'):
        inputs = layers.Input(shape=n_inputs)
        labels = layers.Input(shape=(self.NUM_CLASSES))
        concatenated = layers.Concatenate()([inputs, labels])
        x = Dense(25, activation='relu')(concatenated)
        output = Dense(1, activation='sigmoid')(x)
        model = keras.Model([inputs, labels], output)
        model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])

        return model

    def define_generator(self, latent_dim, n_outputs=100):
        inputs = layers.Input(shape=(latent_dim,))
        labels = layers.Input(shape=(self.NUM_CLASSES))
        concatenated = layers.Concatenate()([inputs, labels])
        x = layers.Dense(500, activation= 'relu')(concatenated)
        output = layers.Dense(n_outputs, activation='linear')(x)

        return keras.Model([inputs, labels], output)

    def define_gan(self, generator, discriminator):
        discriminator.trainable = False
        model = Sequential()
        print("LZDFLKSJDF")
        model.add(generator)
        print("AHHHH")
        model.add(discriminator)
        # This will compile the generator as well
        model.build(input_shape=(generator.input_shape[0], generator.input_shape[1] + self.NUM_CLASSES))
        model.compile(loss='binary_crossentropy', optimizer='adam')
        return model

    def generate_real_samples(self, isolated_waveforms,
                              number_of_samples: int):
        waveform, npe_label = isolated_waveforms

        random_choices = np.random.randint(0, high=len(isolated_waveforms),
                                           size=number_of_samples)
        x_train = waveform[random_choices]
        x_train = x_train.reshape(number_of_samples,
                                  len(isolated_waveforms[0]))
        return [x_train, npe_label]

    label = Input((1), name="class_label")
    l = Embedding(num_classes, embed_dim)(label)
    l = Flatten()(l)

    def generate_fake_samples(self, generator, latent_dim, labels, n):
        random_latent_vectors = tf.random.normal(shape=(n, latent_dim))
        gen_x = generator.predict(random_latent_vectors)
        return [gen_x, labels]

    def summarize_performance(self, epoch, generator, discriminator, latent_dim, isolated_waveforms, labels, n=100, save_dir="Plots/"):

        x_real =  self.generate_real_samples(isolated_waveforms, n)
        y_real = np.ones((n, 1))
        _, acc_real = discriminator.evaluate(x_real, y_real, verbose=0)
        x_fake = self.generate_fake_samples(generator, latent_dim, x_real[1], n)
        y_fake = np.zeros((n, 1))
        _, acc_fake = discriminator.evaluate(x_fake, y_fake, verbose=0)

        print(epoch, acc_real, acc_fake)
        plt.clf()
        plt.plot(x_fake[0], color='blue')
        plt.savefig(save_dir+f"waveform_{epoch}")
        plt.show()

    def train(self, generator, discriminator,
              gan, latent_dim, input_data: Dict[str, np.ndarray],
              n_epochs=10000, n_batch=32,
              n_eval=2000) -> Union[list[float], np.ndarray]:

        half_batch = int(n_batch/2)
        loss: list[float] = []
        y_real = np.ones((half_batch, 1))
        y_fake = np.zeros((half_batch, 1))
        for i in range(n_epochs):
            x_real = self.generate_real_samples(input_data, half_batch)

            x_fake = self.generate_fake_samples(generator, latent_dim, x_real[1], half_batch)
            discriminator.train_on_batch(x_real, y_real)
            discriminator.train_on_batch(x_fake, y_fake)
            x_gan = self.generate_latent_points(latent_dim, n_batch)
            # You only train the discriminator during GAN training
            # Therefore, you want the generator to output data that passes as
            # real data
            y_gan = np.ones((n_batch, 1)) 
            loss.append(gan.train_on_batch(x_gan, y_gan))

            if (i + 1) % n_eval == 0:
                self.summarize_performance(i, generator, discriminator,
                                           latent_dim, input_data, labels)
#        data = self.generate_fake_samples(generator, latent_dim, 1)
#        plt.plot(data[0][0])
#        plt.show()
        return loss, generator.get_weights() 

class ConditionalGAN(keras.Model):
    def __init__(self, generator, discriminator):
        super().__init__()
        self.generator = generator
        self.discriminator = discriminator

    def compile(self, d_optimizer, g_optimizer, loss_fn):
        super().compile()
        self.d_optimizer = d_optimizer
        self.g_optimizer = g_optimizer
        self.loss_fn = loss_fn

    def train_step(self, data, laten_dimension=1000):
        real_waveforms, labels = data

        # Generate Fake Images
        random_latent_vectors = tf.random.normal(shape=(tf.shape(real_waveforms)[0], latent_dimension))
        generated_waveforms = self.generator([random_latent_vectors, labels])

        # Train discriminator
        with tf.GradientTape() as tape:
            fake_output = self.discriminator([generated_waveforms, labels])
            real_output = self.discriminator([real_waveforms, labels])
            d_loss = self.loss_fn(tf.ones_like(real_output), real_output) + self.loss_fn(tf.zeros_like(fake_output), fake_output)
        grads = tape.gradient(d_loss, self.discriminator.trainable_weights)
        self.d_optimizer.apply_gradients(zip(grads, self.discriminator.trainable_weights))

        with tf.GradientTape() as tape:
            generated_waveforms = self.generator([random_latent_vectors, labels])
            fake_output = self.discriminator([generated_images, labels])
            g_loss = self.loss_fn(tf.ones_like(fake_output), fake_output)
        grads = tape.gradient(g_loss, self.generator.trainable_weights)
        self.g_optimizer.apply_gradients(zip(grads, self.generator.trainable_weights))

        return {"d_loss": d_loss, "g_loss": g_loss}

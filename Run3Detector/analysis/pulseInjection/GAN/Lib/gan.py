from typing import Tuple

import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import (Input, Dense, LeakyReLU, Embedding, Flatten,
                                     Concatenate, Reshape, Activation, Normalization)
from tensorflow.keras.models import Model


def build_generator(latent_dim, output_shape, embed_dim, num_classes):
    noise = Input((latent_dim,), name="noise_input")
    x = Dense(256, name="gen_dense0")(noise)
    x = LeakyReLU(0.2, name="gen_relu0")(x)

    label = Input((1,), name="label")
    l = Embedding(num_classes, embed_dim, input_length=1)(label)
    l = Flatten()(l)

    x = Concatenate()([x, l])
    x = Dense(256, name="gen_dense1")(x)
    x = LeakyReLU(0.2, name="gen_relu1")(x)

    return Model([noise, label], output, name="generator")

def build_discriminator(embed_dim, input_shape, num_classes):
    waveform = Input((input_shape,), name="discriminator_input")
    x = Dense(64)(waveform)
    x = LeakyReLU(0.2)(x)
    output = Dense(1, name="disc_dense1")(x)

    label = Input((1,), name="class_label")
    l = Embedding(num_classes, embed_dim)(label)
    l = Flatten()(l)


def calculate_extra_metrics(waveform):
    area = np.trapz(waveform, axis=1)
    height = np.max(waveform, axis=1)
    return np.column_stack((area, height))


# The discriminator loss is defined as the combination of how well it is able
# discriminate against real and fake data. The generator loss measures
# how often the generated data is caught by the discriminator. Even ideally,
# the loss should not go to 0, it will meet in the middle somewhere
@tf.function
def train_step (real_waveforms, real_labels, latent_dim, generator, discriminator, g_opt, d_opt):
    d_loss = 0
    g_loss = 0
    batch_size = tf.shape(real_waveforms)[0]
    cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)

    noise = tf.random.normal([batch_size, latent_dim])

    # Gradient tape keeps track of the forward pass so that you can back-propagate the errors
    with tf.GradientTape() as dtape, tf.GradientTape() as gtape:
        # Generate waveforms
        generated_waveforms = generator(
            [noise, real_labels], training=True)

        gen_extra_info = calculate_extra_metrics(generated_waveforms)

            # The loss of the GAN is the cumulative loss on the real and fake data
            d_real_loss = bce_loss(tf.ones_like(real_output), real_output)
            d_fake_loss = bce_loss(tf.zeros_like(fake_output), fake_output)
            d_loss = d_real_loss + d_fake_loss

        # Train the discriminator over real data and generated data
        real_output = discriminator(
            [real_waveforms, real_labels, real_extra_info], training=True)
        fake_output = discriminator(
            [generated_waveforms, real_labels, gen_extra_info], training=True)

        # The loss of the GAN is the cumulative loss on the real and fake data
        d_real_loss = cross_entropy(tf.ones_like(real_output), real_output)
        d_fake_loss = cross_entropy(tf.zeros_like(fake_output), fake_output)
        d_loss = d_real_loss + d_fake_loss

        # Train generator
        generated_waveforms = generator([noise, real_labels], training=True)
        gen_extra_info = calculate_extra_metrics(generated_waveforms)
        fake_output = discriminator(
            [generated_waveforms, real_labels, gen_extra_info], training=True)
        g_loss = cross_entropy(tf.ones_like(fake_output), fake_output)

    d_grad = dtape.gradient(d_loss, discriminator.trainable_variables)
    d_opt.apply_gradients(zip(d_grad, discriminator.trainable_variables))

    g_grad = gtape.gradient(g_loss, generator.trainable_variables)
    g_opt.apply_gradients(zip(g_grad, generator.trainable_variables))

    return d_loss, g_loss

def generate_waveforms(generator, labels, latent_dim=500):
    noise = tf.random.normal([len(labels), latent_dim])
    labels = tf.convert_to_tensor(labels, dtype='int64')
    return generator([noise, labels], training=False)

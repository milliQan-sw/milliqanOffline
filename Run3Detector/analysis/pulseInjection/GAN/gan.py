from typing import Tuple

import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import (Input, Dense, LeakyReLU, Embedding, Flatten,
                                     Concatenate, Reshape, Activation, Normalization)
from tensorflow.keras.models import Model


def build_generator(latent_dim, output_shape, embed_dim, num_classes):
    noise = Input((latent_dim), name="noise_input")
    x = Dense(256, name="gen_dense0")(noise)
    x = LeakyReLU(0.2, name="gen_relu0")(x)

    label = Input((1), name="label")
    l = Embedding(num_classes, embed_dim, input_length=1)(label)
    l = Flatten()(l)

    x = Concatenate()([x, l])
    x = Dense(256, name="gen_dense1")(x)
    x = LeakyReLU(0.2, name="gen_relu1")(x)
    # x = dense(output_shape)(x)
    # x = leakyrelu(0.2)(x)

    output = Activation("tanh")(x)
    output = Dense(output_shape, name="gen_dense2")(x)
    return Model([noise, label], output, name="generator")


# def build_discriminator(embed_dim, input_shape, num_classes):
#     waveform = Input((input_shape), name="discriminator_input")
#     x = Dense(64)(waveform)
#     x = LeakyReLU(0.2)(x)
#     x = Flatten()(x)

#     label = Input((1), name="class_label")
#     label = Embedding(num_classes, embed_dim)(label)
#     label = Flatten()(label)

#     extra_info = Input((2,), name="extra_info")
#     extra_info = Normalization()(extra_info)

#     x = Concatenate()([x, label, extra_info])
#     output = Dense(1)(x)

#     return Model([waveform, label, extra_info], output, name="discriminator")
# Data input
def build_discriminator(embed_dim, input_shape, num_classes):
    data_input = Input(input_shape, name="data_input")
    x = Flatten()(data_input)

    # Label input
    label_input = Input((1,), name="label")
    label_embedding = Embedding(num_classes, 10)(label_input)
    label_embedding = Flatten()(label_embedding)

    # Extra info input
    extra_info_input = Input((2), name="extra_info_input")
    extra_info_flat = Flatten()(extra_info_input)

    # Concatenate all inputs
    concatenated_inputs = Concatenate(name='disc_concat')(
        [x, label_embedding, extra_info_flat])

    # Discriminator layers
    x = Dense(256, name="disc_dense0")(concatenated_inputs)
    x = LeakyReLU(0.2, name="disc_relu0")(x)
    output = Dense(1, name="disc_dense1", activation="tanh")(x)

    # Create and compile the discriminator model
    discriminator = Model(
        [data_input, label_input, extra_info_input], output, name="discriminator")
    return discriminator


def calculate_extra_metrics(waveform):
    area = np.trapz(waveform, axis=1)
    height = np.max(waveform, axis=1)
    return np.column_stack((area, height))


# The discriminator loss is defined as the combination of how well it is able
# discriminate against real and fake data. The generator loss measures
# how often the generated data is caught by the discriminator. Even ideally,
# the loss should not go to 0, it will meet in the middle somewhere
def train_step(real_waveforms, real_labels, latent_dim, num_classes, generator, discriminator, g_opt, d_opt, batch_size):
    batch_size = tf.shape(real_waveforms)[0]
    bce_loss = tf.keras.losses.BinaryCrossentropy(
        from_logits=True, label_smoothing=0.1)

    noise = tf.random.normal([batch_size, latent_dim])

    for _ in range(3):
        # Gradient tape keeps track of the forward pass so that you can back-propagate the errors
        with tf.GradientTape() as dtape:
            # Generate waveforms
            generated_waveforms = generator(
                [noise, real_labels], training=True)

            gen_extra_info = calculate_extra_metrics(generated_waveforms)

            real_extra_info = calculate_extra_metrics(real_waveforms)

            # Train the discriminator over real data and generated data
            real_output = discriminator(
                [real_waveforms, real_labels, real_extra_info], training=True)
            fake_output = discriminator(
                [generated_waveforms, real_labels, gen_extra_info], training=True)

            # The loss of the GAN is the cumulative loss on the real and fake data
            d_real_loss = bce_loss(tf.ones_like(real_output), real_output)
            d_fake_loss = bce_loss(tf.zeros_like(fake_output), fake_output)
            d_loss = d_real_loss + d_fake_loss

        d_grad = dtape.gradient(d_loss, discriminator.trainable_variables)
        d_opt.apply_gradients(zip(d_grad, discriminator.trainable_variables))

    with tf.GradientTape() as gtape:
        generated_waveforms = generator([noise, real_labels], training=True)
        gen_extra_info = calculate_extra_metrics(generated_waveforms)
        fake_output = discriminator(
            [generated_waveforms, real_labels, gen_extra_info], training=True)
        g_loss = bce_loss(tf.ones_like(fake_output), fake_output)
    g_grad = gtape.gradient(g_loss, generator.trainable_variables)
    g_opt.apply_gradients(zip(g_grad, generator.trainable_variables))

    return d_loss, g_loss

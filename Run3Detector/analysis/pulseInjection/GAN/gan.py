import tensorflow as tf
from tensorflow.keras.layers import (Input, Dense, LeakyReLU, Embedding, Flatten,
                                     Concatenate, Reshape, Activation)
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

    output = Activation("tanh")(x)
    output = Dense(output_shape, name="gen_dense2")(x)
    return Model([noise, label], output, name="generator")

def build_discriminator(embed_dim, input_shape, num_classes):
    waveform = Input((input_shape,), name="discriminator_input")
    x = Dense(64)(waveform)
    x = LeakyReLU(0.2)(x)

    label = Input((1,), name="class_label")
    l = Embedding(num_classes, embed_dim)(label)
    l = Flatten()(l)

    x = Concatenate()([x, l])
    output = Dense(1)(x)

    return Model([waveform, label], output, name="discriminator")

# The discriminator loss is defined as the combination of how well it is able
# discriminate against real and fake data. The generator loss measures
# how often the generated data is caught by the discriminator. Even ideally,
# the loss should not go to 0, it will meet in the middle somewhere
@tf.function
def train_step (real_waveforms, real_labels, latent_dim, generator, discriminator, g_opt, d_opt):
    d_loss = 0
    g_loss = 0
    batch_size = tf.shape(real_waveforms)[0]
    bce_loss = tf.keras.losses.BinaryCrossentropy(from_logits=True, label_smoothing=0.1)

    noise = tf.random.normal([batch_size, latent_dim])

    for _ in range(3):
        # Gradient tape keeps track of the forward pass so that you can back-propagate the errors
        with tf.GradientTape() as dtape:
            # Generate waveforms
            generated_waveforms = generator([noise, real_labels], training=True)

            # Train the discriminator over real data and generated data
            real_output = discriminator([real_waveforms, real_labels], training=True)
            fake_output = discriminator([generated_waveforms, real_labels], training=True)

            # The loss of the GAN is the cumulative loss on the real and fake data
            d_real_loss = bce_loss(tf.ones_like(real_output), real_output)
            d_fake_loss = bce_loss(tf.zeros_like(fake_output), fake_output)
            d_loss = d_real_loss + d_fake_loss

        d_grad = dtape.gradient(d_loss, discriminator.trainable_variables)
        d_opt.apply_gradients(zip(d_grad, discriminator.trainable_variables))

    with tf.GradientTape() as gtape:
        generated_waveforms = generator([noise, real_labels], training=True)
        fake_output = discriminator([generated_waveforms, real_labels], training=True)
        g_loss = bce_loss(tf.ones_like(fake_output), fake_output)
    g_grad = gtape.gradient(g_loss, generator.trainable_variables)
    g_opt.apply_gradients(zip(g_grad, generator.trainable_variables))

    return d_loss, g_loss

def generate_waveforms(generator, labels, latent_dim=500):
    noise = tf.random.normal([len(labels), latent_dim])
    labels = tf.convert_to_tensor(labels, dtype='int64')
    return generator([noise, labels], training=False)
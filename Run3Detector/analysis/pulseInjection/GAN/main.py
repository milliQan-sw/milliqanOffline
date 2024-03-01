import numpy as np
import os
import pickle
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import uproot
import logging
from ROOT import TSpectrum, TFile, TH1
import tensorflow as tf
from tensorflow.keras import layers

logging.basicConfig(level="DEBUG")


class WaveformProcessor():
    def __init__(self, input_file_path: str):
        input_file = uproot.open(input_file_path)
        histogram_names = input_file.keys()

        logging.debug(f"Input file: {input_file}")

        self.ns_per_measurement = 2.5
        self.number_of_measurements = 1024

        stop_time = self.number_of_measurements * self.ns_per_measurement
        self.times = np.arange(0,
                               stop_time,
                               self.ns_per_measurement)

        self.histogram_dict = {}

        for name in histogram_names:
            histogram = input_file[name]
            if histogram.classname == "TH1D":
                data = histogram.values()

                # Remove trailing ;1 from names given by uproot
                self.histogram_dict[name[:name.rfind(";")]] = data

        self.background_estimation(input_file_path)
        logging.debug(f" Histograms: {self.histogram_dict}")
        self.voltage_window = np.zeros(1024)

    def background_estimation(self, input_file: str):
        self.noise_dict = {}
        input_file = TFile(input_file, "READ")
        for key in input_file.GetListOfKeys():
            obj = key.ReadObj()
            if isinstance(obj, TH1):
                spectrum = TSpectrum()
                background_hist = spectrum.Background(obj)
                background_values = [background_hist.GetBinContent(i)
                                     for i in range(background_hist.GetNbinsX())]

                background_array = np.array(background_values)

                self.noise_dict[key.GetName()] = np.mean(background_array)

    def find_waveform_bounds(self) -> None:
        self.peak_dictionary = {}
        for key, value in self.histogram_dict.items():
            peak_positions, _ = find_peaks(value, prominence=5, height=15)
            pulse_bounds = np.empty([len(peak_positions), 2])

            continue_flag = False
            for i, index in enumerate(peak_positions):
                start_index = index
                while (start_index > 0 and
                       value[start_index] > self.noise_dict[key]):
                    start_index -= 1

                pulse_bounds[i][0] = start_index

                stop_index = index
                while (stop_index < len(value) and
                       value[stop_index] > self.noise_dict[key]):
                    stop_index += 1
                pulse_bounds[i][1] = stop_index

                # If the bounds of the waveform lie at the edge of the window,
                # it's probably a messy event so just dump it

                if stop_index == len(value) or start_index == 0:
                    continue_flag = True
                    break

            if continue_flag:
                continue
            self.peak_dictionary[key] = pulse_bounds

        logging.debug(f"Peaks: {self.peak_dictionary}")

    def isolate_waveforms(self):
        number_of_waves: int = sum([len(peak) for peak in
                                    self.peak_dictionary.values()])

        input_data = np.zeros((number_of_waves, 1024))

        index = 0
        for key, value in self.peak_dictionary.items():
            # Slice values in histogram_dict to just capture waveforms
            for waveform in value:

                logging.debug(f"Key: {key} \n"
                              f"Index: {waveform[0]}, {waveform[1]}\n")

                sliced_histogram_values = (self.histogram_dict[key]
                                           [int(waveform[0]):int(waveform[1]+1)])

                input_data[index][:len(sliced_histogram_values)
                                  ] = sliced_histogram_values
                index += 1
        return input_data

    def calculate_npe(self, waveforms: np.ndarray, area_per_spe: float) -> int:
        waveform_area = np.trapz(waveforms, dx=self.ns_per_measurement)
        return np.round(np.divide(waveform_area, area_per_spe))

    def plot_waveforms(self, plotDirectory: str) -> None:
        if not os.path.exists(plotDirectory):
            os.mkdir(plotDirectory)

        for key, value in self.histogram_dict.items():
            plt.clf()
            plt.plot(self.times, value)
            for peak in self.peak_dictionary[key]:
                plt.axvline(peak[0])
                plt.axvline(peak[1])

            plt.savefig("{0}/{1}.png".format(plotDirectory, key))


def build_waveform_generator(latent_dim, num_classes):
    model = tf.keras.Sequential()
    model.add(layers.InputLayer(input_shape = (1024, 1)))
    model.add(layers.Dense(4096, use_bias=False, input_shape=(100,)))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Conv1DTranspose(4096, 10, strides=1, padding='same', use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Conv1DTranspose(1024, 10, strides=1, padding='same', use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())
    print(model.output_shape)


def build_waveform_descriminator(num_npe):
    label = layers.Input(shape=(num_npe,))

    x = layers.Dense(512, activation='relu')(input_data)
    x = layers.Dense(256, activation='relu')(x)
    validity = layers.Dense(1, activation='sigmoid')(x)
    return Model([input_data, label], validity)


if __name__ == "__main__":
    processor = WaveformProcessor(
        "/home/ryan/Documents/Research/Data/MilliQanWaveforms/"
        "outputWaveforms_812_2p5V.root")

    bounds = processor.find_waveform_bounds()
    x_train = processor.isolate_waveforms()
    plt.plot(x_train[0])
    plt.savefig("train_waveform.png")
    y_train = processor.calculate_npe(x_train, 480)

    assert len(x_train) == len(y_train), ("There are not the same number"
                                          "of labels and waveforms")

    latent_dim = 100
    num_classes = 2

    # Build Model
    # discriminator = build_waveform_descriminator(num_classes)
    # discriminator.compile(optimizer='adagrad',
    #                       loss='binary_crossentropy', metrics=['accuracy'])

    generator = build_waveform_generator(latent_dim, num_classes)
    # noise = layers.Input(shape=(latent_dim,))
    # label = layers.Input(shape=(num_classes,))

    # generated_data = generator([noise, label])
    # validity = discriminator([generated_data, label])

    # combined = Model([noise, label], validity)

    # combined.compile(optimizer='adagrad',
    #                  loss='binary_crossentropy', metrics=['accuracy'])
    # generator = build_waveform_generator(latent_dim, num_classes)

    # generator.compile(optimizer='adagrad',
    #                   loss='binary_crossentropy', metrics=['accuracy'])
    # # Train Model
    # batch_size = 64
    # epochs = 1000

    # for epoch in range(epochs):
    #     idx = np.random.randint(0, x_train.shape[0], batch_size)
    #     real_data = x_train[idx]
    #     labels = y_train[idx]

    #     # Generate noise for generator
    #     noise = np.random.normal(0, 1, (batch_size, latent_dim))
    #     fake_labels = np.random.randint(0, num_classes, batch_size)
    #     generated_data = generator.predict([noise, fake_labels])

    #     real_data_with_labels = np.concatenate(
    #         [real_data, labels.reshape(-1, 1)], axis=1)

    #     generated_data_with_labels = np.concatenate(
    #         [generated_data, fake_labels.reshape(-1, 1)], axis=1)

    #     # Train discriminator
    #     desc_loss_real = discriminator.train_on_batch(
    #         [real_data, labels], np.ones((batch_size, 1)))
    #     desc_loss_fake = discriminator.train_on_batch(
    #         [generated_data, fake_labels], np.zeros((batch_size, 1)))

    #     desc_loss = 0.5 * np.add(desc_loss_fake, desc_loss_real)

    #     # Train generator
    #     noise = np.random.normal(0, 1, (batch_size, latent_dim))
    #     fake_labels = np.random.randint(0, num_classes, batch_size)

    #     gen_loss = combined.train_on_batch(
    #         [noise, fake_labels], np.ones((batch_size, 1)))
    #     print(
    #         f"Epoch {epoch+1}, Discriminator Loss: {desc_loss[0]},"
    #         f"Generator Loss: {gen_loss}")

    # noise = np.random.normal(0, 1, (10, latent_dim))
    # labels = np.ones(10)

    # generated_data = generator.predict([noise, labels])

    # with open('gen_waveforms.pickle', 'wb') as f:
    #     pickle.dump(generated_data, f)

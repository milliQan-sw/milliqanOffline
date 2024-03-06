import numpy as np
import os
import pickle
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import uproot
import logging
from ROOT import TSpectrum, TFile, TH1
import tensorflow as tf
from tensorflow.keras import layers, Model
from keras.models import Sequential
from keras.layers import Dense

logging.basicConfig(level="WARNING")


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

    # TODO make way to set bounds manually 
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

        input_data = np.zeros((number_of_waves, 100))

        index = 0
        for key, value in self.peak_dictionary.items():
            # Slice values in histogram_dict to just capture waveforms
            for waveform in value:

                logging.debug(f"Key: {key} \n"
                              f"Index: {waveform[0]}, {waveform[1]}\n")

                sliced_histogram_values = (self.histogram_dict[key]
                                           [int(waveform[0]):int(waveform[1]+1)])

                if len(sliced_histogram_values) > 100: continue
                    
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
            try :
                plt.clf()
                plt.plot(self.times, value)
                for peak in self.peak_dictionary[key]:
                    plt.axvline(self.times[int(peak[0])], color='r')
                    plt.axvline(self.times[int(peak[1])], color='r')
            
                plt.savefig("{0}/{1}.png".format(plotDirectory, key))
            except KeyError: 
                continue

def define_discriminator(n_inputs=100, optimizer='adam'):
    model = Sequential()
    model.add(Dense(25, activation='relu', kernel_initializer='he_uniform', input_dim=n_inputs))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    return model

def define_generator(latent_dim, n_outputs=100):
    model = Sequential()
    model.add(Dense(500, activation = 'relu', kernel_initializer='he_uniform', input_dim=latent_dim))
    model.add(Dense(n_outputs, activation='linear'))
    return model

def define_gan(generator, discriminator):
    discriminator.trainable = False
    model = Sequential()
    model.add(generator)
    model.add(discriminator)
    # This will compile the generator as well
    model.compile(loss='binary_crossentropy', optimizer='adam')
    return model

def generate_real_samples(isolated_waveforms, number_of_samples: int):
    print("ISo:", isolated_waveforms)
    random_choices = np.random.randint(0, high=len(isolated_waveforms),
                                       size=number_of_samples)
    x_train = isolated_waveforms[random_choices]
    x_train = x_train.reshape(number_of_samples, 100)
    y = np.ones((number_of_samples, 1))
    return x_train, y

def generate_latent_points(latent_dim, n):
    x_input = np.random.randn(latent_dim, n)
    x_input = x_input.reshape(n, latent_dim)
    return x_input

def generate_fake_samples(generator, latent_dim, n):
    x_input = generate_latent_points(latent_dim, n)
    gen_x = generator.predict(x_input)
    gen_y = np.zeros((n, 1))
    return gen_x, gen_y

def summarize_performance(epoch, generator, discriminator, latent_dim, isolated_waveforms, n=100):

    x_real, y_real = generate_real_samples(isolated_waveforms, n)
    _, acc_real = discriminator.evaluate(x_real, y_real, verbose=0)
    x_fake, y_fake = generate_fake_samples(generator, latent_dim, n)
    _, acc_fake = discriminator.evaluate(x_fake, y_fake, verbose=0)
    print(epoch, acc_real, acc_fake)
    plt.plot(x_real[0], color='red')
    plt.plot(x_fake[0], color='blue')
    plt.show()

def train(generator, discriminator,
          gan, latent_dim, input_file, n_epochs=10000,
          n_batch=128, n_eval=2000):
    
    processor = WaveformProcessor(input_file)
    bounds = processor.find_waveform_bounds()
    print(bounds)
    isolated_waveforms = processor.isolate_waveforms()
    half_batch = int(n_batch/2)
    for i in range(n_epochs):
        x_real, y_real = generate_real_samples(isolated_waveforms, half_batch)
        x_fake, y_fake = generate_fake_samples(generator, latent_dim, half_batch)
        discriminator.train_on_batch(x_real, y_real)
        discriminator.train_on_batch(x_fake, y_fake)
        x_gan = generate_latent_points(latent_dim, n_batch)

        # You only train the discriminator during GAN training
        # Therefore, you want the generator to output data that passes as
        # real data

        y_gan = np.ones((n_batch, 1)) 
        gan.train_on_batch(x_gan, y_gan)
        if (i + 1) % n_eval == 0:
            summarize_performance(i, generator, discriminator, latent_dim, isolated_waveforms)
            
input_file = "/home/ryan/Documents/Data/MilliQan/outputWaveforms_812_2p5V.root"
latent_dim = 1000
discriminator = define_discriminator()
generator = define_generator(latent_dim)
gan_model = define_gan(generator, discriminator)
train(generator, discriminator, gan_model, latent_dim, n_epochs=10000, input_file=input_file, n_eval=2000)

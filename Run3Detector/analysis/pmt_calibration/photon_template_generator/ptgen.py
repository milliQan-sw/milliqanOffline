import ROOT as r
import numpy as np

model_defs = {
    "r878": {
        "template" : "assets/templates_r878.root",
        "areas" : "assets/r878_areas_1450V.root",
        "input_rates" : [0.7, 1.0, 1.6, 2.0, 5.0],
        },
    "r7725": {
        "template" : "assets/templates_r7725.root",
        "areas" : "assets/r7725_areas_1400V.root",
        "input_rates" : [0.7, 1.0, 1.6, 2.0, 5.0],
        },
    "et": {
        "template" : "assets/templates_et.root",
        "areas" : "assets/et_areas_1700V.root",
        "input_rates" : [0.7, 1.0, 1.6, 2.0, 5.0],
        }
    }

def GenerateSignal(model="r878", samp_freq=2.0, noise=None, extend=None):
    # model defines which PMT to use (see model_defs above)
    # samp_freq is the sampling frequency of the ouput waveform
    # (in GHz, so 2.0 means time bin spacing of 0.5 ns)
    # samp_freq must be in the list of input rates from the model defs
    # if noise is not None, add random gaussian noise of rms 'noise'
    # if extend is not None, extend each side of output waveform by 'extend' ns of zero voltage

    # Set seed
    r.gRandom.SetSeed(0);

    if model not in model_defs:
        raise Exception("No model definition for PMT model {0}!".format(model))

    if samp_freq not in model_defs[model]["input_rates"]:
        raise Exception("Template at sampling frequency {0} GHz does not exist for PMT {1}".format(samp_freq, model))

    template_file = model_defs[model]["template"]

    f = r.TFile(template_file)
    template = f.Get("template_{0}GHz".format(str(samp_freq).replace(".","p")))
    template.SetDirectory(0)
    f.Close()

    prenorm_area = template.Integral("width")

    # Load areas
    f = r.TFile.Open(model_defs[model]["areas"])
    # SPE area dist
    spe_areas = (f.Get("spe_fit")).Clone("spe")
    # Get random area
    area = spe_areas.GetRandom()
    # Scale template y-values
    template.Scale(area/prenorm_area)
    f.Close()

    voltages = np.zeros(template.GetNbinsX())
    for i in range(voltages.size):
        voltages[i] = template.GetBinContent(i+1)

    dt = 1.0/samp_freq
    if extend is not None:
        nsamp = int(extend/dt)
        voltages = np.append(voltages, np.zeros(nsamp))
        voltages = np.append(np.zeros(nsamp), voltages)
        
    if noise is not None:
        voltages += np.random.normal(loc=0.0, scale=noise, size=voltages.size)

    times = np.arange(voltages.size)*dt

    return times, voltages

if __name__ == "__main__":
    # times, voltages = GenerateSignal(model="r878", samp_freq=2.0, noise=0.38, extend=150)
    # times, voltages = GenerateSignal(model="r7725", samp_freq=2.0, noise=0.38, extend=150)
    times, voltages = GenerateSignal(model="et", samp_freq=1.6, noise=0.38, extend=150)

    import matplotlib.pyplot as plt
    plt.plot(times, voltages)
    plt.gca().set_xlim(0,400)
    plt.show()


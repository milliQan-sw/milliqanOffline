import numpy as np
import ROOT
import matplotlib.pyplot as plt
from typing import Union


def plot_loss(discriminator_loss:np.ndarray, generator_loss:np.ndarray,
              save_location="loss.png", show_figure=False,
              save_figure=True)->None:
    plt.plot(discriminator_loss, label="Discriminator")
    plt.plot(generator_loss, label="Generator")
    plt.ylabel("Loss")
    plt.xlabel("Epochs")
    plt.title("Loss vs Epochs")
    plt.legend()

    if save_figure:
        plt.savefig(save_location)
    if show_figure:
        plt.show() 
    
def plot_histogram(data, bins: int, min_value, max_value,
                   canvas_name: str = "canvas",
                   canvas_width=800, canvas_height=600,
                   histogram_name: str = "histogram",
                   histogram_labels="Title;X axis Title;Y Axis Title",
                   write_to_existing_file=False,
                   file_path: Union[str, None] = None) -> ROOT.TH1F:

    histogram = ROOT.TH1F(histogram_name, histogram_labels, bins, min_value,
                          max_value)
    histogram.FillN(len(data), data, np.ones(len(data)))

    histogram.Draw()
    if write_to_existing_file and file_path:
        root_file = ROOT.TFile(file_path, "RECREATE")
        histogram.Write()
        root_file.Close()
    return histogram

import ROOT
import numpy as np
from typing import Union


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

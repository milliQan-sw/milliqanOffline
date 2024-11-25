import ROOT
import unittest
import logging
import os

class WaveformAnalyzer():
    def __init__(self, input_file:ROOT.TFile, distribution:ROOT.TF1):
        self.histogram_array = ROOT.TList() 
        self.distribution = distribution
        for key in input_file.GetListOfKeys():
            obj = key.ReadObj()
            if isinstance(obj, ROOT.TH1):
                self.histogram_array.Add(obj)

        

    def waveform_area_cut(self, min_value:float=1200, max_value:float=1600, sigma:float=1):
        """
        Only grab waveforms that are within 1 for the mean SPE area. 
        """
        min_allowed_value =  self.distribution.GetParameter(1) - (sigma * self.distribution.GetParameter(2))
        max_allowed_value =  self.distribution.GetParameter(1) + (sigma * self.distribution.GetParameter(2))
        for hist in self.histogram_array:
            hist_area = hist.Integral(hist.FindFixBin(min_value),hist.FindFixBin(max_value))
            if not (min_allowed_value <= hist_area <= max_allowed_value):
                self.histogram_array.Remove(hist)
            
    

class TemplateGenerator():
    def __init__(self):
        pass

    def create_spe(self):
        """ Create an SPE peak """
        outfile = ROOT.TFile("./AHHHH.root", "RECREATE")
        canvas = ROOT.TCanvas()
        h = ROOT.TH1D("h", "h", 100, 0, 100)
        h.FillRandom("gaus", 50000)
        h.Draw()
        canvas.Update()
        canvas.Write()


    def add_noise(self):
        pass

    def combine_spe(self):
        pass

class TestWaveformAnalyzer(unittest.TestCase):
    def test_waveform_area_cut(self):
        temp_file = ROOT.TFile("temp.root", "RECREATE")
        # Define parameters for the histogram
        num_bins = 100
        x_min = 0
        x_max = 250
        desired_areas = [ 70, 85, 100, 115, 130]  # Specify the desired area
        # Create the histogram
        for i, area in enumerate(desired_areas):
            histogram = ROOT.TH1F(f"{i}_histogram", "Histogram with Desired Area", num_bins, x_min, x_max)

            # Calculate the width of each bin
            bin_width = (x_max - x_min) / num_bins

            # Set the contents of each bin such that the integral equals the desired area
            for bin_index in range(1, num_bins + 1):
                # Equal area divided by bin width
                bin_content = area / (num_bins * bin_width)  
                histogram.SetBinContent(bin_index, bin_content)

            # Optionally, normalize the histogram to ensure the area under the
            # histogram equals the desired area
            histogram.Scale(area / histogram.Integral())
            histogram.Write()
        temp_file.Close()
        temp_file = ROOT.TFile("temp.root", "READ")
        distribution = ROOT.TF1("gaussian", "gaus", 0, 250)
        distribution.SetParameters(1, 100, 20)
        waveform_analyzer = WaveformAnalyzer(temp_file, distribution)
        waveform_analyzer.waveform_area_cut(min_value=0, max_value=250)
        for hist in waveform_analyzer.histogram_array:
            print(hist.Integral())
            self.assertLessEqual(hist.Integral(), 120)
            self.assertGreaterEqual(hist.Integral(), 80)
        os.remove("temp.root")
        

if __name__ == "__main__":
    unittest.main()
    template_generator = TemplateGenerator()
    template_generator.create_spe()


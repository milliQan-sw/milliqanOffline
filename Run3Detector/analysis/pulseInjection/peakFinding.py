from ROOT import TSpectrum, TFile, TString, TH1, TCanvas, TLine, kRed, TH1F, TF1
import ROOT 
from typing import Union, Callable



def peak_finding ( input_file:TFile, sigma: int = 2,
                 threshold: float = 0.9, max_peaks:int= 20):
    """
    Function to perform peak finding on a set of histograms
    Return location of peaks and estimated background
    """

    if not input_file.IsOpen():
        print("Could not open ROOT file")
        exit()
    keys = input_file.GetListOfKeys()
    print(len(keys))
    peak_locations = []
    for key in keys:
        
        obj = key.ReadObj()
        if isinstance(obj, TH1):
            spectrum = TSpectrum(max_peaks)

            # Find peaks that are 2 sigma above average, and exclude peaks that are less that 0.01 * max height of tallest peak
            peaks = spectrum.Search(obj, sigma, "", threshold) #
            peak_location = []
            for i in range(spectrum.GetNPeaks()):
                peak_location.append((spectrum.GetPositionX()[i], spectrum.GetPositionY()[i]))
            peak_locations.append(peak_location)
    return peak_locations

def get_area (input_item:Union[TFile, TH1],
             start:float, stop:float)-> Union[float, list[float], None] :
    """
    Calculate the area between start and stop. If the input is a hist
    return just the area. If the input is a TFile return the area
    of all hists in that TFile.
    """
    if isinstance(input_item, TH1):
        return input_item.Integral(input_item.FindFixBin(start),
                                   input_item.FindFixBin(stop))

    elif isinstance(input_item, TFile):
        keys = input_item.GetListOfKeys()
        return [key.ReadObj.Integral(key.ReadObj.FindFixBin(start),
                                     key.ReadObj.FindFixBin(stop))
                for key in keys if isinstance(key.ReadObj(), TH1)]
    return None

def draw_area_bounds (canvas:TCanvas, lines:list[float]):
    """
    Draw a list of vertical lines on a TCanvas to designate
    where the area is being taken from.
    """
    draw_canvas = canvas
    for line_pos in lines:
        line = TLine(line_pos, 0, line_pos, 20)
        line.SetLineColor(kRed)
        line.SetLineWidth(2)
        line.Draw()

    draw_canvas.Update()

        
    
    
if __name__ == "__main__":
    ROOT.gROOT.SetBatch(True)

    PEAK_WIDTH = 200
    led_file = TFile("/home/ryan/Documents/Data/MilliQan/"
                      "outputWaveforms_812_2p5V.root", "READ")
    no_led_file = TFile("/home/ryan/Documents/Data/MilliQan/"
                         "outputWaveforms_805_noLED.root", "READ")

    # We only want the highest peak
    no_led_peaks = peak_finding(no_led_file, threshold=.80, max_peaks=100)
    output_file = TFile("areaWaveforms.root", "RECREATE")

    led_areas = get_area(output_file, 10, 20)

    assert len(no_led_peaks) == len(no_led_file.GetListOfKeys()), ("Mismatch"
    "between peaks and keys")

    led_areas = []
    led_area_hist = None
    for i, key in enumerate(led_file.GetListOfKeys()):
        hist = key.ReadObj()
        
        led_area_hist = TH1F("led_hist", "LED Area Histogram",
                             200, -2000, 10000)
        if isinstance(hist, TH1):
            led_area_hist.Fill(get_area(hist, 1200, 1600))
            canvas = TCanvas(f"canvas_{i}")
            hist.Draw()
            line1 = TLine(1200, 0, 1200, 20)
            line1.SetLineColor(kRed)
            line1.SetLineWidth(2)
            line1.Draw()

            line2 = TLine(1600, 0, 1600, 20)
            line2.SetLineColor(kRed)
            line2.SetLineWidth(2)
            line2.Draw()

            canvas.Write()

    g1 = TF1("g1", "gaus", 0, 1000)
    g2 = TF1("g2", "gaus", 0, 1000)
    g3 = TF1("g3", "gaus", 0, 1000)
    

    total = TF1("total", "gaus(0)+gaus(3)+gaus(6)", 0, 1000)
    total.SetLineColor(2)
    if led_area_hist:
        led_area_hist.Fit(total, "E")

    no_led_hist = TH1F("no_led_hist", "No LED Area Histogram", 200, -2000, 10000)
    for i, key in enumerate(no_led_file.GetListOfKeys()):
        hist = key.ReadObj()

        if isinstance(hist, TH1):
            no_led_hist.Fill(get_area(hist, no_led_peaks[i][0] - PEAK_WIDTH,
                                      no_led_peaks[i][0] + PEAK_WIDTH))

    area_canvas = TCanvas("area", "LED Area")
    if led_area_hist:
        led_area_hist.Draw()
    area_canvas.Update()
    area_canvas.Write()
    output_file.Close()
    



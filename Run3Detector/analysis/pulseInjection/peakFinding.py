from ROOT import TSpectrum, TFile, TString, TH1, TCanvas, TLine, kRed, TH1F, TF1
import ROOT 
from typing import Union, Callable
from array import array


def peak_finding ( input_file:TFile):
    """
    Function to perform peak finding on a set of histograms
    Return location of peaks and estimated background
    """

    if not input_file.IsOpen():
        print("Could not open ROOT file")
        exit()
    keys = input_file.GetListOfKeys()
    max_locations = []
    for key in keys:
        
        obj = key.ReadObj()
        if isinstance(obj, TH1):
            max_locations.append(obj.GetBinCenter(obj.GetMaximumBin()))
    return max_locations

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
    output_file = TFile("areaWaveforms.root", "RECREATE")

    led_waveform_dir = output_file.mkdir("led_waveforms")
    no_led_waveform_dir = output_file.mkdir("no_led_waveforms")
    area_dir = output_file.mkdir("area")
    

    led_areas = []
    led_area_hist = TH1F("led_hist", "LED Area Histogram",
                            200, 0, 2000)
    led_waveform_dir.cd()
    for i, key in enumerate(led_file.GetListOfKeys()):
        hist = key.ReadObj()
        
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
    led_area_hist.Scale(1/led_area_hist.Integral())
    par = array( 'd', 9*[0.] )
    g1 = TF1("g1", "gaus", 0, 2000)
    g2 = TF1("g2", "gaus", 0, 2000)


    total = TF1("total", "gaus(0)+gaus(3)", 0, 2000)
    total.SetLineColor(4)

    led_area_hist.Fit(g1, "N")
    led_area_hist.Fit(g2, "N+")

    par1 = g1.GetParameters()


    g2.SetParameter(1, 1000)  
    par2 = g2.GetParameters()


    par[0], par[1], par[2] = par1[0], par1[1], par1[2]
    par[3], par[4], par[5] = par2[0], par2[1], par2[2]

    assert par2[1] == 1000, "the mean did not get set"

    total.SetParameters(par)
    led_area_hist.Fit(total, 'R+')

    no_led_area_hist = TH1F("no_led_hist", "No LED Area Histogram", 200, 0, 2000)
    no_led_peaks = peak_finding(no_led_file)
    no_led_waveform_dir.cd()
    for i, key in enumerate(no_led_file.GetListOfKeys()):
        hist = key.ReadObj()
        if isinstance(hist, TH1):
            no_led_area_hist.Fill(get_area(hist, no_led_peaks[i] - PEAK_WIDTH,
                                      no_led_peaks[i] + PEAK_WIDTH))
            canvas = TCanvas(f"canvas_{i}")
            hist.Draw()
            line1 = TLine(no_led_peaks[i] - PEAK_WIDTH, 0,
                          no_led_peaks[i] - PEAK_WIDTH, 20)
            line2 = TLine(no_led_peaks[i] + PEAK_WIDTH, 0,
                          no_led_peaks[i] + PEAK_WIDTH, 20)
            line1.SetLineColor(kRed)
            line1.SetLineWidth(2)
            line1.Draw()
            line2.SetLineColor(kRed)
            line2.SetLineWidth(2)
            line2.Draw()
            canvas.Write()
            
    no_led_area_hist.Scale(1/no_led_area_hist.Integral())
    no_led_area_hist.Fit(g1, "+", "", 0, 1000)
    area_canvas = TCanvas("area", "LED Area")

    led_area_hist.SetLineColor(2)
    no_led_area_hist.SetLineColor(3)
    if led_area_hist:
        led_area_hist.Draw("")
        no_led_area_hist.Draw("SAME")
    area_canvas.Update()
    area_dir.cd()
    area_canvas.Write()
    output_file.Close()
    



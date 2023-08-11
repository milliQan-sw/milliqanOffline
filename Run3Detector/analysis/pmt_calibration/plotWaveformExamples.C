#include <TBox.h>
#include <TCanvas.h>
#include <TFile.h>
#include <TH1D.h>
#include <TIterator.h>
#include <TKey.h>
#include <TLine.h>
#include <TList.h>
#include <TTree.h>
#include <cassert>
#include <iostream>
#include <sstream>
#include <string>

std::string string_parser(std::string input_string, std::string find_value);
int plotWaveformExamples(int number) {
  // Read waveforms and extra the extra info from root files.
  // The waveforms look like they were saved by event and when reading the files
  // they come in order.
  TFile *waveform_file = TFile::Open("/home/ryan/Documents/Research/MilliQan/"
                                     "DataFiles/outputWaveforms_805_noLED.root",
                                     "READ");

  std::ostringstream hist_name;
  hist_name << "Waves_" << number;
  TH1D *hist =
      dynamic_cast<TH1D *>(waveform_file->Get(hist_name.str().c_str()));
  std::cout << hist_name.str() << std::endl;
  // waveform_file->Close();

  TFile *extra_file =
      TFile::Open("/home/ryan/Documents/Research/MilliQan/"
                  "DataFiles/PreProcessed/Run805preProcessed.root");

  // Setup TTree and Branches
  TTree *tree = dynamic_cast<TTree *>(extra_file->Get("Events"));
  double area;
  double noise;
  double offset;
  tree->SetBranchAddress("area", &area);
  tree->SetBranchAddress("noise", &noise);
  tree->SetBranchAddress("offset", &offset);
  unsigned int entries = tree->GetEntries();
  // Read in waveform plots

  // Assure that there are an equal number of waveforms and events

  // Convert from number to string

  // Get event from extra_data file
  tree->GetEvent(number);
  // Create Canvas to draw everything on
  TCanvas *canvas = new TCanvas("canvas", "Waveform", 800, 600);
  // For every key, read in event from extra data file
  double yMax = offset + noise;
  double yMin = offset - noise;

  std::cout << "Noise: " << noise << std::endl;

  TBox *highlightBox = new TBox(hist->GetXaxis()->GetXmin(), yMin,
                                hist->GetXaxis()->GetXmax(), yMax);
  highlightBox->SetFillColorAlpha(kRed, 0.1);

  TLine *offset_line = new TLine(hist->GetXaxis()->GetXmin(), offset,
                                 hist->GetXaxis()->GetXmax(), offset);
  offset_line->SetLineStyle(2);
  offset_line->SetLineColor(kRed);

  TLine *lower_signal_range = new TLine(1220, 0, 1220, hist->GetMaximum());
  TLine *uppser_signal_range = new TLine(1550, 0, 1550, hist->GetMaximum());

  hist->Draw();

  offset_line->Draw();
  lower_signal_range->Draw("SAME");
  uppser_signal_range->Draw("SAME");
  highlightBox->Draw("SAME");
  canvas->SaveAs("Histogram.png");
  canvas->WaitPrimitive();

  extra_file->Close();
  delete canvas;
  delete highlightBox;
  delete offset_line;
  delete hist;
  return 0;
}

std::string string_parser(std::string input_string, std::string find_value) {
  unsigned int cut_position = input_string.find(find_value);
  if (cut_position + 1 < input_string.length()) {
    std::string substring = input_string.substr(cut_position + 1);
    return substring;
  } else {
    return "";
  }
}

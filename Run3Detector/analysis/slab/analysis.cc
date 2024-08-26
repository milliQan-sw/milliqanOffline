#include <RtypesCore.h>
#include <TFile.h>
#include <algorithm>
#include <iterator>
#include <set>
#include "TCanvas.h"

// Template function to print any vector type
template <typename T>
std::ostream& operator<<(std::ostream& os, const std::vector<T>& vec) {
    os << "[";
    for (size_t i = 0; i < vec.size(); ++i) {
        os << vec[i];
        if (i != vec.size() - 1) {
            os << ", ";  // Add comma and space between elements
        }
    }
    os << "]";
    return os;
}

// Function Declarations
bool fourLayers(const std::vector<float>& vec);
void timingResolution(const std::vector<float> &nPE,
                      const std::vector<float> &pmt_time,
                      const std::vector<float> &time);
std::vector<int> sortTimes(std::vector<float> layers, std::vector<float> time);
std::map<int, float> layerTimeDifference(std::vector<float> times, std::vector<float> layers);

int analysis() {
  TFile *file = TFile::Open(
                            "/home/ryan/Documents/Data/MilliQan/beam_muon_slabMilliQan_flat.root");
  TTree *tree = (TTree *)file->Get("t");

  // Setup variables to hold leaves
  std::vector<float> *nPE = 0;
  std::vector<float> *time = 0;
  std::vector<float> *layer = 0;

  tree->SetBranchAddress("nPE", &nPE);
  tree->SetBranchAddress("pmt_time", &time);
  tree->SetBranchAddress("layer", &layer);

  Long64_t nEntries = tree->GetEntries();
  //std::cout << "Number of entries " << nEntries << std::endl;
  int layer_cut = 0;
  int four_layer_cut = 0;

  // Create histograms to store npe and timing distributions
  TH1F *h_npe = new TH1F("npe", "NPE", 500, 0, 100);
  TH1F *h_time = new TH1F("time", "Time", 500, -100, 100);
  TH1F *h_time_diff = new TH1F("time", "Time Difference", 500, 0, 100);
  TH1F *h_time_diff_1 = new TH1F("time_diff_1", "Time Difference Between Layer 0 and 1", 100, 0, 20);
  TH1F *h_time_diff_2 = new TH1F("time_diff_2", "Time Difference Between Layer 1 and 2", 100, 0, 20);
  TH1F *h_time_diff_3 = new TH1F("time_diff_3", "Time Difference Between Layer 2 and 3", 100, 0, 20);

  for (Long64_t i = 0; i < nEntries; ++i) {
    tree->GetEntry(i);
    
    if (layer->size() < 4)
      continue;

    ++layer_cut;
    if (!(fourLayers(*layer)))
      continue;

    ++four_layer_cut;

    for (const auto &value : *time) {
      h_time->Fill(value);
    }
    for (const auto &value : *nPE) {
      h_npe->Fill(value);
    }

    std::cout << *layer << std::endl;
    std::map<int, float> time_difference_between_layers =
        layerTimeDifference(*time, *layer);


    h_time_diff_1->Fill(time_difference_between_layers[0]);
    h_time_diff_2->Fill(time_difference_between_layers[1]);
    h_time_diff_3->Fill(time_difference_between_layers[2]);
   
    // // Apply straight path

    

    
    // Timing distribution within a slab

  }

  


  TCanvas *canvas1 = new TCanvas("c", "c", 400, 400);
  canvas1->SetLogy(); 
  // Setup Legend
  TLegend *legend = new TLegend(0.1, 0.7, 0.48, 0.9);
  legend->SetHeader("Legend", "C");
  legend->AddEntry(h_time_diff_1, "Max time difference between layer 0 and 1");
  legend->AddEntry(h_time_diff_2, "Max time difference between layer 1 and 2");
  legend->AddEntry(h_time_diff_3, "Max time difference between layer 2 and 3");

  h_time_diff_1->SetLineColor(kRed);
  h_time_diff_2->SetLineColor(kBlue);
  h_time_diff_3->SetLineColor(kGreen);

  canvas1->cd();
  h_time_diff_1->Draw();
  legend->Draw("SAME");
  h_time_diff_2->Draw("SAME");
  h_time_diff_3->Draw("SAME");

  canvas1->SaveAs("max_time_diff.pdf");
  std::cout << "Cutflow" << std::endl;
  std::cout << "4 layers: " << layer_cut << std::endl;
  std::cout << "each layer: " << four_layer_cut << std::endl;


    TCanvas *canvas2 =
        new TCanvas("canvas", "NPE and Timing Distributions", 400, 400);
    canvas2->Divide(2, 1);
    canvas2->cd(1);
    h_npe->Draw();
    canvas2->cd(2);
    h_time->Draw();

    canvas2->Update();
    canvas2->SaveAs("npe_timing_dist.pdf");
    return 0;
}


map<int, float> layerTimeDifference(std::vector<float> times, std::vector<float> layers){

  // Place times into a map for easier manipulation
  map<int, std::vector<float>> times_map = {
                                        {0, {}},
                                        {1, {}},
                                        {2, {}},
                                        {3, {}}};
    // Fill times_map with times associated with that layer
    for (int i=0; i < 4; ++i){
        auto it = layers.begin();
        while (it != layers.end()) {
          // Find layer values inside the layer vector
        it = std::find(it, layers.end(), i);

        if (it != layers.end()) {
            int index = std::distance(layers.begin(), it);
            times_map[i].push_back(times[index]);
            ++it;
        }
        }
        }

    /* Grab time difference. We want to use the smallest values for each
       layer so that we can just look at prompt hits and not be bogged down
       with non-optimal signal paths */
    
    map<int, float> time_difference = {
                                        {0, 0.},
                                        {1, 0.},
                                        {2, 0.}
                                        };
    for (int i = 0; i + 1 < 4; ++i) {
      const float time1 = *std::min_element(times_map[i].begin(), times_map[i].end());
      const float time2 = *std::min_element(times_map[i+1].begin(), times_map[i+1].end());
      if (time1 > 0 && time2 > 0) {
        time_difference[i] = abs(time1 - time2);
      }
    }
        
        return time_difference;
    }

    void timingResolution(const std::vector<float> &nPE,
                          const std::vector<float> &pmt_time,
                          const std::vector<float> &time) {

    }

    bool fourLayers(const std::vector<float> &vec) {

    std::set<float> vecSet(vec.begin(), vec.end());
    std::set<float> valueSet = {0.,1.,2.,3.};

    for (int value : valueSet) {
        // This only occurs if the value is not in the set
        if (vecSet.find(value) == vecSet.end()) {
        return false;
        }
    }
    return true;
    }

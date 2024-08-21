#include <RtypesCore.h>
#include <TFile.h>
#include <set>

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
  std::cout << "Number of entries " << nEntries << std::endl;
  int layer_cut = 0;
  int four_layer_cut = 0;

  // Create histograms to store npe and timing distributions
  TH1F *h_npe = new TH1F("npe", "NPE", 500, 0, 100);
  TH1F *h_time = new TH1F("time", "Time", 500, -100, 100);

  for (Long64_t i = 0; i < nEntries; ++i) {
    tree->GetEntry(i);
    
    if (layer->size() < 4)
      continue;

    ++layer_cut;
    if (!(fourLayers(*layer)))
      continue;

    ++four_layer_cut;

    for (const auto &value : time) {
      h_time->Fill(value);
    }
    for (const auto &value : nPE) {
      h_npe->Fill(value);
    }
  }



  std::cout << "Cutflow" << std::endl;
  std::cout << "4 layers: " << layer_cut << std::endl;
  std::cout << "each layer: " << four_layer_cut << std::endl;


  // Draw histograms
  
  return 0;
}


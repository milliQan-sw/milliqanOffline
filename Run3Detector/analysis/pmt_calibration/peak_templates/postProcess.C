#include <TCanvas.h>
#include <TDirectory.h>
#include <TFile.h>
#include <TH1D.h>
#include <TTree.h>
#include <cassert>
#include <cmath>
#include <iostream>
#include <ostream>
#include <vector>

double trapezoid_rule_area(std::vector<double> x, std::vector<double> y);
template <typename T>
std::vector<T> slice_vector(std::vector<T> input_vector, int start_value,
                            int stop_value);

template <typename T> void print_vector(std::vector<T> input_vector);

double mean(std::vector<double> values);

const double NANOSECONDS_PER_SAMPLE = 2.5;

int postProcess() {
  bool do_timing = false;
  int t_start = 230;
  int t_end = 330;
  std::cout << "Test" << std::endl;
  TFile *input_file =
      new TFile("/home/ryan/Documents/Research/MilliQan/Data/run733.root");
  if (!(input_file->IsZombie())) {
    TTree *event_tree = (TTree *)input_file->Get("Events");
    std::cout << "After getting Event branch" << std::endl;

    std::vector<double> *times = new std::vector<double>{};
    std::vector<double> *voltages = new std::vector<double>{};
    double area[1];
    double offset[1];
    double noise[1];
    double smoothed_max[1];
    double tmax[1];
    double thalfmax[1];
    double fwhm[1];

    event_tree->SetBranchStatus("*", 0);
    event_tree->SetBranchStatus("times", 1);
    event_tree->SetBranchStatus("voltages", 1);

    event_tree->SetBranchAddress("times", &times);
    event_tree->SetBranchAddress("voltages", &voltages);

    // for (Long64_t i = 0; i < event_tree->GetEntries(); i++) {
    //   event_tree->GetEntry(i);
    //   std::cout << voltages->size() << std::endl;
    // }

    event_tree->GetEntry(0);
    TBranch *area_branch = event_tree->Branch("area", &area, "area/D");
    TBranch *offset_branch = event_tree->Branch("offset", &offset, "area/D");
    TBranch *noise_branch = event_tree->Branch("noise", &noise, "area/D");
    TBranch *smoothed_branch =
        event_tree->Branch("smoothed", &smoothed_max, "area/D");

    TBranch *tmax_branch = event_tree->Branch("tmax", &tmax, "area/D");
    TBranch *thalfmax_branch =
        event_tree->Branch("thalfmax", &thalfmax, "area/D");

    // Attempting to emulate python code. Need +1 to account of 0-indexed lists
    // since python calculates start_index and end_index differently
    unsigned int start_index =
        ceil((double)t_start / NANOSECONDS_PER_SAMPLE) + 1;
    unsigned int end_index = ceil((double)t_end / NANOSECONDS_PER_SAMPLE) + 1;

    double xq[2] = {0.95, 0.05};
    double yq[2];
    int offset_voltage_cutoff = start_index * 3. / 4.;
    std::vector<double> sliced_voltages =
        slice_vector(*voltages, 30, offset_voltage_cutoff - 1);
    offset[0] = mean(sliced_voltages);

    TH1F *h = new TH1F("h", "voltage_quantile", 100, -20, 20);
    std::vector<double> noise_voltage_slice =
        slice_vector(*voltages, 0, offset_voltage_cutoff - 1);
    std::vector<double> w(noise_voltage_slice.size(), 1); // weights vector
    h->FillN(noise_voltage_slice.size(), noise_voltage_slice.data(), w.data());
    h->Draw();
    h->GetQuantiles(2, yq, xq);
    std::cout << "0.95 Quantile " << yq[0] << std::endl;
    std::cout << "0.05 Quantile " << yq[1] << std::endl;

    std::cout << "Length Noise " << noise_voltage_slice.size() << std::endl;

    // Noise is a little off
    noise[0] = 0.5 * (yq[0] - yq[1]);
    std::cout << "Noise " << noise[0] << std::endl;
    std::cout << "Offset " << offset[0] << std::endl;
    for (auto &voltage : *voltages) {
      voltage -= offset[0];
    }
    // NOTE: trapezoid rule works!
    std::vector<double> x_test = {1, 2, 3, 4, 5, 6, 7, 23, 233};
    std::vector<double> y_test = {4, 3, 65, 2, 3, 5, 3, 74, 345};
    double area_test = trapezoid_rule_area(x_test, y_test);
    std::cout << area_test << std::endl; // 163
    input_file->Close();
    return 0;
  }
}

double mean(std::vector<double> values) {
  /* Return the average of a vector */
  double sum = 0;
  for (unsigned int i = 0; i < values.size(); i++) {
    sum += values.at(i);
  }
  return sum / values.size();
}

template <typename T>
std::vector<T> slice_vector(std::vector<T> input_vector, int start_value,
                            int stop_value) {
  auto start = input_vector.begin() + start_value;
  auto end = input_vector.begin() + stop_value + 1;

  std::cout << input_vector.size() << std::endl;
  std::vector<T> result(stop_value - start_value + 1);
  copy(start, end, result.begin());
  std::cout << "result_size" << result.size() << std::endl;
  return result;
}

template <typename T> void print_vector(std::vector<T> input_vector) {
  for (auto &value : input_vector) {
    std::cout << value << std::endl;
  }
}

double trapezoid_rule_area(std::vector<double> x, std::vector<double> y) {
  assert(x.size() == y.size());
  double area;
  for (int i = 0; i < x.size() - 1; i++) {
    area += ((y[i] + y[i + 1]) * (x[i + 1] - x[i]));
  };
  return 0.5 * area;
}

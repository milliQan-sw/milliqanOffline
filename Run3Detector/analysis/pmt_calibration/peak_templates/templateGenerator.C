#include <TCanvas.h>
#include <TEntryList.h>
#include <TFile.h>
#include <TH1D.h>
#include <TTree.h>
#include <iostream>
#include <stdexcept>

const float area_min = -5000;
const float area_max = 3000;

std::vector<double> addListsElementwise(const std::vector<double> &list1,
                                        const std::vector<double> &list2);
int templateGenerator() {
  TFile *input_file =
      TFile::Open("/home/ryan/Documents/Research/MilliQan/"
                  "DataFiles/PreProcessed/Run805preProcessed.root",
                  "UPDATE");
  TTree *event_tree = dynamic_cast<TTree *>(input_file->Get("Events"));
  TString plot_directory = TString(
      "/home/ryan/Documents/Research/MilliQan/DataFiles/TemplatePlots/");
  unsigned int tstart = 1220;
  unsigned int tend = 1550;

  TCanvas *canvas = new TCanvas("c", "c", 604, 528);
  TH1D *area_hist =
      new TH1D("h", ";pulse area [pVs];Events / 2 pVs", 75, -5500, 5500);

  area_hist->SetLineColor(kBlack);
  area_hist->SetLineWidth(2);
  // event_tree->Draw("area>>h", Form("area>%f && area<%f", area_min,
  // area_max));

  event_tree->Draw(">>myentrylist",
                   Form("area>%f && area<%f", area_min, area_max), "entrylist");

  TEntryList *myentrylist =
      dynamic_cast<TEntryList *>(gDirectory->Get("myentrylist"));

  if (myentrylist) {

    std::vector<double> *times = new std::vector<double>{};
    std::vector<double> *voltages = new std::vector<double>{};
    event_tree->SetBranchAddress("voltages", &voltages);
    event_tree->SetBranchAddress("times", &times);

    // Need this to access the size of voltages;
    event_tree->GetEntry(0);
    std::vector<double> voltage_average(voltages->size(), 0);

    // Loop through events where area is within specified range
    for (int i = 0; i < myentrylist->GetN(); i++) {
      event_tree->GetEntry(myentrylist->GetEntry(i));
      std::cout << (*voltages)[0] << std::endl;

      voltage_average = addListsElementwise(voltage_average, *voltages);

      std::cout << voltage_average[0] << std::endl;
    }
  }
  unsigned int n_event = myentrylist->GetN();

  input_file->Close();

  return 0;
}

std::vector<double> addListsElementwise(const std::vector<double> &list1,
                                        const std::vector<double> &list2) {
  /* Function to do elementwise addition of two vectors. */
  if (list1.size() != list2.size()) {
    throw std::invalid_argument("Lists must be of the same size");
  }

  std::vector<double> result;
  result.reserve(list1.size());

  for (size_t i = 0; i < list1.size(); ++i) {
    result.push_back(list1[i] + list2[i]);
  }
  return result;
}

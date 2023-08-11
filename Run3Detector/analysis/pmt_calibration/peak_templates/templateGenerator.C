#include <TCanvas.h>
#include <TDirectory.h>
#include <TEntryList.h>
#include <TFile.h>
#include <TGraph.h>
#include <TH1D.h>
#include <TLine.h>
#include <TSystem.h>
#include <TTree.h>
#include <filesystem>
#include <iostream>
#include <stdexcept>

// Setup regions for the control and signal region these values can/should be
// changed
const double control_region_area[2] = {-5000, 5000};
const double signal_region_area[2] = {3, 10};

// Times that will contain your signal
const unsigned int tstart = 1220;
const unsigned int tend = 1550;

// Function Templates
std::vector<double> subtractLists(std::vector<double> list1,
                                  std::vector<double> list2);
std::vector<double> addListsElementwise(const std::vector<double> &list1,
                                        const std::vector<double> &list2);
void divideListElementwise(std::vector<double> &vector, double divisor);
std::vector<double> arange(double start, double end, double step);
std::vector<double> interpolateList(std::vector<double> x_values,
                                    std::vector<double> y_values,
                                    std::vector<double> interpolation_points);

int main() {
  // Grab event TTree
  TFile *input_file = TFile::Open("/home/ryan/Documents/Research/MilliQan/"
                                  "Data/PreProcessed/Run805preProcessed.root",
                                  "UPDATE");
  TTree *event_tree = dynamic_cast<TTree *>(input_file->Get("Events"));

  // Setup Plot Directory and Create it if it doesn't exist
  TString plot_directory = TString(
      "/home/ryan/Documents/Research/MilliQan/DataFiles/TemplatePlots/");
  if (gSystem->AccessPathName(plot_directory) != 0) {
    gSystem->mkdir(plot_directory, true);
  }

  // Baseline of times that will be used later for interpolation
  std::vector<double> t_baseline = arange(0, 2000, 0.2);

  TFile *outputFile = new TFile("histPlot.root", "RECREATE");
  TH1D *h = new TH1D("h", ";pulse area [pVs]; Events", 125, 5000, 5000);
  event_tree->Draw("area>>h", "");
  h->Write();
  outputFile->Close();

  // Get list of events where the area is within control_region_area
  event_tree->Draw(">>myentrylist",
                   Form("area>%f && area<%f", control_region_area[0],
                        control_region_area[1]),
                   "entrylist");
  TEntryList *myentrylist =
      dynamic_cast<TEntryList *>(gDirectory->Get("myentrylist"));

  // Setup tracking for branches
  std::vector<double> *times = new std::vector<double>{};
  std::vector<double> *voltages = new std::vector<double>{};
  event_tree->SetBranchAddress("voltages", &voltages);
  event_tree->SetBranchAddress("times", &times);

  // Grab initial event so that below vector will actually have a size
  event_tree->GetEntry(0);
  std::vector<double> voltage_average(t_baseline.size(), 0);

  // Loop through entry list to find the average waveform for a 0-SPE event
  if (myentrylist) {
    std::cout << "Loop over tree to get average 0-PE control waveform"
              << std::endl;
    std::cout << "Number of events in background region: "
              << myentrylist->GetN() << std::endl;
    // Loop through events where area is within signal range
    // Get average waveform
    std::vector<double> interpolated_voltage;
    for (int i = 0; i < myentrylist->GetN(); i++) {
      event_tree->GetEntry(myentrylist->GetEntry(i));

      // Get a list of interpolated voltages
      interpolated_voltage = interpolateList(*times, *voltages, t_baseline);
      voltage_average =
          addListsElementwise(voltage_average, interpolated_voltage);
    }
    divideListElementwise(voltage_average, myentrylist->GetN());
  }

  std::cout << "Loop over tree to get average control-subtracted SPE Waveform"
            << std::endl;

  // Get values within the signal region
  event_tree->Draw(
      ">>entrylist",
      Form("area>%f && area<%f", signal_region_area[0], signal_region_area[1]),
      "entrylist");
  TEntryList *entrylist =
      dynamic_cast<TEntryList *>(gDirectory->Get("entrylist"));

  int nEvents = entrylist->GetN();

  std::vector<std::vector<double>> waveforms;
  std::vector<double> spe_average_waveform(t_baseline.size(), 0);
  std::vector<double> spe_average_subtract_control(t_baseline.size(), 0);
  std::cout << "Number of events in signal region " << nEvents << std::endl;
  if (entrylist) {
    for (int i = 0; i < nEvents; i++) {
      event_tree->GetEntry(entrylist->GetEntry(i));

      // Do the same interpolation for items in the signal region and subtract
      // off the average 0-SPE voltages
      std::vector<double> vs_interp =
          interpolateList(*times, *voltages, t_baseline);
      std::vector<double> vs_interp_subtract_control =
          subtractLists(vs_interp, voltage_average);

      waveforms.push_back(vs_interp);
      spe_average_waveform =
          addListsElementwise(spe_average_waveform, vs_interp);
      spe_average_subtract_control = addListsElementwise(
          spe_average_subtract_control, vs_interp_subtract_control);
    }
    divideListElementwise(spe_average_waveform, entrylist->GetN());
    divideListElementwise(spe_average_subtract_control, entrylist->GetN());

    // Create TCanvas to draw plots
    TCanvas *canvas = new TCanvas("canvas", "SPE Graphs", 800, 600);

    // Create Plots of the Average 0-PE Control Waveform
    TGraph *zeroPEGraph = new TGraph(voltage_average.size(), t_baseline.data(),
                                     voltage_average.data());
    zeroPEGraph->SetTitle("0-PE Average Voltage");
    zeroPEGraph->GetXaxis()->SetTitle("Time (ns)");
    zeroPEGraph->GetYaxis()->SetTitle("Average Voltage (mV)");
    zeroPEGraph->SetLineColor(kBlack);
    zeroPEGraph->SetLineWidth(2);

    // Create Plots of the average SPE
    TGraph *averageSPE =
        new TGraph(spe_average_waveform.size(), t_baseline.data(),
                   spe_average_waveform.data());
    averageSPE->SetTitle("Average SPE Waveform");
    averageSPE->GetXaxis()->SetTitle("Time (ns)");
    averageSPE->GetYaxis()->SetTitle("Average Voltage (mV)");
    averageSPE->SetLineColor(kRed);
    averageSPE->SetLineWidth(2);

    // Create Lines that will display tstart and tend
    // TODO: Replace GetUymax and GetUymin with actual maximums and minimums
    TLine *tstartLine =
        new TLine(tstart, gPad->GetUymin(), tstart, gPad->GetUymax());
    tstartLine->SetLineStyle(2);
    tstartLine->SetLineColor(kBlue);
    tstartLine->SetLineWidth(2);

    TLine *tendLine = new TLine(tend, gPad->GetUymin(), tend, gPad->GetUymax());
    tendLine->SetLineStyle(2);
    tendLine->SetLineColor(kBlue);
    tendLine->SetLineWidth(2);

    canvas->cd();
    zeroPEGraph->Draw();
    averageSPE->Draw("SAME");
    tstartLine->Draw("SAME");
    tendLine->Draw("SAME");
    TString fileName = TString("avg_spe_control.png");
    canvas->SaveAs(plot_directory + fileName);

    // Create Plot of Average Control Subtracted SPE
    TGraph *averageControlSubtractedSPE =
        new TGraph(spe_average_subtract_control.size(), t_baseline.data(),
                   spe_average_subtract_control.data());
    averageControlSubtractedSPE->SetTitle(
        "Average Control Subtracted Waveform");
    averageControlSubtractedSPE->GetXaxis()->SetTitle("Time (ns)");
    averageControlSubtractedSPE->GetYaxis()->SetTitle("Average Voltage (mV)");
  }

  input_file->Close();

  return 0;
}

std::vector<double> addListsElementwise(const std::vector<double> &list1,
                                        const std::vector<double> &list2) {
  /* Function to do elementwise addition of two vectors. */
  if (list1.size() != list2.size()) {
    throw std::invalid_argument("Lists must be of the same size");
  }

  std::vector<double> result(list1.size());

  for (size_t i = 0; i < list1.size(); ++i) {
    result[i] = list1[i] + list2[i];
  }
  return result;
}

std::vector<double> arange(double start, double end, double step) {
  int vector_length = static_cast<int>((end - start) / step);
  std::vector<double> vector;
  for (double value = start; value <= end; value += step) {
    vector.push_back(value);
  }
  return vector;
}

void divideListElementwise(std::vector<double> &vector, double divisor) {
  for (double &value : vector) {
    value /= divisor;
  }
}

std::vector<double> interpolateList(std::vector<double> x_values,
                                    std::vector<double> y_values,
                                    std::vector<double> interpolation_points) {

  std::cout << "About to interpolate" << std::endl;
  double x_array[x_values.size()];
  double y_array[y_values.size()];
  for (int i = 0; i < x_values.size(); i++) {
    x_array[i] = x_values[i];
    y_array[i] = y_values[i];
  }
  TGraph graph(x_values.size(), x_array, y_array);
  // Interpolate values for x values for each value in interpolation_points
  std::vector<double> interpolated_values(interpolation_points.size());

  for (int i = 0; i < interpolation_points.size(); i++) {
    interpolated_values[i] = graph.Eval(interpolation_points[i]);
  }
  return interpolated_values;
}

std::vector<double> subtractLists(std::vector<double> list1,
                                  std::vector<double> list2) {
  std::vector<double> return_list(list1.size());
  for (int i = 0; i < list1.size(); i++) {
    return_list[i] = list1[i] - list2[i];
  }
  return return_list;
}

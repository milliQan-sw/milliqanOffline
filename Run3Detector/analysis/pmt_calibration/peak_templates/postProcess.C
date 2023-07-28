#include <TFile.h>
#include <TTree.h>

int postProcess(int argc, char *argv[]) {
  bool do_timing = false;
  int t_start = 230;
  int t_end = 330;

  std::unique_ptr<TFile> input_file(TFile::Open(argv[1], "RECREATE"));
  if (!(input_file->IsZombie())) {
    std::unique_ptr<TTree> event_tree((TTree *)input_file->Get("Events"));

    double times[1024];
    double voltages[1024];
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

    std::unique_ptr<TBranch> area_branch(
        event_tree->Branch("area", &area, "area/D"));
    std::unique_ptr<TBranch> offset_branch(
        event_tree->Branch("offset", &offset, "area/D"));
    std::unique_ptr<TBranch> noise_branch(
        event_tree->Branch("noise", &noise, "area/D"));
    std::unique_ptr<TBranch> smoothed_branch(
        event_tree->Branch("smoothed", &smoothed_max, "area/D"));
    std::unique_ptr<TBranch> tmax_branch(
        event_tree->Branch("tmax", &tmax, "area/D"));
    std::unique_ptr<TBranch> thalfmax_branch(
        event_tree->Branch("thalfmax", &thalfmax, "area/D"));
    std::unique_ptr<TBranch> fwhm_branch(
        event_tree->Branch("fwhm", &fwhm, "area/D"));

    for (int i = 0; i < 5; ++i) {
      event_tree->GetEntry(i);
      if (i % 1000 == 0) {
        std::cout << "Event: " << i << std::endl;
      }

      std::cout << times[0] << std::endl;
    }
  }

  return 0;
}

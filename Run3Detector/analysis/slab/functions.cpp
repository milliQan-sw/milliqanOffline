#include "functions.h"
#include <map>
#include <set>
#include <algorithm>
#include <stdlib.h>
#include "TH1F.h"


struct eventInfo {
  std::vector<float> time;
  std::vector<float> npe;
};

bool fourLayers(const std::vector<int> &vec) {
    std::set<float> vecSet(vec.begin(), vec.end());
    std::set<float> valueSet = {0.,1.,2.,3.};

    for (int value : valueSet) {
        // This only occurs if the value is not in the set
        if (vecSet.find(value) == vecSet.end()) {
        return false;
        }
    }
    return true;
};


void timingResolution(const std::vector<float> &nPE,
                        const std::vector<float> &pmt_time,
                        const std::vector<float> &time) {

}

std::map<int, float> layerTimeDifference(const std::vector<float>& times,
                                    const std::vector<int>& layers,
                                    const std::vector<float>& nPE, const float npe_cut){
  // Place times into a std::map for easier manipulation
    std::map<int, eventInfo> times_map;
  // Fill times_std::map with times associated with that layer
    for (int i=0; i < 4; ++i){
        auto it = layers.begin();
        while (it != layers.end()) {
          // Find layer values inside the layer vector
        it = std::find(it, layers.end(), i);

        if (it != layers.end()) {
            int index = std::distance(layers.begin(), it);
            times_map[i].time.push_back(times[index]);
            times_map[i].npe.push_back(nPE[index]);
            ++it;
        }
        }
        }

    /* Grab time difference. We want to use the smallest values for each
       layer so that we can just look at prompt hits and not be bogged down
       with non-optimal signal paths. We also apply a nPE  */
    
    std::map<int, float> time_difference = {
                                        {0, 0.},
                                        {1, 0.},
                                        {2, 0.}
                                        };
    for (int i = 0; i + 1 < 4; ++i) {
      const float time1 = *std::min_element(times_map[i].time.begin(), times_map[i].time.end());
      const float time2 = *std::min_element(times_map[i + 1].time.begin(),
                                            times_map[i+1].time.end());
      bool break_flag = false;
      for (const auto npe : times_map[i].npe){
        if (npe < npe_cut) break_flag = true;}
      if (break_flag) break;
      if (time1 > 0 && time2 > 0) {
        time_difference[i] = abs(time1 - time2);
      }
    }
        return time_difference;
}


std::map<float, std::map<int, float>> scanTimeDifference(std::vector<float> &npeCuts, std::vector<float> &times,
                        std::vector<int> &layers,
                        std::vector<float> &nPE,
                        std::function<std::map<int, float>(
                            const std::vector<float>&, const std::vector<int>&,
                            const std::vector<float>&, const float&)>
                            func) {

  std::map<float, std::map<int, float>> mapCombinedTimeDifference;

  for (const float &npeCut : npeCuts) {
    std::map<int, float> mapTimeDifference = func(times, layers, nPE, npeCut);
    mapCombinedTimeDifference[npeCut] = mapTimeDifference;
  }
  return mapCombinedTimeDifference;
}


void plotTimeDifference(const std::map<float, std::map<int, float>> &timeDifferences) {
  // Loop through all keys inside map
  for (auto const &[npe, timeDiff] : timeDifferences) {
    TH1F *npeHist1 = new TH1F("timeDiff1", "Time Difference Between Layer 0 and 1", 100, 0, 20);
    TH1F *npeHist2 = new TH1F("timeDiff2", "Time Difference Between Layer 1 and 2", 100, 0, 20);
    TH1F *npeHist3 = new TH1F("timeDiff3", "Time Difference Between Layer 2 and 3", 100, 0, 20);
    // Plot all inside histograms inside the same canvas

  }

}


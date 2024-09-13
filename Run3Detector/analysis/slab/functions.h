#include <map>
#include <vector>
#include <functional>
#include "TH1F.h"

struct eventInfo {
  std::vector<float> time;
  std::vector<float> npe;
};

bool fourLayers(const std::vector<int> &vec);

void timingResolution(const std::vector<float> &nPE,
                      const std::vector<float> &pmt_time,
                      const std::vector<float> &time, TH1F);

std::vector<int> sortTimes(std::vector<float> layers, std::vector<float> time);

std::map<int, eventInfo> layerTimeDifference(const std::vector<float> &times,
                                    const std::vector<int> &layers,
                                    const std::vector<float> &nPE);

void scanTimeDifference(std::vector<float> &npeCuts, std::function <
                        std::map<int, float>(const std::vector<float>,
                                             const std::vector<int>,
                                             const std::vector<float>, const float&)> func) ;

void fillTimeDifference(TH1F &histogram,
                        std::map<int, eventInfo> timeDifferences,
                        const int &layer1, const int &layer2);

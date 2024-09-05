#include <map>
#include <vector>
#include <functional>

bool fourLayers(const std::vector<int> &vec);

void timingResolution(const std::vector<float> &nPE,
                      const std::vector<float> &pmt_time,
                      const std::vector<float> &time, TH1F);

std::vector<int> sortTimes(std::vector<float> layers, std::vector<float> time);

std::map<int, float> layerTimeDifference(const std::vector<float> &times,
                                    const std::vector<int> &layers,
                                    const std::vector<float> &nPE, const float npe_cut);

void scanTimeDifference(std::vector<float> &npeCuts, std::function <
                        std::map<int, float>(const std::vector<float>,
                                             const std::vector<int>,
                                             const std::vector<float>, const float&)> func) ;

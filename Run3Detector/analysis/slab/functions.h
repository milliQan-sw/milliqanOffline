#include <map>
#include <vector>

bool fourLayers(const std::vector<int> &vec);

void timingResolution(const std::vector<float> &nPE,
                      const std::vector<float> &pmt_time,
                      const std::vector<float> &time);

std::vector<int> sortTimes(std::vector<float> layers, std::vector<float> time);

std::map<int, float> layerTimeDifference(const std::vector<float> times,
                                    const std::vector<int> layers,
                                    const std::vector<float> nPE, const float npe_cut);

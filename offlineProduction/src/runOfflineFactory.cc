#include "/home/milliqan/milliqanOffline/offlineProduction/interface/OfflineFactory.h"
int main(int argc, char **argv){
    OfflineFactory offlineFactory = OfflineFactory("/home/milliqan/data_2022/testing_07_12_22/MilliQan_Cd109Shell.root","testOutput.root");
    offlineFactory.loadJsonConfig("/home/milliqan/milliqanOffline/offlineProduction/configuration/chanMaps/testMap.json");
    offlineFactory.loadJsonConfig("/home/milliqan/milliqanOffline/offlineProduction/configuration/pulseFinding/pulseFindingTest.json");
    offlineFactory.loadJsonConfig("/home/milliqan/milliqanOffline/offlineProduction/configuration/calibrations/testCalibration.json");
    offlineFactory.process();
    return 0;
}


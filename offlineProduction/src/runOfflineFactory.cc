#include "/home/milliqan/milliqanOffline/offlineProduction/interface/OfflineFactory.h"
int main(int argc, char **argv){
    OfflineFactory offlineFactory = OfflineFactory("/home/milliqan/data_2022/testing_07_12_22/MilliQan_Cd109Shell.root","testOutput.root");
    offlineFactory.loadChanMap("/home/milliqan/milliqanOffline/offlineProduction/configuration/chanMaps/testMap.json");
    offlineFactory.process();
    return 0;
}


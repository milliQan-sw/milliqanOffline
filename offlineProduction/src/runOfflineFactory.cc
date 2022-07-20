#include "/home/milliqan/milliqanOffline/offlineProduction/interface/OfflineFactory.h"
int main(int argc, char **argv){
    OfflineFactory offlineFactory = OfflineFactory("/home/milliqan/milliqanOffline/trees/_processed_MilliQan_Cd109Shell.root","testOutput.root");
    offlineFactory.process();
    return 0;
}


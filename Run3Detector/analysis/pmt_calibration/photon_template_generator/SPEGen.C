#include "SPEGen.h"
#include <iostream>

void SPEGen() {
    gRandom->SetSeed(0);
    SPE* spe = new SPE("et", 1.6, true);
    // spe->SetVerbose(true);
    // spe->SetOutputSampleFreq(1.5); // generate at 1.5 GHz
    TH1D *out = spe->Generate();
    out->Draw();

    return;
}

#!/bin/bash

for ((num = 1; num <= 300; num ++))
do
    python3 SimCosmicMuonTag_V2.py $num /home/czheng/SimCosmicFlatTree/cutEffCheckResult_sim_20NPEcut/CosmicStraight/purestraightCut/cutflow7
done    

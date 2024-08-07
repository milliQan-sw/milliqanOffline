#!/bin/bash

for ((num = 301; num <= 1300; num ++))
do
    python3 simCosMuon.py $num /home/czheng/SimCosmicFlatTree/cutEffCheckResult_sim_20NPEcut/CosmicStraight/purestraightCut/cutflow7
done    

#!/bin/bash

for ((num = 101; num <= 1300; num ++))
do
    python3 SimCosmicMuonTag_V2.py $num /home/czheng/SimCosmicFlatTree/cutEffCheckResult_sim_20NPEcut
done    

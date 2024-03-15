#!/bin/bash

for ((num = 1; num <= 1300; num ++))
do
    python3 SimCosmicMuonTag_V2.py $num /home/czheng/SimCosmicFlatTree/cutEffCheckResult_sim_2500NPEcut
done    

#!/bin/bash

for ((num = 6; num <= 1300; num ++))
do
    python3 SimCosmicMuonTag_V4.py $num /home/czheng/SimCosmicFlatTree/cutEffCheckResult_sim_2500NPEcut
done    

#!/bin/bash

for ((num = 1; num <= 3; num ++))
do
    python3 SimCosmicMuonTag_2.py $num /home/czheng/SimCosmicFlatTree/cutEffCheckResult_sim_2500NPEcut
done    

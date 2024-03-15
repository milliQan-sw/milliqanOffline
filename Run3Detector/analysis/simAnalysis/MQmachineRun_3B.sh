#!/bin/bash

for ((num = 1; num <= 100; num ++))
do
    python3 SimCosmicMuonTag_3B.py $num /home/czheng/SimCosmicFlatTree/cutEffCheckResult_sim_2500NPEcut
done    

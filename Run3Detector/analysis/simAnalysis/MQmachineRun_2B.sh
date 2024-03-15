#!/bin/bash

for ((num = 1; num <= 100; num ++))
do
    python3 SimCosmicMuonTag_2B.py $num /home/czheng/SimCosmicFlatTree/cutEffCheckResult_sim_2500NPEcut
done    

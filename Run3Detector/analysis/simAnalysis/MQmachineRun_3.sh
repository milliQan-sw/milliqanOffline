#!/bin/bash

for ((num = 101; num <= 1300; num ++))
do
    python3 SimCosmicMuonTag_3.py $num /home/czheng/SimCosmicFlatTree/cutEffCheckResult_sim_2500NPEcut
done    

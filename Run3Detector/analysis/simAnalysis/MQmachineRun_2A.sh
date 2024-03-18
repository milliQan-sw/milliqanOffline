#!/bin/bash

for ((num = 1; num <= 1300; num ++))
do
    python3 SimCosmicMuonTag_2A.py $num /home/czheng/SimCosmicFlatTree/cutEffCheckResult_sim_20NPEcut
done    

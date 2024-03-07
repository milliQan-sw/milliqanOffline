#!/bin/bash

for ((num = 0; num <= 1; num ++))
do
    python3 SimCosmicMuonTag_V2.py $num /home/czheng/SimCosmicFlatTree/cutEffCheckResult
done    

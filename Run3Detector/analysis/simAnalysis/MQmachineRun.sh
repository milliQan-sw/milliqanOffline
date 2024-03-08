#!/bin/bash

for ((num = 1; num <= 1300; num ++))
do
    python3 SimCosmicMuonTag_V2.py $num /home/czheng/SimCosmicFlatTree/cutEffCheckResult
done    

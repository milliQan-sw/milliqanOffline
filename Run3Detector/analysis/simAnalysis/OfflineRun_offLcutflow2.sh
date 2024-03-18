#!/bin/bash

for ((num = 1; num <= 207; num ++))
do
    python3 OLCosmicMuonTag_V2_CF2.py 1163  $num /home/czheng/SimCosmicFlatTree/cutEffCheckResult_OffL_20NPEcut
done    

#!/bin/bash

for ((num = 1; num <= 207; num ++))
do
    python3 OLCosmicMuonTag_V2.py 1163  $num /home/czheng/SimCosmicFlatTree/cutEffCheckResult_OffL_20NPEcut/cosmicStraight/Histograms/cutflow7
done   
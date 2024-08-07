#!/bin/bash

for ((num = 1; num <= 65; num ++))
do
    python3 OfflineCosMuon.py 1500  $num /home/czheng/SimCosmicFlatTree/offline_Area_NPE/1500Result/B100bar100
done   

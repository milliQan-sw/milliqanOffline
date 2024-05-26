#!/bin/bash

for ((num = 11; num <= 100; num ++))
do
    python3 OfflineCosMuon.py 1039  $num /home/czheng/SimCosmicFlatTree/offline_Area_NPE
done   

#!/bin/bash

for ((num = 1; num <= 100; num ++))
do
    python3 SimCosmicMuonTag_V2.py $num /mnt/hadoop/se/store/user/czheng/SimFlattree/COSmicStraight
done    

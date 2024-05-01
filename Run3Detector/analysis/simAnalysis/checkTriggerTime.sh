#!/bin/bash

for ((num = 1; num <= 50; num ++))
do
    python3 TimeCheck.py 1163 $num /home/czheng/SimCosmicFlatTree/CheckTriggerTime
done  
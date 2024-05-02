#!/bin/bash


for ((num = 1; num <= 200; num ++))
do
    python3 NPEVSarea.py 1163 $num /home/czheng/SimCosmicFlatTree/offline_Area_NPE/no_cutNPE_Area_run1163

done

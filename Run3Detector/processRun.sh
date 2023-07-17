#!/usr/bin/bash

run=66

for i in {0..12}
do
    python3 scripts/runOfflineFactory.py --inputFile /store/user/milliqan/run3/0/0006/MilliQanSlab_Run${run}.${i}_default.root --outputFile MilliQanSlab_Run${run}.${i}_fullProcessed.root --exe ./run.exe 
done

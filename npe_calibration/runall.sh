#! /bin/bash

#for run in 2573 2574 2575 2576 2577 2578 2579 2588 2599 2604 2608 2609 2611 2614 2616 2617 2620
for run in 2753 2755 2757 2759	
#for run in 2573
do
    python measureSPE_v2.py $run &> /dev/null &
done


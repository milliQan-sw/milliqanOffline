#!/usr/bin/bash

source ~/root_condor.sh

python3 checkMatching.py -d $1 -s $2

mv *.json $3

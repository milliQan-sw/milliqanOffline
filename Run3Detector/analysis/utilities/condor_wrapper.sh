#!/bin/bash
source ~/root_condor.sh

cat /etc/hostname
python3 $1 $2 $3
mv *.root $4

#!/usr/bin/bash

hostname=$(cat /proc/sys/kernel/hostname)

echo "working on compute node $hostname"

echo "All arguments: $@"

tar -xzvf milliqanOffline*.tar.gz
tar -xzvf MilliDAQ.tar.gz
tar -xzvf milliQanSim.tar.gz

if [ ! -f "milliqanOffline/Run3Detector/run.exe" ]; then
    echo "Compiling executable run.exe"
    singularity exec -B ../../milliqanOffline/,../../MilliDAQ /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline\:x86/ bash compile.sh run.exe
fi

echo Trying to run process number $1

singularity exec -B /data/ /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline\:x86/ python3 processSimFiles.py -n $1 -f $2 -d $3

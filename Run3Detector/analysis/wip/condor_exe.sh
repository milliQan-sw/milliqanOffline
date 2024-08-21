#!/usr/bin/bash

hostname=$(hostname)

echo "Running on $hostname at $PWD"
echo "arguments passed to script $@"

tar -xzvf milliqanProcessing.tar.gz

sleep $3

singularity run -B $5 /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_uproot\:latest/ python3 $1 $2 $3 $4

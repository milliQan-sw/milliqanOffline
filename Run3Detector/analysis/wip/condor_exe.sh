#!/usr/bin/bash

hostname=$(hostname)

echo "Running on $hostname at $PWD"
echo "arguments passed to script $@"
export SINGULARITY_CACHEDIR=$4

tar -xzvf milliqanProcessing.tar.gz

singularity run -B $5 /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_uproot\:latest/ /usr/bin/bash -c "export PYTHONPATH=$PYTHONPATH:/root/lib/ && export SINGULARITY_CACHEDIR=$4 && source /root/bin/thisroot.sh && python3 $1 $2 $3 $4"
#singularity run -B $5 /data/users/mcarrigan/milliqan_uproot8.sif /usr/bin/bash -c "export PYTHONPATH=$PYTHONPATH:/rootV6/lib/ && export SINGULARITY_CACHEDIR=$4 && source /rootV6/bin/thisroot.sh && python3 $1 $2 $3 $4"

mv *.root $4

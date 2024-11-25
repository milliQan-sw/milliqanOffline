#!/bin/bash

singularity exec --bind /abyss/users/rsantos/MilliQan/:/data,/store/user/milliqan/trees/v35/bar/1900/:/store  /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline:x86/ root -b -q globalEventConv.C+($1)


echo "Finished"

#!/usr/bin/bash

name=`basename "$0"`
pidTest=$(pgrep -f moveFiles.py)

if [[ $pidTest != '' ]]; then
    echo "script $name already running"
    echo "pid found $pidTest and pid running $$"
    exit 1
fi

cd /share/scratch0/milliqan/CMSSW_12_4_7/src
source /cvmfs/cms.cern.ch/cmsset_default.sh
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/cvmfs/cms.cern.ch/slc7_amd64_gcc10/cms/cmssw-patch/CMSSW_12_4_7/external/slc7_amd64_gcc10/lib
PYTHONPATH=$PYTHONPATH:./CMSSW_12_4_11_patch3/python:.
eval `scramv1 runtime -sh`
cd -

echo $PATH
echo $LD_LIBRARY_PATH
python3 /share/scratch0/milliqan/milliqanTools/moveFiles.py
echo "Finished moving files"

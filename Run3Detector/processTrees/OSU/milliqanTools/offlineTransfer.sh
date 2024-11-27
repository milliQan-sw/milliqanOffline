#!/usr/bin/bash

name=`basename "$0"`
pidTest=$(pgrep -f transferOfflineFiles.py)

if [[ $pidTest != '' ]]; then
    echo "script $name already running"
    echo "pid found $pidTest and pid running $$"
    exit 1
fi

cd /share/scratch0/milliqan/CMSSW_12_4_7/src
source /cvmfs/cms.cern.ch/cmsset_default.sh
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/cvmfs/cms.cern.ch/slc7_amd64_gcc10/cms/cmssw-patch/CMSSW_12_4_7/external/slc7_amd64_gcc10/lib
export PYTHONPATH=$PYTHONPATH:./CMSSW_12_4_11_patch3/python:.
export PATH=$PATH:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/usr/totalview/bin:/opt/ganglia/bin:/opt/ganglia/sbin:/usr/java/latest/bin:/opt/rocks/bin:/opt/condor/bin:/opt/condor/sbin:/opt/gridengine/bin/lx-amd64
export CONDOR_CONFIG=/opt/condor/etc/condor_config
eval `scramv1 runtime -sh`
cd -

echo "Attempting to run transfer script"
python3 /home/milliqan/scratch0/milliqanOffline/Run3Detector/scripts/transferOfflineFiles.py
python3 /home/milliqan/scratch0/milliqanOffline/Run3Detector/scripts/transferOfflineFilesMod.py
echo "Finished Transfer"

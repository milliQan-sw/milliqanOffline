#!/usr/bin/bash

#get hostname to figure out OSU, UCSB, or other
name=$(hostname)

echo $name

host_osu='ohio-state'
host_osuCompute='compute-0-'
host_ucsb='cms'

if [[ "$name" == *"$host_osu"* || "$name" == *"$host_osuCompute"* ]]; then
  echo "Working on OSU T3"
  export MILLIDAQDIR="../../MilliDAQ"
  export ROOT_INCLUDE_PATH=$MILLIDAQDIR/interface/
  export OFFLINESITE="OSU"
  export OFFLINEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
elif [[ "$name" == *"$host_ucsb"* ]]; then
  echo "Working on UCSB cluster"
  source /net/cms17/cms17r0/schmitz/root6/install/bin/thisroot.sh
  export MILLIDAQDIR="/homes/milliqan/MilliDAQ"
  export ROOT_INCLUDE_PATH=$MILLIDAQDIR/interface/
  export OFFLINESITE="UCSB"
  export OFFLINEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
else
  echo "Working on a system other than OSU/UCSB, please make sure to set teh correct paths below"
  export MILLIDAQDIR="../../MilliDAQ"
  export ROOT_INCLUDE_PATH=$MILLIDAQDIR/interface/
  export OFFLINESITE="Other"
  export OFFLINEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
fi



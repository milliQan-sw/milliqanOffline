#!/usr/bin/bash

if [ $# -ge 1 ]
  then
    echo "Building container" $1
    container=$1
  else
    echo "Building container offline"
    container=offline
fi

if [ $# -ge 2 ]
  then
    echo "Executable name" $2
    executable=$2
  else
    echo "Executable name run.exe"
    executable=run
fi

if [ ! -e "mQContainer.def" ]
  then
    echo "Downloading mQContainer.def file"
    wget https://raw.githubusercontent.com/carriganm95/milliqanOffline/compilationUpdates/mQContainer.def
fi

singularity build --fakeroot --sandbox $container mQContainer.def

cd $container/milliqanOffline/offlineProduction

sed -i 's|/home/milliqan/MilliDAQ/|$PWD/../../MilliDAQ|' setup.sh

source setup.sh

bash compile.sh ${executable}.exe

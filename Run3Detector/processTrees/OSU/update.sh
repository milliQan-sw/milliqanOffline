#! /usr/bin/bash

source /home/milliqan/root_condor.sh

if [ ! -d "$PWD/milliqanOffline" ]; then
  echo "Opening the tar file milliqanOffline.tar.gz..."

  tar -xzf milliqanOffline*.tar.gz
else
  echo "milliqanOffline directory exists!"
fi

if [ ! -d "$PWD/MilliDAQ" ]; then
  echo "Opening the tar file MilliDAQ.tar.gz..."

  tar -xzvf MilliDAQ.tar.gz
else
  echo "MilliDAQ directory exists!"
fi

export PYTHONPATH=$PYTHONPATH:$PWD'/milliqanOffline/Run3Detector/scripts/'

python3 update_wrapper.py "$@"
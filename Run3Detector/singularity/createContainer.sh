#!/usr/bin/bash

site='' #site you are running from 
container=offline.sif #name of offline container, no .sif if using sandbox
executable=run #name of executable for milliqanOffline
testing=false #if not running a sandbox should be set to false

while getopts ":s:c:e:t:" opt; do
  case $opt in
    s) site="$OPTARG"
    ;;
    c) container="$OPTARG"
    ;;
    e) executable="$OPTARG"
    ;;
    t) testing=true
    ;;
    o) offline="$OPTARG"
    ;;
    m) daq="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    exit 1
    ;;
  esac

  case $OPTARG in
    -*) echo "Option $opt needs a valid argument"
    exit 1
    ;;
  esac
done

if [ ! -e "mQContainer.def" ]
  then
    echo "Downloading mQContainer.def file"
    wget https://raw.githubusercontent.com/milliQan-sw/milliqanOffline/master/Run3Detector/singularity/mQContainer.def
fi

#singularity build --fakeroot $container mQContainer.def

#if not creating sandbox need to download repos ourselves
if [ -f $daq ]; then
  if [ ! -d "$PWD/MilliDAQ" ]; then
    git clone https://gitlab.cern.ch/MilliQan/MilliDAQ.git
  fi
  cd MilliDAQ/
  touch make_shared.sh
  echo "#!/usr/bin/bash" > make_shared.sh
  echo "make clean && make shared" > make_shared.sh
  singularity exec ../offline.sif ./make_shared.sh
  echo "Compiled MilliDAQ shared library"
  cd ../
  daq="$PWD/MilliDAQ"
fi

if [ -f $offline ]; then
  offline="$PWD/milliqanOffline"
  if [ ! -d "$PWD/milliqanOffline" ]; then
    git clone https://github.com/milliQan-sw/milliqanOffline.git
  fi
fi

if [ $site=="OSU" ]; then
  cd "$offline/Run3Detector"
  sed -i 's|/homes/milliqan/MilliDAQ|$PWD/../../MilliDAQ|' setup.sh
  sed -i 's|source /net/cms17/cms17r0/schmitz/root6/install/bin/thisroot.sh||' setup.sh
  sed -i 's|OFFLINESITE="UCSB"|OFFLINESITE="OSU"|' setup.sh
  cd -
fi

singularity exec $container bash -c "cd $offline/Run3Detector && echo $PWD && source setup.sh && bash compile.sh ${executable}.exe"

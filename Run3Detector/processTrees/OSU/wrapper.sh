#!/usr/bin/bash

hostname=$(cat /proc/sys/kernel/hostname)

echo "working on compute node $hostname"

#mv milliqanOffline*.tar.gz milliqanOffline.tar.gz
tar -xzvf milliqanOffline*.tar.gz
tar -xzvf MilliDAQ.tar.gz

cp tree_wrapper.py milliqanOffline/Run3Detector/
cp filelist*.json milliqanOffline/Run3Detector/filelist.json

for ARG in "$@"; do
    if [ $ARG == "-m" ]; then
        echo "Compiling the MilliDAQ library"
        cd MilliDAQ/
        singularity exec /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline\:x86/ bash compile.sh
        cd ../
    fi
done
 
if [ ! -f "MilliDAQ/libMilliDAQ.so" ]; then
    echo "Compiling the MilliDAQ library"
    cp compile.sh MilliDAQ/
    cd MilliDAQ/
    singularity exec /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline\:x86/ bash compile.sh
    cd ../
fi

cd milliqanOffline/Run3Detector/

for ARG in "$@"; do
    if [ $ARG == "-c" ]; then
        echo "Compiling executable run.exe"
        singularity exec -B ../../milliqanOffline/,../../MilliDAQ /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline\:x86/ bash compile.sh run.exe
    fi
done

if [ ! -f "run.exe" ]; then
    echo "Compiling executable run.exe"
    singularity exec -B ../../milliqanOffline/,../../MilliDAQ /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline\:x86/ bash compile.sh run.exe
fi

if [ $# -gt 6 ]; then
    #Running single job
    echo Running single job $6 $7
    if $7; then
        echo "Processing slab data"
        singularity exec -B ../../milliqanOffline/,../../MilliDAQ,/store/ /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline\:x86/ python3 tree_wrapper.py -s $6 -i $2 -v $5 --slab
    else
        singularity exec -B ../../milliqanOffline/,../../MilliDAQ,/store/ /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline\:x86/ python3 tree_wrapper.py -s $6 -i $2 -v $5
    fi
else
    echo Trying to run process number $1
    if $6; then
        echo "Processing slab data"
        singularity exec -B ../../milliqanOffline/,../../MilliDAQ,/store/ /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline\:x86/ python3 tree_wrapper.py -p $1 -i $2 -v $5 --slab
    else
        singularity exec -B ../../milliqanOffline/,../../MilliDAQ,/store/ /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline\:x86/ python3 tree_wrapper.py -p $1 -i $2 -v $5
    fi
fi

filename="MilliQan*_Run*.*.root"

outputFiles=($(ls $filename))

if [ ${#outputFiles[@]} -gt 0 ]; then
    for file in "${outputFiles[@]}"; do
        echo "Changing location of file $file to $4 in mongoDB"
        mv "$file" "$4"
        singularity exec -B ../../milliqanOffline/,../../MilliDAQ,/store/ /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline:x86/ python3 $PWD/scripts/utilities.py -i "$file" -l "$4" -s "OSU"
    done
else
    echo "No files matched the pattern"
fi

#if [ ! -z $outputFiles -a $outputFiles != " " ]; then
#    echo "Changing location of file $outputFiles to $4 in mongoDB"
#    mv $outputFiles $4
#    singularity exec -B ../../milliqanOffline/,../../MilliDAQ,/store/ /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline\:x86/ python3 $PWD/scripts/utilities.py -i "$outputFiles" -l "$4" -s "OSU"
#fi


#!/usr/bin/bash

tar -xzvf milliqanOffline*.tar.gz milliqanOffline/
tar -xzvf MilliDAQ.tar.gz

cp tree_wrapper.py milliqanOffline/Run3Detector/
cp filelist.txt milliqanOffline/Run3Detector/

for ARG in "$@"; do
    if [ $ARG == "-m" ]; then
        echo "Compiling the MilliDAQ library"
        cd MilliDAQ/
        singularity exec ../offline.sif bash compile.sh
        cd ../
    fi
done
 
if [ ! -f "MilliDAQ/libMilliDAQ.so" ]; then
    echo "Compiling the MilliDAQ library"
    cp compile.sh MilliDAQ/
    cd MilliDAQ/
    singularity exec ../offline.sif bash compile.sh
    cd ../
fi

cd milliqanOffline/Run3Detector/

for ARG in "$@"; do
    if [ $ARG == "-c" ]; then
        echo "Compiling executable run.exe"
        singularity exec -B ../../milliqanOffline/,../../MilliDAQ ../../offline.sif bash compile.sh run.exe
    fi
done

if [ ! -f "run.exe" ]; then
    echo "Compiling executable run.exe"
    singularity exec -B ../../milliqanOffline/,../../MilliDAQ ../../offline.sif bash compile.sh run.exe
fi

echo Trying to run process number $1
singularity exec -B ../../milliqanOffline/,../../MilliDAQ,/store/ ../../offline.sif python3 tree_wrapper.py $1 $2 $5

filename="MilliQan_Run*.*.root"

if compgen -G $filename > /dev/null; then
    mv $filename $4
fi

#if [ -f "filelist.txt" ]; then
#    rm "filelist.txt"
#fi

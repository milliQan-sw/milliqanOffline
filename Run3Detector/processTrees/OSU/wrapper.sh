#!/usr/bin/bash

hostname=$(cat /proc/sys/kernel/hostname)

echo "working on compute node $hostname"

#mv milliqanOffline*.tar.gz milliqanOffline.tar.gz
tar -xzvf milliqanOffline*.tar.gz
tar -xzvf MilliDAQ.tar.gz

cp tree_wrapper.py milliqanOffline/Run3Detector/
cp filelist*.txt milliqanOffline/Run3Detector/filelist.txt

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

if [ $# -gt 5 ]; then
    #Running single job
    echo Running single job
    singularity exec -B ../../milliqanOffline/,../../MilliDAQ,/store/ ../../offline.sif python3 tree_wrapper.py -s $6 -i $2 -v $5
else
    echo Trying to run process number $1
    singularity exec -B ../../milliqanOffline/,../../MilliDAQ,/store/ ../../offline.sif python3 tree_wrapper.py -p $1 -i $2 -v $5
fi

filename="MilliQan_Run*.*.root"

outputFiles=$(ls $filename)

if [ ! -z $outputFiles -a $outputFiles != " " ]; then
    echo "Changing location of file $outputFiles to $4 in mongoDB"
    mv $outputFiles $4
    singularity exec -B ../../milliqanOffline/,../../MilliDAQ,/store/ ../../offline.sif python3 $PWD/scripts/utilities.py -i "$outputFiles" -l "$4" -s "OSU"
fi


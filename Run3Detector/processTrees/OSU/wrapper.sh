#!/usr/bin/bash
# hostname=$(cat /proc/sys/kernel/hostname)
#
# echo "working on compute node $hostname"

#mv milliqanOffline*.tar.gz milliqanOffline.tar.gz
tar -xzvf milliqanOffline*.tar.gz > /dev/null
tar -xzvf MilliDAQ.tar.gz > /dev/null

cp tree_wrapper.py milliqanOffline/Run3Detector/
cp filelist*.txt milliqanOffline/Run3Detector/filelist.txt
home=${PWD}

# singularity shell -B /afs -B /eos -B /cvmfs /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline\:x86/
export EOS_MGM_URL=root://eosexperiment.cern.ch

echo 1 $1
echo 2 $2
echo 3 $3
echo 4 $4
echo 5 $5
echo 6 $6
echo 7 $7
echo 8 $8
echo 9 $9
echo 

for ARG in "$@"; do
    if [ $ARG == "-m" ]; then
        echo "Compiling the MilliDAQ library"
        cd MilliDAQ/
        singularity exec --home ${home} bash compile.sh
        cd ../
    fi
done
 
if [ ! -f "MilliDAQ/libMilliDAQ.so" ]; then
    echo "Compiling the MilliDAQ library"
    cp compile.sh MilliDAQ/
    cd MilliDAQ/
    singularity exec --home ${home} /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline\:x86/ bash compile.sh
    cd ../
fi

cd milliqanOffline/Run3Detector/
echo "Listing directory before compilation"
ls .

for ARG in "$@"; do
    if [ $ARG == "-c" ]; then
        echo "Compiling executable run.exe" 
        singularity exec --home ${home} /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline\:x86/ bash compileForBatch.sh run.exe
    fi
done

if [ ! -f "run.exe" ]; then
    echo "Compiling executable run.exe"
    singularity exec  --home ${home} /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline\:x86/ bash compileForBatch.sh run.exe
fi
echo "Listing directory after compilation"
ls .

if [ $# -gt 8 ]; then
    #Running single job
    echo Running single job $6 $7
    if $8; then 
        echo "Processing formosa data"
        singularity exec  --home ${home}  -B /eos /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline:x86/ python3 tree_wrapper.py -s $6 -i $2 -v $5 --formosa
    else
        if $7; then
            echo "Processing slab data"
            singularity exec --home ${home}  -B /eos /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline:x86/ python3 tree_wrapper.py -s $6 -i $2 -v $5 --slab
        else
            singularity exec --home ${home}  -B /eos /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline:x86/ python3 tree_wrapper.py -s $6 -i $2 -v $5
        fi
    fi
else
    echo Trying to run process number $1
    if $7; then 
        echo "Processing formosa data"
        singularity exec --home ${home}  -B /eos /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline:x86/ python3 tree_wrapper.py -p $1 -i $2 -v $5 --formosa
    else
        if $6; then
            echo "Processing slab data"
            singularity exec --home ${home}  -B /eos /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline:x86/ python3 tree_wrapper.py -p $1 -i $2 -v $5 --slab
        else
            singularity exec --home ${home}  -B /eos /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline:x86/ python3 tree_wrapper.py -p $1 -i $2 -v $5
        fi
    fi
fi

echo "Listing directory after processing"
ls .

filename="MilliQan*_Run*_v*.root"

outputFiles=$(ls $filename)
echo $outputFiles
echo "${#outputFiles[@]}"
lenOutput=${#outputFiles[@]}
if [ "$lenOutput" -gt "0" ]; then
    for outputFile in ${outputFiles}; do
	echo "Changing location of file $outputFile to $4 in mongoDB"
	eos cp $outputFile $4
	singularity exec --home ${home} /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_offline:x86/ python3 $PWD/scripts/utilities.py -i "$outputFile" -l "$4" -s "eos" -d "formosa" -t "FORMOSA"
    done
fi

#clean up
rm *.root

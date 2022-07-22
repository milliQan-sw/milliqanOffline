#!/bin/bash

if [ $# != 1 ]
	then echo "Please provide exactly one argument, the desired macro name."
	exit 
fi

MILLIDAQDIR=/home/milliqan/MilliDAQ/

NAME=$1


SHORT_TAG=`git describe --tag --abbrev=0`
LONG_TAG=`git describe --tags --long`

#echo $SHORT_TAG
echo "milliqanOffline version $LONG_TAG"

sed "s/shorttagplaceholder/$SHORT_TAG/g" src/runOfflineFactory.cc > make_tree_temporary_for_compile.C
sed -i "s/longtagplaceholder/$LONG_TAG/g" make_tree_temporary_for_compile.C

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

g++ -o $NAME make_tree_temporary_for_compile.C ./src/jsoncpp.cpp ./src/OfflineFactory.cc ${MILLIDAQDIR}/src/ConfigurationReader.cc ${MILLIDAQDIR}/libMilliDAQ.so -lpython2.7 `root-config --cflags --glibs` -Wno-narrowing -I$SCRIPT_DIR -I$MILLIDAQDIR # same as above but with correct local file path

if [ $? -eq 0 ]; then
    echo "Compiled macro $NAME"
else
    echo "FAILED to compile macro $NAME"
fi
rm make_tree_temporary_for_compile.C



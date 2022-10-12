#!/bin/bash

if [ $# != 1 ]
	then echo "Please provide exactly one argument, the desired macro name."
	exit 
fi


NAME=$1

SHORT_TAG=`git describe --tag --abbrev=0`
LONG_TAG=`git describe --tags --long`

#echo $SHORT_TAG
echo "milliqanOffline version $LONG_TAG"

sed "s/shorttagplaceholder/$SHORT_TAG/g" src/OfflineFactory.cc > src/OfflineFactory_temporary_for_compile.cc
sed -i "s/longtagplaceholder/$LONG_TAG/g" src/OfflineFactory_temporary_for_compile.cc

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source ${SCRIPT_DIR}/setup.sh

g++ -o $NAME src/runOfflineFactory.cc ./src/jsoncpp.cpp ./src/OfflineFactory_temporary_for_compile.cc ${MILLIDAQDIR}/src/ConfigurationReader.cc ${MILLIDAQDIR}/libMilliDAQ.so -lpython2.7 `root-config --cflags --glibs` -Wno-narrowing -I$SCRIPT_DIR -I$MILLIDAQDIR -I$ROOT_INCLUDE_PATH # same as above but with correct local file path

if [ $? -eq 0 ]; then
    echo "Compiled macro $NAME"
else
    echo "FAILED to compile macro $NAME"
fi
rm ./src/OfflineFactory_temporary_for_compile.cc



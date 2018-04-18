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

sed "s/shorttagplaceholder/$SHORT_TAG/g" make_tree.C > make_tree_temporary_for_compile.C
sed -i "s/longtagplaceholder/$LONG_TAG/g" make_tree_temporary_for_compile.C

g++ -o $NAME make_tree_temporary_for_compile.C /net/cms26/cms26r0/milliqan/milliDAQ/libMilliDAQ.so `root-config --cflags --glibs` -Wno-narrowing

rm make_tree_temporary_for_compile.C
echo "Compiled macro $NAME"



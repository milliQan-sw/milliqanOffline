#!/bin/bash

DIRECTORY=`pwd`
cd /net/cms2/cms2r0/babymaker/CMSSW_8_0_8/src/
. /net/cms2/cms2r0/babymaker/cmsset_default.sh
eval `scramv1 runtime -sh`
cd $DIRECTORY;

# Execute command
$@

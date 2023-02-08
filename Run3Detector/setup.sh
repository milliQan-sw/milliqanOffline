#Change these as appropriate
source /net/cms17/cms17r0/schmitz/root6/install/bin/thisroot.sh
export MILLIDAQDIR="/homes/milliqan/MilliDAQ"
export ROOT_INCLUDE_PATH=$MILLIDAQDIR/interface/
export OFFLINESITE="UCSB"
export OFFLINEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )


jobsRunning=$(condor_q | grep mcitron |grep running | grep -oP '(?<=idle, )[0-9]+')
echo "Jobs running" ${jobsRunning}
if [ "$jobsRunning" == "0" ]; then
    cd /afs/cern.ch/user/m/mcitron/milliqanOffline/Run3Detector/processTrees/OSU
    source ../../setup.sh
    for run in 600 700 800; do for sub in {0..9}; do python3 run_processTrees.py -r ${run} -s 000${sub} --formosa -v 36; done; done
fi

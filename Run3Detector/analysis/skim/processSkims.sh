#!/usr/bin/bash

# directory, outputFile, beam, goodRun, skim

beam="False"
goodRun="goodRunMedium"
skim="signal"

for run in {1100..1100..100}; do
    echo "Processing run $run, beam $beam, goodRun $goodRun, and skim $skim"

    # Determine beam state
    if [ "$beam" = "False" ]; then
        beam_state="beamOff"
    else
        beam_state="beamOn"
    fi

    # Determine good run criteria
    if [ "$goodRun" = "goodRunTight" ]; then
        goodRunCriteria="tight"
    elif [ "$goodRun" = "goodRunMedium" ]; then
        goodRunCriteria="medium"
    elif [ "$goodRun" = "goodRunLoose" ]; then
        goodRunCriteria="loose"
    else    
        goodRunCriteria="none"
    fi

    # Run the Python script
    python3 -u do_skim.py /store/user/milliqan/trees/v36/bar/${run}/ \
        MilliQan_Run${run}_v36_${skim}_${beam_state}_${goodRunCriteria}.root \
        $beam $goodRun $skim
done

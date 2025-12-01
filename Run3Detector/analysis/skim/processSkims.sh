#!/usr/bin/bash

# directory, outputFile, beam, goodRun, skim

beam="False"
goodRun="goodRunTight"
skim="zeroBias"

for run in {1300..1900..100}; do
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
    python3 -u do_skim.py /store/user/milliqan/trees/v35/bar/${run}/ \
        MilliQan_Run${run}_v35_${skim}_${beam_state}_${goodRunCriteria}.root \
        $beam $goodRun $skim
done
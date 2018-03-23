These scripts are used to create the background predictions (as presented at the yearly meeting [here](https://indico.cern.ch/event/684514/contributions/2806411/attachments/1568388/2472920/milliqanYearlyMeetingMC.pdf))

First change into the scripts directory
```bash
cd milliqanOffline/milliqanScripts
```

If you want to remake the inputs use ./milliqanScripts/skims/makeTrueTripleSkim.py (changing the selection string and output file name to make beam and non beam input files). The variable 'inputFileName' 
in milliqanOffline/milliqanScripts/backgroundMeasurement/makeBackgroundRatePlots.py must also be updated.  

Then run makeBackgroundRatePlots.py
```bash
python backgroundMeasurement/makeBackgroundRatePlots.py
```

This will make the large number of rate vs npe plots for many different scenarios. The beautified plots and predictions can then be made using makePrettyFinalPlots.py depending
on the functions used:
```bash
python backgroundMeasurement/makePrettyFinalPlots.py
```


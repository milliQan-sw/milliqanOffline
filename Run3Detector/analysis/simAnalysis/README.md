milliQanSim analysis
----------------------------------------------------------------

Files in this folder are to analysis the Flat simulatoin tree.
You can find the details for how generate the raw data at https://github.com/rtschmitz/milliQanSim/tree/main
The tree flattening script can be found at https://github.com/CollinKa/CreateSimFlattree


I create some analysis script for cosmic background analysis with the flat tree.




CosmicEventDebug.py: this file is used to get the details of the specified events in case you need to do some debugging.

withPhotonAnalysis.py: count the number of sim events that pass the geometric, NPE ratio and correct time cut for each event and print the results. The result will be collect to reconstruct the table 1 in https://journals.aps.org/prd/pdf/10.1103/PhysRevD.104.032002 with latest detector configuration.
Usage: python3 withPhotonAnalysis.py > output.txt

summingResult.py: count the number of sim events that pass different cuts from all of the files.


SimMuon_tag.py: find the events that matches the cosmic muon characteristic and then send the eventID and file ID to muonTagPlot.py to create histograms.


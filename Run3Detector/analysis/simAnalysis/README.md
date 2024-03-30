milliQanSim analysis
----------------------------------------------------------------

Files in this folder are to analysis the Flat simulatoin tree.
You can find the details for how generate the raw data at https://github.com/rtschmitz/milliQanSim/tree/main
The tree flattening script can be found at https://github.com/CollinKa/CreateSimFlattree


I create some analysis script for cosmic background analysis with the flat tree.




CosmicEventDebug.py: this file is used to get the details of the specified events in case you need to do some debugging.

withPhotonAnalysis.py: count the number of sim events that pass the geometric, NPE ratio and correct time cut for each event and print the results. The result will be collect to reconstruct the table 1 in https://journals.aps.org/prd/pdf/10.1103/PhysRevD.104.032002 with latest detector configuration. Event that pass correct time cut is rare, so I didn't write a script to do the counting. But you can mannualy count them by searching "signal like event" in output.

Usage: python3 withPhotonAnalysis.py > output.txt


summingResult.py: count the number of sim events that pass different cuts from all of the files. The event that can pass concecutive correct time is an interesting event. You can find them inside output.txt by searching "signal like event is found!"

offlineCheck1.py: check the result by applying the analysis to offline data


SimMuon_tag.py: find the events that matches the cosmic muon characteristic and then send the eventID and file ID to muonTagPlot.py to create histograms.

SimCosmicMuonTag_V3.py: this file is created based on SimCosmicMuonTag_V2.py. The reason for creating this file is complicated. So previously, I notice milliqan can't make a plot once I used the EmptylistFilter(). I talk to mike but he can't find any obvious issue in my script. One of the solution that he suggest is not to apply cut in EmptylistFilter() but just create the mask. see the sample file at https://github.com/milliQan-sw/milliqanOffline/commit/fdce0a1ecc9de527415523424b7d76af8bf64f28. 
To make the SimCosmicMuonTag_V3.py work, I add two extra methods for bar and cosmic panel tagging which also check the "empty" mask. The latest result shows the the number of events that pass the cosmic event tag is zero and all of events are are non-empty (these are definitely wrong). 





OLCosmicMuonTag_V2.py: offline analysis that uses the fuctions I defined in SimCosmicMuonTag_V2.py.  

----------------------sample for using condor job------------------
to check the progress use condor_q --allusers


1.test the job submission script and create json file
python3 SIMCondor.py -i /mnt/hadoop/se/store/user/czheng/SimFlattree/withPhotonMuontag/ -o /home/czheng/scratch0/SIManalysisDEV/milliqanOffline/Run3Detector/analysis/simAnalysis/condorTest/ -s layerConstrainDemo_job.py -t

use the first file and test if the script is running as expected
bash condor_wrapper.sh layerConstrainDemo_job.py 0 filelist.json locationForsavingFile

if thing is working fine then 
python3 SIMCondor.py -i /mnt/hadoop/se/store/user/czheng/SimFlattree/withPhotonMuontag/ -o /home/czheng/scratch0/SIManalysisDEV/milliqanOffline/Run3Detector/analysis/simAnalysis/condorTest/ -s layerConstrainDemo_job.py


When doing the cut efficiency test, I save the out to txt files. So Condor_wrapper.sh requires an new script "mv *.txt $4" and comment out the mv *.root $4.
I save the txt file location at /home/czheng/scratch0/SIManalysisDEV/milliqanOffline/Run3Detector/analysis/simAnalysis/CutEffCheck


python3 SimCosmicMuonTag_V2.py -i /mnt/hadoop/se/store/user/czheng/SimFlattree/withPhotonMuontag/ -o /home/czheng/scratch0/SIManalysisDEV/milliqanOffline/Run3Detector/analysis/simAnalysis/CutEffCheck/ -s SimCosmicMuonTag_V2.py -t


--------------------------run the analysis script on milliqan machine---------------------------------------------
currently has a weird bug, so I move the analysis script to here.

I create a bash script that can run the tagging algorism effectively at here



source MQmachineRun.sh



------------------------sample for using bsub job(TBD) ----------------
UCSB cluster doesn't come with uproot now
python3 



----------------------------3-18 new files update-------------------

simCosmicMuonTag_*.py : the "*" is for cutflow I defined in the  simCosmicMuonTag_V2.py
I create multiple files of this kind so I can process multiple cutflow at the same time.

I also craete multiple OLCosmicMuonTag_V2_*.py for same reason.



----------------------------3-30 new file update---------------------
SimCosmicMuonTag_SimBeamData.py: I apply the cosmic muon event tag on the beam sim files
SIMMQplotter_containtBeta.py: my first demo that don't use self.events = self.events[eventCut], so the MQPlotter can work properly.








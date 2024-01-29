### Output tree contents

Each event of the tree contains several vectors storing details such as the channel, nPE, area and time of the pulses. The most important are summarised below:

- chan: channel that recorded the pulse. See mapping [here](https://github.com/milliQan-sw/milliqanOffline/files/10484641/channelMapping.pdf)
- layer: layer of channel 
- area: area of the pulse in pVs
- nPE: number of photons contained in pulse (determined through SPE calibration, approximate)
- duration: pulse duration in ns
- height: maximum amplitude in pulse in mV
- timeFit: uncalibrated time of pulse in ns
- timeFit_module_calibrated: calibrated time of pulse in ns (currently the same as time)
- ipulse: pulse index

In addition there are quantities that provide a single per channel measure of the noise and activity in each channel per event. These are vectors of length = number of channels (rather than number of pulses).

- sidebandMean: the mean of the first 50ns of the waveform (this period is not used to find pulses)
- sidebandRMS: the RMS of the first 50ns of the waveform

At UCSB per run offline trees are stored here: /homes/milliqan/milliqanOffline/Run3Detector/outputRun3/

### Compiling the code:

For the compilation to succeed, one must specify the path to the MilliDAQ shared object file (libMilliDAQ.so) and `ConfigurationReader.cc` in the compile script 
`compile.sh`.
This involves editing `setup.sh` to have the correct environmental variables. The OFFLINESITE is used to define the site for the database

To compile the code, which produces an executable file (from the macro) that will be used for the tree-making, execute the following command

```bash
. setup.sh
./compile.sh (target macro name).exe

```

Keep track of the "target macro name" as this macro will be needed when making the offline trees.

From the milliqanOffline directory you can run on a single file using the runMakeTree.py script.
### Making the Offline Trees
The code is run by executing the `runOfflineFactory.py` script. You may execute the `runMakeTree.py` script using the following command:
```bash
   python3 scripts/runOfflineFactory.py --inFile "input_filename".root --outputFile "output_filename".root --exe ./(target macro name).exe (--publish) ...
```
Where `(target macro name).exe` is the one specified when running the `compile.sh` script. The publish option will include the file details in the mongoDB database.

NB. The jsons used to define the configurations are set by default within the scripts/runOfflineFactory.py script but this can be overrided with the --configuration option. Use the -h option to see more details.

### Processing full runs

At UCSB, use the processRuns.py script to run over larger quantities of data on the UCSB batch system. The input is determined by a mongoDB selection string and the command to run can be as follows:

```bash
python3 scripts/processRuns.py -a <string to append to tag for output naming> -s <selection string> -o <output directory>
```
 NB. Use the -h option to see more details

### Making the event displays for specific events
The code is run by executing the `runOfflineFactory.py` script and providing the event numbers to be displayed
```bash
   python3 scripts/runOfflineFactory.py --inFile "input_filename".root --outputFile "output_filename".root --exe ./(target macro name).exe (--publish) --display "event_number1" "event_number2"
```
Where `(target macro name).exe` is the one specified when running the `compile.sh` script. The publish option will include the file details in the mongoDB database. The display option will provide event displays for specified events. The event displays are saved in a displays//Run(run_number) directory.
The event displays show the waveform in all the channels above the threshold, the hit map for the detector and details of 10 pulses with maximum height.


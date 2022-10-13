### milliqanOffline

### Output tree details

Each event of the tree contains several vectors storing details such as the channel, nPE, area and time of the pulses (defined as detailed [here](https://indico.cern.ch/event/684514/contributions/2806409/attachments/1568387/2472867/Heller_MilliqanCollaboration_0930.pdf)). The most important are summarised below:

- chan: channel that recorded the pulse
- layer: layer of channel (negative for sidecars)
- area: area of the pulse in pVs
- nPE: number of photons contained in pulse (determined through SPE calibration)
- duration: pulse duration in ns
- height: maximum amplitude in pulse in mV
- time: uncalibrated time of pulse in ns
- time_module_calibrated: calibrated time of pulse in ns (using method documented [here](https://indico.cern.ch/event/684514/contributions/2806411/attachments/1568388/2472920/milliqanYearlyMeetingMC.pdf))
- ipulse: pulse index

The offline trees are automatically made at UCSB with the latest stable tag. They can be found in /net/cms26/cms26r0/milliqan/milliqanOffline/trees/

### Installation and Dependencies

Clone the milliqanOffline repo:

```bash

git clone https://github.com/kdownham/milliqanOffline.git

```
Install pyROOT and python3-root (requires sudo privileges):

```bash

pip3 install pyROOT
sudo yum install python3-root

```

### Compiling the code:

For the compilation to succeed, one must specify the path to the MilliDAQ shared object file (libMilliDAQ.so) and `ConfigurationReader.cc` in the compile script 
`compile.sh`.
This involves editing line 22 of `compile.sh` (the compilation command). The macro that performs the offline tree-making is specified in line 17 of `compile.sh` (the 
default is `simple_macro.C`).

To compile the code, which produces an executable file (from the macro) that will be used for the tree-making, execute the following command

```bash

./compile.sh (target macro name).exe

```

Keep track of the "target macro name" as this macro will be needed when making the offline trees.

##To use common scripts, log onto milliqan username on SL6 machine (e.g. cms1, cms3, cms6, cms29)

From the milliqanOffline directory you can run on a single file using the runMakeTree.py script.

From anywhere, you can:
	processRun.py <runNumber> (submits batch jobs)

	submitAllRuns.py (WARNING: this will attempt to submit jobs to reprocess all runs. Best to initiate from a `screen` terminal)

	makeDisplays.py 
		positional arguments:
		  runNumber             Run number for display
		  nEvents               Number of diplays to make

		optional arguments:
	 -h, --help            show this help message and exit
  	 -s SELECTION, --selection SELECTION
                        Selection, if you call this script from bash and use
                        the symbol $ in selection, you must use single quotes
                        or backslash to escape.
 	 -t TAG, --tag TAG     Filename tag
  	 -r RANGEFORTIME RANGEFORTIME, --rangeForTime RANGEFORTIME RANGEFORTIME
                        Force time range for plots (default is zoomed to
                        pulses)
 	 -v RANGEFORVOLTAGE RANGEFORVOLTAGE, --rangeForVoltage RANGEFORVOLTAGE RANGEFORVOLTAGE
                        Force y range for plots (default is zoomed to pulses)
 	 --noBounds            Disable display of pulsefinding bounds.
 	 -c FORCECHANS [FORCECHANS ...], --forceChans FORCECHANS [FORCECHANS ...]
                        List of channels to force in display (space separated,
                        any length)
 	 -f, --fft             run FFT
  	 -l, --LPF             apply low pass filter
  	 -p, --pulseInject     Inject pulses
  	 -q SIGNALINJECT, --signalInject SIGNALINJECT
                        Inject signal
 	 -o, --onlyForceChans  Only show forced chans


##### Tags and versions #######
To mark a new version number after pushing a commit, make a new "lightweight tag" like this:
```bash
git tag v11
git push --tags
```
This tag name is used to define the version number and the tree directory name.
The full tag (output of `git describe --tags --long`)will be saved to the output root file, which will appear like this:
```bash
v7-0-g57ec693
```
This indicates the tagged version, the number of commits since the last tag was made, and the hash for the latest commit.


### Making the Offline Trees
The code is run by executing the `runMakeTree.py` script. You may execute the `runMakeTree.py` script using the following command:
```bash
   python3 runMakeTree.py --inFile "input_filename".root --exe ./(target macro name).exe -d
```
Where `(target macro name).exe` is the one specified when running the `compile.sh` script.
	
ROOT files containing the output trees are by default placed in the `milliqanOffline/trees` directory.

### MilliDAQ shared libraries
To compile the MilliDAQ shared library, `libMilliDAQ.so`, necessary for reading the "raw" data, do the following:
```bash
	cd /net/cms26/cms26r0/milliqan/MilliDAQ
	make clean
	make shared
```


	


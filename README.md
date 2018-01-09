### milliqanOffline

### Compiling the code:

g++ -o make_tree make_tree.C /net/cms26/cms26r0/milliqan/MilliDAQ/libMilliDAQ.so `root-config --cflags --glibs` -Wno-narrowing

##To use common scripts, log onto milliqan username on SL6 machine (e.g. cms1, cms3, cms6, cms29)

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
		                        Force time range for p


### Link dependencies
The above scripts rely on the following links in `/homes/milliqan/bin`
	findEvents.py  
	makeDisplays.py  
	make_tree  
	processRun.py  
	wrapper.sh
They should all point to the corresponding executables in the milliqanOffline directory
/homes/milliqan/bin must be added to the csh path in ~/.cshrc as well, since batch jobs are executed in csh.

### Batch system
Make sure the batch system has a reasonable skipped nodes list in $JOBS(see committed example as starting point).

### MilliDAQ shared libraries
To compile the MilliDAQ shared library, `libMilliDAQ.so`, necessary for reading the "raw" data, do the following:
	cd /net/cms26/cms26r0/milliqan/MilliDAQ
	make clean
	make shared

The Makefile has 3 modified lines to avoid dependencies on unnecessary CAEN libraries (already done on the cms26 installation).

The diff of the changes are:
	-LDFLAGS = -L./. $(shell root-config --libs) -lCAENDigitizer -lCAENVME
	+LDFLAGS = -L./. $(shell root-config --libs)

	@@echo "Generating dictonary..."
	-       @@rootcint -f $@ -c $(INCLUDE) interface/Event.h interface/V1743Configuration.h interface/LinkDef.h
	+       @@rootcint -f $@ -c $(INCLUDE) interface/Event.h interface/LinkDef.h

	 libMilliDAQ.so: Dict.cxx
        @@echo "Making $@ ..."
	-       @@$(CXX) $(CXXFLAGS) $(SOFLAGS) -o $@ $(LDFLAGS) src/Event.cc src/V1743Configuration.cc $<
	+       @@$(CXX) $(CXXFLAGS) $(SOFLAGS) -o $@ $(LDFLAGS) src/Event.cc $<


Also remove the following line from LinkDef.h:
#pragma link C++ class mdaq::V1743Configuration+;








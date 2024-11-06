# MilliQan Processor and Utilities

Overview:
    This directory contains the main tools for processing milliqan offline trees including the milliqanProcessor. An overview of the main tools defining the milliqan analysis framework is given below.

### milliqanProcessor:

This class acts as a wrapper for the uproot iterate method. Inputs to the processor are: 
- filelist (required): list of input files for the processor to run over, these should be offline trees 
- branches (required): list of all branches from the offline files that are needed for the specific analysis 
- schedule (required): milliqanScheduler class instance containing a list of all cuts and plots that will be made 
- cuts (depreciated): milliqanCuts class instance passed directly to processor 
- plotter (depreciated): milliqanPlotter class instance passed directly to processor 
- max_events: max number of events that should be run over 
- qualityLevel: quality cut to require from the filelist 
    - override: allow all files 
    - loose: default trigger configs, file is well trigger and digitizer matched 
    - medium: loose requirements and 2 or fewer channels without pulses 
    - tight: loose requirements and no channels without pulses 
    - single_trigger: special run with single triggers only 
- verbosity: verbose output level for print outs from the processor (off, minimal, full) 

### milliqanCuts:

This is a class containing functions for all standard cuts applied to data. Any useful cuts should be added to this class in a PR. There is also a cutflow tool to add event counts after each cut to a print out table at the end of jobs.

### milliqanScheduler:

This class contains an ordered list of all cuts and plots that will be made when processing. All items passed to the scheduler are checked to make sure they exist before being added to the schedule. A list of inputs to this class are listed below:
- inputs: ordered list of cuts and plots that will be applied/created
- cuts: milliqanCuts object to get all of the standard cuts from
- plotter: miliqanPlotter object to used to create all of the requested plots

### milliqanPlotter:

This class contains a dictionary of plots and root histogram objects that should be created when running the processor. Is it passed to the processor through the scheduler.

  

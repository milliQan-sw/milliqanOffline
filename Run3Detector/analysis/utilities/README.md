Overview:
  This directory contains the main tools for processing milliqan offline trees including the milliqanProcessor. An overview of the main tools defining the milliqan analysis framework is given below.
  
milliqanProcessor: This class acts as a wrapper for the uproot iterate method. Inputs to the processor are: <br>
  -filelist (required): list of input files for the processor to run over, these should be offline trees <br>
  -branches (required): list of all branches from the offline files that are needed for the specific analysis <br>
  -schedule (required): milliqanScheduler class instance containing a list of all cuts and plots that will be made <br>
  -cuts (depreciated): milliqanCuts class instance passed directly to processor <br>
  -plotter (depreciated): milliqanPlotter class instance passed directly to processor <br>
  -max_events: max number of events that should be run over <br>
  -qualityLevel: quality cut to require from the filelist <br>
    -override: allow all files <br>
    -loose: default trigger configs, file is well trigger and digitizer matched <br>
    -medium: loose requirements and 2 or fewer channels without pulses <br>
    -tight: loose requirements and no channels without pulses <br>
    -single_trigger: special run with single triggers only <br>
  -verbosity: verbose output level for print outs from the processor (off, minimal, full) <br>

milliqanCuts:

milliqanScheduler:

milliqanPlotter:

  

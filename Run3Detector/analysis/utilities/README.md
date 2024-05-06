Overview:
  This directory contains the main tools for processing milliqan offline trees including the milliqanProcessor. An overview of the main tools defining the milliqan analysis framework is given below.
  
milliqanProcessor: This class acts as a wrapper for the uproot iterate method. Inputs to the processor are
  filelist (required): list of input files for the processor to run over, these should be offline trees
  branches (required): list of all branches from the offline files that are needed for the specific analysis
  schedule (required): milliqanScheduler class instance containing a list of all cuts and plots that will be made
  cuts (depreciated): milliqanCuts class instance passed directly to processor
  plotter (depreciated): milliqanPlotter class instance passed directly to processor
  max_events: max number of events that should be run over
  qualityLevel: quality cut to require from the filelist
    override: allow all files 
    loose: default trigger configs, file is well trigger and digitizer matched, 
    medium: loose requirements and 2 or fewer channels without pulses
    tight: loose requirements and no channels without pulses
    single_trigger: special run with single triggers only
  verbosity: verbose output level for print outs from the processor (off, minimal, full)

milliqanCuts:

milliqanScheduler:

milliqanPlotter:

  

Overview:
  This directory contains useful scripts for running analysis on milliqan offline data.

Condor Jobs (Multiprocessing):
  If running analysis jobs on a computer that has condor the run_jobs.py file can be used to help submit jobs. Required arguments are:
  
  Input Directory(-i): Data to run over
  
  Output Directory(-o): Directory to save files to
    
  Script(-s): The python analysis script to run
    
    Ex. python3 run_jobs.py -i /store/user/mcarrigan/skim/muon/v30/ -o /store/user/mcarrigan/test/muon_skim_test/ -s exampleLooperMultiprocess.py

  

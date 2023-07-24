Bar Detector Calibration:

*Note: Scripts do not currently support panel swaps made in between runs, e.g. cannot handle analyzing runs 1006 and 1114 together. Will be updated.

The bar detector is a multi-layered calibration job and requires that channels in any given column are first calibrated to their leading channel, which I have chosen to define as the reference or "true" column time. This is done by running the muon_analysis_bars_columns.py script and setting the elements of fix_pan68 and fix_pan72 to zero. The corrections can be found from the output root file containing histograms with associated stat boxes. 

            


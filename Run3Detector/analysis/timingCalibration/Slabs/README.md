This directory holds the various scripts used to do a base calibration of the timing systems for the slab detector. These scripts are intended to be used to analyze detector properties and determine cuts for finding quality pulses likely from beam and cosmic muons, and then apply these selections to the timing difference. 

The time difference between the two slabs should correspond to the physical length of the detector roughly divided by the speed of light. However because of cable lengths this requires some maneuvering. 

A Beam muon registers a traversal time of (t_2 + l_2)-(t_2+l_1) and a Cosmic muon registers -(t'_2 + l'_2)+(t'_2+l'_1) since cosmics typically arrive from above the cavern. Finding the time difference between the peak Cosmic and Beam traversal time allows us to get rid of cable lengths and get a sense of how well the slabs are calibrated to each other.


To this end we must search for the following key quantities: 

1) Slab pulse height saturation, 1250 mv usually for this digitizer
2) Slab pulse area distribution which should have a peak at high values reflecting the large $N_{PE}$ of high energy muons

We expect the time difference between peaks to be ~2L/c for L being the length of the detector.


The typical chain of analysis would be to obtain pulse height cuts for the slabs, likely from the ROOT terminal e.g. 

t->Draw("height[chan==71]") or t->Draw("height[chan==75]")

to observe the point of pulse saturation and use this to define a cut applied to the Pulse_area_Slabs_study.py which further allows one to define an area cut. This new information is then passed to muon_analysis_slabs.py for the final time difference calculations and a stylized/fit plot is created in the Fitting_histo_slabs.py. 

*Note:Refinements need to made to handle channel swaps and export the channel cuts.

# This file is used to keep track of detector geometry values like channel mappings.
#endCaps = (71, 75)
npeCutoff = 60
pickupCutoff = 500
height_threshold = 2

muon_height_thr = 500.0 #pulse height in mV

#This block sets the channel map for the panels for each running period (or era).
#The channels numbers are stored as a tuple and added as values to the dictionary.  These are in order of layer (closest to IP is first).
#The names of the run periods are the keys for the dictionary.
endCaps = {}
endCapsA = (71,75)
endCaps.update({'EraA': endCapsA})
endCapsB = (74,75)
endCaps.update({'EraB': endCapsB})

topPanels = {}
topPanelsA = (68,72)
topPanels.update({'EraA': topPanelsA})
topPanelsB = (68,69)
topPanels.update({'EraB': topPanelsB})

#For the right and left panels, these are from the POV of the IP looking toward the bar detector.
rightPanels = {}
rightPanelsA = (69,73)
rightPanels.update({'EraA': rightPanelsA})
rightPanelsB = (72,73)
rightPanels.update({'EraB': rightPanelsB})

leftPanels = {}
leftPanelsA = (70,74)
leftPanels.update({'EraA': leftPanelsA})
leftPanelsB = (70,71)
leftPanels.update({'EraB': leftPanelsB})

#!/usr/bin/python3

#threshold panels have to pass in order to trigger (mV)
panelThreshold = 700 

#nLayers trigger n value
nLayers = 3

#nHits trigger n value
nHits = 3

#trigger window pulses must be within to trigger (ns)
trigWindow = 160

#top panel channels
topPanels = [68,69]

#bottom bar channels in bar detector
bottomBars = [10, 11, 14, 15, 26, 27, 30, 31, 42, 43, 46, 47, 58, 59, 62, 63]

#front and back panel channels
frontBack = [74, 75]

#straight line paths
straightPaths = [[[0, 1], [16, 17], [32, 33], [48, 49]], 
                [[4, 5], [20, 21], [36, 37], [52, 53]], 
                [[2, 3], [18, 19], [34, 35], [50, 51]],
                [[6, 7], [22, 23], [38, 39], [54, 55]], 
                #[[8, 9], [24, 25], [40, 41], [56, 57]],
                [[8, 9], [78, 79], [40, 41], [56, 57]],
                [[12, 13], [28, 29], [44, 45], [60, 61]],
                [[10, 11], [26, 27], [42, 43], [58, 59]],
                [[14, 15], [30, 31], [46, 47], [62, 63]]]

#inputs to read in through uproot
uprootInputs = ["event", "fileNumber", "time", "nPE", "height", "area", "chan", "row", "column", "layer", "type", "event_time_fromTDC", "tTrigger", "duration"]

#list of online trigger names to search for
offlineTrigNames = ['fourLayers', 'threeInRow', 'separateLayers', 'adjacentLayers', 'nLayers', 'nHits', 'topPanels', 'topBotPanels', 'frontBack']

#list of offline trigger names to search for
offlineTrigArray = [['fourLayers', 0], ['threeInRow', 1], ['separateLayers', 2], ['adjacentLayers', 3], ['nLayers', 4], ['nHits', 6], 
                    ['topPanels', 8], ['topBotPanels', 9], ['frontBack', 10]]

#list of separate layer combinations
separateCombos = [[0, 2], [0, 3], [1, 3]]

#list of adjacent layer combinations
adjacentCombos = [[0, 1], [1, 2], [2, 3]]

pedestalCorrections = [0.1, -0.4, 0.4, 1.2, 0.5, -0.1, 0.8, -0.4, 0.6, 0.2, 0.7, -0.2, 1.1, 0.3, 0.2, -0.2, 5.8, -0.2, 0.0, 0.6, 0.1, 0.0, 0.1, 0.2, 0.0, 0.2, -0.2, 0.0, 0.0, -0.2, 0.1, 0.0, 0.5, 0.3, 0.1, 0.0, 0.2, -0.3, -0.1, 0.2, -0.2, -0.3, 0.7, 0.1, 0.6, 0.1, 0.1, 0.0, 0.7, 1.0, 0.5, -1.9, 1.0, 1.0, -1.1, -0.1, -0.1, -0.6, 0.1, -1.2, 0.6, -0.5, 0.0, 0.1, -0.5, -0.2, 0.6, 0.1, 0.5, -2.3, -0.2, 0.2, -0.3, -2.0, -5.3, -7.8, 0.8, -0.3, 0.1, 0.3]


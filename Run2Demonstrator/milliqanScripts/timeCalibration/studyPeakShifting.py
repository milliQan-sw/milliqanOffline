import pickle 

triplePeakDict = "triplePeakStudy_interModuleUpThresh/triplePeakDictInterLayer.pkl"

triplePeakDict = pickle.load(open(triplePeakDict))

modulelayers = [(4,5,6,7),(8,9,10,11)]
scenarios = [("cosmic","cosmic"),("rad","cosmic"),("cosmic","rad")]
outputDict = {}
for scenario in scenarios:
    for layer,modules in enumerate(modulelayers):

        meanMean = 0
        weightMean = 0
        for module in modules:
            meanInfo = triplePeakDict[tuple([module]+list(scenario))]
            meanMean += meanInfo[0]/meanInfo[1]**2
            weightMean += 1./meanInfo[1]**2
        meanMean /= weightMean
        outputDict[layer+2,scenario] = meanMean

print 3, "rad,cosmic shift", outputDict[3,("rad","cosmic")] - outputDict[3,("cosmic","cosmic")]
print 3, "cosmic,rad shift", outputDict[3,("cosmic","rad")] - outputDict[3,("cosmic","cosmic")]
print 2, "rad,cosmic shift", outputDict[2,("rad","cosmic")] - outputDict[2,("cosmic","cosmic")]
print 2, "cosmic,rad shift", outputDict[2,("cosmic","rad")] - outputDict[2,("cosmic","cosmic")]

import pickle
from collections import defaultdict

closureDict = pickle.load(open("outputIntercalibration_closure100/calibrationDictClosure.pkl"))
variances = defaultdict(list)
variances[11].append(0.5*(closureDict[11,10][2]**2 - closureDict[10,9][2]**2 + closureDict[11,9][2]**2))
variances[11].append(0.5*(closureDict[11,10][2]**2 - closureDict[10,8][2]**2 + closureDict[11,8][2]**2))
variances[11].append(0.5*(closureDict[11,9][2]**2 - closureDict[9,8][2]**2 + closureDict[11,8][2]**2))

variances[10].append(0.5*(closureDict[11,10][2]**2 - closureDict[11,9][2]**2 + closureDict[10,9][2]**2))
variances[10].append(0.5*(closureDict[11,10][2]**2 - closureDict[11,8][2]**2 + closureDict[10,8][2]**2))
variances[10].append(0.5*(closureDict[10,9][2]**2 - closureDict[9,8][2]**2 + closureDict[10,8][2]**2))

variances[9].append(0.5*(closureDict[11,9][2]**2 - closureDict[11,10][2]**2 + closureDict[10,9][2]**2))
variances[9].append(0.5*(closureDict[11,9][2]**2 - closureDict[11,8][2]**2 + closureDict[9,8][2]**2))
variances[9].append(0.5*(closureDict[10,9][2]**2 - closureDict[10,8][2]**2 + closureDict[9,8][2]**2))

variances[8].append(0.5*(closureDict[11,8][2]**2 - closureDict[11,10][2]**2 + closureDict[10,8][2]**2))
variances[8].append(0.5*(closureDict[11,8][2]**2 - closureDict[11,9][2]**2 + closureDict[9,8][2]**2))
variances[8].append(0.5*(closureDict[10,8][2]**2 - closureDict[10,9][2]**2 + closureDict[9,8][2]**2))

variances[7].append(0.5*(closureDict[7,6][2]**2 - closureDict[6,5][2]**2 + closureDict[7,5][2]**2))
variances[7].append(0.5*(closureDict[7,6][2]**2 - closureDict[6,4][2]**2 + closureDict[7,4][2]**2))
variances[7].append(0.5*(closureDict[7,5][2]**2 - closureDict[5,4][2]**2 + closureDict[7,4][2]**2))

variances[6].append(0.5*(closureDict[7,6][2]**2 - closureDict[7,5][2]**2 + closureDict[6,5][2]**2))
variances[6].append(0.5*(closureDict[7,6][2]**2 - closureDict[7,4][2]**2 + closureDict[6,4][2]**2))
variances[6].append(0.5*(closureDict[6,5][2]**2 - closureDict[5,4][2]**2 + closureDict[6,4][2]**2))

variances[5].append(0.5*(closureDict[7,5][2]**2 - closureDict[7,6][2]**2 + closureDict[6,5][2]**2))
variances[5].append(0.5*(closureDict[7,5][2]**2 - closureDict[7,4][2]**2 + closureDict[5,4][2]**2))
variances[5].append(0.5*(closureDict[6,5][2]**2 - closureDict[6,4][2]**2 + closureDict[5,4][2]**2))

variances[4].append(0.5*(closureDict[7,4][2]**2 - closureDict[7,6][2]**2 + closureDict[6,4][2]**2))
variances[4].append(0.5*(closureDict[7,4][2]**2 - closureDict[7,5][2]**2 + closureDict[5,4][2]**2))
variances[4].append(0.5*(closureDict[6,4][2]**2 - closureDict[6,5][2]**2 + closureDict[5,4][2]**2))

variances[3].append(0.5*(closureDict[3,2][2]**2 - closureDict[2,1][2]**2 + closureDict[3,1][2]**2))
variances[2].append(0.5*(closureDict[3,2][2]**2 - closureDict[3,1][2]**2 + closureDict[2,1][2]**2))
variances[1].append(0.5*(closureDict[3,1][2]**2 - closureDict[3,2][2]**2 + closureDict[2,1][2]**2))
ET = [7,3,2,1]
R878 = [6,5,4]
R7725 = [11,10,9,8]
ETMean = 0
ETN = 0
R878Mean = 0
R878N = 0
R7725Mean  = 0
R7725N = 0
for i in range(1,12):
    print i
    for var in variances[i]:
        if var < 0: continue
        print var**0.5
        if i in ET:
            ETMean += var**0.5
            ETN +=1
        if i in R878:
            R878Mean += var**0.5
            R878N +=1
        if i in R7725:
            R7725Mean += var**0.5
            R7725N +=1
print
print "mean ET:",ETMean/ETN
print "mean R878:",R878Mean/R878N
print "mean R7725:",R7725Mean/R7725N
    #     if var > 0:
    #         print var**0.5
    # print "****"

    

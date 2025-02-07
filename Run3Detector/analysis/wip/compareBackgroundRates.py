import matplotlib.pyplot as plt
import math

#number of passing events and total time of runs from running backgroundPlots.py script
info = {1200: [34847.0, 1046425.0], 1300: [97827.0, 3062278.0], 1400: [144143.0, 4520195.0], 1500: [63524.0, 1977118.0], 1600: [64504.0, 1898334.0], 1700: [29271.0, 894174.0]}

if __name__ == "__main__":

    #add the rates to the info

    for k, v in info.items():
        print(k, v)
        info[k].append(v[0]/v[1])
    
    print(info)
    print(info.keys(), info.values())

    errors = []
    rates = []
    for k, v in info.items():
        #err = math.sqrt(v[0]) / v[1]
        err = v[0] / v[1] * math.sqrt(1/v[0] + 1/v[1])
        errors.append(err)

        rate = v[0] / v[1]
        rates.append(rate)

    print(errors)

    #plt.scatter(info.keys(), [x[2] for x in info.values()], color='blue', marker='o')
    plt.errorbar(info.keys(), rates, yerr=errors, color='blue', marker='o')
    plt.ylim(0.02, 0.04)
    plt.xlabel('Runs')
    plt.ylabel('Rate (events/time(s))')
    plt.title('4 Pulses in Line Rate')
    plt.savefig('plots/backgroundRatesVsRuns.png')

    totalCounts = 0
    totalTime = 0
    for key, value in info.items():
        totalTime += value[1]
        totalCounts += value[0]

    print("total rate: ", totalCounts/totalTime)

    

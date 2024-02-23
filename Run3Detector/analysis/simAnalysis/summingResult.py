import os

event_sums = {}

"""
input_files = []

directory= "/net/cms26/cms26r0/zheng/barSimulation/withPhotonAnalysis/newFlatResult/"
#base_name = "WPIndividual" #old counting come with NPE > 0
#base_name = "WPIndividual_new"
base_name = "withOutPhotonCutresult"
#base_name = "special_new"


for filename in os.listdir(directory):
    if filename.startswith(base_name) and filename.endswith(".txt"):
        input_files.append(directory+filename)
"""
input_files = ["/home/czheng/scratch0/sim_uproot/milliqanOffline/Run3Detector/analysis/utilities/output.txt"]

interestFile = list()

#print(input_files)
files = 0
for filepath in input_files:
    if not os.path.exists(filepath):
        continue
    interestFile.append(filepath)
    with open(filepath, 'r') as file:
        lines = file.readlines()
        files += 1
        for line in lines:
            if ':' in line:
                parts = line.split(':')

                
                event = parts[0]
                if "event" in event : continue
                if event == "MilliQan Scheduler" or event == "found it! run number": continue
                
                #print(event)
                
                count = int(parts[1])
                #print(count)
                #count = int(count.strip())
                # update the count in the dictionary
                if event in event_sums:
                    event_sums[event] += count
                else:
                    event_sums[event] = count

print(len(interestFile))      
for event, count in event_sums.items():
    print(f"{event}: {count}")

#print(files)

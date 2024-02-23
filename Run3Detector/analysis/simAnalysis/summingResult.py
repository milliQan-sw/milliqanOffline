import os

event_sums = {}

input_files = ["/share/scratch0/czheng/SIManalysisDEV/milliqanOffline/Run3Detector/analysis/simAnalysis/withPhotonResultSim.txt"]

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

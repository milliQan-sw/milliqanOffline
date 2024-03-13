#this file is made for doing the cut efficiency analysis for study the cosmic muon tagging algorism

import os

event_sums = {}

input_files = []

directory= "/home/czheng/SimCosmicFlatTree/cutEffcheckOffline/"

base_name = "Run1163"

for filename in os.listdir(directory):
    if filename.startswith(base_name) and filename.endswith("Flow3.txt"):
        input_files.append(directory+filename)

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

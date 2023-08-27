import json 

#Read in the Channel_Calibrations json to obtain the corrections from the previous stage
Previous_stage = {}

with open('Channel_Calibrations.json', 'r') as filename:
	json_data = json.load(filename)
	for key in json_data:
		Previous_stage[key] = []
		for item in json_data[key]:
			Previous_stage[key].append(item)

print(Previous_stage)

#Use the leading channels to fill lists containing all the channels in a given layer
Lead1 = [0, 1, 4, 5]
Lead2 = [16, 17, 20, 21]
Lead3 = [32, 33, 36, 37]
Lead4 = [48, 49, 52, 53]
Leads = [Lead1, Lead2, Lead3, Lead4]

Layers = {'Layer1': [], 'Layer2': [], 'Layer3':[], 'Layer4':[]}
Keys = [key for key in Layers.keys()]
print(Keys)
#Populate the dictionary with relevant channels
for idx in range(4):
	Lead = Leads[idx]
	key = Keys[idx]
	for lead in Lead:
		if lead!=16 and lead!=17:
			Layers[key].append(lead)
			Layers[key].append(lead+2)
			Layers[key].append(lead+8)
			Layers[key].append(lead+10)
		elif lead==16 or lead==17:
			Layers[key].append(lead)
			Layers[key].append(lead+2)
			Layers[key].append(lead+8)
			Layers[key].append(lead+8+54)
			Layers[key].append(lead+10)
print(Layers)

#Layer corrections to the first layer defined below and are in ascending order of layer

Corrections = [-10.881096971880945, 2.8-10.881096971880945, 18.7-10.881096971880945, 25.9-10.881096971880945]


for key in Keys:
	print(f'Looking at {key}')
	channels = Layers[key]
	Correct = Corrections[Keys.index(key)]
	for chan in channels:
		Previous_stage['timing'][chan]+=Correct
print(f' Corrections for SUBTRACTING: {Previous_stage}')

for idx in range(len(Previous_stage['timing'])):
	if Previous_stage['timing'][idx]!=0:
		Previous_stage['timing'][idx]=-1*Previous_stage['timing'][idx]

Previous_stage['timing'][75]+=-17.4

print(f'Corrections for ADDING: {Previous_stage}')

with open('Final_Calibrations.json', 'w') as filename:
	json.dump(Previous_stage, filename)

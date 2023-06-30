import ROOT as r

treeChain = r.TChain('t')
treeChain.Add('/store/user/milliqan/trees/v31/MilliQan_Run1046.*_v31_firstPedestals.root')
num=treeChain.GetEntries() 
print("total evnets:" + str(num))
EV=9320
print("events is " + str(EV))
# checking data
#"""

def listConvertion(list):
        List1 = []
        for item in list:
            List1.append(item)
        return List1
for ievent, event in enumerate(treeChain):
    if event.DAQEventNumber == EV:
        layer_list = listConvertion(event.layer)
        time_list =listConvertion(event.timeFit)
        height_list = listConvertion(event.height)

        sorted_time_list = sorted(enumerate(time_list), key=lambda x: x[1])
        sorted_E_list = list()
        sorted_layer_list = list()
        sorted_E_list = list()
        new_time_list = list()
        for index, time in sorted_time_list:
            new_time_list.append(time)
            sorted_layer_list.append(layer_list[index])
            sorted_E_list.append(height_list[index])
        
        print("time:"+str(new_time_list))
        print("layer"+str(sorted_layer_list))
        print("E: " + str(sorted_E_list))




#"""
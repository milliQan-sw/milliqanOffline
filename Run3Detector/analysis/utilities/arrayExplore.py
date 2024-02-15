import awkward as ak
import uproot 
import numpy as np
import array

"""
python_dicts = [
    {"x": 1, "y": 1.1, "z": "one"}
]
"""

#python_dicts=[{'dummy': array([array([0], dtype=int)])}]
"""
python_dicts={'height': [1.27e+03, 1.27e+03]}

awkward_array = ak.Array(python_dicts)
awkward_array["f"] = "junk"
print(awkward_array['height']/10)
print(awkward_array)

python_dicts=[{'height': [1.27e+03, 1.27e+03]},{'height': [1.27e+03, 1.27e+03]}]
run_dicts = [{'runNumber': [1]},{'runNumber': [1]}]
awkward_array = ak.Array(python_dicts)
array2 = ak.Array(run_dicts)
print(ak.broadcast_arrays(5,[1, 2, 3, 4, 5]))
print(ak.broadcast_arrays(array2.runNumber,awkward_array.height))
"""
#upfile = uproot.open("/mnt/hadoop/se/store/user/milliqan/trees/v34/MilliQan_Run1190.4_v34.root") #load the root file
#uptree = upfile["t"]

#branches = uptree.arrays(["runNumber","height", "area","type"], cut="height >= 500", entry_stop=3) #Crash when using non-pulse based branches
#print(branches[:3])

#print(ak.to_pandas(branches))
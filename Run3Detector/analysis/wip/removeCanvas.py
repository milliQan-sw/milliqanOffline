import ROOT

# Open the ROOT file in "UPDATE" mode
root_file = ROOT.TFile("run1024_TimeFitdistributionEX1Hit.root", "UPDATE")

# Get the list of objects (including canvases) in the ROOT file
root_file_objects = root_file.GetListOfKeys()

# Loop through the list of objects to find and remove canvases
for obj in root_file_objects:
    obj_name = obj.GetName()
    print(obj_name)

    obj_class = obj.GetClassName()
    print(obj_class)

    # Check if the object is a TCanvas
    if obj_class == "TCanvas":
        # Remove the canvas
        print(obj_name)
        root_file.Delete(obj_name + ";*")

# Save and close the modified ROOT file
root_file.Write()
root_file.Close()
import ROOT
from ROOT import TFile, TTree, TChain
import numpy as np

def my_looper(input_files, out_file):
    # Create a TChain from the input files
    fChain = TChain("tree")  # Replace "tree" with the actual tree name
    for file in input_files:
        fChain.Add(file)

    # Ensure the input chain is valid
    if fChain.GetEntries() == 0:
        print("No entries in the input chain.")
        return

    # Open the output ROOT file
    foutput = TFile(out_file, "recreate")

    # Create an output tree by cloning the input tree structure
    tout = fChain.CloneTree(0)

    # Open a text file in append mode to log results
    with open("skim_results.txt", "a") as output_text_file:
        # Minimum area threshold
        min_area = 500000

        # Get the number of entries in the chain
        nentries = fChain.GetEntries()
        passed = 0  # Counter for events passing the selection

        # Loop through each entry
        for jentry in range(nentries):
            if jentry % 1000 == 0:
                print(f"Processing entry {jentry}/{nentries}")

            # Load the entry
            fChain.GetEntry(jentry)

            # Retrieve the variables from the tree
            chan = np.array(fChain.chan)
            area = np.array(fChain.area)
            layer = np.array(fChain.layer)
            row = np.array(fChain.row)
            type_ = np.array(fChain.type)

            # Sanity check: Ensure `chan` and `area` vectors have the same size
            if len(chan) != len(area):
                print(f"Mismatch in sizes of chan and area vectors at entry {jentry}")
                continue

            # Analyze the event
            hits_by_layer_and_row = {}

            # Loop over all channels in the event
            for k in range(len(chan)):
                if area[k] > min_area and type_[k] == 0:
                    layer_id = layer[k]
                    row_id = row[k]
                    if layer_id not in hits_by_layer_and_row:
                        hits_by_layer_and_row[layer_id] = set()
                    hits_by_layer_and_row[layer_id].add(row_id)

            # Check if any layer has hits in more than 3 rows
            valid_event = any(len(rows) > 3 for rows in hits_by_layer_and_row.values())

            # Save the event to the output tree if the condition is met
            if valid_event:
                tout.Fill()
                passed += 1

        # Write the output tree to the file
        foutput.WriteTObject(tout)
        foutput.Close()

        # Calculate and log the fraction of events that passed the selection
        frac = passed / nentries
        output_text_file.write(f"Output file contains {passed} events\n")
        output_text_file.write(f"Input file contains {nentries} events\n")
        output_text_file.write(f"Fraction of passed events: {frac:.5f}\n\n")

    print("Processing completed.")
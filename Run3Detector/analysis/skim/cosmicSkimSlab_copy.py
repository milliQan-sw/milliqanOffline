import ROOT

def loop(chain, outFile, lumi, runTime):
    # Check that the input tree/chain exists
    if not chain:
        return

    # Open the output file
    foutput = ROOT.TFile.Open(outFile, "recreate")
    if not foutput or foutput.IsZombie():
        print("Could not create output file")
        return

    # Create TNamed objects to store luminosity and runtime info
    t_lumi = ROOT.TNamed("luminosity", lumi)
    t_time = ROOT.TNamed("runTime", runTime)

    # Clone the tree structure (but not the events yet)
    tout = chain.CloneTree(0)

    # Open a text file in append mode to log results
    with open("skim_results.txt", "a") as outputTextFile:
        # Set the minimum area requirement
        minArea = 100000.0

        # Get the total number of entries
        nentries = chain.GetEntriesFast()
        passed = 0

        for jentry in range(nentries):
            # Load the tree entry (safety check)
            ientry = chain.LoadTree(jentry)
            if ientry < 0:
                break
            chain.GetEntry(jentry)

            # Provide feedback every 1000 events
            if jentry % 1000 == 0:
                print("Processing {}/{}".format(jentry, nentries))

            # Sanity check (assuming 'chan' and 'area' are arrays or vectors)
            if len(chain.chan) != len(chain.area):
                print("Different sizes in 'chan' and 'area' for entry {}".format(jentry))

            # Initialize a 3D list to record slab hits: dimensions 4 layers x 4 rows x 3 columns.
            slabHit = [[[False for _ in range(3)] for _ in range(4)] for _ in range(4)]

            # Loop over hits in the event
            for k in range(len(chain.chan)):
                # Apply the standard cuts
                if chain.pickupFlagTight[k]:
                    continue
                if chain.boardsMatched[k]:
                    continue
                if chain.ipulse[k] != 0:
                    continue
                if chain.timeFit_module_calibrated[k] < 900 or chain.timeFit_module_calibrated[k] > 1500:
                    continue
                if chain.area[k] < minArea:
                    continue

                # Get the offline channel number for this hit
                ch = chain.chan[k]

                # Determine the layer from the channel number.
                # Channels 0-23: Layer 0, 24-47: Layer 1, 48-71: Layer 2, 72-95: Layer 3.
                layer = ch // 24  # integer division in Python
                if layer < 0 or layer > 3:
                    continue  # safety check

                # Determine the channel number within the layer.
                ch_in_layer = ch % 24

                # Determine the column:
                # ch_in_layer in [0,7] -> column 2, [8,15] -> column 1, [16,23] -> column 0.
                if ch_in_layer < 8:
                    col = 2
                elif ch_in_layer < 16:
                    col = 1
                else:
                    col = 0

                # Determine the row:
                # For each column block of 8 channels, row = 3 - ((ch_in_layer % 8) // 2)
                row = 3 - ((ch_in_layer % 8) // 2)

                # Mark this slab as hit in the given layer.
                slabHit[layer][row][col] = True

            # Now, for each slab position (row, col), count how many layers are hit.
            straightLineEvent = False
            for r in range(4):
                if straightLineEvent:
                    break
                for c in range(3):
                    layersHit = sum(1 for l in range(4) if slabHit[l][r][c])
                    # Require the slab to be hit in at least 3 layers.
                    if layersHit >= 3:
                        straightLineEvent = True
                        break

            # Fill the event only if the straight-line cut is satisfied.
            if straightLineEvent:
                tout.Fill()
                passed += 1

        # Write the output tree and additional objects to the ROOT file
        foutput.WriteTObject(tout)
        t_lumi.Write()
        t_time.Write()
        # In Python, deleting the object is optional; we simply close the file.
        foutput.Close()

        # Write summary information to the text file
        frac = (passed / nentries) if nentries > 0 else 0.0
        outputTextFile.write("Output file has    {} events\n".format(passed))
        outputTextFile.write("Input  file has    {} events\n".format(nentries))
        outputTextFile.write("Fraction of passed {:.5f}\n".format(frac))
        outputTextFile.write("\n")

if __name__ == "__main__":
    # Example usage:
    # Create a TChain and add input files.
    chain = ROOT.TChain("treeName")  # Replace "treeName" with your actual tree name.
    chain.Add("inputFile.root")       # Replace with your actual input ROOT file.

    # Call the loop function with the output filename, luminosity, and runtime information.
    loop(chain, "output.root", "lumi_value", "run_time_value")
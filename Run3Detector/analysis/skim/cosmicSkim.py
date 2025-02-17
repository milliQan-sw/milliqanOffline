import ROOT
import sys
import math
from array import array

def Loop(fChain, outFile, lumi, runTime):
    # Check that the input tree/chain exists
    if not fChain:
        print("fChain is not defined")
        return

    # Create the output file
    foutput = ROOT.TFile.Open(outFile, "RECREATE")
    if not foutput or foutput.IsZombie():
        print("Could not create output file")
        return

    # Create TNamed objects to store luminosity and runtime info
    t_lumi = ROOT.TNamed("luminosity", lumi)
    t_time = ROOT.TNamed("runTime", runTime)

    # Clone the tree structure (but not the events yet)
    tout = fChain.CloneTree(0)

    # Open a text file in append mode to log results
    textFileName = "skim_results.txt"
    outputTextFile = open(textFileName, "a")

    # Set the minimum area requirement
    minArea = 100000.

    # Get the total number of entries
    nentries = fChain.GetEntriesFast()
    passed = 0

    # Loop over entries in the tree
    for jentry in range(nentries):
        # Load the jentry-th entry
        ientry = fChain.LoadTree(jentry)
        if ientry < 0:
            break

        nb = fChain.GetEntry(jentry)

        # Provide feedback every 1000 entries
        if jentry % 1000 == 0:
            print("Processing {}/{}".format(jentry, nentries))

        # --- Sanity Check ---
        # We assume that 'chan' and 'area' are branches that are vectors.
        # Adjust the branch names as needed.
        if fChain.chan.size() != fChain.area.size():
            print("Different sizes in 'chan' and 'area' for entry", jentry)

        # Create a 16x4 array (list of lists) to track hit paths
        straightPathsHit = [[False for _ in range(4)] for _ in range(16)]

        # Flags for front and back panel hits
        frontPanelHit = False
        backPanelHit = False

        # Loop over the elements in the event (assuming vector branches)
        nElements = fChain.chan.size()
        for k in range(nElements):
            # Check the type branch
            if fChain.type.at(k) == 2:
                if fChain.layer.at(k) == 0:
                    frontPanelHit = True
                if fChain.layer.at(k) == 2:
                    backPanelHit = True

            # Apply a series of cuts
            if fChain.pickupFlagTight.at(k):
                continue
            if fChain.type.at(k) != 0:
                continue
            if fChain.ipulse.at(k) != 0:
                continue
            time_val = fChain.timeFit_module_calibrated.at(k)
            if time_val < 900 or time_val > 1500:
                continue
            if fChain.height.at(k) < 15:
                continue
            if fChain.area.at(k) < minArea:
                continue

            # Determine index based on layer and column
            index = fChain.layer.at(k) * 4 + fChain.column.at(k)
            row = fChain.row.at(k)
            # Mark that the straight path (at given index and row) has been hit
            straightPathsHit[index][row] = True

        # Check if the event qualifies by having at least 3 hits in any allowed path
        straightLineEvent = False
        for i in range(16):
            # Only check the corresponding panel if it was hit
            if i < 8 and not frontPanelHit:
                continue
            if i >= 8 and not backPanelHit:
                continue

            # Count the number of hit rows in this straight path
            straightPathCount = 0
            for j in range(4):
                if straightPathsHit[i][j]:
                    straightPathCount += 1
                if straightPathCount >= 3:
                    straightLineEvent = True
                    break
            if straightLineEvent:
                break

        # If the event passes the straight-line criteria, fill the output tree
        if straightLineEvent:
            tout.Fill()
            passed += 1

    # Write the output tree and additional objects to the ROOT file
    foutput.WriteTObject(tout)
    t_lumi.Write()
    t_time.Write()
    foutput.Close()

    # Write summary information to the text file
    frac = float(passed) / nentries if nentries > 0 else 0
    outputTextFile.write("Output file has    {} events\n".format(passed))
    outputTextFile.write("Input  file has    {} events\n".format(nentries))
    outputTextFile.write("Fraction of passed {:.5f}\n".format(frac))
    outputTextFile.write("\n")
    outputTextFile.close()

# Example usage:
if __name__ == "__main__":
    # Create a TChain and add input ROOT files (adjust the tree name and file names as needed)
    chain = ROOT.TChain("t")
    chain.Add("SomeOtherRun.root")
    chain.Add("YetAnotherRun.root")

    # Call the Loop function with desired parameters
    Loop(chain, "outfile.root", "35.9", "3600")

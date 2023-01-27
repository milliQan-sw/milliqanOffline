import ROOT as r

# Create Data Class
class DataHandler():

    # Create TChain with all data you will need for your analysis
    # wildcards can be used in datapath
    def initializeData(self, datapath):
       treeChain = r.TChain('t')
       treeChain.Add(datapath)
       return treeChain


    # Print out certain datafile statistics
    def viewData(self):
        return

    def npeCut(self):
        data = self.initializeData('/store/user/mcarrigan/trees/v29/MilliQan_Run591.*_v29_firstPedestals.root')
        for event in data:
            # nPE is not an integer, the README file in the github says the number of photons is approximate though
            # There are also negative numbers?
            nPEratio = max(event.nPE)/min(event.nPE)
            if nPEratio > 10:
                continue
            print(nPEratio)

if __name__ == "__main__":
    data = DataHandler()
    data.npeCut()

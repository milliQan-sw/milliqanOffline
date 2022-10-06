import ROOT as r
r.gROOT.SetBatch()

def TurnOn_f1(x, par):
    halfpoint = par[0];
    slope = par[1];
    plateau = par[2];
    offset = 0.;
    pt = r.TMath.Max(x[0],0.000001);
    arg = 0;
    arg = (pt - halfpoint)/(r.TMath.Sqrt(2)*slope);
    fitval = offset+0.5*plateau*(1+r.TMath.Erf(arg));
    return fitval;

def readFitFunctions():
    f1 = r.TFile("fitFunctions.root")
    outputFile = r.TFile("fitFunctionsReadable","RECREATE")
    fitFuncs = {}
    for key in f1.GetListOfKeys():
        if "16" not in key.GetName() and "17" not in key.GetName() and "TC" not in key.GetName(): continue
        raw_f = key.ReadObj()
        f = r.TF1(raw_f.GetName(), TurnOn_f1, raw_f.GetXmin(), raw_f.GetXmax(), 3 )
        f.SetParameters( raw_f.GetParameter(0), raw_f.GetParameter(1), 1)#raw_f.GetParameter(2) )
        chan = int(key.GetName().split("_")[1].replace("CH",""))
        fitFuncs[chan] = f
    return fitFuncs

if __name__ == "__main__":
    readFitFunctions()


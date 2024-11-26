import ROOT as r


#create tchain of files to use
mychain = r.TChain('t')
mychain.Add('/store/user/milliqan/trees/v35/bar/1700/MilliQan_Run1720.*_v35.root')

#using draw statement to make selections and save to histogram called h1
#selections on 
#   1. channel
#   2. riseSamples >= 3
#   3. fallSamples >= 3
#   4. !pickupFlagTight (pickupFlagTight is false)
mychain.Draw("area>>h1(200, 0, 400e3)", "chan==10 && riseSamples >=3 && fallSamples >= 3 && !pickupFlagTight")

#create TCanvas to draw
c1 = r.TCanvas("c1", "c1", 800, 600)

#set limits for fitting
x_min = 50e3
x_max = 500e3

#create fit function, landau + gaussian
f1 = r.TF1("f1", 'landau + [3]*exp(-0.5*((x-[4])/[5])^2)')

#set low and high parameters for fit function
limits_lo = [1.0e4, -1.0e4, 1.0e1, 1.0e1, 1.0e4, 3.0e4]
limits_hi = [1.0e7, 1.0e1, 1.0e3, 2.0e1, 1.0e6, 5.0e4]
for i in range(6):
    f1.SetParLimits(i, limits_lo[i], limits_hi[i])

#set initial parameters for fit function
f1.SetParameters(5.8e6, -7e3, 1.0e2, 1.3e1, 1.6e5, 4.4e4)

#get histogram from directory (because we made it with draw statement)
h1 = r.gDirectory.Get('h1')
h1.Draw()

#fit histogram with our fit function between x limits
fit_out = h1.Fit(f1,  "S", "", x_min, x_max)

#draw everything to canvas
c1.Draw()
c1.SetLogy()

#get chi2 and degrees of freedom
chi2 = fit_out.Chi2()
ndof = fit_out.Ndf()

print("Chi 2 {}, NDOF {}, fit {}".format(chi2, ndof, chi2/ndof))

# Draw text on the canvas
text = r.TText()
text.SetTextSize(0.04)  # Set text size
text.SetTextColor(r.kRed)  # Set text color
text.DrawText(100e3, 100, "Gaussian mean: {}, Fit chi2/ndof {}".format(round(f1.GetParameter(4), 2), round(chi2/ndof, 2)))

#write output to root file
fout = r.TFile.Open("fitOutput.root", 'recreate')

fout.cd()

c1.Write()
h1.Write()

fout.Close()
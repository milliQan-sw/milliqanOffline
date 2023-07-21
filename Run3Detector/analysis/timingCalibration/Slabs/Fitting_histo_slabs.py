import ROOT as r

#set the X errors to zero

r.gStyle.SetErrorX(0)

#enforce current style choices

r.gROOT.ForceStyle()

#Point to the root file hist

TimeDiffHisto = r.TFile.Open('Cosmic_TimeDiffHisto_Slabs.root', 'READ')

hist = TimeDiffHisto.Get('t[75-71]')

#Defining a double Gaussian Function

#DGauss = "[0]*exp(-0.5*((x-[1])/[2])^2) +[3]*exp(-0.5*((x-[4])/[5])^2)"

#Define the fitting range

gaussFit = r.TF1('gaussfit', 'gaus', -32, 40)

gaussFit.SetParameters(178, 15, 2, 30, -5, 3)

#make a canvas

canvas = r.TCanvas()

#Make canvas follow style set above

canvas.UseCurrentStyle()

#use the defined canvas

canvas.cd()

#stylize the plot

hist.SetStats(0)

hist.GetYaxis().SetTitle('Counts')

hist.GetXaxis().SetTitle('\Delta t [ns]')

hist.SetMarkerStyle(20)

hist.SetLineWidth(3)

#Fitting the hist with Log likelihood

hist.Fit(gaussFit, 'L')

#Hist will have only Poisson errors; bars have caps at the end

hist.DrawCopy('e1')

#Getting the normalized Chi-square and the parameters

pval = gaussFit.GetProb()

mean1 = gaussFit.GetParameter(1)

#mean2 = gaussFit.GetParameter(4)

std1 = gaussFit.GetParameter(2)

#std2 = gaussFit.GetParameter(5)

#Setting up legends and labels

legend = r.TLegend(0.2, 0.75,0.35, 0.8)

legend.SetTextSize(0.03)

legend.AddEntry(hist, 'Data')

legend.AddEntry(gaussFit, 'Fit')

legend.SetLineWidth(0)

legend.Draw('same')

latex = r.TLatex()

latex.SetNDC()

latex.SetTextSize(0.03)

latex.DrawText(0.55, 0.50,"t(Cosmic) = %.1f ns"%(mean1))

latex.DrawText(0.55, 0.45,"sigma(Cosmic) = %.1f ns"%(std1))

latex.DrawText(0.55, 0.40,"p = %.4f"%(pval))

latex.DrawText(0.55, 0.8, 'MilliQan 2023')

latex.DrawText(0.55, 0.75, 'Muon Events')

#Saving the Plot
canvas.SaveAs('Cosmic_TimingFit_slabs_Likelihood.png')

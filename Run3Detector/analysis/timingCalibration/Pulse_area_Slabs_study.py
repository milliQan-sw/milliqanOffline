import ROOT as r

#set the file paths

path = '/net/cms26/cms26r0/milliqan/outputRun3Hadd/v32/'

#collect the Runs and point to their location; add them to a defined chain

chain = r.TChain('t')

Run_nums = ['1006', '1031', '1032', '1035', '1038', '1039']

Runs = []

for num in Run_nums:
	Run = path+f'MilliQan_Run{num}_default_v32.root'

	Runs.append(Run)
	
	print(f'Successfully added Run {num} to the chain')

for run in Runs:
	chain.Add(run)

df = r.RDataFrame(chain)

#Require saturation of the slabs by a triggering pulse


through = df.Filter('Sum(chan==71&&ipulse==0)').Filter('Sum(chan==75&&ipulse==0)').Filter('Sum(height[chan==71&&ipulse==0]>1000&&height[chan==75&&ipulse==0]>1000)')

Bar_Req = through.Filter('Sum(row==0&&ipulse==0)&&Sum(row==1&&ipulse==0)&&Sum(row==2&&ipulse==0)&&Sum(row==3&&ipulse==0)')

AreaChan71 = through.Define('areaChan71', 'area[chan==71&&ipulse==0]')


AreaChan75 = through.Define('areaChan75', 'area[chan==75&&ipulse==0]')

AreaChan71BarReq = Bar_Req.Define('areaChan71BarReq', 'area[chan==71&&ipulse==0]')


AreaChan75BarReq = Bar_Req.Define('areaChan75BarReq', 'area[chan==75&&ipulse==0]')

#make histos

AreaChan71Histo = AreaChan71.Histo1D(('Area(Chan=71)', 'Effect of Bar Requirement on Pulse Area Distribution; mV ns', 50, 50.e3,600.e3), 'areaChan71')


AreaChan75Histo = AreaChan75.Histo1D(('Area(Chan=75)', 'Effect of Bar Requirement on Pulse Area Distribution; mV ns', 50, 50.e3, 600.e3), 'areaChan75')

AreaChan71BarHist = AreaChan71BarReq.Histo1D(('Area(Chan=71&Bar_hit)', 'Effect of  Bar Requirement on Pulse Area Distribution; mV ns', 50, 50.e3, 600.e3), 'areaChan71BarReq')


AreaChan75BarHist = AreaChan75BarReq.Histo1D(('Area(Chan=75&Bar_hit)', 'Effect of Bar Requirement on Pulse Area Distribution; mV ns', 50, 50.e3, 600.e3), 'areaChan75BarReq')

#Make Canvas and set y axis to log scale

Canvas = r.TCanvas()

Canvas.cd()

r.gPad.SetLogy()

#Set the line color

AreaChan71Histo.SetLineColor(r.kRed)

AreaChan75Histo.SetLineColor(r.kBlack)

AreaChan71BarHist.SetLineColor(r.kBlue)

AreaChan75BarHist.SetLineColor(r.kGreen)

#set the axes

AreaChan71Histo.GetYaxis().SetTitle('Number of Events')

AreaChan71Histo.GetXaxis().SetTitle('Pulse Area [mV ns]')

#Remove the stats box

AreaChan71Histo.SetStats(0)

AreaChan75Histo.SetStats(0)

AreaChan71BarHist.SetStats(0)

AreaChan75BarHist.SetStats(0)

# Draw the plots

AreaChan71Histo.Draw()

AreaChan75Histo.Draw('same')

AreaChan71BarHist.Draw('same')

AreaChan75BarHist.Draw('same')

#Make legend

legend=r.TLegend(0.7,0.6,0.85,0.75) 

legend.AddEntry(AreaChan71Histo.GetPtr() ,"Chan 71") 

legend.AddEntry(AreaChan75Histo.GetPtr() ,"Chan 75") 

legend.AddEntry(AreaChan71BarHist.GetPtr() ,"Chan 71 w/ Bar hit") 

legend.AddEntry(AreaChan75BarHist.GetPtr() ,"Chan 75 w/ Bar hit") 

legend.SetLineWidth(0) 

legend.Draw("same")

latex = r.TLatex()

latex.SetNDC()

latex.SetTextSize(0.04)

latex.DrawText(0.7, 0.83, 'MilliQan 2023')

latex.SetTextSize(0.03)

latex.DrawText(0.7, 0.8, 'Muon Events')

#Save the plot

Canvas.SaveAs('Pulse_Area_comp_bar_requirement_Slabs.png')

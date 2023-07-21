import ROOT as r

r.gROOT.SetBatch(1)

chain = r.TChain('t')

path = '/net/cms26/cms26r0/milliqan/outputRun3Hadd/v32/'

#The first instance of Run_num is purely beam off while the second is a mix of beam off and on

Run_num = ['1035', '1038', '1039'] 

#Run_num = ['1006', '1031', '1032', '1035', '1038', '1039']

Runs = []

for i in Run_num:
	Run = path+f'MilliQan_Run{i}_default_v32.root'
	Runs.append(Run)

	print(f'Added Run {i}')

for Run in Runs:
	chain.Add(Run)


df = r.RDataFrame(chain)

#now time to do an event by event filter to accept all events with an initial hit in the front or back slabs

#Each filter represents a condition for us to meet or fail at; the sum allows us to pass if even one element meets the condition

#the arguments in .Define follow (VariableName,variable) 

through_going = df.Filter('Sum(chan==71&&ipulse==0)').Filter('Sum(chan==75&&ipulse==0)')

#Obtain the heights from each of the channels (71 and 75) and add them to the DataFrame

through_going = through_going.Define('height_chan71', 'height[chan==71]')

through_going = through_going.Define('height_chan75', 'height[chan==75]')

#make variables for the filtered heights 

height_chan71 = through_going.Define('heightChan71', 'height[chan==71&&ipulse==0]').Filter('Sum(chan==71&&ipulse==0)')

height_chan75 = through_going.Define('heightChan75', 'height[chan==75&&ipulse==0]').Filter('Sum(chan==75&&ipulse==0)')

#Timing needs to be done only for the muons; these saturate the digitizer

through_going = through_going.Define('timeChan71', 'time[chan==71&&ipulse==0]').Filter('Sum(height[chan==71&&ipulse==0]>1200)').Filter('Sum(320.e3<area[chan==71])')


through_going = through_going.Define('timeChan75', 'time[chan==75&&ipulse==0]').Filter('Sum(height[chan==75&&ipulse==0]>1200)').Filter('Sum(150.e3<area[chan==75])')

#time difference for saturation; note that the variables of saturated time were #defined before so we can just subtract

through_going = through_going.Define('timeDiff_Chan75_Chan71', 'timeChan75-timeChan71')

#Histogram only those values which are from the newly defined structure and from 
#channels (71 or 75) and meet the ipulse criteria ipulse==0 

height_chan71Histo = height_chan71.Histo1D(('heightChan71_RDF', 'Endcap Pulse Height;height', 100, 1240, 1260), 'heightChan71')


height_chan75Histo = height_chan75.Histo1D(('heightChan75_RDF', 'Endcap Pulse Height;height', 100, 1240, 1260), 'heightChan75')

#make the timing histogram objects

time_chan71Histo = through_going.Histo1D(('timeChan71_RDF', 'Endcap Timing; time', 100, 1000,1500), 'timeChan71')


time_chan75Histo = through_going.Histo1D(('timeChan75_RDF', 'Endcap Timing; time', 100, 1000, 1500), 'timeChan75')

#make the time difference Histograms

timeDiffHisto = through_going.Histo1D(('t[75-71]', 'Elapsed Time Between Channels 75 and 71; time', 20, -25,25),'timeDiff_Chan75_Chan71')

#make output root file

output = r.TFile('Cosmic_TimeDiffHisto_Slabs.root', 'RECREATE')

output.cd()

timeDiffHisto.Write()

#make a canvas to plot on

oC = r.TCanvas()

#create sub-canvas

height_chan71Histo.SetLineColor(r.kRed)

height_chan75Histo.SetLineColor(r.kBlack)

height_chan71Histo.GetYaxis().SetTitle('Number of Events')

height_chan71Histo.GetXaxis().SetTitle('Pulse Height [mV]')

height_chan75Histo.GetXaxis().SetTitle('Pulse Height [mV]')

#Remove the stats box

height_chan71Histo.SetStats(0)

height_chan75Histo.SetStats(0)

#Draw the plot

height_chan71Histo.DrawCopy()

height_chan75Histo.DrawCopy('same')
#Extra

legend=r.TLegend(0.7,0.6,0.85,0.75) 

legend.AddEntry(height_chan71Histo.GetPtr() ,"Chan 71") 

legend.AddEntry(height_chan75Histo.GetPtr() ,"Chan 75") 

legend.SetLineWidth(0) 

legend.Draw("same")

latex = r.TLatex()

latex.SetNDC()

latex.SetTextSize(0.04)

latex.DrawText(0.7, 0.83, 'MilliQan 2023')

latex.SetTextSize(0.03)

latex.DrawText(0.7, 0.8, 'Muon Events')

#save the plot

oC.SaveAs('HeightHistofromRDF_Slabs.png')

#Drawing for the time distributions

C2 = r.TCanvas()

time_chan71Histo.SetLineColor(r.kRed)

time_chan75Histo.SetLineColor(r.kBlack)

time_chan71Histo.GetYaxis().SetTitle('Number of Events')

time_chan71Histo.GetXaxis().SetTitle('Time')

time_chan75Histo.GetXaxis().SetTitle('Time')


time_chan71Histo.SetStats(0)

time_chan75Histo.SetStats(0)

time_chan71Histo.DrawCopy('h')

time_chan75Histo.DrawCopy('h, same')


legend=r.TLegend(0.7,0.6,0.85,0.75) 

legend.AddEntry(time_chan71Histo.GetPtr() ,"Chan 71") 

legend.AddEntry(time_chan75Histo.GetPtr() ,"Chan 75") 

legend.SetLineWidth(0) 

legend.Draw("same")

latex = r.TLatex()

latex.SetNDC()

latex.SetTextSize(0.04)

latex.DrawText(0.7, 0.83, 'MilliQan 2023')

latex.SetTextSize(0.03)

latex.DrawText(0.7, 0.8, 'Muon Events')

C2.SaveAs('Timing_Slabs.png')

#Doing the time difference drawings

C3 = r.TCanvas()

timeDiffHisto.Draw('h')

timeDiffHisto.GetYaxis().SetTitle('Number of Events')

timeDiffHisto.GetXaxis().SetTitle('\Delta t[ns]')

latex = r.TLatex()

latex.SetNDC()

latex.SetTextSize(0.03)

latex.DrawText(0.75, 0.5, 'MilliQan 2023')

latex.SetTextSize(0.02)

latex.DrawText(0.75, 0.45, 'Muon Events')

C3.SaveAs('TimeDiff_Slabs.png')

output.Close()

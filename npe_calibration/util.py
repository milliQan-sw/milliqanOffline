#!/usr/bin/env python
import os, sys, re
import ROOT
import os
import cfg
import glob
from array import array
import shutil
import subprocess

def makeDirRecursive(dire):
    cumul=""
    for subDir in dire.split("/"):
        cumul=cumul+subDir+"/"
        if not os.path.exists(cumul):
            os.mkdir(cumul)



def getTrees(runNum):
    t = ROOT.TChain("t")
    runDir= glob.glob(cfg.treeDir+"Run"+runNum+"_*")[0]
    t.Add(runDir+"/*.root")
    return t


def findTotalTime(hist,binw):
    time=0.
    for i in range(1,hist.GetNbinsX()+1):
        if hist.GetBinContent(i)>0: time = time+binw
    return time

def defineColors():
    reds =[255./255.,31./255.,235./255.,111./255.,219./255.,151./255.,185./255.,194./255.,127./255.,98./255.,211./255.,69./255.,220./255.,72./255.,225./255.,145./255.,233./255.,125./255.,147./255.,110./255.,209./255.,44]
    greens=[255./255.,30./255.,205./255.,48./255.,106./255.,206./255.,32./255.,188./255.,128./255.,166./255.,134./255.,120./255.,132./255.,56./255.,161./255.,39./255.,232./255.,23./255.,173./255.,53./255.,45./255.,54]
    blues=[255./255.,30./255.,62./255.,139./255.,41./255.,230./255.,54./255.,130./255.,129./255.,71./255.,178./255.,179./255.,101./255.,150./255.,49./255.,139./255.,87./255.,22./255.,60./255.,21./255.,39./255.,23]

    global palette
    global colors
    palette = []
    colors = []

    for icolor in range(len(reds)):
        palette.append(ROOT.TColor(2000+icolor,reds[icolor],greens[icolor],blues[icolor]))
        colors.append(2000+icolor)

    colors[9] = 419 #kGreen+3
    colors[2] = 2009
    #colors[7]=2008
    #colors[8]=2007
    colors[3] = 2013
    colors[12]= 2017


def getTubeType(ichan):
    ttype=0
    if cfg.tubeSpecies[ichan]=="R878": ttype=1
    if cfg.tubeSpecies[ichan]=="R7725": ttype=2
    return ttype


def getHist(chain, name, title, selection, variable, nbins, minx, maxx):
    hist = ROOT.TH1F(name,title,nbins,minx,maxx)
    hist.Sumw2()
    chain.Project(name,variable,selection)
    #print name,variable,selection
    return hist

def cosmeticTH1(hist,chan):
    hist.SetLineWidth(2)
    hist.SetStats(0)
    hist.SetLineColor(colors[chan])
    hist.SetTitleSize(0.045,"X")
    hist.SetTitleSize(0.045,"Y")
    hist.SetTitleOffset(1.1,"Y")
def cutToString(cut):
    return cut.replace("==","").replace("&&","_").replace("<=","lte").replace(">=","gte").replace("<","lt").replace(">","gt").replace("$","").replace("(","").replace(")","").replace(".","p")


def replaceTableRow(tableName,runNum,ichan,HV,mean,err,rate):
    tmpName =tableName.replace("table_run","tmp_table_run")
    newTable = open(tmpName,"w")
    if os.path.exists(tableName):
        with open(tableName,"r") as oldTable:
            for line in oldTable:
                # see if this line corresponds to the channel/run that is being updated. if not, then copy old line
                if not (line.split(",")[0] == runNum and line.split(",")[1] == str(ichan)):
                    newTable.write(line)

    #add latest measurement to end
    newTable.write(",".join([runNum,str(ichan),str(HV),str(round(mean,1)),str(round(err,2)),str(round(rate,4))+"\n"]))
    newTable.close()
    #copy tmp to overwrite original file
    shutil.move(tmpName,tableName)



def copyPlot(runNum, ichan,filename,field,measure,isCosmic=True):
    ##Delete old measure plots for this run and channel
    if field:
        bstring = "3p8"
    else:
        bstring = "0"

    if int(runNum)>250:
        bstring="postYETS"

    webDir = cfg.webBaseDir + "field%s/channel%i/"%(bstring,ichan)
    if not isCosmic:
        webDir = webDir+"SPE/"

    if measure:
        webDir=webDir+"Measure/"
    else:
        webDir=webDir+"Run%s/"%runNum
#"/Users/heller/Sites/milliqan/field%s/channel%i/"%(bstring,ichan)
    makeDirRecursive(webDir)
    #if not os.path.exists(webDir):
    #    os.mkdir(webDir)

    if isCosmic: zoom = int(filename.split("zoom")[1].split(".pdf")[0])
    else: zoom = int(filename.replace("fullrange","").replace("_vetoOtherChan","").split("zoom")[1].split(".pdf")[0])
    var = filename.split("Run%s_" % runNum)[-1].split("_ch")[0].replace("cosmic_","")
#    print var
    #print "zoom is",str(zoom)
    extraSel=""
    if not isCosmic and "heightgt" in filename:
        extraSel = "heightgt"
    # print filename
    # print extraSel
    if measure:
        oldFiles= webDir+"Run%s_%s_ch%i_*%s*.png" % (runNum,var,ichan,extraSel)
    else:
        oldFiles= webDir+"Run%s_%s_ch%i*%s*_zoom%i*.png" % (runNum,var,ichan,extraSel,zoom)
#    print filename,measure
#    print oldFiles
    for f in glob.glob(oldFiles):
        # print f
        os.remove(f)
    if measure:
        oldFiles= webDir+"log/Run%s_%s_ch%i_*%s*log.png" % (runNum,var,ichan,extraSel)
    else:
        oldFiles= webDir+"log/Run%s_%s_ch%i*%s*_zoom%i*_log.png" % (runNum,var,ichan,extraSel,zoom)
    for f in glob.glob(oldFiles):
        #print f
        os.remove(f)
    ##Copy .png file to web directory
    #filename=filename.replace(".pdf",".png")
    #subprocess.check_output(['bash','-c','source ~/.bashrc && pdftopng %s'%filename])

    baseFileName= filename.split("/")[-1].replace(".pdf",".png")
    if "cosmic" in baseFileName:
        baseFileName = baseFileName.replace("cosmic_","")

    subprocess.call(["cp",filename.replace(".pdf",".png"),webDir+baseFileName])
    if ".pdf" in filename:
        webDir = webDir+"log/"
        makeDirRecursive(webDir)
        subprocess.call(["cp",filename.replace(".pdf","_log.png"),webDir+baseFileName.replace(".png","_log.png")])
    #shutil.move(filename.replace(".pdf",".png"),webDir+baseFileName)
    #subprocess.call(["cp", filename, measureFilename])
    #subprocess.call(["cp", filename.replace(".png","_log.png"), measureFilename.replace(".root","_log.root")])


def printTH1s(hists,legTitles,filename,runDuration=1,findMean=False,cosmicMode=False,printIntegral=False,thresh=500.,useNarrowRange=True, savePNG=True,meanCorr=1.00):
    #print findMean
    c = ROOT.TCanvas()
    c.SetGrid()
    xstart =0.65
    ystart =0.7
    if(len(hists)>3 and len(hists)<=6): ystart=0.55
    if printIntegral or cosmicMode: xstart=0.5


    leg = ROOT.TLegend(xstart,ystart,0.9,0.9)

    maxy=0
    miny=0.1
    for i,h in enumerate(hists):
        if h.GetMaximum()>maxy: maxy = h.GetMaximum()
        if h.GetMinimum()<miny and h.GetMinimum()!=0: miny = h.GetMinimum()

        thisleg = legTitles[i]
        if printIntegral:
            integral= h.Integral(h.FindBin(thresh),h.GetNbinsX()+1)
            if integral.is_integer():
                thisleg = thisleg+", N > 500: %i #pm %0.f" % (integral,pow(integral,0.5))
            else:
                thisleg = thisleg+", Rate > 500: %0.1f #pm %0.2f mHz" % (1000.*integral,1000.*pow(integral*runDuration,0.5)/runDuration)
        if "noSat" not in thisleg: leg.AddEntry(h,thisleg,"l")


    if cosmicMode:
        if maxy > 2.*hists[-1].GetMaximum():
            maxy = 2.*hists[-1].GetMaximum()
        maxy = 420

    coordStart=0
    coordEnd=0
    mean=0
    meanErr=0
    halfMax=0
    nSel=0
    rate=0

    if findMean:
        meanHist=-2
        halfMax = 0.5 * hists[meanHist].GetMaximum()
         #if not cosmicMode:
        meanHist=-1
        if cosmicMode: hists[meanHist].SetAxisRange(thresh,hists[meanHist].GetBinLowEdge(hists[meanHist].GetNbinsX()+1)-0.001)
        peakBin = array( 'i', [ 0 ] )#ROOT.Long(-1)
        hists[meanHist].GetBinWithContent(hists[meanHist].GetMaximum(),peakBin)
        halfMax = 0.5 * hists[meanHist].GetMaximum()

        start=peakBin[0]
        while hists[meanHist].GetBinContent(start) > halfMax and start>hists[meanHist].FindBin(thresh)-1: start = start - 1
        start= start+1
        if cosmicMode:

            hists[meanHist].SetAxisRange(thresh,peakBin[0])
            #print thresh, peakBin[0]
            #print hists[meanHist].GetMinimum()

            ## avoid case where valley is not deep enough to be < halfmax, and range goes all the way to minimum
            if hists[meanHist].GetMinimum()>halfMax:
                newStart = array( 'i', [ 0 ] )
                hists[meanHist].GetBinWithContent(hists[meanHist].GetMinimum(),newStart)
                start = newStart[0]
                #print start
            hists[meanHist].SetAxisRange(thresh,hists[meanHist].GetBinLowEdge(hists[meanHist].GetNbinsX()+1)-0.001)


        end=peakBin[0]
        #print halfMax
        while (hists[meanHist].GetBinContent(end) > halfMax and end<hists[meanHist].GetNbinsX()+1):
            #print end
            #print hists[meanHist].GetBinContent(end)
            end = end + 1

        if start==peakBin[0]:
            start -= 1

        if end-start > 5:
            start = peakBin[0]-2
            end = peakBin[0]+3

        coordStart = hists[meanHist].GetBinLowEdge(start) ## start at left edge of first bin > HM
        coordEnd = hists[meanHist].GetBinLowEdge(end)-0.001 ## start at right edge of last bin > HM
        if not useNarrowRange:
            coordStart=hists[meanHist].GetBinLowEdge(1)
            coordEnd=hists[meanHist].GetBinLowEdge(hists[meanHist].GetNbinsX()+1)-0.001

        nSel = hists[meanHist].Integral(hists[meanHist].FindBin(thresh),hists[meanHist].GetNbinsX()+1)
        rate=float(nSel)/float(runDuration)

        if cosmicMode:
            hists[meanHist].SetAxisRange(coordStart,coordEnd)
            #Get mean and meanerr
            mean=hists[meanHist].GetMean()
            meanErr=hists[meanHist].GetMeanError()
            #reset plotting range
            #if not cosmicMode:
            hists[meanHist].SetAxisRange(hists[meanHist].GetBinLowEdge(1),hists[meanHist].GetBinLowEdge(hists[meanHist].GetNbinsX()+1)-0.001)
            #print hists[-1].GetName(),mean
        else: 
            fit = ROOT.TF1("fit", "gaus", coordStart, coordEnd)
            maxval = hists[meanHist].GetBinContent(peakBin[0])
            fit.SetParameter(0, maxval)
            fit.SetParLimits(0, 0.8*maxval, 1.2*maxval)
            fit.SetParameter(1, hists[meanHist].GetBinCenter(peakBin[0]))
            fit.SetParameter(2, (coordEnd-coordStart)/2)        
            hists[meanHist].Fit(fit, "QNR")
            mean = fit.GetParameter(1)
            meanErr = fit.GetParError(1)

        mean *= meanCorr
        meanErr *= meanCorr

    for i,h in enumerate(hists):
        h.SetMaximum(1.1*maxy)
        if miny<0: miny=miny*1.1
        elif miny!=0.1: miny=0.5*miny
        h.SetMinimum(miny)
        if "Diff" not in filename:
            if i == 0: h.Draw("hist")
            else: h.Draw("hist same")
        else:
            h.SetMarkerStyle(20)
            h.SetMarkerColor(h.GetLineColor())
            if i == 0: h.Draw("ep")
            else: h.Draw("ep same")

        if (not findMean) and "area" in filename:
            c.Print(filename.replace(".pdf","layer%i.pdf"%i))

    leg.Draw("same")
    #hists[-1].Draw("hist")
    c.Print(filename.replace(".pdf","noMean.pdf"))
    if findMean:
        line = ROOT.TLine()
        line.SetLineColor(hists[-1].GetLineColor())
        line.SetLineWidth(4)
        line.SetLineStyle(7)
        line.DrawLine(coordStart,0,coordStart,1.1*halfMax)
        line.DrawLine(coordEnd,0,coordEnd,1.1*halfMax)
        line.SetLineStyle(1)
        line.DrawLine(mean,0,mean,2.2*halfMax)
        line.SetLineWidth(2)
        line.DrawLine(thresh,0,thresh,2.2*halfMax)
        if not cosmicMode:
            fit.SetLineColor(hists[-1].GetLineColor())
            fit.SetLineWidth(3)
            fit.Draw("SAME")

        tla = ROOT.TLatex()
        tla.SetTextSize(0.045)
        tla.SetTextFont(42)
        tla.SetTextColor(hists[-1].GetLineColor())
        tla.DrawLatexNDC(0.60,0.6,"Mean: %0.1f #pm %0.01f pVs" %(mean,meanErr))
        if cosmicMode:tla.DrawLatexNDC(0.65,0.55,"Rate: %0.3f Hz" %(rate))


    makeDirRecursive(os.path.dirname(filename))
    #if not os.path.exists(os.path.dirname(filename)):
    #    os.mkdir(os.path.dirname(filename))

    c.Print(filename)
    if savePNG: c.Print(filename.replace(".pdf",".png"))
    if "Diff" not in filename:
        c.SetLogy()
        c.Print(filename.replace(".pdf","_log.pdf"))
        if savePNG: c.Print(filename.replace(".pdf","_log.png"))

    if findMean:
        return mean,meanErr,rate
    else: return 0,0,0

#! /usr/bin/env python

## take a binary file output from DRS scope
## create a ROOT file with time and voltage arrays
##
## note that time values are different for every event since
## DRS binning is uneven, and the trigger can occur in any bin

import struct
import datetime as dt
import json
import numpy as np
import ROOT as r

# name = "r878_Helm0p0ALong_1450V_1p92V_13ns_300Hz_50000evnts"
name = "r878_1250V_1p55V_20ns_50000evnts"
# name = "afterpulses/r7725_1450V_2p4V_13ns_300Hz_1p0GHz_500000evnts"
# name = "r7725/r7725b_1500V_1p91V_13ns_300Hz_50000evnts"

indir =  "/nfs-7/userdata/bemarsh/milliqan/pmt_calib/scope_output"
outdir = "/nfs-7/userdata/bemarsh/milliqan/pmt_calib/test"

fin = indir+"/{0}.dat".format(name)
fout = r.TFile(outdir+"/{0}.root".format(name), "RECREATE")

READ_CHN = 2 # can be a single integer or list of integers
N_BINS = 1024 # number of timing bins per channel
POLARITY = 1 # use -1 to invert. peaks must be positive

if type(READ_CHN) == int:
    READ_CHN = [READ_CHN]
ts = {c: np.zeros(1024, dtype='float') for c in READ_CHN}
vs = {c: np.zeros(1024, dtype='float') for c in READ_CHN}
t = r.TTree("Events","Events")
for c in READ_CHN:
    extra = "" if len(READ_CHN)==1 else "_"+str(c)
    t.Branch("times"+extra, ts[c], 'times{0}[1024]/D'.format(extra))
    t.Branch("voltages"+extra, vs[c], 'voltages{0}[1024]/D'.format(extra))
        

def getStr(fid, length):
    data = fid.read(length)
    if len(data)==0:
        return None
    res = struct.unpack("c"*length, data)
    return "".join(res)

def getShort(fid, num=1):
    data = fid.read(2*num)
    if len(data)==0:
        return None
    res = struct.unpack("H"*num, data)
    return res[0] if num==1 else res

def getFloat(fid, num=1):
    data = fid.read(4*num)
    if len(data)==0:
        return None
    res = struct.unpack("f"*num, data)
    return res[0] if num==1 else res

def getInt(fid, num=1):
    data = fid.read(4*num)
    if len(data)==0:
        return None
    res = struct.unpack("I"*num, data)
    return res[0] if num==1 else res

fid = open(fin,'rb')

# make sure file header is correct
fhdr = getStr(fid, 4)
if fhdr != "DRS2":
    print "ERROR: unrecognized header "+fhdr
    exit(1)

# make sure timing header is correct
thdr = getStr(fid, 4)
if thdr != "TIME":
    print "ERROR: unrecognized time header "+thdr
    exit(1)

# get the boards in file
n_boards = 0
channels = []
board_ids = []
bin_widths = []
while True:
    bhdr = getStr(fid, 2)
    if bhdr != "B#":
        fid.seek(-2, 1)
        break
    board_ids.append( getShort(fid) )
    n_boards += 1
    bin_widths.append([])
    print "Found Board #"+str(board_ids[-1])

    while True:
        chdr = getStr(fid, 3)
        if chdr != "C00":
            fid.seek(-3, 1)
            break
        cnum = int(getStr(fid, 1))
        print "  Found channel #"+str(cnum)
        channels.append(cnum)
        bin_widths[n_boards-1].append(getFloat(fid, N_BINS))

    if len(bin_widths[n_boards-1])==0:
        print "ERROR: Board #{0} doesn't have any channels!".format(board_ids[-1])

if n_boards==0:
    print "ERROR: didn't find any valid boards!"
    exit(1)

if n_boards > 1:
    print "ERROR: only support one board. Found {0} in file.".format(n_boards)
    exit(1)

for c in READ_CHN:
    if c not in channels:
        print "ERROR: set to read channel {0}, but it isn't in the file!".format(c)
        exit(1)

bin_widths = bin_widths[0]
n_chan = len(bin_widths)
rates = []

n_evt = 0
while True:
    ehdr = getStr(fid, 4)
    if ehdr == None:
        break
    if ehdr != "EHDR":
        raise Exception("Bad event header!")

    n_evt += 1
    # print "Found Event #"+str(n_evt)
    serial = getInt(fid)
    # print "  Serial #"+str(serial)
    date = getShort(fid, 7)
    date = dt.datetime(*date[:6], microsecond=1000*date[6])
    # print "  Date: "+str(date)
    rangeCtr = getShort(fid)
    # print "  Range Center: "+str(rangeCtr)
    getStr(fid, 2)
    b_num = getShort(fid)
    getStr(fid, 2)
    trig_cell = getShort(fid)
    # print "  Trigger Cell: "+str(trig_cell)

    time0 = None
    for ichn in range(n_chan):
        chdr = getStr(fid, 4)
        if chdr != "C00"+str(channels[ichn]):
            print "ERROR: bad event data!"
            exit(1)

        scaler = getInt(fid)
        voltages = np.array(getShort(fid, N_BINS))
        if channels[ichn] not in READ_CHN:
            continue
        voltages = voltages/65535. * 1000 - 500 + rangeCtr
        voltages *= POLARITY
        times = np.roll(np.array(bin_widths[ichn]), N_BINS-trig_cell)
        times = np.cumsum(times)
        times = np.append([0], times[:-1])
        rates.append((times[-1]-times[0])/(times.size-1))

        if time0 is None:
            time0 = times[(N_BINS-trig_cell) % N_BINS]
        else:
            times -= (times[(N_BINS-trig_cell) % N_BINS] - time0)

        np.copyto(ts[channels[ichn]], times)
        np.copyto(vs[channels[ichn]], voltages)
        
    t.Fill()

print "Measured sampling rate: {0:.2f} GHz".format(1.0/np.mean(rates))
t.Write("Events", r.TObject.kWriteDelete)
fout.Close()





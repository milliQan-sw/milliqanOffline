# -*- coding: utf-8 -*-
import os, re

runNum = "1334"
runDescription = "_Physics"

runDir = "/store/user/llavezzo/trees_v19/Run" + runNum + runDescription
hs_file_dir= "/store/user/llavezzo/HSdata/2018/"

count = 0 # testing

for file in os.listdir(runDir):
    if count > 0: exit()
    fileNum = file[file.find(runNum)+5:file.find("_",file.find(runNum))]
    outFileName = "/data/users/bmanley/HS_Run"+runNum+runDescription+"_"+fileNum+".root"
    inFileName = runDir+'/'+file

    os.system("root -l -b -q 'add_hsdata.cpp(\"{0}\", \"{1}\", {2}, {3}, \"{4}\")'".format(inFileName,outFileName,runNum,fileNum,hs_file_dir)) 
    count += 1
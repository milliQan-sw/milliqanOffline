import os
import sys

#################################################################################################
## Script will check multiple locations and look for differences in what files are saved there
##################################################################################################

files = {"milliDAQ" : '/home/milliqan/tmp/fileList.txt', "OSU" : '/home/milliqan/tmp/fileListOSU.txt', "UCSB" : '/home/milliqan/tmp/fileListUCSB.txt'}

destinations = {"UCSB":"milliqan@cms17.physics.ucsb.edu:/net/cms26/cms26r0/milliqan/Run3/", "OSU":"milliqan@128.146.39.20:/store/user/milliqan/run3/"} #temporary change to OSU ip address

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def getFileList(site):
    if site == "milliDAQ":
        os.system('ls -1 /home/milliqan/data/ > ' + files['milliDAQ'])
    else: os.system('ssh ' + destinations[site].split(":")[0] + ' ls -1 ' + destinations[site].split(":")[-1] + ' > ' + files[site])

def checkRemote(site):

    missingList = open('/home/milliqan/tmp/notTransferred.txt', 'a+')
 
    prevMissing = []
    for line in missingList:
        missing_site = line.split('\t')[0].strip()
        filename = line.split('\t')[-1].strip()
        prevMissing.append([missing_site, filename])

    missingFiles, missingPrimary, transferredFiles = 0, 0, 0

    host = destinations[site].split(':')[0]
    filePath = destinations[site].split(':')[-1]

    siteFiles = []
    for line in open(files[site], 'r'):
        filename = line.strip()
        siteFiles.append(filename)

    for line1 in open(files['milliDAQ'], "r"):
        filename1 = line1.split()[-1]
        if not 'root' in filename1: continue
        fileAtDest = True if filename1 in siteFiles else False
        if not fileAtDest:
            if not [site, filename1] in prevMissing: missingList.write(site + '\t' + filename1 + '\n')
            missingFiles += 1
            if 'milliQan' in filename1 or 'TriggerBoard' in filename1: missingPrimary += 1
            print("Host {0} is missing file {1}".format(site, filePath+filename1))
        else:
            transferredFiles += 1
            #print("Found file {0} on host {1}".format(filePath+filename1, site))
    missingList.close()
    return missingFiles, missingPrimary, transferredFiles

def checkOldMissing():
    notTransferredList = []

    ucsbFiles = []
    for line in open(files['UCSB'], 'r'):
        filename = line.strip()
        ucsbFiles.append(filename) 

    osuFiles = []
    for line in open(files['OSU'], 'r'):
        filename = line.strip()
        osuFiles.append(filename)

    for line1 in open('/home/milliqan/tmp/notTransferred.txt', 'r+'):
        site = line1.split('\t')[0]
        filename = line1.split('\t')[-1].strip()
        isTransferred = False
        if site == 'OSU':
            if filename in osuFiles: isTransferred = True
        elif site == 'UCSB':
            if filename in ucsbFiles: isTransferred = True
        else:
            print("Error: site is not UCSB or OSU")

        if isTransferred == True:
            print("File {0} has been transferred to site {1}".format(filename, site))
        if not isTransferred: 
            notTransferredList.append([site, filename])
            #print("Still missing file {0} on site {1}".format(filename, site))
    
    notTransferred = open('/home/milliqan/tmp/notTransferred.txt', 'w+')
    for x in notTransferredList:
        notTransferred.write(x[0] + '\t' + x[1] + '\n')
    notTransferred.close()
    return len(notTransferredList)

if __name__ == "__main__":

    totalMissing, totalPrimaryMissing, totalTransferred = 0, 0, 0

    getFileList('milliDAQ')
    
    for site in destinations.keys():
        print("Checking site {0}".format(site))
        getFileList(site)
        missing, primary, transferred = checkRemote(site)
        totalMissing += missing
        totalPrimaryMissing += primary
        totalTransferred += transferred
        print("Site {0}, Total Files {1}, Missing Files {2}, Missing Primary Files {3}".format(site, missing+transferred, missing, primary))

    numMissing = checkOldMissing()
    if numMissing != totalMissing:
        print("There are {0} untransferred files listed in notTransferred.txt and there are {1} untransferred files found now... there may be files missing from DAQ computer".format(numMissing, totalMissing))

    print("Among all sites... Missing Files {0}, Missing Primary Files {1}".format(totalMissing, totalPrimaryMissing))


import os


#This function returns the base directory where the offline data is stored. 
def getData_dir() -> str:
    myhost = os.uname()[1]
    if 'interactive' in myhost:
        filepath = '/store/user/milliqan/trees/v34/'
    elif 'cms' in myhost:
        filepath = '/net/cms26/cms26r0/milliqan/Run3Offline/v34/'
    else:
        print('Warning: host not found!  No file path defined!')
    return filepath

#This function returns a list of root files given a list of run numbers and the base data directory.
#You can get the base data directory using getData_dir() or you can put it in yourself.
def makeFilelist(pruns: list, pfilepath: str) -> list: 
    fullfilelist = os.listdir(pfilepath)
    _filelist = []
    for run in pruns:
        for file in fullfilelist:
                if "Run{0}".format(run) in file:
                    _filelist.append(pfilepath+file+':t')
    return _filelist
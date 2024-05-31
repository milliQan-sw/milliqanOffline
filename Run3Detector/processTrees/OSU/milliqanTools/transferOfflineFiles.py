import os


if __name__ == '__main__':
    
    #make sure these commands are run from the shell first so that passwordless ssh is enabled
    #eval "$(ssh-agent -s)"
    #ssh-add ~/.ssh/id_ucsb_milliqan

    ucsbDir = '/net/cms26/cms26r0/milliqan/Run3Offline/v34/'
    transferPath = 'milliqan@tau.physics.ucsb.edu:/{}'.format(ucsbDir)

    inPath = '/store/user/milliqan/trees/v34/'

    cmd = 'rsync -zh {0}MilliQan_Run141?.*_v34.root {1}'.format(inPath, transferPath)
    os.system(cmd)
    

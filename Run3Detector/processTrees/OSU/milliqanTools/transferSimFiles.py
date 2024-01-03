import os


if __name__ == '__main__':
    
    #make sure these commands are run from the shell first so that passwordless ssh is enabled
    #eval "$(ssh-agent -s)"
    #ssh-add ~/.ssh/id_ucsb_milliqan

    ucsbDir = '/net/cms26/cms26r0/schmitz/milliQanFlatSim/cosmic/barNoPhoton/raw/'
    transferPath = 'milliqan@cms3.physics.ucsb.edu:/{}'.format(ucsbDir)

    outPath = '/store/user/milliqan/sim/bar/cosmics/flat/noGamma/'

    cmd = 'scp -r {0}* {1}'.format(transferPath, outPath)
    os.system(cmd)
    

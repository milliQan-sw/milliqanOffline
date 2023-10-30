import os
import shutil

dataDir = '/store/user/milliqan/trees/v31/'

combinedDir = dataDir + 'combined/'

if not os.path.exists(combinedDir):
    os.mkdir(combinedDir)

files = []

force = False

for filename in os.listdir(dataDir):
    if not filename.startswith('MilliQan_Run') or not filename.endswith('.root'): continue
    fileStem = filename.split('.')[0]
    if os.path.exists(combinedDir + fileStem + '_combined.root') and not force: continue
    if fileStem not in files: files.append(fileStem)


for i, run in enumerate(files):
    cmd = 'hadd {0}_combined.root {1}{0}*.root'.format(run, dataDir)
    os.system(cmd)
    os.system('mv {0}_combined.root {1}'.format(run, combinedDir))

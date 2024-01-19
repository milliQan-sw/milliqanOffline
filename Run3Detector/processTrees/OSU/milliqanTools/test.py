import subprocess
       
cmd = 'python3 /share/scratch0/milliqan/processTrees/run_processTrees.py -S {0}.{1} -r {2} -s {3}'.format(900, 1, 900, 0000)
print(cmd)
p = subprocess.run([cmd], shell=True, cwd='/share/scratch0/milliqan/processTrees/')
#p = subprocess.run(['echo testing'], shell=True)

import os
import shutil
from flopy import run_model

# Create a new test-out folder here where the list files will go
dest = 'test-out'
if os.path.exists(dest):
    try:
        shutil.rmtree(dest)
    except:
        os.system('rmdir /S /Q "{}"'.format(dest))
os.mkdir(dest)

# Copy the test-run folder here
pth = 'test-run'
if os.path.exists(pth):
    try:
        shutil.rmtree(pth)
    except:
        os.system('rmdir /S /Q "{}"'.format(pth))
shutil.copytree('../test-run', './test-run')

# get a list of the name files and run them in the test-run folder
namefiles = [f for f in os.listdir('test-run') if f.endswith('.nam')]
exe = os.path.join('..', 'bin', 'mf2005.exe')
exe = os.path.abspath(exe)
for f in namefiles:
    run_model(exe, f, 'test-run')

# copy the list files to the test-out folder
listfiles = [f for f in os.listdir('test-run') if f.endswith('.lst')]
for f in listfiles:
    src = os.path.join('test-run', f)
    dst = os.path.join('test-out', f)
    print('copy {} ==> {}'.format(src, dst))
    shutil.copy(src, dst)

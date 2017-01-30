"""
Python code to create a MODFLOW-2005 distribution

"""
import os
import subprocess
import shutil
import zipfile
import shlex

def zipdir(dirname, zipname):
    zipf = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(dirname):
        for file in files:
            if '.DS_Store' not in file:
                fname = os.path.join(root, file)
                arcname = fname.split(dirname, 1)[1]
                print('adding to zip: ==> ', arcname)
                zipf.write(fname, arcname=arcname)
    zipf.close()
    return

destpath = '.'
version = 'MF2005.1_12'
dest = os.path.join(destpath, version)

print(2*'\n')
print('Creating MODFLOW-2005 distribution: {}'.format(version))
print('\n')

if os.path.exists(dest):
    # Raise Exception('Destination path exists.  Kill it first.')
    print('Clobbering destination directory: {}'.format(dest))
    print('\n')
    shutil.rmtree(dest)


# Create subdirectories
binpath = os.path.join(dest, 'bin')
docpath = os.path.join(dest, 'doc')
msvspath = None # os.path.join(dest, 'msvs')
sourcepath = os.path.join(dest, 'src')
toutpath = os.path.join(dest, 'test-out')
trunpath = os.path.join(dest, 'test-run')

# leave out some folders because they will be created with copytree
subdirs = [f for f in [dest, binpath, msvspath, toutpath] if f is not None]
print('Creating directories')
for sd in subdirs:
    print(' {}'.format(sd))
    os.mkdir(sd)
print('\n')


# Copy the executables
print('Copying MODFLOW executables')
bins = ['mf2005.exe', 'mf2005dbl.exe', 'mnw1to2.exe', 'hydfmt.exe']
for b in bins:
    fname = os.path.join('..', 'bin', b)
    shutil.copy(fname, os.path.join(binpath, b))
    print('  {} ===> {}'.format(fname, os.path.join(binpath, b)))
print('\n')


# Copy the documentation, but leave out the docx files
print('Copying documentation')
shutil.copytree('../doc', docpath,
                ignore=shutil.ignore_patterns('.DS_Store', 'tmp*', '*.docx'))
print('\n')

# Copy release notes
doclist = [os.path.join('..', 'Mf2005.txt'),
		   os.path.join('..', 'problems.txt'),
		   os.path.join('..', 'readme.txt'),
		   os.path.join('..', 'release.txt')]
print('Copying release notes')
for d in doclist:
    print('  {} ===> {}'.format(d, dest))
    shutil.copy(d, dest)
print('\n')


# Copy the test folder to the distribution folder
print('Copying test folder')
shutil.copytree('../test-run', trunpath, ignore=shutil.ignore_patterns('.DS_Store', 'tmp*'))
print('  {} ===> {}'.format('../test-run', trunpath))
print('\n')


# Copy the source code
print('Copying the source code')
print('  {} ===> {}'.format('../src', sourcepath))
shutil.copytree('../src', sourcepath, ignore=shutil.ignore_patterns('.DS_Store', 'tmp*'))
print('\n')


# Copy Visual Studio files
#print('Copying the Visual Studio file')
#fnames = ['mfusg.vfproj']
#for f in fnames:
#    shutil.copy(os.path.join('../msvs', f), os.path.join(msvspath, f))
#    print('  {} ===> {}'.format(os.path.join('../msvs', f), os.path.join(msvspath, f)))
#print('\n')


# Prior to zipping, enforce windows line endings on all text files
cmd = 'for /R %G in (*) do unix2dos "%G"'
args = shlex.split(cmd)
p = subprocess.Popen(cmd, cwd=dest, shell=True)
print(p.communicate())

# Zip the distribution
zipname = version + '.zip'
if os.path.exists(zipname):
    print('Removing existing file: {}'.format(zipname))
    os.remove(zipname)
print('Creating zipped file: {}'.format(zipname))
zipdir(dest, zipname)
print('\n')

print('Done...')
print('\n')

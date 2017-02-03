"""
Python code to create a MODFLOW-2005 distribution

"""
import os
import subprocess
import shutil
import zipfile
import shlex

unix = True

def zipdir(dirname, zipname):
    print('zipping directory: {}'.format(dirname))
    zipf = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(dirname):
        for file in files:
            if '.DS_Store' not in file:
                fname = os.path.join(root, file)
                print('adding to zip: ==> ', fname)
                zipf.write(fname, arcname=fname)
    zipf.close()
    return

destpath = '.'
version = 'MF2005.1_12'
if unix: version += 'u'
dest = os.path.join(destpath, version)

print(2*'\n')
print('Creating MODFLOW-2005 distribution: {}'.format(version))
print('\n')

if os.path.exists(dest):
    print('Clobbering destination directory: {}'.format(dest))
    print('\n')
    try:
        shutil.rmtree(dest)
    except:
        os.system('rmdir /S /Q "{}"'.format(dest))


# Create subdirectories
binpath = os.path.join(dest, 'bin')
docpath = os.path.join(dest, 'doc')
msvspath = None # os.path.join(dest, 'msvs')
sourcepath = os.path.join(dest, 'src')
toutpath = os.path.join(dest, 'test-out')
trunpath = os.path.join(dest, 'test-run')
makepath = os.path.join(dest, 'make')
if unix:
    binpath = None

# leave out some folders because they will be created with copytree
subdirs = [f for f in [dest, binpath, msvspath] if f is not None]
print('Creating directories')
for sd in subdirs:
    print(' {}'.format(sd))
    os.mkdir(sd)
print('\n')


# Copy the executables
if not unix:
    print('Copying MODFLOW executables')
    bins = ['mf2005.exe', 'mf2005dbl.exe', 'hydfmt.exe']
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
           os.path.join('..', 'release.txt')]
if unix:
    doclist.append(os.path.join('..', 'readme_unix.txt'))
else:
    doclist.append(os.path.join('..', 'readme.txt'))
print('Copying release notes')
for d in doclist:
    print('  {} ===> {}'.format(d, dest))
    shutil.copy(d, dest)
print('\n')


# Copy the test folder to the distribution folder
print('Copying test-run folder')
shutil.copytree('../test-run', trunpath, ignore=shutil.ignore_patterns('.DS_Store', 'tmp*'))
print('  {} ===> {}'.format('../test-run', trunpath))
print('\n')


# Copy the test folder to the distribution folder
print('Copying test-out folder')
shutil.copytree('../test-out', toutpath, ignore=shutil.ignore_patterns('.DS_Store', 'tmp*'))
print('  {} ===> {}'.format('../test-out', toutpath))
print('\n')


# Copy the source code
print('Copying the source code')
print('  {} ===> {}'.format('../src', sourcepath))
shutil.copytree('../src', sourcepath, ignore=shutil.ignore_patterns('.DS_Store', 'tmp*'))
print('\n')


# Copy make folder
if unix:
    print('Copying the make folder')
    print('  {} ===> {}'.format('../make', makepath))
    shutil.copytree('../make', makepath, ignore=shutil.ignore_patterns('.DS_Store', 'tmp*'))
    print('\n')


# Prior to zipping, enforce windows line endings on all text files
cmd = 'for /R %G in (*) do unix2dos "%G"'
if unix:
    cmd = 'for /R %G in (*) do dos2unix "%G"'
args = shlex.split(cmd)
p = subprocess.Popen(cmd, cwd=dest, shell=True)
print(p.communicate())


# if unix, then change openspec.inc
replacestrings = [
    ("      DATA ACCESS/'SEQUENTIAL'/", "C     DATA ACCESS/'SEQUENTIAL'/"),
    ("C     DATA ACCESS/'STREAM'/", "      DATA ACCESS/'STREAM'/"),
    ("C      DATA FORM/'UNFORMATTED'/", "       DATA FORM/'UNFORMATTED'/"),
    ("      DATA FORM/'BINARY'/", "C     DATA FORM/'BINARY'/")]
if unix:
    fname = os.path.join(sourcepath, 'openspec.inc')
    with open(fname, 'r') as f:
        newlines = []
        for line in f.readlines():
            for s, r in replacestrings:
                if s in line:
                    line = line.replace(s, r)
            newlines.append(line)
    with open(fname, 'w') as f:
        for line in newlines:
            f.write(line)


# Zip the distribution
zipname = version + '.zip'
if os.path.exists(zipname):
    print('Removing existing file: {}'.format(zipname))
    os.remove(zipname)
print('Creating zipped file: {}'.format(zipname))
zipdir(version, zipname)
print('\n')

print('Done...')
print('\n')

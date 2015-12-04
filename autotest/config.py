import os

# Autotest information
testdir = 'temp'
retain = False
target_dict = {}

exclude = None #('MNW2-Fig28',) #, 'swi2ex4sww') #None

# Development version information
exdir = 'test-run'
arcdir = 'test-arc'
testdev = 'test-dev'
testpaths = [os.path.join('..', exdir), os.path.join('..', arcdir), os.path.join('..', testdev)]
srcdir = os.path.join('..', 'src')
program = 'mf2005'
version = '1.12.00'
target = os.path.join(testdir, program + '_' + version)
target_dict[os.path.basename(target)] = target

# Release version information
url_release = 'http://water.usgs.gov/ogw/modflow/MODFLOW-2005_v1.11.00/mf2005v1_11_00_unix.zip'
dir_release = os.path.join(testdir, 'Unix')
srcdir_release = os.path.join(dir_release, 'src')
version_release = '1.11.00'
target_release = os.path.join(testdir, program + '_' + version_release)
target_dict[os.path.basename(target_release)] = target_release

target_dict[program] = target_release

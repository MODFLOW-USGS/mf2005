import os

# Autotest information
testdir = 'temp'
retain = False

exclude = 'MNW2-Fig28' #None

# Development version information
exdir = 'test-run'
testpaths = [os.path.join('..', exdir)]
srcdir = os.path.join('..', 'src')
program = 'mf2005'
version = '1.12.00'
target = os.path.join(testdir, program + '_' + version)

# Release version information
url_release = 'http://water.usgs.gov/ogw/modflow/MODFLOW-2005_v1.11.00/mf2005v1_11_00_unix.zip'
dir_release = os.path.join(testdir, 'UNIX')
srcdir_release = os.path.join(dir_release, 'src')
version_release = '1.11.00'
target_release = os.path.join(testdir, program + '_' + version_release)

import os
import platform

# Autotest information
testdir = 'temp'
retain = False
target_dict = {}
fc = 'gfortran'  # 'ifort' or 'gfortran'
cc = 'cc'        # 'cl'    or 'cc'

# set executable extension for windows
exe_ext = ''
if platform.system() == 'Windows':
    exe_ext = '.exe'

# List of examples to skip from the testing
exclude = None  #('MNW2-Fig28',)

# Test problems to run with autotest
#   exdir:   regression tests for models distributed with mf2005
#   arcdir:  regression tests for models not distributed with mf2005
#   testdev: comparison tests for features/bug fixes in develop version
#   testswr: comparison tests for models using SWR
exdir   = 'test-run'
arcdir  = 'test-arc'
testdev = 'test-dev'
testswr = 'test-swr'
testpaths = [os.path.join('..', exdir),
             os.path.join('..', arcdir),
             os.path.join('..', testdev),
             os.path.join('..', testswr)
             ]

# Development version information
srcdir = os.path.join('..', 'src')
program = 'mf2005'
version = '1.12.00'
target = os.path.join(testdir, program + '_' + version + exe_ext)
target_dict[os.path.basename(target)] = target

# Release version information
url_release = ('http://water.usgs.gov/ogw/modflow/MODFLOW-2005_v1.11.00/'
               'mf2005v1_11_00_unix.zip')
dir_release = os.path.join(testdir, 'Unix')
srcdir_release = os.path.join(dir_release, 'src')
version_release = '1.11.00'
target_release = os.path.join(testdir, program + '_' + version_release +
                              exe_ext)
target_dict[os.path.basename(target_release)] = target_release

target_dict[program] = target_release

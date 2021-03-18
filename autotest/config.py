import os
import platform
import pymake

ebindir = os.path.abspath(
    os.path.join(os.path.expanduser("~"), ".local", "bin")
)
if not os.path.exists(ebindir):
    os.makedirs(ebindir)

testdir = "temp"
target_dict = {}

# set executable extension for windows
exe_ext = ""
if platform.system() == "Windows":
    exe_ext = ".exe"

# List of examples to skip from the testing
exclude = None  # ('MNW2-Fig28',)

# Test problems to run with autotest
#   exdir:   regression tests for models distributed with mf2005
#   arcdir:  regression tests for models not distributed with mf2005
#   testdev: comparison tests for features/bug fixes in develop version
#   testswr: comparison tests for models using SWR
exdir = "test-run"
arcdir = "test-arc"
testdev = "test-dev"
testswr = "test-swr"
testpaths = (
    os.path.join("..", exdir),
    os.path.join("..", arcdir),
    os.path.join("..", testdev),
    os.path.join("..", testswr),
)

# Development version information
program = "mf2005"
srcdir = os.path.join("..", "src")
target = os.path.join(testdir, program + exe_ext)
target_dict[program] = target

# Release version information
target_release = os.path.join(ebindir, program + exe_ext)
target_dict["release"] = target_release

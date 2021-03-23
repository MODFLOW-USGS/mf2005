import os
import sys
import platform
import pymake

ebindir = os.path.abspath(
    os.path.join(os.path.expanduser("~"), ".local", "bin")
)
if not os.path.exists(ebindir):
    os.makedirs(ebindir)

testdir = "temp"
retain = False
target_dict = {}

# set executable extension for windows
exe_ext = ""
if platform.system() == "Windows":
    exe_ext = ".exe"

# List of examples to skip from the testing
is_CI = "CI" in os.environ
# test-arc remove after v 1.13.00 is released
exclude = ("UzfTest",)
if not is_CI:
    exclude += ("MNW2-Fig28",)

FC = os.environ.get("FC")
# if FC is not None:
#     if sys.platform.lower() == "darwin":
#         exclude += (
#             "bcf2ss",
#             "sfrtest4",
#             "simple_bcf2ss",
#         )


# default regression tolerances
htol = 5e-6
pdtol = 0.01

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
target = program + exe_ext
target_dict[program] = os.path.abspath(os.path.join(testdir, target))

# Release version information
target_release = os.path.join(ebindir, program + exe_ext)
target_dict["release"] = os.path.abspath(target_release)


def get_htol(test_name):
    htols = {
        "swr007_mh2013ex1": 0.0002,
        "swtex4": 5e-5,
    }
    if test_name in list(htols.keys()):
        tol = htols[test_name]
    else:
        tol = htol
    return tol


def get_pdtol(test_name):
    # dir_namefile no extension on namefile
    pdtols = {
        "sfr4test_sfrtest4": 1e6,
        "lakeex2_l2a_2k": 1e6,
        "transroute_nounsat_testsfr2_tab_transroute_nounsat": 0.1,
    }
    if test_name in list(pdtols.keys()):
        tol = pdtols[test_name]
    else:
        tol = pdtol
    return tol


def teardown(success, test_model):
    _write_success(success)
    if success:
        if not retain:
            print("\ttearing down...{}".format(test_model))
            pymake.teardown(test_model)
    assert success, "{} model did not run".format(test_model)

    return


def get_success():
    fpth = os.path.join(testdir, "success")
    with open(fpth) as f:
        lines = f.read().splitlines()
    if lines[0] == "False":
        success = False
    else:
        success = True
    # delete the success file
    os.remove(fpth)
    return success


def _write_success(success):
    fpth = os.path.join(testdir, "success")
    if success:
        if not os.path.isfile(fpth):
            f = open(fpth, "w")
            f.write("{}\n".format(success))
            f.close()
    else:
        f = open(fpth, "w")
        f.write("{}\n".format(success))
        f.close()
    return

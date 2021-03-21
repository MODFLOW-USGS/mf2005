import os
import sys
import pymake
import config

# paths to executables for previous versions of MODFLOW
ebindir = os.path.abspath(
    os.path.join(os.path.expanduser("~"), ".local", "bin")
)
if not os.path.exists(ebindir):
    os.makedirs(ebindir)

FC = os.environ.get("FC")
fflags = None
if FC is not None:
    if sys.platform.lower() == "win32":
        fflags = "-fp:strict"
    else:
        fflags = "-fp-model:strict"


def test_compile_dev():
    pm = pymake.Pymake()
    pm.target = config.target
    pm.srcdir = config.srcdir
    pm.appdir = config.testdir
    pm.include_subdirs = False
    pm.inplace = False
    pm.makeclean = True
    if fflags is not None:
        pm.fflags = fflags

    # build the release version of MODFLOW-2005
    pm.build()

    return


def test_compile_ref():
    # Compile reference version of the program from the source.
    pm = pymake.Pymake(verbose=True)
    pm.target = "mf2005"
    pm.appdir = config.ebindir
    if fflags is not None:
        pm.fflags = fflags

    download_pth = os.path.join("temp")
    pm.download_target(pm.target, download_path=download_pth)

    # build the release version of MODFLOW-2005
    pm.build()

    msg = "{} does not exist.".format(pm.target)
    assert pm.returncode == 0, msg

    # finalize the build
    pm.finalize()

    return


if __name__ == "__main__":
    test_compile_ref()
    test_compile_dev()

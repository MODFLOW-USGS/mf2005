import os
import flopy
import pymake
from pymake import get_namefiles
import config


def run_mf2005(namefile, comparison=True):
    """
    Run the simulation.

    """

    # Set root as the directory name where namefile is located
    testname = pymake.get_sim_name(namefile, rootpth=config.testpaths[2])[0]

    # set htol
    htol = config.get_htol(testname)

    # set percent discrepancy
    pdtol = config.get_pdtol(testname)

    # Set nam as namefile name without path
    nam = os.path.basename(namefile)

    # Setup
    testpth = os.path.join(config.testdir, testname)
    pymake.setup(namefile, testpth)

    # run test models
    print("running model...{}".format(testname))
    exe_name = config.target_dict[config.program]
    success, buff = flopy.run_model(
        exe_name,
        nam,
        model_ws=testpth,
        silent=False,
    )

    if success and comparison:
        testname_reg = os.path.basename(config.target_release)
        testpth_reg = os.path.join(testpth, testname_reg)
        pymake.setup(namefile, testpth_reg)
        print("running regression model...{}".format(testname_reg))
        exe_name = config.target_dict["release"]
        success, buff = flopy.run_model(
            exe_name,
            nam,
            model_ws=testpth_reg,
            silent=False,
        )

        if success:
            outfile1 = os.path.join(
                os.path.split(os.path.join(testpth, nam))[0], "bud.cmp"
            )
            outfile2 = os.path.join(
                os.path.split(os.path.join(testpth, nam))[0], "hds.cmp"
            )
            success = pymake.compare(
                os.path.join(testpth, nam),
                os.path.join(testpth_reg, nam),
                precision="single",
                max_cumpd=pdtol,
                max_incpd=pdtol,
                htol=htol,
                outfile1=outfile1,
                outfile2=outfile2,
            )
            if not success:
                print("{} comparison failed".format(testname))

    # Clean things up
    config.teardown(success, testpth)

    return


def test_mf2005():
    if config.exclude is None:
        exclude = []
    else:
        exclude = list(config.exclude)
    namefiles = sorted(get_namefiles(config.testpaths[2], exclude=exclude))
    for namefile in namefiles:
        yield run_mf2005, namefile
    return


if __name__ == "__main__":
    if config.exclude is None:
        exclude = []
    else:
        exclude = list(config.exclude)
    namefiles = sorted(get_namefiles(config.testpaths[2], exclude=exclude))
    for namefile in namefiles:
        run_mf2005(namefile)

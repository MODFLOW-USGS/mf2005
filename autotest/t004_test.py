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
    testname = pymake.get_sim_name(namefile, rootpth=config.testpaths[3])[0]

    # if "VCatch" not in testname:
    #     return

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

    # If it is a comparison, then look for files in the comparison
    # folder (.cmp)
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
            namefile1 = os.path.join(testpth, nam)
            namefile2 = os.path.join(testpth_reg, nam)
            outfile1 = os.path.join(
                os.path.split(os.path.join(testpth, nam))[0], "bud.cmp"
            )
            outfile2 = os.path.join(
                os.path.split(os.path.join(testpth, nam))[0], "hds.cmp"
            )
            success_cmp = pymake.compare(
                namefile1,
                namefile2,
                precision="single",
                max_cumpd=pdtol,
                max_incpd=pdtol,
                htol=htol,
                outfile1=outfile1,
                outfile2=outfile2,
            )
            if not success_cmp:
                print("{} comparison failed".format(testname))

            outfile3 = os.path.join(
                os.path.split(os.path.join(testpth, nam))[0], "swr.bud.cmp"
            )
            success_swr = pymake.compare_swrbudget(
                namefile1,
                namefile2,
                max_cumpd=pdtol,
                max_incpd=pdtol,
                outfile=outfile3,
            )
            if not success_swr:
                print("{} swr budget comparison failed".format(testname))

            # stage comparison
            outfile4 = os.path.join(
                os.path.split(os.path.join(testpth, nam))[0],
                "swr.stage.cmp",
            )
            success_stg = pymake.compare_stages(
                namefile1=namefile1,
                namefile2=namefile2,
                htol=htol,
                outfile=outfile4,
            )
            if not success_stg:
                print("{} swr stage comparison failed".format(testname))

            if success_cmp and success_swr and success_stg:
                success = True
            else:
                success = False

    # Clean things up
    config.teardown(success, testpth)

    return


def test_mf2005():
    if config.exclude is None:
        exclude = []
    else:
        exclude = list(config.exclude)
    namefiles = sorted(get_namefiles(config.testpaths[3], exclude=exclude))
    for namefile in namefiles:
        yield run_mf2005, namefile
    return


if __name__ == "__main__":
    if config.exclude is None:
        exclude = []
    else:
        exclude = list(config.exclude)
    namefiles = sorted(get_namefiles(config.testpaths[3], exclude=exclude))
    for namefile in namefiles:
        run_mf2005(namefile)

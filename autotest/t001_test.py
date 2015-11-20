from __future__ import print_function
import os
import shutil
import flopy
import pymake
from pymake.autotest import get_namefiles, compare_budget, compare_heads
import config


def compare(namefile1, namefile2):
    """
    Compare the results from two simulations
    """

    # Compare budgets from the list files in namefile1 and namefile2
    outfile = os.path.join(os.path.split(namefile1)[0], 'bud.cmp')
    success1 = compare_budget(namefile1, namefile2, max_cumpd=0.01, max_incpd=0.01,
                              outfile=outfile)

    outfile = os.path.join(os.path.split(namefile1)[0], 'hds.cmp')
    success2 = compare_heads(namefile1, namefile2, htol=0.001,
                             outfile=outfile)

    success = False
    if success1 and success2:
        success = True
    return success


def run_mf2005(namefile, regression=True):
    """
    Run the simulation.

    """

    # Set root as the directory name where namefile is located
    testname = pymake.get_sim_name(namefile, rootpth=config.testpaths[0])[0]

    # Set nam as namefile name without path
    nam = os.path.basename(namefile)

    # #
    # ocf = pymake.get_filename_from_namefile(namefile, 'OC')
    # outd = flopy.modflow.ModflowOc.get_ocoutput_units(ocf)
    # headfn = None
    # if outd[0] != 0:
    #     headfn = pymake.get_filename_from_namefile(namefile, unit=abs(outd[0]))

    # Setup
    testpth = os.path.join(config.testdir, testname)
    pymake.setup(namefile, testpth)

    # run test models
    print('running model...{}'.format(testname))
    exe_name = os.path.abspath(config.target)
    success, buff = flopy.run_model(exe_name, nam, model_ws=testpth,
                                    silent=True)

    # If it is a regression run, then setup and run the model with the
    # release target and the reference target
    success_reg = True
    if regression:
        testname_reg = os.path.basename(config.target_release)
        testpth_reg = os.path.join(testpth, testname_reg)
        pymake.setup(namefile, testpth_reg)
        print('running regression model...{}'.format(testname_reg))
        exe_name = os.path.abspath(config.target_release)
        success_reg, buff = flopy.run_model(exe_name, nam,
                                            model_ws=testpth_reg,
                                            silent=True)

        if success_reg:
            success_reg = compare(os.path.join(testpth, nam),
                                  os.path.join(testpth_reg, nam))
        # # Make comparison
        # if headfn is None:
        #     success_reg = compare(os.path.join(testpth, nam),
        #                           os.path.join(testpth_reg, nam))
        # else:
        #     f1 = os.path.join(testpth, os.path.basename(headfn))
        #     f2 = os.path.join(testpth_reg, os.path.basename(headfn))
        #     success_reg = pymake.compare_heads(f1, f2,
        #                                        outfile=os.path.join(testpth, 'hds.cmp'))

    # Clean things up
    if success and success_reg and not config.retain:
        pymake.teardown(testpth)
    assert success and success_reg

    return


def test_mf2005():
    namefiles = get_namefiles(config.testpaths[0], exclude=config.exclude)
    for namefile in namefiles:
        yield run_mf2005, namefile
    return


if __name__ == '__main__':
    namefiles = get_namefiles(config.testpaths[0], exclude=config.exclude)
    for namefile in namefiles:
        run_mf2005(namefile)

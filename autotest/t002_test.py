from __future__ import print_function
import os
import shutil
import flopy
import pymake
from pymake.autotest import get_namefiles, compare_budget
import config


def compare(namefile1, namefile2):
    """
    Compare the results from two simulations
    """

    # Compare budgets from the list files in namefile1 and namefile2
    outfile = os.path.join(os.path.split(namefile1)[0], 'bud.cmp')
    success = compare_budget(namefile1, namefile2, max_cumpd=0.01, max_incpd=0.1,
                             outfile=outfile)
    return success


def run_mf2005(namefile, comparison=True):
    """
    Run the simulation.

    """

    # Set root as the directory name where namefile is located
    testname = pymake.get_sim_name(namefile, rootpth=config.testpaths[1])[0]

    # Set nam as namefile name without path
    nam = os.path.basename(namefile)

    # Setup
    testpth = os.path.join(config.testdir, testname)
    #pymake.setup(namefile, testpth)

    # run test models
    print('running model...{}'.format(testname))
    exe_name = os.path.abspath(config.target)
    #success, buff = flopy.run_model(exe_name, nam, model_ws=testpth,
    #                                silent=True)
    success_cmp = True
    if comparison:
        testname_reg = os.path.basename(config.target_release)
        testpth_reg = os.path.join(testpth, testname_reg)
        action = pymake.setup_comparison(namefile, testpth)
        #print('running regression model...{}'.format(testname_reg))
        #exe_name = os.path.abspath(config.target_release)
        #success_reg, buff = flopy.run_model(exe_name, nam,
        #                                    model_ws=testpth_reg,
        #                                    silent=True)
    ## Clean things up
    #if success and not config.retain:
    #    pymake.teardown(testpth)
    #assert success

    return


def test_mf2005():
    namefiles = get_namefiles(config.testpaths[1])
    for namefile in namefiles:
        yield run_mf2005, namefile
    return


if __name__ == '__main__':
    namefiles = get_namefiles(config.testpaths[1])
    for namefile in namefiles:
        run_mf2005(namefile)

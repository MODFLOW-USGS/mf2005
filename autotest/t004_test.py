from __future__ import print_function
import os
import flopy
import pymake
from pymake.autotest import get_namefiles
import config


def run_mf2005(namefile, comparison=True):
    """
    Run the simulation.

    """

    # Set root as the directory name where namefile is located
    testname = pymake.get_sim_name(namefile, rootpth=config.testpaths[3])[0]

    # Set nam as namefile name without path
    nam = os.path.basename(namefile)

    # Setup
    testpth = os.path.join(config.testdir, testname)
    pymake.setup(namefile, testpth)

    # run test models
    print('running model...{}'.format(testname))
    exe_name = os.path.abspath(config.target)
    success, buff = flopy.run_model(exe_name, nam, model_ws=testpth,
                                    silent=True)

    # If it is a comparison, then look for files in the comparison
    # folder (.cmp)
    success_cmp = True
    if comparison:
        action = pymake.setup_comparison(namefile, testpth)
        testpth_cmp = os.path.join(testpth, action)
        if action is not None:
            files_cmp = None
            if action.lower() == '.cmp':
                files_cmp = []
                files = os.listdir(testpth_cmp)
                for file in files:
                    files_cmp.append(
                            os.path.abspath(os.path.join(testpth_cmp, file)))
                success_cmp = True
                print(files_cmp)
            else:
                print('running comparison model...{}'.format(testpth_cmp))
                key = action.lower().replace('.cmp', '')
                exe_name = os.path.abspath(config.target_dict[key])
                success_cmp, buff = flopy.run_model(exe_name, nam,
                                                    model_ws=testpth_cmp,
                                                    silent=True)

            if success_cmp:
                namefile1 = os.path.join(testpth, nam)
                namefile2 = os.path.join(testpth_cmp, nam)
                outfile1 = os.path.join(
                        os.path.split(os.path.join(testpth, nam))[0],
                        'bud.cmp')
                outfile2 = os.path.join(
                        os.path.split(os.path.join(testpth, nam))[0],
                        'hds.cmp')
                success_cmp = pymake.compare(namefile1,
                                             namefile2,
                                             precision='single',
                                             max_cumpd=0.01, max_incpd=0.01,
                                             htol=0.001,
                                             outfile1=outfile1,
                                             outfile2=outfile2,
                                             files2=files_cmp)

                outfile3 = os.path.join(
                        os.path.split(os.path.join(testpth, nam))[0],
                        'swr.bud.cmp')
                success_swr = pymake.compare_swrbudget(namefile1,
                                                       namefile2,
                                                       max_cumpd=0.01,
                                                       max_incpd=0.01,
                                                       outfile=outfile3,
                                                       files2=files_cmp)

                # stage comparison
                outfile4 = os.path.join(
                        os.path.split(os.path.join(testpth, nam))[0],
                        'swr.stage.cmp')
                success_stg = pymake.compare_stages(namefile1=namefile1,
                                                    htol=0.001,
                                                    outfile=outfile4,
                                                    files2=files_cmp)

                if success_cmp and success_swr and success_stg:
                    success_cmp = True
                else:
                    success_cmp = False
    # Clean things up
    if success and success_cmp and not config.retain:
        pymake.teardown(testpth)
    assert success, 'model did not run'
    assert success_cmp, 'comparison model did not meet comparison criteria'

    return


def test_mf2005():
    if config.exclude is None:
        exclude = []
    else:
        exclude = list(config.exclude)
    exclude.append('.cmp')
    namefiles = get_namefiles(config.testpaths[3], exclude=exclude)
    for namefile in namefiles:
        yield run_mf2005, namefile
    return


if __name__ == '__main__':
    if config.exclude is None:
        exclude = []
    else:
        exclude = list(config.exclude)
    exclude.append('.cmp')
    namefiles = get_namefiles(config.testpaths[3], exclude=exclude)
    for namefile in namefiles:
        run_mf2005(namefile)

from __future__ import print_function
import os
import shutil
import textwrap
import numpy as np
import pymake
import flopy

max_pd = 0.001


def test_modflow2005():

    # set up a few paths
    binpth = os.path.join('..', 'bin')
    srcdir = os.path.join('..', 'src')
    dstpth = os.path.join('temp')
    examplepth = os.path.join('..', 'test-run')
    refpth = os.path.join('..', 'test-out')

    # create bin path if necessary
    if not os.path.exists(binpth):
        os.makedirs(binpth)

    # working directory if necessary
    if not os.path.exists(dstpth):
        os.makedirs(dstpth)

    # compile code
    targetname = 'mf2005'
    target = os.path.abspath(os.path.join(binpth, targetname))

    # compile modflow
    #pymake.main(srcdir, target, 'gfortran', 'gcc', makeclean=True,
    #            expedite=False, dryrun=False, double=False, debug=False,
    #            include_subdirs=False)
    
    # make sure executable has been built
    assert os.path.isfile(target) is True

    # copy example files to
    examplefiles = os.listdir(examplepth)
    for file in examplefiles:
        fn = os.path.join(examplepth, file)
        if os.path.isfile(fn):
            shutil.copy(fn, dstpth)

    # run test models
    exe_name = target
    errors = []
    namefiles = []
    headers = ['"INCREMENTAL IN"', '"INCREMENTAL OUT"',
               '"CUMULATIVE IN"', '"CUMULATIVE OUT"']
    exclude = ['MNW2-Fig28.nam']
    for file in os.listdir(dstpth):
        if file.endswith('.nam'):
            namefiles.append(file)
    for namefile in namefiles:
        if namefile in exclude:
            continue
        print('\nrunning model...{}'.format(namefile))
        success, buff = pymake.run_model(exe_name, namefile, model_ws=dstpth, silent=True)
        assert success is True

        # check budgets in the list files
        root = os.path.splitext(namefile)[0]
        lstname = '{}.lst'.format(root)
        reff = os.path.join(refpth, lstname)
        refobj = flopy.utils.MfListBudget(reff)
        ref = refobj.get_recarrays()
        simf = os.path.join(dstpth, lstname)
        simobj = flopy.utils.MfListBudget(simf)
        sim = simobj.get_recarrays()
        icnt = 0
        for idx in range(4):
            kper = ref[idx]['stress_period']
            kstp = ref[idx]['time_step']
            names = ref[idx].dtype.names
            v0 = np.zeros(kper.shape[0], dtype=np.float)
            v1 = np.zeros(kper.shape[0], dtype=np.float)
            for name in names[2:]:
                t0 = ref[idx][name]
                t1 = sim[idx][name]
                for jdx in range(kper.shape[0]):
                    v0[jdx] += t0[jdx]
                    v1[jdx] += t1[jdx]
            for jdx in range(kper.shape[0]):
                denom = v0[jdx]
                err = 0.
                if denom > 0.:
                    err = 100. * (v1[jdx] - v0[jdx]) / denom
                if err > max_pd:
                    icnt += 1
                    e = 'Error {:03d}: {} percent difference  ({}) for stress '.format(icnt, headers[idx], err) + \
                        'period {} and time step {} > {}.'.format(kper[jdx], kstp[jdx], max_pd) + \
                        ' Reference value = {}. Simulated value = {}.'.format(v0.sum(), v1.sum())
                    e = textwrap.wrap(e, 70)
                    for ee in e:
                        t = '  {}'.format(ee)
                        errors.append(t)
                        print(t)
                    print('')
        if icnt < 1:
            print('  Passed budget criteria test...')

    # test for failure
    assert len(errors) < 1




if __name__ == '__main__':
    test_modflow2005()

from __future__ import print_function
import os
import shutil
import numpy as np

import textwrap

import pymake
import flopy


logf = open('nosetest.log', 'w')

max_cumpd = 0.01
max_incpd = 0.01

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

# executable names and paths
# release
targetnamer = 'mf2005r'
targetr = os.path.abspath(os.path.join(binpth, targetnamer))
# development
targetname = 'mf2005'
target = os.path.abspath(os.path.join(binpth, targetname))

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
headers = ('INCREMENTAL', 'CUMULATIVE')
dir = ('IN', 'OUT')
exclude = ('MNW2-Fig28.nam')
for file in os.listdir(dstpth):
    if file.endswith('.nam'):
        if file in exclude:
            continue
        namefiles.append(file)

def compile_src():

    # Download the MODFLOW-2005 distribution
    url = 'http://water.usgs.gov/ogw/modflow/MODFLOW-2005_v1.11.00/mf2005v1_11_00_unix.zip'
    msg = 'downloading MODFLOW-2005 from {}'.format(url)
    print(msg)
    logf.write(msg+'\n')
    pymake.download_and_unzip(url, dstpth)
    # Remove the existing MF2005.1_11u directory if it exists
    if os.path.isdir(os.path.join(dstpth, 'MF2005.1_11u')):
        shutil.rmtree(os.path.join(dstpth, 'MF2005.1_11u'))
    # Rename Unix to a more reasonable name
    os.rename(os.path.join(dstpth, 'Unix'), os.path.join(dstpth, 'MF2005.1_11u'))

    msg = 'compiling MODFLOW-2005 downloaded from {}'.format(url)
    print(msg)
    logf.write(msg+'\n')
    pymake.main(os.path.join(dstpth, 'MF2005.1_11u', 'src'), targetr,
                'gfortran', 'gcc', makeclean=True,
                expedite=False, dryrun=False, double=False, debug=False,
                include_subdirs=False)
    assert os.path.isfile(targetr) is True

    # compile modflow
    msg = 'compiling MODFLOW-2005'
    print(msg)
    logf.write(msg+'\n')
    pymake.main(srcdir, target, 'gfortran', 'gcc', makeclean=True,
                expedite=False, dryrun=False, double=False, debug=False,
                include_subdirs=False)

    # make sure executable has been built
    assert os.path.isfile(target) is True

    return True


def test_modflow():

    msg = 'Starting MODFLOW-2005 autotest'
    print(msg)
    logf.write(msg+'\n')

    # compile the release and development versions of the code
    #compile_src()

    for namefile in namefiles:
        yield run_modflow, namefile
        #yield waterbudget_compare, namefile

    logf.close()

    return

def run_modflow(namefile):
    msg = 'running test ' + namefile
    logf.write(msg + '\n')
    logf.write('  Release version\n')
    success, buff = pymake.run_model(targetr, namefile, model_ws=dstpth, silent=True)
    assert success is True
    # copy release list file
    root = os.path.splitext(namefile)[0]
    lstname = '{}.lst'.format(root)
    savname = '{}.lst.sav'.format(root)
    logf.write('  copy {} to {}\n'.format(lstname, savname))
    shutil.copyfile(os.path.join(dstpth, lstname), os.path.join(dstpth, savname))
    # run development version
    logf.write('  Development version\n')
    success, buff = pymake.run_model(target, namefile, model_ws=dstpth, silent=True)
    assert success is True

    # evaluate water budget differences
    waterbudget_compare(namefile)

def waterbudget_compare(namefile):
    # check budgets in the list files
    root = os.path.splitext(namefile)[0]
    lstname = '{}.lst'.format(root)
    savname = '{}.lst.sav'.format(root)
    reff = os.path.join(dstpth, savname)
    refobj = flopy.utils.MfListBudget(reff)
    ref = []
    ref.append(refobj.get_incremental())
    ref.append(refobj.get_cumulative())
    simf = os.path.join(dstpth, lstname)
    simobj = flopy.utils.MfListBudget(simf)
    sim = []
    sim.append(simobj.get_incremental())
    sim.append(simobj.get_cumulative())

    icnt = 0
    v0 = np.zeros(2, dtype=np.float)
    v1 = np.zeros(2, dtype=np.float)
    err = np.zeros(2, dtype=np.float)
    for idx in range(2):
        if idx > 0:
            max_pd = max_cumpd
        else:
            max_pd = max_incpd
        kper = ref[idx]['stress_period']
        kstp = ref[idx]['time_step']
        for jdx in range(kper.shape[0]):
            err[:] = 0.
            t0 = ref[idx][jdx]
            t1 = sim[idx][jdx]
            v0[0] = t0['TOTAL_IN']
            v1[0] = t1['TOTAL_IN']
            if v0[0] > 0.:
                err[0] = 100. * (v1[0] - v0[0]) / v0[0]
            v0[1] = t0['TOTAL_OUT']
            v1[1] = t1['TOTAL_OUT']
            if v0[1] > 0.:
                err[1] = 100. * (v1[1] - v0[1]) / v0[1]
            for kdx, t in enumerate(err):
                if abs(t) > max_pd:
                    icnt += 1
                    e = '"{} {}" percent difference ({})'.format(headers[idx], dir[kdx], t) + \
                        ' for stress period {} and time step {} > {}.'.format(kper[jdx]+1, kstp[jdx]+1, max_pd) + \
                        ' Reference value = {}. Simulated value = {}.'.format(v0[kdx], v1[kdx])
                    for ee in textwrap.wrap(e, 68):
                        logf.write('    {}\n'.format(ee))
                    logf.write('\n')
    # test for failure
    success = True
    if icnt > 0:
        success = False
    else:
        logf.write('    PASSED water budget criterion\n')
    assert success is True

if __name__ == '__main__':

    for f in namefiles:
        test_modflow(f)

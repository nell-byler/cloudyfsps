#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import, unicode_literals)

import os
import sys
import numpy as np
import fsps
import itertools
from cloudyfsps.ASCIItools import (writeASCII, compileASCII, checkCompiled, compiledExists)
from cloudyfsps.cloudyInputTools import writeParamFiles
from cloudyfsps.generalTools import calcForLogQ

# this code snippet goes through every step needed
# to integrate FSPS into Cloudy.
# This example uses stellar pops with a constant SFH
# as the input ionizing source.
# 1. Write an ascii file in Cloudy format with grid
#    of FSPS spectra in all available ages and
#    metallicities
# 2. Compile asii file into binary format required
#    for Cloudy use. Assumes $CLOUDY_EXE is set to
#    your /path/to/cloudy.exe
# 3. Writes Cloudy input files for a subset of grid
#    parameters.
# 4. Runs Cloudy on the *.in files
# 5. Formats the various output files

zsun = 0.0142

exec_write_ascii = True
exec_write_input = True
exec_run_cloudy = False
exec_write_output = False
exec_gen_FSPS_grid = False
make_condor = True

# Function to write the ascii file.
# This is where you set the properties of the
# ionizing spectrum (SSP/CSFH, IMF, FBHB, etc)

def mist_ascii(fileout, **kwargs):
    # change these parameters to modify the ionizing source grid
    # default mode is to produce an ascii grid in age and Z,
    # though different variables and more dimensions are possible.
    sp_dict = dict(zcontinuous=1,
                   imf_type=2,
                   sfh=0,
                   const=0.0,
                   sf_start=0.0)
    sp = fsps.StellarPopulation(**sp_dict)
    # all ages and Zs
    ages = 10.**sp.log_age
    logZs = np.log10(sp.zlegend/zsun)
    modpars = [(age, logZ) for age in ages for logZ in logZs]
    lam = sp.wavelengths
    all_fluxs = []
    for logZ in logZs:
        sp.params['logzsol'] = logZ
        all_fluxs.append(sp.get_spectrum()[1]) #lsun per hz
    nmod = len(modpars)
    # flatten flux for writing
    flat_flux = np.array([all_fluxs[j][i]
                          for i in range(len(ages))
                          for j in range(len(logZs))])
    # this function is flexible, ndim can be 3/4/n.
    writeASCII(fileout, lam, flat_flux, modpars,
               nx=len(lam), ndim=2, npar=2, nmod=nmod)
    return
#---------------------------------------------------------------------
# ASCII FILE: WRITE AND COMPILE
#---------------------------------------------------------------------
# assumes you have $CLOUDY_EXE and $CLOUDY_DATA_PATH set as sys vars.

# name of ascii file
ascii_file = 'FSPS_MIST_SSP.ascii'

# or if there is an already-compiled one you want to use, specify here
compiled_ascii = '{}.mod'.format(ascii_file.split('.')[0])
if exec_write_ascii:
    print("Executing write ascii sequence...")
    if not compiledExists(ascii_file):
        print("No compiled model exists...Writing.")
        mist_ascii(ascii_file)
        print("Compiling {} with Cloudy".format(ascii_file))
        compileASCII(ascii_file)
        print("Checking to see if compilation was successful...")
        if checkCompiled(ascii_file):
            print("Your model {} is ready to run.".format(compiled_ascii))
        else:
            sys.exit()
    else:
        print("{} already exists.".format(compiled_ascii))
#---------------------------------------------------------------------
# WRITE CLOUDY INPUT
#---------------------------------------------------------------------
# local folder to read and write *.in, *.out files
#mod_dir = '/home/oliver/research/emission/output_salp/'
mod_dir = '/astro/users/ebyler/research/newem/output_mist_ssp/'
mod_prefix = 'ZAU'

# GRID PARAMETERS FOR CLOUDY RUN
#--------------
ages = np.array([0.5e6, 1.0e6, 2.0e6, 3.0e6, 5.0e6, 7.0e6, 10.0e6])
logUs =  np.array([-4.0, -3.5, -3.0, -2.5, -2.0, -1.5, -1.0])
logZs =  np.array([-2.5, -1.5, -0.75, -0.50, -0.25, 0.0, 0.25, 0.5])

#
Rinners =  np.array([19.])
nhs = np.array([100.0])
#--------------
pars = np.array([(Z, a, U, R, calcForLogQ(logU=U, Rinner=10.0**R, nh=n), n, -1.0, 0.0)
                 for Z in logZs
                 for a in ages
                 for U in logUs 
                 for R in Rinners
                 for n in nhs])

if exec_write_input:
    print('Writing input files...')
    writeParamFiles(dir_=mod_dir,
                    model_prefix=mod_prefix,
                    cloudy_mod=compiled_ascii, # file from above
                    run_cloudy=False, #don't run yet
                    ages=ages,
                    logZs=logZs,
                    logUs=logUs,
                    r_inners=Rinners,
                    nhs=nhs,
                    use_Q=True,
                    verbose=False, #don't print output to screen
                    set_name='dopita',
                    dust=False,
                    extra_output=True,
                    extras='set WeakHeatCool 0.001\nsave last cooling each ".cool"')
    print('Wrote {} param files'.format(len(pars)))
else:
    print('Skipping input writing.')


#=======================================================================
#-----------------------------------------------------------------------
#=======================================================================

#-----------------------------------------------------------------------
#print all the jobs you would like to run into myjobs.cfg
#-----------------------------------------------------------------------
#set up outfile and essential info
outstr = 'mist_ssp'
jobfile = '/astro/users/ebyler/research/newem/condor/cloudy_{0}_jobs.cfg'.format(outstr)
jobfolder = '/astro/users/ebyler/research/newem/condor/output_{0}/'.format(outstr)

prefix_str = '''Notification = never
getenv = true

Executable = /astro/users/ebyler/research/newem/condor/run_cloudy.sh
Initialdir = /astro/users/ebyler/research/newem/condor/

Universe = vanilla
'''
#-----------------------------------------------------------------------

f = open(jobfile, 'w')
f.write(prefix_str+'\n')

for i in range(len(pars)):
    modstr = '''Log = {0}log{1}.txt
Output = {0}run{1}.out
Error = {0}run{1}.err
Arguments = {2} {3} {1}
Queue\n'''.format(jobfolder, i+1, mod_dir, mod_prefix)
    f.write(modstr+'\n')
f.close()

print('Added {0} jobs to {1}'.format(len(pars), jobfile.split('/')[-1]))

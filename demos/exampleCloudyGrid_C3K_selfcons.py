#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import (division, print_function, absolute_import, unicode_literals)
from builtins import range

import sys
import numpy as np
import fsps
import itertools
from cloudyfsps.ASCIItools import compiledExists
from cloudyfsps.cloudyInputTools import writeParamFiles, cloudyInput
from cloudyfsps.generalTools import calcForLogQ
from cloudyfsps.cloudyOutputTools import formatAllOutput
from cloudyfsps.outputFormatting import writeFormattedOutput

from astropy.constants import h as h_planck
h_planck = h_planck.to('erg s').value
L_sun = 3.83900000e+33 # erg/s

# This code snippet goes through how to create a grid
# of Cloudy models.

# It assumes that you have generated 'FSPS_MIST_SSP.ascii'
# using generateCloudyBinaryFile.py, which assumes SSPs
# as the input ionizing source.

# In this example you will:

# 1. Write Cloudy input files that vary in
#    SSP age, SSP metallicity, and gas metallicity
# 2. Run Cloudy on the *.in files
# 3. Format the various output files into nice units.

exec_write_input = True # write all of the input files
exec_run_cloudy = False # don't actually run Cloudy yet
exec_write_condor_jobs = False # don't write clustered computing script
exec_format_cloudy_output = False # for making the output in nice units
#---------------------------------------------------------------------
# ASCII FILE: CHECK THIS EXISTS
#---------------------------------------------------------------------
# Assumes you have run generateCloudyBinary.py
ascii_file = 'FSPS_MIST_C3K_SSP.ascii'
compiled_ascii = '{}.mod'.format(ascii_file.split('.')[0])

# alternatively, you could set compiled_ascii as 
# a different Cloudy model atmosphere file, e.g. popstar.

if not compiledExists(ascii_file):
    print("No compiled model exists for {}...Error!".format(ascii_file))
    sys.exit()

#---------------------------------------------------------------------
# WRITE CLOUDY INPUT
#---------------------------------------------------------------------
# local folder to read and write *.in, *.out files
mod_dir = './output_mist_c3k_ssp/'
mod_prefix = 'ZAU'

# GRID PARAMETERS FOR CLOUDY RUN
#--------------
# ages between 1 and 7 Myr
with open('../../c17.03/data/FSPS_MIST_C3K_SSP.ascii') as fsps_file:
    c3k_data = fsps_file.readlines()
cage_met_grid = np.array([float(y) for x in c3k_data[11:332] for y in x.split()])
cage = np.array(sorted(list(set(cage_met_grid[ ::2]))))
cmet = np.array(sorted(list(set(cage_met_grid[1::2]))))

ages = cage
# ionization parameters are irrelevant: use SSP spectrum.
logUs = np.array([np.nan,])
# stellar metallicities
logZs =  cmet
# gas phase metallicities
gas_logZs = np.linspace(-2.0, 0.0, 5)

# Other default parameters based off of Byler+2017
Rinners =  np.array([19.]) # inner radius of HII region, 3pc
nhs = np.array([100.0]) # density of gas, cm-3
efrac = -1.0 # calculation is stopped when H is 10^efrac % neutral
set_name='dopita' # abundances from Dopita+2001
dust=False # don't include dust in nebula
extra_output=True # include lots of outputs
#--------------------------------------------------------np.linspace(1., 7., 7)*1.e6---------

def calcForLogQ_from_SSP(age, met):

    age_ind = np.argmin(np.abs(cage-age))
    met_ind = np.argmin(np.abs(cmet-met))
    index   = np.ravel_multi_index((age_ind, met_ind), cage.shape+cmet.shape)
    cwave = np.array([
        float(y) for x in c3k_data[332:9808] for y in x.split()])
    dcwave = np.diff(cwave)
    dcwave = np.hstack([dcwave, dcwave[-1]]) # Delta lambda.
    cspec = np.array([
        float(y) for x in c3k_data[9808+47380//5*index:9808+47380//5*(index+1)] for y in x.split()])

    # Minimum and maximum wavelength of ionizing radiation.
    lambda_max = 911.26705058 # AA
    lambda_min =   0.00012391 # AA
    ionising_range = (cwave<lambda_max) & (cwave>lambda_min)
    logQ = np.sum( (cspec*dcwave/cwave)[ionising_range] ) * L_sun / h_planck
    print(logQ)

    return np.log10(logQ)



# iterate through all of the above parameters
# calcForLogQ just calculates Q = U*4*pi*Ri^2*nH

pars = np.array([(Z, a, U, R, calcForLogQ_from_SSP(a, Z), n, efrac)
                 for Z in logZs
                 for a in ages
                 for U in logUs 
                 for R in Rinners
                 for n in nhs])
#                 for gasZ in gas_logZs])

if exec_write_input:
    for i,par in enumerate(pars):
        name = f"{mod_prefix}{i+1:04d}"
        cloudyInput(
            mod_dir, name,
            logZ=par[0],
            age=par[1],
            logU=par[2],
            r_inner=par[3],
            logQ=par[4],
            dens=par[5],
            efrac=par[6],
            set_name=set_name,
            use_Q=True,
            dust=dust,
            re_z=False,
            cloudy_mod=compiled_ascii,
            verbose=False,
            geometry="sphere",
            extras="",
            extra_output=extra_output)

    print('Writing input files...')
    """
    writeParamFiles(dir_=mod_dir,
                    model_prefix=mod_prefix,
                    cloudy_mod=compiled_ascii,
                    run_cloudy=False, # don't run yet
                    ages=ages,
                    logZs=logZs,
                    logUs=logUs,
                    logQs=
                    r_inners=Rinners,
                    nhs=nhs,
                    use_Q=True,
                    # if False, will use logU;
                    # does not matter in this case,
                    # since Q is calculated at
                    # each specified logU.
                    verbose=False, # don't print output to screen
                    set_name=set_name,
                    dust=dust, 
                    extra_output=extra_output)
    """
    print('Wrote {} param files'.format(len(pars)))
else:
    print('Skipping input writing.')

# otherwise just run the models by hand
# e.g. for /your/mod/dir/ZAU42.in:
# cd $dir && $CLOUDY_EXE -r ZAU42
# Or with cloudyfsps/scripts/runCloudy.sh
# and cloudyfsps/scripts/runCloudy.py for output formatting.

#=======================================================================
#-----------------------------------------------------------------------
#=======================================================================
# if you don't want to run each model on your laptop,
# Clustered computing option
#-----------------------------------------------------------------------
# print all the jobs you would like to run into cloudy_MIST_jobs.cfg
#-----------------------------------------------------------------------
#set up outfile and essential info
mod_dir='/'.join(mod_dir.split('/')[0:-1])
outstr = 'MIST'
jobfile = './condor/cloudy_{0}_jobs.cfg'.format(outstr)
jobfolder = './condor/output_{0}'.format(outstr)

prefix_str = '''Notification = never
getenv = true

Executable = ~/cloudyfsps/scripts/runCloudy.sh
Initialdir = ./condor

Universe = vanilla
'''
#-----------------------------------------------------------------------
if exec_write_condor_jobs:
    f = open(jobfile, 'w')
    f.write(prefix_str+'\n')
    for i in range(len(pars)):
        modstr = '''Log = {0}/log{1}.txt
Output = {0}/run{1}.out
Error = {0}/run{1}.err
Arguments = {2} {3} {1}
Queue\n'''.format(jobfolder, i+1, mod_dir, mod_prefix)
        f.write(modstr+'\n')
        f.close()
    print('Added {0} jobs to {1}'.format(len(pars), jobfile.split('/')[-1]))


#=======================================================================
#-----------------------------------------------------------------------
#=======================================================================
# if you have run the Cloudy models, format the output
#-----------------------------------------------------------------------
if exec_format_cloudy_output:
    formatAllOutput(mod_dir, mod_prefix, write_line_lum=True)
    # if write_line_lum = False, the output will be in lum/Q
#-----------------------------------------------------------------------

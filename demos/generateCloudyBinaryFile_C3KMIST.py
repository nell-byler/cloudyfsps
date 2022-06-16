#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import (division, print_function, absolute_import, unicode_literals)
from past.utils import old_div
from builtins import range

import sys
import numpy as np
import pickle
from cloudyfsps.ASCIItools import (writeASCII, compileASCII, checkCompiled, compiledExists)

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

zsun = 0.0142 # this is solar metallicity for the MIST isochrones

exec_write_ascii = True

# Function to write the ascii file.
# This is where you set the properties of the
# ionizing spectrum (SSP/CSFH, IMF, FBHB, etc)

def mist_ascii(fileout, **kwargs):
    # change these parameters to modify the ionizing source grid
    # default mode is to produce an ascii grid in age and Z,
    # though different variables and more dimensions are possible.
    # Created this file with /science/projects/215_project/00_spectral_templates/fsps/create_SSP_MIST_C3K_pckl.py
    fsps_mist_c3k = pickle.load(open(
        '/science/projects/215_project/00_spectral_templates/fsps/'
        'SSP_MIST_C3K_Salpeter.pckl', 'rb'))
    # this function is flexible, ndim can be 3/4/n.
    # in this example, however, ndim is 2 (age, logz).
    lam = fsps_mist_c3k['wave']
    flat_flux = fsps_mist_c3k['flat_flux']
    modpars = fsps_mist_c3k['modpars']
    writeASCII(fileout, lam, flat_flux, modpars,
               nx=len(lam), ndim=2, npar=2, nmod=len(modpars))
    return
#---------------------------------------------------------------------
# ASCII FILE: WRITE AND COMPILE
#---------------------------------------------------------------------
# assumes you have $CLOUDY_EXE and $CLOUDY_DATA_PATH set as sys vars.

# name of ascii file
ascii_file = 'FSPS_MIST_C3K_SSP.ascii'

# the ascii file takes a while to generate, so if an already-compiled
# version exists, the code will not overwrite it.

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

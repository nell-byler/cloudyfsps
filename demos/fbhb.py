import os
from cloudyfsps import cloudy_input
from cloudyfsps import cloudy_output
from cloudyfsps import cloudytools as ct
from cloudyfsps import write_ascii
from cloudyfsps import write_ascii
from cloudyfsps import write_output
import numpy as np
import fsps

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

zsun = 0.019

exec_write_ascii = False
exec_write_input = True
exec_run_cloudy = True
exec_write_output = True
exec_gen_FSPS_grid = False

# Function to write the ascii file.
# This is where you set the properties of the
# ionizing spectrum (SSP/CSFH, IMF, FBHB, etc)

def fbhb_ascii(fileout, **kwargs):
    # change these parameters to modify the ionizing source grid
    # default mode is to produce an ascii grid in age and Z,
    # though different variables and more dimensions are possible.
    sp_dict = dict(zcontinuous=1,
                   imf_type=2,
                   sfh=0,
                   fbhb=0.5) # fraction of blue HB stars
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
    write_ascii.FileOps(fileout, lam, flat_flux,
                        modpars, ndim=2, npar=2, nmod=nmod)
    return
#---------------------------------------------------------------------
# ASCII FILE: WRITE AND COMPILE
#---------------------------------------------------------------------
# assumes you have $CLOUDY_EXE and $CLOUDY_DATA_PATH set as sys vars.

# name of ascii file
ascii_file = 'FSPS_FBHB_5.ascii'

# or if there is an already-compiled one you want to use, specify here
compiled_ascii = '{}.mod'.format(ascii_file.split('.')[0])

if exec_write_ascii:
    print 'Executing write ascii sequence...'
    if not write_ascii.mod_exists(ascii_file):
        print 'No compiled model exists...Writing.'
        fbhb_ascii(ascii_file)
        print 'Compiling {} with Cloudy'.format(ascii_file)
        write_ascii.compile_mod(ascii_file)
        print 'Checking to see if compilation was successful...'
        if not write_ascii.check_compiled_mod(ascii_file):
            print 'Something went wrong!'
            sys.exit()
        else:
            print 'Your model {} is ready to run.'.format(compiled_ascii)
    else:
        print '{} already exists.'.format(compiled_ascii)

#---------------------------------------------------------------------
# WRITE CLOUDY INPUT
#---------------------------------------------------------------------
# local folder to read and write *.in, *.out files
#mod_dir = '/home/oliver/research/emission/output_salp/'
mod_dir = '/Users/Nell/research/newem/out_fbhb/'
mod_prefix = 'ZAU'

# GRID PARAMETERS FOR CLOUDY RUN
#--------------
ages = np.array([3.0e9, 5.0e9, 10.0e9])
#ages = np.array([0.5e6, 1.0e6, 2.0e6, 4.0e6, 6.0e6])
logUs =  np.array([-4.0, -3.5, -3.0, -2.5, -2.0, -1.5, -1.0])
logZs =  np.array([-1.3, -1.0, -0.7, -0.5, -0.3, -0.1, 0.0, 0.2])
#
Rinners =  np.array([19.])
nhs = np.array([100.0])
#--------------
pars = np.array([(Z, a, U, R, ct.calc_4_logQ(logU=U, Rinner=10.0**R, nh=n), n)
                 for Z in logZs
                 for a in ages
                 for U in logUs 
                 for R in Rinners
                 for n in nhs])


if exec_write_input:
    print 'Writing input files...'
    cloudy_input.param_files(dir_=mod_dir,
                             model_prefix=mod_prefix,
                             cloudy_mod=compiled_ascii, #this is the ascii file from above
                             run_cloudy=False, #don't run yet
                             ages=ages,
                             logZs=logZs,
                             logUs=logUs,
                             r_inners=Rinners,
                             nhs=nhs,
                             use_Q=True,
                             verbose=False, #don't print output to screen
                             set_name='dopita',
                             extras='save last physical conditions ".phys"') #abundance set to use
    print 'Wrote {} param files'.format(len(pars))
else:
    print 'Skipping input writing.'
#---------------------------------------------------------------------
# RUN CLOUDY ON ALL INPUT FILES
#---------------------------------------------------------------------
if exec_run_cloudy:
    print 'Running Cloudy....'
    cloudy_input.run_make(dir_=mod_dir, n_proc=4, model_name=mod_prefix)
    print 'Cloudy finished.'
else:
    print 'Not running Cloudy. Skipping to formatting output.'
#---------------------------------------------------------------------
# FORMAT OUTPUT
#---------------------------------------------------------------------
if exec_write_output:
    print 'Starting shell script...\n'
    # fast way to pull needed columns from raw cloudy output
    cloudy_output.format_lines(mod_dir, mod_prefix)
    print 'Shell script finished. Formatting output files...'
    cloudy_output.format_all(mod_dir, mod_prefix)
else:
    print '\n\nNot formatting output. DONE.'
if exec_gen_FSPS_grid:
    print 'Creating FSPS input grids...'
    write_output.PrepOutput(mod_dir, mod_prefix, '_FBHB')
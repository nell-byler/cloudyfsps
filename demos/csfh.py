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

# Function to write the ascii file.
# This is where you set the properties of the
# ionizing spectrum (SSP/CSFH, IMF, FBHB, etc)

def csfh_ascii(fileout='FSPS_csfh.ascii', **kwargs):
    # change these parameters to modify the ionizing source grid
    # default mode is to produce an ascii grid in age and Z,
    # though different variables and more dimensions are possible.
    sp_dict = dict(zcontinuous=1,
                   imf_type=2,
                   sfh=1, #constant sfh
                   const=1.0, #mass formed in const SFH
                   sf_start=0.0, #start time of SFH in Gyr
                   fburst=0.0, #fraction mass formed in inst burst
                   tburst=0.0) #time burst occured
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

# you should set this to your cloudy data directory
ascii_dir = '/Users/Nell/programs/cloudy/c13.01/data/'
# name of ascii file
ascii_file = 'FSPS_csfh.ascii'
# or if there is an already-compiled one you want to use,
# specify here
compiled_ascii = '{}.mod'.format(ascii_file.split('.')[0])

if exec_write_ascii:
    # will not attempt to re-compile if a .mod file already exists
    if not os.path.exists(ascii_dir+compiled_ascii):
        # write ascii file
        csfh_ascii(fileout=ascii_dir+ascii_file)
        # compile ascii file with cloudy
        write_ascii.compile_mod(ascii_dir, ascii_file)
        # check that it was successful
        if not write_ascii.check_compile(ascii_dir, ascii_file):
            print 'bad model compilation, try again'

#---------------------------------------------------------------------
# WRITE CLOUDY INPUT
#---------------------------------------------------------------------
# location to read and write *.in, *.out files
mod_dir = '/Users/Nell/research/newem/output_csfh/'
mod_prefix = 'ZAU'

#modify these as you see fit
#--------------
ages = np.array([1.0e6, 2.0e6, 3.0e6, 5.0e6, 10.0e6])
logUs =  np.array([-4.0, -3.5, -3.0, -2.5, -2.0, -1.5, -1.0])
logZs =  np.array([-2.0, -1.5, -1.0, -0.5, 0.0, 0.2])
# don't need to change these, persay
Rinners =  np.array([19.])
nhs = np.array([10.0])
#--------------
pars = np.array([(Z, a, U, R, ct.calc_4_logQ(logU=U, Rinner=10.0**R, nh=n), n)
                 for Z in logZs
                 for a in ages
                 for U in logUs 
                 for R in Rinners
                 for n in nhs])
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
                         set_name='dopita') #abundance set to use
print 'wrote {} param files'.format(len(pars))
#---------------------------------------------------------------------
# RUN CLOUDY ON ALL INPUT FILES
#---------------------------------------------------------------------
print 'running cloudy....'
cloudy_input.run_make(dir_=mod_dir, n_proc=4, model_name=mod_prefix)
#---------------------------------------------------------------------
# FORMAT OUTPUT
#---------------------------------------------------------------------
print 'running finished, starting shell script'
# fast way to pull needed columns from raw cloudy output
cloudy_output.format_lines(mod_dir, mod_prefix)
print 'shell script finished. formatting output files'
cloudy_output.format_all(mod_dir, mod_prefix)
# this is the file that is input to FSPS
write_output.PrepOutput(mod_dir, mod_prefix, 'CSFH_')
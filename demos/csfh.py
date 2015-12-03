import os
from cloudyfsps import cloudy_input
from cloudyfsps import cloudy_output
from cloudyfsps import cloudytools as ct
from cloudyfsps import write_ascii
from cloudyfsps import write_ascii
import numpy as np
import fsps

zsun = 0.019

def csfh_ascii(fileout='FSPS_csfh.ascii', **kwargs):
    sp_dict = dict(zcontinuous=1,
                   imf_type=2,
                   sfh=1, #constant sfh
                   tau=1.0, #efolding time for exp SFH in Gyr
                   const=1.0, #mass formed in const SFH
                   sf_start=0.0, #start time of SFH in Gyr
                   fburst=0.0, #fraction mass formed in inst burst
                   tburst=0.0) #time burst occured
    sp = fsps.StellarPopulation(**sp_dict)
    ages = 10.**sp.log_age
    lam = sp.wavelengths
    logZs = np.log10(sp.zlegend/zsun)
    modpars = [(age, logZ) for age in ages for logZ in logZs]
    all_fluxs = []
    for logZ in logZs:
        sp.params['logzsol'] = logZ
        all_fluxs.append(sp.get_spectrum()[1]) #lsun per hz
    nmod = len(modpars)
    flat_flux = np.array([all_fluxs[j][i]
                          for i in range(len(ages))
                          for j in range(len(logZs))])
    write_ascii.FileOps(fileout, lam, flat_flux,
                        modpars, ndim=2, npar=2, nmod=nmod)
    return

ascii_file = 'FSPS_csfh.ascii'
ascii_dir = '/astro/users/ebyler/pro/cloudy/data/'
compiled_ascii = '{}.mod'.format(ascii_file.split('.')[0])
if not os.path.exists(ascii_dir+compiled_ascii):
    # write ascii file
    csfh_ascii(fileout=ascii_dir+ascii_file)
    # compile ascii file with cloudy
    write_ascii.compile_mod(ascii_dir, ascii_file)
    if not write_ascii.check_compile(ascii_dir, ascii_file):
        print 'bad model compilation, try again'

# write grid of input files, run cloudy
mod_dir = './output_csfh/'
mod_prefix = 'ZAU'

ages = np.array([1.0e6, 2.0e6, 3.0e6, 5.0e6, 10.0e6])
nhs = np.array([10.0])
logUs =  np.array([-4.0, -3.5, -3.0, -2.5, -2.0, -1.5, -1.0])
Rinners =  np.array([19.])
logZs =  np.array([-2.0, -1.5, -1.0, -0.5, 0.0, 0.2])

pars = np.array([(Z, a, U, R, ct.calc_4_logQ(logU=U, Rinner=10.0**R, nh=n), n)
                 for Z in logZs
                 for a in ages
                 for U in logUs 
                 for R in Rinners
                 for n in nhs])

cloudy_input.param_files(dir_=mod_dir, model_prefix=mod_prefix,
                         cloudy_mod=compiled_ascii,
                         run_cloudy=False,
                         ages=ages,
                         logZs=logZs,
                         logUs=logUs,
                         r_inners=Rinners,
                         nhs=nhs,
                         use_Q=True,
                         set_name='dopita')
print 'wrote {} param files'.format(len(pars))
print 'running cloudy....'
cloudy_input.run_make(dir_=mod_dir, n_proc=4, model_name=mod_prefix)

print 'running finished, starting shell script'

cloudy_output.format_lines(mod_dir, mod_prefix)

print 'shell script finished. formatting output files'

cloudy_output.format_all(mod_dir, mod_prefix)

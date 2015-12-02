import os
import write_input
import cloudy_output
import write_output
from mytools import cloudytools as ct
import numpy as np

#write grid of input files, run cloudy
mod_dir = './output_ND/'
mod_prefix = 'ZAU'

#3 par
#ages = np.array([0.5e6, 1.0e6, 1.5e6, 2.0e6, 3.0e6, 5.0e6, 10.0e6,
#                 50.0e6, 500.0e6, 1.0e9, 5.0e9, 10.0e9])
ages = np.array([0.5e6, 1.0e6, 1.5e6, 2.0e6, 3.0e6, 5.0e6, 10.0e6,
                  50.0e6, 500.0e6,
                  1.0e9, 3.0e9, 5.0e9, 8.0e9, 10.0e9, 12.0e9, 14.0e9])
nhs = np.array([10.0])
logUs =  np.array([-4.0, -3.5, -3.0, -2.5, -2.0, -1.5, -1.0])
Rinners =  np.array([19.])
logZs =  np.array([-1.5, -1.0, -0.75, -0.5, -0.25, 0.0, 0.2])

pars = np.array([(Z, a, U, R, ct.calc_4_logQ(logU=U, Rinner=10.0**R, nh=n), n)
                 for Z in logZs
                 for a in ages
                 for U in logUs 
                 for R in Rinners
                 for n in nhs])

write_input.param_files(dir_=mod_dir, model_prefix=mod_prefix,
                        run_cloudy=False,
                        ages=ages,
                        logZs=logZs,
                        logUs=logUs,
                        r_inners=Rinners,
                        nhs=nhs,
                        use_Q=True,
                        set_name='dopita',
                        dust=False,
                        re_z=False,
                        cloudy_mod='FSPS_IMF2a.mod')

print 'wrote {} param files'.format(len(pars))
print 'running cloudy....'
write_input.run_make(dir_=mod_dir, n_proc=4, model_name=mod_prefix)

print 'running finished, starting shell script'

cloudy_output.format_lines(mod_dir, mod_prefix)

print 'shell script finished. formatting output files'

cloudy_output.format_all(mod_dir, mod_prefix)

write_output.PrepOutput(mod_dir, mod_prefix, 'ND')

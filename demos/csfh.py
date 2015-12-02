import os
import write_input
import cloudy_output
from mytools import cloudytools as ct
import numpy as np
import pdb

# ascii_file = 'FSPS_csfh.ascii'
# ascii_dir = '/astro/users/ebyler/pro/cloudy/data/'
# #write ascii file with default pars
# write_ascii.csfh_main(fileout=ascii_dir+ascii_file)
# #compile ascii file with cloudy
# write_ascii.compile_mod(ascii_dir, ascii_file)
# if not write_ascii.check_compile(ascii_dir, ascii_file):
#     print 'bad model compilation, try again'

#write grid of input files, run cloudy
mod_dir = './output_csfh/'
mod_prefix = 'ZU'

ages = np.array([4.0e6])
nhs = np.array([10.0])
logUs =  np.array([-3.5, -3.0, -2.5, -2.0, -1.5, -1.0])
Rinners =  np.array([19.])
logZs =  np.array([-2.0, -1.5, -1.0, -0.5, 0.0, 0.2])

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
                        set_name='dopita')
print 'wrote {} param files'.format(len(pars))
print 'running cloudy....'
write_input.run_make(dir_=mod_dir, n_proc=4, model_name=mod_prefix)

print 'running finished, starting shell script'

cloudy_output.format_lines(mod_dir, mod_prefix)

print 'shell script finished. formatting output files'

cloudy_output.format_all(mod_dir, mod_prefix)

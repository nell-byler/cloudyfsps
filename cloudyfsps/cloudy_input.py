import os
import numpy as np
import subprocess
import cloudytools as ct
from scipy.interpolate import InterpolatedUnivariateSpline 
import neb_abund

this_dir = os.getcwd()

def write_input(dir_, model_name, to_file=True, verbose=True, **kwargs):
    '''
    write_input('./test/', 'ZAU115', logZ=-0.5, age=5.0e6, logU=-2.0)
    writes standard cloudy input to ./test/ZAU115.in
    defaults: 3 Myr, solar, logU=-1.0, nH=30, r_inner=0.01 pc
    '''
    if to_file:
        file_name = dir_+model_name+'.in'
        f = file(file_name, 'w')
    def this_print(s, eol=True):
        if s is None:
            print '"None" parameter not printed'
        else:
            to_print = s.strip()
            if verbose:
                print(to_print)
            if to_file:
                if eol: to_print += '\n'
                f.write(to_print)
    pars = {'age':3.0e6, #age in years
            'logZ': 0.0, #logZ/Zsol (-2.0 to 0.2)
            'logQ':47.0,
            'logU':-1.0, #log of ionization parameter
            'dens':30.0, # number density of hydrogen
            'r_inner':0.01, #inner radius of cloud
            'r_in_pc':False,
            'use_Q:':True,
            'set_name':'dopita',
            'dust':True,
            're_z':False,
            'cloudy_mod':'FSPS_IMF2a.mod'
            }
    for key, value in kwargs.iteritems():
        pars[key] = value
    #-----------------------------------------------------
    abunds = neb_abund.get_abunds(pars['set_name'],
                                  pars['logZ'],
                                  dust=pars['dust'],
                                  re_z=pars['re_z'])
    
    this_print('////////////////////////////////////')
    this_print('title {0}'.format(model_name.split('/')[-1]))
    this_print('////////////////////////////////////')
    this_print('set punch prefix "{0}"'.format(model_name))
    this_print('set line precision 6')
    ####
    this_print('table star "{0}" age={1:.2e} logz={2:.2f}'.format(pars['cloudy_mod'], pars['age'],pars['logZ']))
    #this_print('table star "FSPS_csfh.mod" age={0:.2e} logz={1:.2f}'.format(pars['age'], pars['logZ']))
    if pars['use_Q']:
        this_print('Q(H) = {0:.3f} log'.format(pars['logQ']))
    else:
        this_print('ionization parameter = {0:.3f} log'.format(pars['logU']))
    ####
    this_print(abunds.solarstr)
    if pars['dust']:
        this_print('metals grains {0:.2f} log'.format(pars['logZ']))
    for line in abunds.elem_strs:
        this_print(line)
    ####
    if pars['r_in_pc']:
        pc_to_cm = 3.08568e18
        r_out = np.log10(pars['r_inner']*pc_to_cm)
    else:
        r_out = pars['r_inner']
    
    this_print('radius {0:.3f} log'.format(r_out))
    this_print('hden {0:.3f} log'.format(np.log10(pars['dens'])))
    this_print('sphere')
    this_print('cosmic ray background')
    this_print('iterate to convergence max=5')
    this_print('stop temperature 100.0')
    this_print('stop efrac -1.0')
    this_print('save last linelist ".lin" "{}/data/cloudy_lines.dat" absolute column'.format(this_dir))
    this_print('save last outward continuum ".outwcont" units Angstrom no title')
    this_print('save last incident continuum ".inicont" units Angstrom no title')
    if to_file:
        print('Input written in {0}'.format(file_name))
        f.close()

def write_make(dir_=None):
    makefile = open('{0}/Makefile'.format(dir_), 'w')
    txt_exe = 'CLOUDY = {0}\n'.format(os.environ['CLOUDY_EXE'])
    txt = """
SRC = $(wildcard ${name}*.in)
OBJ = $(SRC:.in=.out)

#Usage: make -j N name='NAME'
#N is the number of processors
#optional: NAME is a generic name, all models named NAME*.in will be run

all: $(OBJ)

%.out: %.in
\t-$(CLOUDY) < $< > $@
#notice the previous line has TAB in first column
"""
    makefile.write(txt_exe)
    makefile.write(txt)
    makefile.close()

def run_make(dir_=None, n_proc=1, model_name=None):
    if dir_ is None:
        dir_='./'
    to_run = 'cd {0} ; make -j {1:d}'.format(dir_, n_proc)
    if model_name is not None:
        to_run += ' name="{0}"'.format(model_name)
    stdin = None
    stdout = subprocess.PIPE
    print 'running: {0}'.format(to_run)
    proc = subprocess.Popen(to_run, shell=True, stdout=stdout, stdin=stdin)
    proc.communicate()

def print_par_file(dir_, mod_prefix, pars):
    outfile = '{}{}.pars'.format(dir_, mod_prefix)
    f = open(outfile, 'w')
    for i in range(len(pars)):
        par = pars[i]
        pstr = '{0} {1:.2f} {2:.2e} {3:.2f} {4:.2f} {5:.2f} {6:.2f}\n'.format(i+1, *par)
        f.write(pstr)
    f.close()
    return

def param_files(**kwargs):
    nom_dict = {'dir_':'./ftest/',
                'model_prefix':'ZAU',
                'ages':np.arange(1.0e6, 6.0e6, 1.0e6),
                'logZs':np.linspace(-2.0, 0.2, 5),
                'logQs':np.linspace(45,49, 5),
                'logUs':np.linspace(-3.0, -1.0, 5),
                'r_inners':np.array([0.1]),
                'nhs':np.array([30.0]),
                'pc_to_cm':False,
                'run_cloudy':False,
                'set_name':'dopita',
                'use_Q':True,
                'dust':True,
                're_z':False,
                'cloudy_mod':'FSPS_IMF2a.mod'}
    for key, val in kwargs.iteritems():
        nom_dict[key] = val
    print '{} ages, {} logZs, {} logUs'.format(len(nom_dict['ages']),
                                               len(nom_dict['logZs']),
                                               len(nom_dict['logUs']))
    pars = [(Z, a, U, R, ct.calc_4_logQ(logU=U, Rinner=10.0**R, nh=n), n)
            for Z in nom_dict['logZs']
            for a in nom_dict['ages']
            for U in nom_dict['logUs']
            for R in nom_dict['r_inners']
            for n in nom_dict['nhs']]
        
    print '{} models'.format(len(pars))
    full_model_names = ['{}{}'.format(nom_dict['model_prefix'], n+1)
                        for n in range(len(pars))]
    print_par_file(nom_dict['dir_'], nom_dict['model_prefix'], pars)
    #--------------------------------------------
    for par, name in zip(pars, full_model_names):
        write_input(nom_dict['dir_'],
                    name,
                    logZ=par[0],
                    age=par[1],
                    logU=par[2],
                    r_inner=par[3],
                    logQ=par[4],
                    dens=par[5],
                    set_name=nom_dict['set_name'],
                    use_Q=nom_dict['use_Q'],
                    dust=nom_dict['dust'],
                    re_z=nom_dict['re_z'],
                    cloudy_mod=nom_dict['cloudy_mod'])
    #--------------------------------------------
    write_make(dir_=nom_dict['dir_'])
    #--------------------------------------------
    if nom_dict['run_cloudy']:
        run_make(dir_=nom_dict['dir_'], n_proc=4, model_name=nom_dict['model_prefix'])
    


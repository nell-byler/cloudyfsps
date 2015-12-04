import os
from os import listdir
from os.path import isfile, join, splitext
import numpy as np
import subprocess
from .astrotools import air_to_vac
from scipy.interpolate import interp1d
import pkg_resources
import fsps

#grid: 2 files: line, cont

#columns: wavelengths
#rows: models

#header
#wavelength grid
#age, Z, logU
#flux1
#flux2
#flux3
sp = fsps.StellarPopulation()
fsps_lam = sp.wavelengths

class PrepOutput(object):
    def __init__(self, dir_, mod_prefix, mod_suffix, **kwargs):
        self.dir_, self.mod_prefix = dir_, mod_prefix
        self.file_pr = dir_ + mod_prefix
        if mod_suffix is None:
            self.out_pr = dir_ + mod_prefix
        else:
            self.out_pr = dir_ + mod_prefix + mod_suffix
        # each model's final info will be in prefix00.lines, prefix00.cont
        self.line_out = self.out_pr + '.lines'
        self.cont_out = self.out_pr + '.cont'
        self.loadModInfo() # load each model's parameters from prefix.pars
        self.doLineOut() # print ordered emission line wavelengths + fluxes
        self.doContOut() # interp and print neb cont onto FSPS wavelenth arr
        return
    def loadModInfo(self, **kwargs):
        '''
        reads model parameters from "ZAU.pars"
        '''
        name_keys = ['mod_num', 'logZ', 'Age', 'logU', 'logR', 'logQ', 'nH']
        data = np.genfromtxt(self.file_pr+'.pars', names=name_keys)
        self.__setattr__('modpars', data)
        for k in name_keys:
            self.__setattr__(k, data[k])
        return
    def doLineOut(self, **kwargs):
        '''
        prints line fluxes to prefix00.lines file
        '''
        f = open(self.line_out, 'w')
        self.printLineLam(f)
        for pars in self.modpars:
            self.printLineFlu(f, pars) 
        f.close()
        print 'lines: {0:.0f} models to file {1}'.format(self.modpars[-1][0],
                                                         self.line_out)
        return
    def printLineLam(self, f):
        '''
        prints the wavelength array for the emission lines as the second
        line in the output file. converts all wavelengths to vacuum.
        '''
        #read in file containing wavelength info
        linefile = pkg_resources.resource_filename(__name__, "data/ordered_lambda.dat")
        data = np.genfromtxt(linefile)
        data_vac = air_to_vac(data)
        nlines = len(data)
        nmods = np.max(self.mod_num)
        #print header to file
        head_str = '#{0} cols {1:.0f} rows logZ Age logU'.format(nlines, 
                                                               nmods)
        f.write(head_str+'\n')
        #print lambda array
        p_str = ' '.join(['{0:1.6e}'.format(dat) for dat in data_vac])
        f.write(p_str+'\n')
        return
    def printLineFlu(self, f, pars):
        #write model parameters
        tstr = '{0: 2.4e} {1: 2.4e} {2: 2.4e}\n'.format(pars['logZ'],
                                                        pars['Age'],
                                                        pars['logU'])
        f.write(tstr)
        #read in and print emission line intensities (Lsun/Q)
        nst = '{0:.0f}'.format(pars['mod_num'])
        filename = self.file_pr+nst+'.out_lines'
        dat = np.genfromtxt(filename, names=['lam', 'I'])
        I_lin = dat['I']
        I_str = ['{0: 1.4e}'.format(s) for s in I_lin]
        tstr = ' '.join(I_str)
        f.write(tstr+'\n')
        return

    def doContOut(self, **kwargs):
        f = open(self.cont_out, 'w')
        self.printContLam(f)
        for pars in self.modpars:
            self.printContFlu(f, pars) 
        f.close()
        print 'cont: {0:.0f} models to file {1}'.format(self.modpars[-1][0],
                                                         self.cont_out)
        return
    def printContFlu(self, f, pars):
        #write model parameters
        tstr = '{0: 2.4e} {1: 2.4e} {2: 2.4e}\n'.format(pars['logZ'],
                                                        pars['Age'],
                                                        pars['logU'])
        f.write(tstr)
        #read in and print emission line intensities
        nst = '{0:.0f}'.format(pars['mod_num'])
        filename = self.file_pr+nst+'.out_cont'
        # read lambda, incident flux, attenuated incident, diffuse cont
        m_data = np.genfromtxt(filename, names=['lam', 'IF', 'AI', 'DC'])
        # cloudy has vac < 3000AA and air >3000A
        x = air_to_vac(m_data['lam'])
        newx = self.fsps_lam
        fluxs_out = [m_data['IF'], m_data['AI'], m_data['DC']]
        fluxs_out = [m_data['DC']]
        # interpolate them onto FSPS grid
        for y in fluxs_out:
            newy = interp1d(x, y)(newx)
            y_str = ' '.join(['{0: 1.4}'.format(yy) for yy in newy])
            f.write(y_str+'\n')
        return
    def printContLam(self, f):
        '''
        prints header in first line of file, and the FSPS wavelength array
        (for the nebular continuum) as the second line in the output file.
        # nlam cols nmod rows logZ Age logU
        # fsps_lam_1 fsps_lam_2 .... fsps_lam_n
        '''
        #grab fsps wavelength info
        self.__setattr__('fsps_lam', fsps_lam)
        nlam = len(fsps_lam)
        nmods = np.max(self.mod_num)
        #print header to file
        head_str = '#{0} cols {1:.0f} rows logZ Age logU'.format(nlam, nmods)
        f.write(head_str+'\n')
        #print lambda array
        p_str = ' '.join(['{0:1.6e}'.format(lam) for lam in fsps_lam])
        f.write(p_str+'\n')
        return
        

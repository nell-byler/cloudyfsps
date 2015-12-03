import os
from os import listdir
from os.path import isfile, join, splitext
import numpy as np
import subprocess
from .astrotools import air_to_vac
from scipy.interpolate import interp1d
import pkg_resources

#grid: 2 files: line, cont

#columns: wavelengths
#rows: models

#header
#wavelength grid
#age, Z, logU
#flux1
#flux2
#flux3

class PrepOutput(object):
    def __init__(self, dir_, mod_prefix, mod_suffix, **kwargs):
        self.dir_, self.mod_prefix = dir_, mod_prefix
        self.file_pr = dir_ + mod_prefix
        if mod_suffix is None:
            self.out_pr = dir_ + mod_prefix
        else:
            self.out_pr = dir_ + mod_prefix + mod_suffix
        self.line_out = self.out_pr + '.lines'
        self.cont_out = self.out_pr + '.cont'
        self.loadModInfo()
        self.doLineOut()
        self.doContOut()
        return
    def loadModInfo(self, **kwargs):
        name_keys = ['mod_num', 'logZ', 'Age', 'logU', 'logR', 'logQ', 'nH']
        data = np.genfromtxt(self.file_pr+'.pars', names=name_keys)
        self.__setattr__('modpars', data)
        for k in name_keys:
            self.__setattr__(k, data[k])
        return
    def doLineOut(self, **kwargs):
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
        linefile = pkg_resources.resource_string(__name__, "data/ordered_lambda.dat")
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
        #read in and print emission line intensities
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
        m_data = np.genfromtxt(filename, names=['lam', 'IF', 'AI', 'DC'])
        x = air_to_vac(m_data['lam'])
        newx = self.fsps_lam
        fluxs_out = [m_data['IF'], m_data['AI'], m_data['DC']]
        fluxs_out = [m_data['DC']]
        for y in fluxs_out:
            newy = interp1d(x, y)(newx)
            y_str = ' '.join(['{0: 1.4}'.format(yy) for yy in newy])
            f.write(y_str+'\n')
        return
    def printContLam(self, f):
        '''
        prints the wavelength array for the emission lines as the second
        line in the output file. converts all wavelengths to vacuum.
        '''
        #read in file containing wavelength info
        linefile = pkg_resources.resource_string(__name__, "data/fsps_lam.dat")
        data = np.genfromtxt(linefile)
        self.__setattr__('fsps_lam', data)
        nlines = len(data)
        nmods = np.max(self.mod_num)
        #print header to file
        head_str = '#{0} cols {1:.0f} rows logZ Age logU'.format(nlines, nmods)
        f.write(head_str+'\n')
        #print lambda array
        p_str = ' '.join(['{0:1.6e}'.format(dat) for dat in data])
        f.write(p_str+'\n')
        return
        

import os
import sys
import numpy as np
import itertools
from scipy.integrate import simps
#import pyCloudy as pc
#pc.config.cloudy_exe = os.environ["CLOUDY_EXE"]

def calcQ(lamin0, specin0, mstar=1.0, helium=False, f_nu=False):
    '''
    Claculate the number of lyman ionizing photons for given spectrum
    Input spectrum must be in ergs/s/A!!
    Q = int(Lnu/hnu dnu, nu_0, inf)
    '''
    lamin = np.asarray(lamin0)
    specin = np.asarray(specin0)
    c = 2.9979e18 #ang/s
    h = 6.626e-27 #erg/s
    if helium:
        lam_0 = 304.0
    else:
        lam_0 = 911.6
    if f_nu:
        nu_0 = c/lam_0
        inds, = np.where(c/lamin >= nu_0)
        hlam, hflu = c/lamin[inds], specin[inds]
        nu = hlam[::-1]
        f_nu = hflu[::-1]
        integrand = f_nu/(h*nu)
        Q = simps(integrand, x=nu)
    else:
        inds, = np.nonzero(lamin <= lam_0)
        lam = lamin[inds]
        spec = specin[inds]
        integrand = lam*spec/(h*c)
        Q = simps(integrand, x=lam)*mstar
    return Q

def calcU_avg(lamin, specin, Rinner=0.01, nh=100.0, eff=1.0, mass=1.0):
    '''
    Calculate <U>, the average ionization parameter
    '''
    Q = calcQ(lamin, specin)*mass
    Rin = Rinner*3.09e18
    alphab = 2.59e-13
    c = 2.9979e10
    U = ((3.0*Q*nh*eff**2)/(4.0*np.pi))**(1./3)*alphab**(2./3)/c
    return U
def calcU(lamin=None, specin=None, Rinner=0.01, nh=30.0, Q=None):
    '''
    Calculate U, the ionization parameter
    '''
    if Q is None:
        Q = calcQ(lamin, specin)
    Rin = Rinner*3.09e18
    c = 2.9979e10
    return Q/(4.0*np.pi*Rin**2.0*nh*c)

def calc_4_logQ(logU=None, Rinner=None, nh=None, logQ=None):
    c = 2.9979e10
    if Rinner > 500.0:
        #means it is in cm
        Rin = Rinner
    else:
        Rin = Rinner*3.09e18
    Q = 10.0**logU*(4.0*np.pi*Rin**2.0*nh*c)
    return np.log10(Q)

def calcRs(lamin, specin, eff=1.0, nh=100.0):
    '''
    Calculate the schwarzchild radius
    '''
    alphab = 2.59e-13
    Q = calcQ(lamin, specin)
    Rs = (3.0*Q/(4.0*np.pi*nh*nh*eff*alphab))**(1./3)
    return Rs

def find_nearest(array, val):
    '''
    shortcut to find element in array nearest to val
    returns index
    '''
    return (np.abs(array-val)).argmin()

def grouper(n, iterable):
    '''
    Iterate through array in groups of n
    '''
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk

#-----------------------------------------------------------------------------

class FileOps:
    '''
    Print FSPS data into ascii files readable by CLOUDY
    Calling sequence:
        FileOps('outfile.ascii', lamda_array, spec_array, model_array, **kwargs)
    Dictionary with header information - change any of these values by
    inputting them as kwargs.
    '''
    def __init__(self, outfile, lam, flu, mods, **kwargs):
        self.nom_dict = {'nmod': 11, 'ndim': 1, 'npar':1, 'nfreq':1221,
                         'xax':'lambda', 'conv1':1.0, 'f_type':'F_lambda',
                         'conv2':1.0, 'par1':'Age', 'par2':'Z'}
        for key, value in kwargs.items():
            if key in self.nom_dict:
                self.nom_dict[key] = value
        self.file = open(outfile, 'w')
        #interpolate onto linear grid
        
        FileOps.write_header(self, mods)
        FileOps.write_data(self, lam)
        #correct to erg/s/AA
        solar_lum = 3.839e33
        fluout = flu*solar_lum
        for i in range(self.nom_dict['nmod']):
            FileOps.write_data(self, fluout[i,:])
        self.file.close()
    
    def write_header(self, mods):
        '''
        Header for cloudy ascii files
        '''
        self.file.write("  20060612\n")
        self.file.write("  %i\n" %self.nom_dict['ndim'])
        self.file.write("  %i\n" %self.nom_dict['npar'])
        self.file.write("  %s\n" %self.nom_dict['par1'])
        if self.nom_dict['npar'] > 1:
            self.file.write("  %s\n" %self.nom_dict['par2'])
        self.file.write("  %i\n" %self.nom_dict['nmod'])
        self.file.write("  %i\n" %self.nom_dict['nfreq'])
        self.file.write("  %s\n" %self.nom_dict['xax'])
        self.file.write("  %.8e\n" %self.nom_dict['conv1'])
        self.file.write("  %s\n" %self.nom_dict['f_type'])
        self.file.write("  %.8e\n" %self.nom_dict['conv2'])
        for chunk in grouper(4, mods):
            if self.nom_dict['npar'] > 1:
                self.file.write("  " + "  ".join("%1.3e  %.1f" %(x[0], x[1]) for x in chunk) + "\n")
            else:
                self.file.write("  " + "  ".join("%1.3e" %x for x in chunk) + "\n")
    
    def write_data(self, array):
        '''
        write array with 5 items per line in format 1.0000e+00
        '''
        for chunk in grouper(5, array):
            self.file.write("  " + "  ".join("%1.4e" %x for x in chunk) + "\n")

#-----------------------------------------------------------------------------

import os
from os import listdir
from os.path import isfile, join, splitext
import numpy as np
import subprocess
from scipy.interpolate import InterpolatedUnivariateSpline
from astropy.convolution import Gaussian1DKernel
from astropy.convolution import convolve
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def format_lines(dir_, model_prefix, **kwargs):
    filelist = [f.split('.')[0] for f in listdir(dir_) if (isfile(join(dir_, f)) and f.split('.')[-1] == 'out')]
    modnums = np.array([int(f.strip(model_prefix)) for f in filelist])
    startnum = modnums.min()
    endnum = modnums.max()
    to_run = 'cd {} ; ./mk_linefile.sh {} {}'.format(dir_, startnum, endnum)
    stdout = subprocess.PIPE
    proc = subprocess.Popen(to_run, shell=True, stdout=stdout)
    proc.communicate()
    
def format_output(dir_, model_prefix, modnum, modpars, **kwargs):
    logZ, age, logU, logR, logQ, nH = modpars[1:7]
    
    dist_fact = 4.0*np.pi*(10.0**logR)**2.0
    lsun = 3.846e33
    c = 2.9979e18 #ang/s
    
    line_info = np.genfromtxt('{}{}{}.lineflux'.format(dir_,
                                                       model_prefix,
                                                       modnum))
    inds = np.argsort(line_info[:,0])
    line_wav = line_info[:,0][inds]
    #line luminosity in solar lums per Q
    line_flu = line_info[:,1][inds]/lsun/(10.0**logQ)
    print_file = '{}{}{}.out_lines'.format(dir_, model_prefix, modnum)
    print 'Lines were printed to file {}'.format(print_file)
    f = open(print_file, 'w')
    f.write('# lam (A) L (Lsun/Q)\n')
    for i in range(len(line_wav)):
        printstring = '{0:.6e} {1:.6e}\n'.format(line_wav[i], line_flu[i])
        f.write(printstring)
    f.close()
    
    cont_data = np.genfromtxt('{}{}{}.outwcont'.format(dir_,
                                                       model_prefix,
                                                       modnum),
                              skip_header=1)
    cont_1 = cont_data[:,1] * dist_fact / lsun * cont_data[:,0] / c
    cont_2 = cont_data[:,2] * dist_fact / lsun * cont_data[:,0] / c
    
    contwav = cont_data[:,0][::-1]
    cont_AI = cont_1[::-1] /(10.0**logQ) #attenuated incident
    cont_DC = cont_2[::-1] /(10.0**logQ) #diffuse continuum
    
    ini_data = np.genfromtxt('{}{}{}.inicont'.format(dir_, model_prefix, modnum), skip_header=1)
    # F_nu / (nu=c/lambda) per solar lum
    icont = ini_data[:,1] * dist_fact / lsun * ini_data[:,0] / c
    icont_wav = ini_data[:,0][::-1]
    cont_IF = icont[::-1]/(10.0**logQ) #initial flux
    #####
    #####
    print_file = '{}{}{}.out_cont'.format(dir_, model_prefix, modnum)
    print 'The continuum was printed to file {}'.format(print_file)
    f = open(print_file, 'w')
    f.write('# lam (ang) incid (lsun/hz) attenuated_incid (lsun/hz) diffuse_cont (lsun/hz)\n')
    
    for i in range(len(contwav)):
        printstring = '{0:.6e} {1:.6e} {2:.6e} {3:.6e}\n'.format(contwav[i],
                                                                 cont_IF[i],
                                                                 cont_AI[i],
                                                                 cont_DC[i])
        f.write(printstring)
    f.close()
    return

def format_all(dir_, model_prefix, **kwargs):
    filelist = [f.split('.')[0] for f in listdir(dir_) if (isfile(join(dir_, f)) and f.split('.')[-1] == 'out')]
    modnums = np.array([int(f.strip(model_prefix)) for f in filelist])
    data = np.genfromtxt(dir_+model_prefix+'.pars')
    [format_output(dir_, model_prefix, num, data[num-1]) for num in modnums]
    return

def spec(dir_, model_prefix, modnum, make_plot=False, print_line=False, conv=False, **kwargs):
    '''
    numpts = number of pts in output spectrum
    contrast = multiplier for emission lines to account for covering factor
    '''
    FWHM = kwargs.get('FWHM', 2.3) #angstroms
    numpts = kwargs.get('numpts', 5000)
    startwav = kwargs.get('startwav', 3000.0)
    endwav = kwargs.get('endwav', 9000.0)
    c = 2.9979e18
    wav = np.linspace(startwav, endwav, numpts)
    dwav = np.mean(np.diff(wav))
    flux = np.zeros(numpts)
    
    line_info = np.genfromtxt('{}{}{}.out_lines'.format(dir_, model_prefix, modnum), skip_header=1)
    line_wav, line_flu = line_info[:,0], line_info[:,1]
    aa, = np.where((line_wav >= startwav) & (line_wav <= endwav))
    linewav, lineflux = line_wav[aa], line_flu[aa]
    
    if print_line:
        wav_id = kwargs.get('wav_id', 6562.85)
        #hb 4861.36, n2 6584.00, o3 5007.00
        matchind = np.argmin(np.abs(line_wav - wav_id))
        print_flux = line_flu[matchind]
        return print_flux
    
    print 'Adding emission lines...'
    for i in range(len(linewav)):
        idx = find_nearest(wav, linewav[i])
        flux[idx] += lineflux[i]*wav[idx]/dwav
    
    print 'Adding continuum...'
    cont_info = np.genfromtxt('{}{}{}.out_cont'.format(dir_, model_prefix, modnum), skip_header=1)
    
    contwav_in = cont_info[:,0]
    contflux_in = (cont_info[:,2]+cont_info[:,3])* c / cont_info[:,0]
    a, = np.where((contwav_in >= startwav) & (contwav_in <= endwav))
    contwav, contflux = contwav_in[a], contflux_in[a]
    
    scontflux = InterpolatedUnivariateSpline(contwav, contflux)(wav)
    flux += scontflux
    
    if conv:
        observed = convolve_spec(numpts, wav, flux, FWHM)
    else:
        observed = flux/c*wav
    if make_plot:
        plt.plot(wav, observed)
    
    return (wav, observed)


def find_nearest(array, value):
    idx = (np.abs(array-value)).argmin()
    return idx

def convolve_spec(numpts, wav, flux, FWHM):
    
    gauss_kernel = Gaussian1DKernel(width=FWHM/2.355)
    out = convolve(flux, gauss_kernel, boundary='extend')
    
    return  out

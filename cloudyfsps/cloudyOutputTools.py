#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (division, print_function, absolute_import,
                        unicode_literals)
#__all__ = ["format_output"]

import numpy as np
import subprocess
import pkg_resources

def formatCloudyOutput(dir_, model_prefix, modnum, modpars, **kwargs):
    '''
    for formatting the output of a single cloudy job
    '''
    # model information
    logZ, age, logU, logR, logQ, nH = modpars[1:7]
    
    dist_fact = 4.0*np.pi*(10.0**logR)**2.0 # cm**2
    lsun = 3.846e33 # erg/s
    c = 2.9979e18 #ang/s
    
    oldfile = "{}{}{}.lin".format(dir_, model_prefix, modnum)
    newfile = "{}{}{}.lineflux".format(dir_, model_prefix, modnum)
    print_file = "{}{}{}.out_lines".format(dir_, model_prefix, modnum)
    # read cloudy output
    dat = np.genfromtxt(oldfile, skip_header=2, delimiter="\t",
                        dtype="S20,f8")
    line_names = [d[0] for d in dat]
    datflu = np.array([d[1] for d in dat])
    # non-ordered wavelengths
    wavfile = pkg_resources.resource_filename(__name__, "data/shell_lambda.dat")
    wl = np.genfromtxt(wavfile)
    # sort them by wavelength
    sinds = np.argsort(wl)
    output = np.column_stack((wl[sinds], datflu[sinds]))
    np.savetxt(newfile, output, fmt=str("%4.6e"))
    # save line luminosity in solar lums per Q
    line_wav = wl[sinds]
    line_flu = datflu[sinds]/lsun/(10.0**logQ)
    print_output = np.column_stack((line_wav, line_flu))
    np.savetxt(print_file, print_output, fmt=(str("%.6e"),str("%.6e")))
    # print to file
    print("Lines were printed to file {}".format(print_file))
    cont_data = np.genfromtxt("{}{}{}.outwcont".format(dir_, model_prefix, modnum), skip_header=1)
    # cont is nu L_nu / (4 pi R**2): Hz * (erg/s/Hz) * (1/cm**2)
    # [erg / s / cm^2 ] -> [ erg / s / Hz ]
    atten_0, diffuse_0  = cont_data[:,1], cont_data[:,2]
    ang_0 = cont_data[:,0]
    nu_0 = c / cont_data[:,0]
    # reverse arrays
    atten_in, diffuse_in = atten_0[::-1], diffuse_0[::-1]
    ang = ang_0[::-1]
    nu = nu_0[::-1]
    # attenuated incident continuunm
    atten_out = atten_in / nu * dist_fact / pow(10., logQ)/ lsun
    # diffuse continuum
    diffuse_out = diffuse_in / nu * dist_fact / pow(10., logQ) / lsun
    
    inidata = np.genfromtxt("{}{}{}.inicont".format(dir_, model_prefix, modnum), skip_header=1)
    iang_0 = inidata[:,0]
    inu_0 = c / iang_0
    inu = inu_0[::-1]
    iang = iang_0[::-1]
    incid_0 = inidata[:,1]
    incid_in = incid_0[::-1]
    #
    incid_out = incid_in / inu * dist_fact / pow(10., logQ) / lsun
    # F_nu / (nu=c/lambda) per solar lum
    #####
    #####
    print_file = "{}{}{}.out_cont".format(dir_, model_prefix, modnum)
    print("The continuum was printed to file {}".format(print_file))
    f = open(print_file, "w")
    f.write("# lam (ang) incid (lsun/hz/Q) attenuated_incid (lsun/hz/Q) diffuse_cont (lsun/hz/Q)\n")
    
    for i in range(len(ang)):
        printstring = "{0:.6e} {1:.6e} {2:.6e} {3:.6e}\n".format(ang[i], incid_out[i], atten_out[i], diffuse_out[i])
        f.write(printstring)
    f.close()
    return


def formatAllOutput(dir_, mod_prefix):
    '''
    for formatting output after running a batch of cloudy jobs
    '''
    data = np.genfromtxt(dir_+mod_prefix+".pars")
    def get_pars(modnum):
        return data[np.int(modnum)-1, 1:]
    for modnum in data[:,0]:
        mnum = np.int(modnum)
        formatCloudyOutput(dir_, mod_prefix, mnum, get_pars(mnum))
    return

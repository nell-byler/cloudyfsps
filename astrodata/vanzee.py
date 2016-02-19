#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)
__all__ = ["plot_bpt", "plot_NO"]

import numpy as np
import matplotlib.pyplot as plt
import pkg_resources

def plot_bpt(var_label, ax=None, line_ratio='NII', **kwargs):
    '''
    vanzee.plot_bpt(True, auto_corr=True)
    '''
    auto_corr =  kwargs.get('auto_corr', True)
    if var_label:
        lab = 'Van Zee (1998)'
    else:
        lab = '__nolegend__'
    linefile = pkg_resources.resource_filename(__name__, "data/vanzee_lines.dat")
    OII,e_OII,NeIII,e_NeIII,OIII,e_OIII,OI,e_OI,SIII,e_SIII,Ha,e_Ha,NII,e_NII,SII,e_SII,ArIII,e_ArIII,cHb,e_cHb = np.genfromtxt(linefile, delimiter=';', comments='#', unpack=True)
    # Van Zee uses [O III] 4959 + 5007 and [N II] 6548 + 6584
    # removing contribution from doublet lines I_b = 2.88*I_a
    if line_ratio[-1] == 'a' or line_ratio[-1] == 'b':
        corr=np.log10(3.0/4.0)
    else:
        corr=0.0
    # assume standard y axis
    y = np.log10(OIII) + corr
    yerr = e_OIII/(OIII*np.log(10))
    def calc_err(x, xerr, y, yerr):
        err = ((xerr/(x*np.log(10)))**2.0 + (yerr/(y*np.log(10)))**2.0)**0.5
        return err
    if line_ratio[0] == 'N':
        x = np.log10(NII/Ha) + corr
        xerr = calc_err(NII, e_NII, Ha, e_Ha)
    if line_ratio[0] == 'S':
        x = np.log10(SII/Ha) + corr
        xerr = calc_err(SII, e_SII, Ha, e_Ha)
    if line_ratio == 'OI':
        x = np.log10(OI/Ha) + corr
        xerr = calc_err(OI, e_OI, Ha, e_Ha)
    if line_ratio == 'OII':
        y = np.log10(OIII/OII)
        yerr = calc_err(OIII, e_OIII, OII, e_OII)
        x = np.log10(NII/OII)
        xerr = calc_err(NII, e_NII, OII, e_OII)
    if line_ratio == 'R23':
        y = np.log10(OIII/OII)
        yerr = calc_err(OIII, e_OIII, OII, e_OII)
        x = np.log10(OII + OIII)
        xerr = e_OIII/(OIII*np.log(10))
    if ax is None:
        ax = plt.gca()
    ax.errorbar(x,y,xerr=xerr, yerr=yerr,
                capsize=0, fmt='s', color='white', ecolor='k', 
                label=lab)
    return


def get_abunds():
    '''
    returns data, with column names
          temp, logO, logOerr, logNO, logNOerr
          T(O++), log(O/H), log(N/O)
    '''
    linefile = pkg_resources.resource_filename(__name__, "data/vanzee_abund.dat")
    data = np.genfromtxt(linefile, delimiter='\t',
                         names='temp, logO, logOerr, logNO, logNOerr')
    return data

def plot_NO(ax=None, lab='__nolabel__', plot_dop=True, **kwargs):
    data = get_abunds()
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    ax.errorbar(data['logO'], data['logNO'],
                xerr=data['logOerr'], yerr=data['logNOerr'],
                marker='o', color='grey', alpha=0.8, linestyle='None',
                markersize=8, label=lab)
    if plot_dop:
        xx = np.array([7.39, 7.5, 7.69, 7.99, 8.17, 8.39, 8.69, 8.8, 8.99, 9.17, 9.39])
        yy = np.array([-2. , -1.97, -1.92, -1.78, -1.68, -1.53, -1.29, -1.2 , -1.03, -0.84, -0.56])
        
    ax.set_xlabel('12 + log (O/H)')
    ax.set_ylabel('log (N/O)')
    return

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)
__all__ = ["plot_bpt"]

import numpy as np
import matplotlib.pyplot as plt
import pkg_resources

c = 2.9979e10

def plot_bpt(logq_val='all', z_val=1.0, kappa_val=20, label='Dopita (2013)',
             line_ratio='NIIb', ax=None, color='k', tcolor='k',
             lw=2, make_faint=False, alpha=0.5, zlims=(-1.3, 0.7),
             **kwargs):
    '''
    dopita.plot_bpt(logq_val='all', color='blue', use_doublet=True)
    '''
    linefile = pkg_resources.resource_filename(__name__, "data/dopita_lines.dat")
    Z, kappa, logq, OIIa, OIIb, OIIIa, OIIIb, OI, NIIa, Ha, NIIb, SIIa, SIIb = np.genfromtxt(linefile, comments='#', delimiter=';', missing_values='  ', filling_values=np.inf, unpack=True)
    data = dict(Z=Z, kappa=kappa, logq=logq, OIIa=OIIa, OIIb=OIIb, OIIIa=OIIIa,
                OIIIb=OIIIb, OI=OI, NIIa=NIIa, Ha=Ha, NIIb=NIIb, SIIa=SIIa,
                SIIb=SIIb)
    if line_ratio in ['NII', 'SII']:
        rat_x = np.log10((data[line_ratio+'a']+data[line_ratio+'b'])/data['Ha'])
        rat_y = np.log10(data['OIIIa']+data['OIIIb'])
    if line_ratio in ['NIIb','OI']:
        rat_x = np.log10(data[line_ratio]/data['Ha'])
        rat_y = np.log10(data['OIIIb'])
    if line_ratio == 'OII':
        rat_x = np.log10((data['NIIa']+data['NIIb'])/(data['OIIa']+ data['OIIb']))
        rat_y = np.log10((data['OIIIa']+data['OIIIb'])/(data['OIIa']+ data['OIIb']))
    if line_ratio == 'R23':
        rat_x = np.log10((data['OIIIa'] + data['OIIIb'] + data['OIIa'] + data['OIIb']))
        rat_y = np.log10((data['OIIIa']+data['OIIIb'])/(data['OIIa']+ data['OIIb']))
    if ax is None:
        ax = plt.gca()
    if logq_val == 'all':
        inds, = np.where((data['kappa'] == kappa_val) &
                         (np.log10(data['Z']) >= zlims[0]) &
                         (np.log10(data['Z']) <= zlims[1]))
        if make_faint:
            zinds, = np.where((data['kappa'] == kappa_val) &
                              (np.log10(data['Z']) > zlims[1]))
    else:
        inds, = np.where((data['logq'] == logq_val) &
                         (data['Z'] == z_val) &
                         (data['kappa'] == kappa_val))
    do_grid = kwargs.get('do_grid', True)
    add_labels = kwargs.get('add_labels', False)
    if do_grid:
        i=0
        for q in np.unique(data['logq']):
            inds, = np.where((data['logq'] == q) & (data['kappa'] == kappa_val) & (np.log10(data['Z']) >= zlims[0]) & (np.log10(data['Z']) <= zlims[1]))
            zinds, = np.where((data['logq'] == q) & (data['kappa'] == kappa_val) & (np.log10(data['Z']) >= zlims[1]))
            if i == 0:
                ax.plot(rat_x[inds], rat_y[inds], color=color, label=label, lw=lw)
            else:
                ax.plot(rat_x[inds], rat_y[inds], color=color,
                        label='__nolegend__', lw=lw)
            if make_faint:
                ax.plot(rat_x[zinds], rat_y[zinds], color=color,
                        label='__nolegend__', lw=lw, alpha=alpha)
            if add_labels:
                ax.annotate('{0:.1f}'.format(np.log10((10.0**q)/c)),
                            xy=(rat_x[inds][-1], rat_y[inds][-1]),
                            xycoords='data',
                            xytext=(-10,0), textcoords='offset points',
                            horizontalalignment='right',
                            verticalalignment='bottom',
                            size=18, color=tcolor)
            i+=1
        for z in np.unique(data['Z']):
            if (np.log10(z) >= zlims[0]) & (np.log10(z) >= zlims[0]):
                inds, = np.where((data['Z'] == z) & (data['kappa'] == kappa_val))
                ax.plot(rat_x[inds], rat_y[inds], color=color, lw=lw)
                if add_labels:
                    ax.annotate('{0:.1f}'.format(np.log10(z)),
                                xy=(rat_x[inds][-1], rat_y[inds][-1]),
                                xycoords='data',
                                xytext=(0,-10), textcoords='offset points',
                                horizontalalignment='left',
                                verticalalignment='top',
                                size=18, color=tcolor)
            elif np.log10(z) >= zlims[1]:
                inds, = np.where((data['Z'] == z) & (data['kappa'] == kappa_val))
                ax.plot(rat_x[inds], rat_y[inds], color=color, lw=lw, alpha=alpha)
    return


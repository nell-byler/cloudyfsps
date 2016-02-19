#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

from cloudyfsps import outObj as ob
from astrodata import dopita

# this code assumes you have run "csfh.py"
# to produce a grid of cloudy models and now
# want to look at the data

dir_ = './output_csfh/'
mod_prefix='ZAU'
# Read in output
csf = ob.allmods(dir_, mod_prefix) #read_out=True for dust
# this is a python object with lots of model info.
# Line strengths, gas properties and ionizing properties, etc.

#Plot general BPT diagram
ages = [0.5e6, 1.0e6, 2.0e6, 4.0e6, 6.0e6]
cols = ['#7fcdbb','#41b6c4','#1d91c0','#225ea8','#0c2c84']

fig = plt.figure()
ax = fig.add_subplot(111)
for age, col in zip(ages, cols):
    pd=False
    var_label=False
    if age == 1.0e6: #only plot the observed data once
        pd=True
    if age == 2.0e6: #only plot the labels once
        var_label=True
    csf.makeBPT(ax=ax, val1=age, color=col, line_ratio='NIIb',
                par_label='{0:.1f} Myr'.format(age*1.0e-6),
                plot_data=pd, var_label=var_label)
plt.title('CSFH Models')
fig.savefig('CSFH_BPT.png')

#Plot comparison with Dopita data
age = 4.0e6
col = '#08519c'
dcol = '#a50f15'
pd=True
var_label=True
fig = plt.figure()
ax = fig.add_subplot(111)
dopita.plot_bpt(line_ratio='NIIb', color=dcol, tcolor=dcol, kappa_val=np.inf)
csf.makeBPT(ax=ax, val1=age, color=col, line_ratio='NIIb',
            par_label='{0:.1f} Myr CSFH'.format(age*1.0e-6),
            plot_data=pd, var_label=var_label)


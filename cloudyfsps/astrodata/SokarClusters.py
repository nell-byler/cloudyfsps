#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)
__all__ = ["plot_bpt", "plot_NO"]

import numpy as np
import matplotlib.pyplot as plt
import pkg_resources

def get_cluster_lines(cluster_type='WR'):
    '''
    returns data, with column names
          temp, logO, logOerr, logNO, logNOerr
          T(O++), log(O/H), log(N/O)
    '''
    if cluster_type == 'WR':
        fl = "data/WRclusters.dat"
    else:
        fl = "data/nonWRclusters.dat"
    filename = pkg_resources.resource_filename(__name__, fl)
    
    data = np.genfromtxt(linefile, dtype=None, names=True,
                         delimiter='\t', skip_header=4)
    n_col = len(dat[0])
    names = [dat.dtype.names[i] for i in range(1,n_col-1)]
    linelam = [float(dat[0][i]) for i in range(1,n_col-1)]
    lines = {}
    for name in names:
        sarr = dat[name][1::]
        farr = np.array([float(x.split('(')[0])
                         if x.split('(')[0] != ' ... '
                         else -99.9
                         for x in sarr])
        lines[name] = farr
    return (linelam, names, lines)

def return_ratio(numerator=['NII_6584', 'NII_6548'], denominator='Ha',
                 lines):
    tops = np.sum([lines[n] for n in numerator], axis=0)
    bottoms = lines[denominator]
    return np.log10(tops/bottoms)

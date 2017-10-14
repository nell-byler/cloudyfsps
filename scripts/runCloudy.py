#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import

import os
import sys
import subprocess
import numpy as np
from cloudyfsps.cloudyOutputTools import formatCloudyOutput

use_extended_lines=False

def get_pars(dir_, mod_prefix, modnum):
    '''
    reads from your/mod/dir/PREFIX.pars
    order is:
    logZ, Age, logU, logR, logQ, nH, efrac, gas_logZ
    '''
    data = np.genfromtxt(dir_+mod_prefix+".pars")
    return data[np.int(modnum)-1, 1:]

def output_OK(fl):
    '''
    looks in PREFIX123.out for 'Cloudy exited OK'
    '''
    f = open(fl, 'r')
    l = f.readlines()[-1]
    if 'OK' in l:
        return True
    else:
        return False
def main(argv):
    fulloutfile=argv[0]
    dir_='/'.join(fulloutfile.split('/')[0:-1])+'/'
    fname = fulloutfile.split('/')[-1]
    mod_prefix=fname.split('.out')[0][0:3]
    modnum=fname.split('.out')[0][3::]
    if os.path.exists(fulloutfile):
        if output_OK(fulloutfile):
            print("Cloudy exited OK.")
            print("Formatting output...")
            modpars = get_pars(dir_, mod_prefix, modnum)
            formatCloudyOutput(dir_, mod_prefix, modnum, modpars,
                               use_extended_lines=use_extended_lines)
        else:
            print("CLOUDY ERROR in {}. Stopping.".format(fname))
    else:
        print("ERROR, no outfile. Stopping.")

if __name__ == "__main__":
    main(sys.argv[1:])

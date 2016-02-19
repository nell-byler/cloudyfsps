#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function, absolute_import

import os
import sys
import subprocess
import numpy as np
from cloudyfsps.cloudyOutputTools import formatCloudyOutput

def get_pars(dir_, mod_prefix, modnum):
    data = np.genfromtxt(dir_+mod_prefix+".pars")
    return data[np.int(modnum)-1, 1:]

def main(argv):
    dir_, mod_prefix, modnum = argv[0], argv[1], argv[2]
    infile = mod_prefix + modnum + ".in" # removed dir
    outfile = mod_prefix + modnum + ".out"
    cloudy_exe = os.environ["CLOUDY_EXE"]
    print("Your CLOUDY_EXE env is set to: {}".format(cloudy_exe))
    to_run = "cd {0} ; {1} {2}".format(dir_, cloudy_exe, infile)
    print("running {}{}".format(mod_prefix, modnum))
    proc = subprocess.Popen(to_run, shell=True)
    proc.communicate()
    print("CLOUDY finished running.")
    if os.path.exists(dir_ + outfile):
        print("{} exists. Formatting output.".format(outfile))
        modpars = get_pars(dir_, mod_prefix, modnum)
        formatCloudyOutput(dir_, mod_prefix, modnum, modpars)
    else:
        print("No outfile. Stopping.")

if __name__ == "__main__":
    main(sys.argv[1:])

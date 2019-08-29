#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import object

import numpy as np
import pkg_resources
import fsps
import os
import linecache
#grid: 2 files: line, cont
#columns: wavelengths
#rows: models
#header
#wavelength grid
#age, Z, logU
#flux1
#flux2
#flux3

###
# reads from ZAU***.out_lines, ZAU***.out_cont
# produces ZAU_**.lines, ZAU_**.cont
###
class writeFormattedOutput(object):
    #sp = fsps.StellarPopulation()
    #fsps_lam = sp.wavelengths
    def __init__(self, dir_, mod_prefix, mod_suffix,
                 use_extended_lines=False, more_info=False,**kwargs):
        '''
        writeFormattedOutput(mod_dir, 'ZAU', 'BPASS')
        '''
        self.dir_, self.mod_prefix = dir_, mod_prefix
        self.file_pr = dir_ + mod_prefix
        if mod_suffix is None:
            self.out_pr = dir_ + mod_prefix
        else:
            self.out_pr = dir_ + mod_prefix + mod_suffix
        # each model's final info will be in prefix00.lines, prefix00.cont
        self.line_out = self.out_pr + ".lines"
        self.cont_out = self.out_pr + ".cont"
        # load each model's parameters from prefix.pars
        self.loadModInfo()
        # print ordered emission line wavelengths + fluxes
        self.doLineOut(use_extended_lines=use_extended_lines,
                       more_info=more_info)
        # interp and print neb cont onto FSPS wavelenth arr
        self.doContOut()
        return
    def loadModInfo(self, **kwargs):
        '''
        reads model parameters from "ZAU.pars"
        '''
        name_keys = ["mod_num", "logZ", "Age", "logU", "logR", "logQ", "nH", "efrac"]
        data = np.genfromtxt(self.file_pr+".pars", unpack=True)
        ddata = {}
        for i,key in enumerate(name_keys):
            ddata[key] = data[i]
            self.__setattr__(key, data[i])
        self.__setattr__("modpars", ddata)
        self.NZ = len(np.unique(self.logZ))
        self.NA = len(np.unique(self.Age))
        self.NU = len(np.unique(self.logU))
        return
    def doLineOut(self, more_info=False, **kwargs):
        '''
        prints line fluxes to prefix00.lines file
        '''
        f = open(self.line_out, "w")
        self.printLineLam(f, **kwargs)
        for n in self.mod_num:
            self.printLineFlu(f, n.astype(int), more_info=more_info)
        f.close()
        print("lines: {0:.0f} models to file {1}".format(self.mod_num[-1], self.line_out))
        return
    def printLineLam(self, f, use_extended_lines=False):
        '''
        prints the wavelength array for the emission lines as the second
        line in the output file. converts all wavelengths to vacuum.
        '''
        #read in file containing wavelength info
        if use_extended_lines:
            linefile = pkg_resources.resource_filename(__name__, "data/orderedLinesEXT.dat")
        else:
            linefile = pkg_resources.resource_filename(__name__, "data/orderedLines.dat")
        data_vac = np.genfromtxt(linefile)
        #data_vac = air_to_vac(data) # new file is already in vac
        nlines = len(data_vac)
        nmods = np.max(self.mod_num)
        #print header to file
        head_str = "#{0} cols {1:.0f} rows {2} logZ {3} Age {4} logU".format(nlines, nmods, self.NZ, self.NA, self.NU)
        f.write(head_str+"\n")
        #print lambda array
        p_str = " ".join(["{0:1.6e}".format(dat) for dat in data_vac])
        f.write(p_str+"\n")
        return
    def printLineFlu(self, f, n, more_info=False):
        #write model parameters
        if more_info:
            tstr = linecache.getline(self.file_pr+'.pars', n)
        else:
            tstr = "{0:2.4e} {1:2.4e} {2:2.4e}\n".format(self.logZ[n-1], self.Age[n-1], self.logU[n-1])
        f.write(tstr)
        #read in and print emission line intensities (Lsun/Q)
        nst = "{0}".format(n)
        filename = self.file_pr+nst+".out_lines"
        lam, flu = np.genfromtxt(filename, unpack=True)
        I_str = ["{0:1.4e}".format(s) for s in flu]
        tstr = " ".join(I_str)
        f.write(tstr+"\n")
        return
    def doContOut(self, **kwargs):
        f = open(self.cont_out, "w")
        self.printContLam(f)
        for num in self.modpars['mod_num']:
            iind = num.astype(int)
            pars = dict(logZ=self.logZ[iind-1],
                        Age=self.Age[iind-1],
                        nH=self.nH[iind-1],
                        logQ=self.logQ[iind-1],
                        logU=self.logU[iind-1],
                        logR=self.logR[iind-1],
                        mod_num=iind,
                        efrac=self.efrac[iind-1])
            self.printContFlu(f, pars)
        f.close()
        print("cont: {0:.0f} models to file {1}".format(self.modpars['mod_num'][-1], self.cont_out))
        return
    def printContFlu(self, f, pars):
        #write model parameters
        tstr = "{0:2.4e} {1:2.4e} {2:2.4e}".format(pars["logZ"],
                                                   pars["Age"],
                                                   pars["logU"])
        f.write(tstr+"\n")
        #read in and print emission line intensities
        nst = "{0}".format(pars["mod_num"])
        filename = self.file_pr+nst+".out_cont"
        # read lambda, diffuse cont
        mdata = np.genfromtxt(filename)
        lam = mdata[:,0]
        flu = mdata[:,1]
        y_str = " ".join(["{0:1.4}".format(y) for y in flu])
        f.write(y_str+"\n")
        return
    def printContLam(self, f):
        '''
        prints header in first line of file, and the FSPS wavelength array
        (for the nebular continuum) as the second line in the output file.
        # nlam cols nmod rows logZ Age logU
        # fsps_lam_1 fsps_lam_2 .... fsps_lam_n
        '''
        #grab fsps wavelength info
        lamfile = pkg_resources.resource_filename(__name__, "data/FSPSlam.dat")
        fsps_lam = np.genfromtxt(lamfile)
        self.__setattr__("fsps_lam", fsps_lam)
        nlam = len(fsps_lam)
        nmods = np.max(self.mod_num).astype(int)
        #print header to file
        head_str = "#{0} cols {1} rows {2} logZ {3} Age {4} logU".format(nlam, nmods, self.NZ, self.NA, self.NU)
        f.write(head_str+"\n")
        #print lambda array
        p_str = " ".join(["{0:1.6e}".format(lam) for lam in fsps_lam])
        f.write(p_str+"\n")
        return



#------------------------------------------------
def zmet_to_nuZ(zmet):
    '''
    zmet = 1,2,3,4,5,6,7,8
        ...corresponding to...
    m1.00, m1.02, m1.04, m1.06, p0.00, p0.02, p0.04, p0.06
    '''
    zmets = np.array([1,2,3,4,5,6,7,8])
    zs = np.array([-1.00, -1.02, -1.04, -1.06, 0.00, 0.02, 0.04, 0.06])
    if type(zmet) is float:
        ii, = np.where(zmets == zmet)[0]
        out_val = zs[ii]
    else:
        out_val = np.zeros_like(zmet, dtype='float')
        for i in range(len(zmet)):
            ii, = np.where(zmets == zmet[i])[0]
            out_val[i] = zs[ii]
    return out_val

class writeAltFormattedOutput(object):
    #sp = fsps.StellarPopulation()
    #fsps_lam = sp.wavelengths
    def __init__(self, dir_, mod_prefix, mod_suffix,
                 use_extended_lines=False, more_info=False,**kwargs):
        '''
        writeFormattedOutput(mod_dir, 'ZAU', 'BPASS')
        '''
        self.dir_, self.mod_prefix = dir_, mod_prefix
        self.file_pr = dir_ + mod_prefix
        if mod_suffix is None:
            self.out_pr = dir_ + mod_prefix
        else:
            self.out_pr = dir_ + mod_prefix + mod_suffix
        # each model's final info will be in prefix00.lines, prefix00.cont
        self.line_out = self.out_pr + ".lines"
        self.cont_out = self.out_pr + ".cont"
        self.loadModInfo() # load each model's parameters from prefix.pars
        # print ordered emission line wavelengths + fluxes
        self.doLineOut(use_extended_lines=use_extended_lines,
                       more_info=more_info)
        self.doContOut() # interp and print neb cont onto FSPS wavelenth arr
        return
    def loadModInfo(self, **kwargs):
        '''
        reads model parameters from "ZAU.pars"
        '''
        name_keys = ["mod_num", "logZ", "Age", "logU", "logR", "logQ", "nH", "efrac", "zmet"]
        data = np.genfromtxt(self.file_pr+".pars", unpack=True)
        ddata = {}
        for i,key in enumerate(name_keys):
            if key == 'zmet':
                temp_arr = zmet_to_nuZ(data[i])
                ddata[key] = temp_arr
                self.__setattr__(key, temp_arr)
            else:
                ddata[key] = data[i]
                self.__setattr__(key, data[i])
        self.__setattr__("modpars", ddata)
        self.NZ = len(np.unique(self.zmet))
        self.NA = len(np.unique(self.Age))
        self.NU = len(np.unique(self.logU))
        return
    def doLineOut(self, more_info=False, **kwargs):
        '''
        prints line fluxes to prefix00.lines file
        '''
        f = open(self.line_out, "w")
        self.printLineLam(f, **kwargs)
        for n in self.mod_num:
            self.printLineFlu(f, n.astype(int), more_info=more_info)
        f.close()
        print("lines: {0:.0f} models to file {1}".format(self.mod_num[-1], self.line_out))
        return
    def printLineLam(self, f, use_extended_lines=False):
        '''
        prints the wavelength array for the emission lines as the second
        line in the output file. converts all wavelengths to vacuum.
        '''
        #read in file containing wavelength info
        if use_extended_lines:
            linefile = pkg_resources.resource_filename(__name__, "data/orderedLinesEXT.dat")
        else:
            linefile = pkg_resources.resource_filename(__name__, "data/orderedLines.dat")
        data_vac = np.genfromtxt(linefile)
        #data_vac = air_to_vac(data) # new file is already in vac
        nlines = len(data_vac)
        nmods = np.max(self.mod_num)
        #print header to file
        head_str = "#{0} cols {1:.0f} rows {2} logZ {3} Age {4} logU".format(nlines, nmods, self.NZ, self.NA, self.NU)
        f.write(head_str+"\n")
        #print lambda array
        p_str = " ".join(["{0:1.6e}".format(dat) for dat in data_vac])
        f.write(p_str+"\n")
        return
    def printLineFlu(self, f, n, more_info=False):
        #write model parameters
        if more_info:
            tstr = linecache.getline(self.file_pr+'.pars', n)
            f.write(tstr)
        else:
            tstr = "{0:2.4e} {1:2.4e} {2:2.4e}".format(self.zmet[n-1], self.Age[n-1], self.logU[n-1])
            f.write(tstr+"\n")
        #read in and print emission line intensities (Lsun/Q)
        nst = "{0}".format(n)
        filename = self.file_pr+nst+".out_lines"
        lam, flu = np.genfromtxt(filename, unpack=True)
        I_str = ["{0:1.4e}".format(s) for s in flu]
        tstr = " ".join(I_str)
        f.write(tstr+"\n")
        return
    def doContOut(self, **kwargs):
        f = open(self.cont_out, "w")
        self.printContLam(f)
        for num in self.modpars['mod_num']:
            iind = num.astype(int)
            pars = dict(logZ=self.logZ[iind-1],
                        Age=self.Age[iind-1],
                        nH=self.nH[iind-1],
                        logQ=self.logQ[iind-1],
                        logU=self.logU[iind-1],
                        logR=self.logR[iind-1],
                        mod_num=iind,
                        zmet=self.zmet[iind-1])
            self.printContFlu(f, pars)
        f.close()
        print("cont: {0:.0f} models to file {1}".format(self.modpars['mod_num'][-1], self.cont_out))
        return
    def printContFlu(self, f, pars):
        #write model parameters
        tstr = "{0:2.4e} {1:2.4e} {2:2.4e}".format(pars["zmet"],
                                                   pars["Age"],
                                                   pars["logU"])
        f.write(tstr+"\n")
        #read in and print emission line intensities
        nst = "{0}".format(pars["mod_num"])
        filename = self.file_pr+nst+".out_cont"
        # read lambda, diffuse cont
        mdata = np.genfromtxt(filename)
        lam = mdata[:,0]
        flu = mdata[:,1]
        y_str = " ".join(["{0:1.4}".format(y) for y in flu])
        f.write(y_str+"\n")
        return
    def printContLam(self, f):
        '''
        prints header in first line of file, and the FSPS wavelength array
        (for the nebular continuum) as the second line in the output file.
        # nlam cols nmod rows logZ Age logU
        # fsps_lam_1 fsps_lam_2 .... fsps_lam_n
        '''
        #grab fsps wavelength info
        lamfile = pkg_resources.resource_filename(__name__, "data/FSPSlam.dat")
        fsps_lam = np.genfromtxt(lamfile)
        self.__setattr__("fsps_lam", fsps_lam)
        nlam = len(fsps_lam)
        nmods = np.max(self.mod_num).astype(int)
        #print header to file
        head_str = "#{0} cols {1} rows {2} logZ {3} Age {4} logU".format(nlam, nmods, self.NZ, self.NA, self.NU)
        f.write(head_str+"\n")
        #print lambda array
        p_str = " ".join(["{0:1.6e}".format(lam) for lam in fsps_lam])
        f.write(p_str+"\n")
        return

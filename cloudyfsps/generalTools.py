#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

import numpy as np
import itertools
from scipy.integrate import simps

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

def calcForLogQ(logU=None, Rinner=None, nh=None, logQ=None):
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

def name_to_sym(val=None):
    elem_keys = dict(helium="He",
                     carbon="C",
                     nitrogen="N",
                     oxygen="O",
                     neon="Ne",
                     magnesium="Mg",
                     silicon="Si",
                     sulphur="S",
                     argon="Ar",
                     calcium="Ca",
                     iron="Fe",
                     sodium="Na",
                     aluminum="Al",
                     chlorine="Cl",
                     nickel="Ni")
    if val is None:
        return elem_keys
    else:
        try:
            return elem_keys[val.lower()]
        except KeyError:
            print("key must be in ", elem_keys.keys())

def sym_to_name(val=None):
    elem_keys = dict(He="helium",
                     C="carbon",
                     N="nitrogen",
                     O="oxygen",
                     Ne="neon",
                     Mg="magnesium",
                     Si="silicon",
                     S="sulphur",
                     Ar="argon",
                     Ca="calcium",
                     Fe="iron",
                     Na="sodium",
                     Al="aluminum",
                     Cl="chlorine",
                     Ni="nickel")
    if val is None:
        return elem_keys
    else:
        try:
            return elem_keys[val.title()]
        except KeyError:
            print("element not in ", elem_keys.keys())
        
def air_to_vac(inpt, no_uv_conv=True):
    '''
    from morton 1991
    preserves order of input array
    '''
    if type(inpt) is float:
        wl = np.array([inpt])
    else:
        wl = np.asarray(inpt)
    to_vac = lambda lam: (6.4328e-5 + (2.94981e-2/(146.0-(1.0e4/lam)**2.0)) + (2.554e-4/(41.0-(1.0e4/lam)**2.0)))*lam + lam
    if no_uv_conv:
        outpt = np.array([to_vac(lam) if lam > 2000.0 else lam for lam in wl])
    else:
        outpt = to_vac(wl)
    return outpt

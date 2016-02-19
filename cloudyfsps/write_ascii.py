#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

__all__ = ["FileOps", "compile_mod", "check_compiled_mod", "mod_exists"]

import os
import numpy as np
from cloudytools import grouper
import fsps
import subprocess

try:
    CLOUDY_EXE = os.environ['CLOUDY_EXE']
except KeyError:
    print 'Must have set system environment CLOUDY_EXE'

try:
    # taking the last in path, if more than one directory given
    CLOUDY_DATA_PATH = os.environ['CLOUDY_DATA_PATH'].split(':')[-1]
except KeyError:
    print 'Cloudy data path not set. Assuming standard cloudy structure'
    CLOUDY_DATA_PATH = '/'.join(CLOUDY_EXE.split('/')[:-2])+'/data'

class FileOps:
    '''
    Print FSPS data into ascii files readable by CLOUDY
    Calling sequence:
        FileOps('outfile.ascii', lamda_array, spec_array, model_array, **kwargs)
    Dictionary with header information - change any of these values by
    inputting them as kwargs.
    '''
    def __init__(self, outfile, lam, flu, modpars, **kwargs):
        self.nom_dict = {'nmod': 94, 'ndim': 1, 'npar':1, 'nx':1963,
                         'x':'lambda', 'conv1':1.0, 'peraa':False,
                         'conv2':3.839e33, 'par1':'age', 'par2':'logz'}
        FileOps.init_pars(self, **kwargs)
        
        self.file = open('/'.join([CLOUDY_DATA_PATH,outfile]), 'w')
        FileOps.write_header(self, modpars)
        FileOps.write_body(self, lam, flu, modpars)
        self.file.close()
        
    def init_pars(self, **kwargs):
        for key, value in kwargs.items():
            self.nom_dict[key] = value
        if self.nom_dict['peraa']:
            self.nom_dict['f_type'] = 'F_lambda'
        else:
            self.nom_dict['f_type'] = 'F_nu'
        
    def write_header(self, modpars):
        '''
        Header for cloudy ascii files
        '''
        self.file.write("  20060612\n")
        self.file.write("  %i\n" %self.nom_dict['ndim'])
        self.file.write("  %i\n" %self.nom_dict['npar'])
        self.file.write("  %s\n" %self.nom_dict['par1']) #first param
        if self.nom_dict['npar'] > 1:
            self.file.write("  %s\n" %self.nom_dict['par2']) #second param
        self.file.write("  %i\n" %self.nom_dict['nmod']) #total number of mods
        self.file.write("  %i\n" %self.nom_dict['nx']) #number of lam pts
        self.file.write("  %s\n" %self.nom_dict['x']) #lambda or freq
        self.file.write("  %.8e\n" %self.nom_dict['conv1']) #AA or Hz
        self.file.write("  %s\n" %self.nom_dict['f_type'])#F_lam or F_nu
        self.file.write("  %.8e\n" %self.nom_dict['conv2'])#units
        for chunk in grouper(4, modpars):
            if self.nom_dict['npar'] > 1:
                self.file.write("  " + "  ".join("{0:>6.2e}{1:>6.2f}".format(x[0], x[1]) for x in chunk) + "\n")
            else:
                self.file.write("  " + "  ".join("{0:>4.2e}".format(x) for x in chunk) + "\n")
    
    def write_data(self, array):
        '''
        write array with 5 items per line in format 1.0000e+00
        '''
        for chunk in grouper(5, array):
            self.file.write("  " + "  ".join("%1.4e" %x for x in chunk) + "\n")
    def write_body(self, lam, flu, modpars):
        FileOps.write_data(self, lam)
        flu[(flu < 0.0)] = 0.0
        [FileOps.write_data(self, fl) for fl in flu]
        
def compile_mod(ascii_file, **kwargs):
    comp_file = CLOUDY_DATA_PATH+'/compile.in'
    f = open(comp_file, 'w')
    f.write('compile stars "{}"\n'.format(ascii_file))
    f.close()
    to_run = 'cd {} ; {} compile.in'.format(CLOUDY_DATA_PATH, CLOUDY_EXE)
    print 'compiling {}'.format(ascii_file)
    proc = subprocess.Popen(to_run, shell=True)
    proc.communicate()

def check_compiled_mod(ascii_file, **kwargs):
    '''
    checks to make sure ascii_file.mod exists and that 
    the words "Cloudy exited OK' are in compile.out
    '''
    out_file = CLOUDY_DATA_PATH+'/compile.out'
    f = open(out_file, 'r')
    content = f.readlines()
    f.close()
    comp_mod = '{}/{}.mod'.format(CLOUDY_DATA_PATH, ascii_file.split('.')[0])
    check = np.all(['OK' in content[-1],
                    os.path.exists(comp_mod)])
    return check
    
def mod_exists(filename):
    if filename.split('.')[-1] == 'mod':
        return os.path.exists('/'.join([CLOUDY_DATA_PATH, filename]))
    else:
        return os.path.exists('/'.join([CLOUDY_DATA_PATH, filename.split('.')[0]+'.mod']))

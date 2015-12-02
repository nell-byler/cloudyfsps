import os
import write_input
import write_ascii
import cloudy_output
from mytools import cloudytools as ct
import numpy as np

ascii_file = 'FSPS_fbhb.ascii'
ascii_dir = '/astro/users/ebyler/pro/cloudy/data/'

write_ascii.fbhb_main(fileout=ascii_dir+ascii_file)
write_ascii.compile_mod(ascii_dir, ascii_file)
if not write_ascii.check_compile(ascii_dir, ascii_file):
    print 'bad model compilation'

mod_dir = './output_fbhb/'

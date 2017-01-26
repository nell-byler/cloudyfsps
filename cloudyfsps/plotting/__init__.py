import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm as cmx

mpl.rc('xtick', labelsize=12)
mpl.rc('ytick', labelsize=12)
mpl.rc('font', size=16, family='serif', serif=[r'cmr10'], style='normal', variant='normal', stretch='normal', weight='heavy')
mpl.rc('legend', labelspacing=0.1, handlelength=2, fontsize=16)
mpl.rcParams['axes.unicode_minus'] = False

mpl.colors.colorConverter.colors['black'] = (0.145, 0.145, 0.145)
mpl.colors.colorConverter.colors['k'] = (0.145, 0.145, 0.145)
mpl.colors.colorConverter.colors['blue'] = (0.031, 0.271, 0.580)
mpl.colors.colorConverter.colors['b'] = (0.031, 0.271, 0.580)
mpl.colors.colorConverter.colors['red'] = (0.647, 0.059, 0.082)
mpl.colors.colorConverter.colors['r'] = (0.647, 0.059, 0.082)
mpl.colors.colorConverter.colors['green'] = (0.0, 0.427, 0.173)
mpl.colors.colorConverter.colors['g'] = (0.0, 0.427, 0.173)
mpl.colors.colorConverter.cache = {}

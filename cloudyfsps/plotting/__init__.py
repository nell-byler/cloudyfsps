import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mpl_colors
from matplotlib import cm as cmx
from matplotlib import rc

rc('font', **{'family': 'serif', 'serif': ['Computer Modern'], 'weight':'bold', 'size':'18'})
rc('text', usetex=True)
mpl_colors.colorConverter.colors['black'] = (0.145, 0.145, 0.145)
mpl_colors.colorConverter.colors['k'] = (0.145, 0.145, 0.145)
mpl_colors.colorConverter.colors['blue'] = (0.031, 0.271, 0.580)
mpl_colors.colorConverter.colors['b'] = (0.031, 0.271, 0.580)
mpl_colors.colorConverter.colors['red'] = (0.647, 0.059, 0.082)
mpl_colors.colorConverter.colors['r'] = (0.647, 0.059, 0.082)
mpl_colors.colorConverter.colors['green'] = (0.0, 0.427, 0.173)
mpl_colors.colorConverter.colors['g'] = (0.0, 0.427, 0.173)
mpl_colors.colorConverter.cache = {}

def get_colors(vals, cname='CMRmap', minv=0.05, maxv=0.8, cmap=None,
               set_bad_vals=False, return_cNorm=False):
    '''
    sM = get_colors(arr, cname='jet', minv=0.0, maxv=1.0)
    sM = get_colors(arr, cmap=cubehelix.cmap())
    '''
    if cmap is None:
        cmap = plt.get_cmap(cname)
    new_cmap = mpl_colors.LinearSegmentedColormap.from_list('trunc({0}, {1:.2f}, {2:.2f})'.format(cmap.name, minv, maxv), cmap(np.linspace(minv, maxv, 100)))
    if set_bad_vals:
        new_cmap.set_bad('white', alpha=1.0)
    cNorm = mpl_colors.Normalize(vmin=vals.min(), vmax=vals.max())
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=new_cmap)
    if return_cNorm:
        return scalarMap, cNorm
    else:
        scalarMap.set_array(vals)
        return scalarMap

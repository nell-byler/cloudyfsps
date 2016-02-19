import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mpl_colors
from matplotlib import cm as cmx

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

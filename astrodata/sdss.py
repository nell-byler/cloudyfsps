import numpy as np
import matplotlib.pyplot as plt
import cubehelix
import matplotlib.colors as mpl_colors
import matplotlib.cm as cmx
from astroML.datasets import fetch_sdss_corrected_spectra
from astroML.datasets.tools.sdss_fits import log_OIII_Hb_NII
from astrodata.kewley import *

this_dir = '/astro/users/ebyler/python/pro/astrodata/'

def plot_bpt(var_label, ax=None, color_code=False, **kwargs):
    '''
    sdss.plot_bpt(True)
    '''
    if var_label:
        lab = 'SDSS'
    else:
        lab = '__nolegend__'
    data = fetch_sdss_corrected_spectra()
    if ax is None:
        ax = plt.gca()
    if color_code:
        i = np.where((data['lineindex_cln'] == 4) | (data['lineindex_cln'] == 5))
        ax.scatter(data['log_NII_Ha'][i], data['log_OIII_Hb'][i],
                   c=data['lineindex_cln'][i], s=9, lw=0,
                   label=lab)
    else:
        ax.plot(data['log_NII_Ha'], data['log_OIII_Hb'], 'o', markersize=2.0, color='k', alpha=0.5)
    NII_OIII_agn_lim(ax=ax)
    NII_OIII_sf_lim(ax=ax)
    ax.set_xlim(-2.0, 1.0)
    ax.set_ylim(-1.2, 1.5)
    return

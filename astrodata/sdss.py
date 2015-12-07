import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mpl_colors
import matplotlib.cm as cmx
from astroML.datasets import fetch_sdss_corrected_spectra
#from astroML.datasets.tools.sdss_fits import log_OIII_Hb_NII
from astrodata.kewley import NII_OIII_agn_lim, NII_OIII_sf_lim
from astrodata.kewley import OI_OIII_agn_lim, SII_OIII_agn_lim

def plot_bpt(var_label, ax=None, color_code=False, line_ratio='NII', **kwargs):
    '''
    sdss.plot_bpt(True)
    '''
    assert line_ratio in ['NII','NIIb','SII','OI', 'OIa', 'OII']
    if var_label:
        lab = 'SDSS'
    else:
        lab = '__nolegend__'
    data = fetch_sdss_corrected_spectra()
    lineindex_cln = 'lineindex_cln_{}'.format(line_ratio)
    single_OIII = kwargs.get('single_OIII', False)
    if line_ratio == 'OII': # this produces NII/OII by OIII/OII plot
        yratio = 'log_OIII_OII'
        xratio = 'log_NII_OII'
        lineindex_cln = 'lineindex_cln_{}'.format(line_ratio)
    else:
        xratio = 'log_{}_Ha'.format(line_ratio)
        if (line_ratio[-1] == 'b' or line_ratio[-1] == 'a'):
            yratio = 'log_OIIIb_Hb'
        else:
            yratio = 'log_OIII_Hb'
        if single_OIII:
            yratio = 'log_OIII_Hb'
    if ax is None:
        plt.figure()
        ax = plt.gca()
    if color_code:
        i, = np.where((data[lineindex_cln] == 4) | (data[lineindex_cln] == 5))
        ax.scatter(data[xratio][i], data[yratio][i],
                   c=data[lineindex_cln][i], s=9, lw=0,
                   label=lab)
    else:
        ax.plot(data[xratio], data[yratio], 'o',
        markersize=2.0, color='k', alpha=0.5)
    if line_ratio[0] == 'N':
        NII_OIII_agn_lim(ax=ax)
        NII_OIII_sf_lim(ax=ax)
        ax.set_xlim(-2.0, 1.0)
        ax.set_ylim(-1.2, 1.5)
    if line_ratio[0] == 'S':
        SII_OIII_agn_lim(ax=ax)
        ax.set_xlim(-2.0, 0.3)
        ax.set_ylim(-1.2, 1.5)
    if (line_ratio == 'OI' or line_ratio == 'OIa'):
        OI_OIII_agn_lim(ax=ax)
        ax.set_xlim(-2.0, 0.0)
        ax.set_ylim(-1.2, 1.5)
    if (line_ratio == 'OII'):
        ax.set_ylim(-2.0, 1.0)
        ax.set_xlim(-1.3, 1.3)
    return

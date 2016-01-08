import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mpl_colors
import matplotlib.cm as cmx
import pkg_resources
from astrodata.kewley import NII_OIII_agn_lim, NII_OIII_sf_lim
from astrodata.kewley import OI_OIII_agn_lim, SII_OIII_agn_lim

def load_spec():
    linefile = pkg_resources.resource_filename(__name__, "data/sdss_data_ls.npz")
    data = np.load(linefile)
    outdata = dict()
    for key, val in data.iteritems():
        outdata[key] = val
    outdata['log_OIII_OII'] = np.log10(data['strength_OIII']/data['strength_OII'])
    outdata['log_NII_OII'] = np.log10(data['strength_NII']/data['strength_OII'])
    outdata['log_OIII_Hb'] = np.log10(data['strength_OIII']/data['strength_Hb'])
    outdata['log_OIIIb_Hb'] = np.log10(data['strength_OIIIb']/data['strength_Hb'])
    outdata['log_NII_Ha'] = np.log10(data['strength_NII']/data['strength_Ha'])
    outdata['log_NIIb_Ha'] = np.log10(data['strength_NIIb']/data['strength_Ha'])
    outdata['log_SII_Ha'] = np.log10(data['strength_SII']/data['strength_Ha'])
    outdata['log_OI_Ha'] = np.log10(data['strength_OI']/data['strength_Ha'])
    outdata['log_OIa_Ha'] = np.log10(data['strength_OIa']/data['strength_Ha'])
    outdata['log_OII_Ha'] = np.log10(data['strength_OII']/data['strength_Ha'])
    outdata['HaHb'] = data['strength_Ha']/data['strength_Hb']
    return outdata

def get_line_ratio(data, line_ratio, **kwargs):
    lineindex_cln = 'lineindex_cln_{}'.format(line_ratio)
    single_OIII = kwargs.get('single_OIII', False)
    if line_ratio == 'OII': # this produces NII/OII by OIII/OII plot
        yratio = 'log_OIII_OII'
        xratio = 'log_NII_OII'
        lineindex_cln = 'lineindex_cln_{}'.format(line_ratio)
    elif line_ratio == 'R23':
        yratio = 'log_OIII_OII'
        xratio = 'log_OIII_Hb'
        lineindex_cln = 'lineindex_cln_OIII'
        o2hb = data['log_OIII_Hb'] - data['log_OIII_OII']
        yval = np.log10(((10.0**o2hb) + (10.0**data['log_OIII_Hb'])))
    else:
        xratio = 'log_{}_Ha'.format(line_ratio)
        if (line_ratio[-1] == 'b' or line_ratio[-1] == 'a'):
            yratio = 'log_OIIIb_Hb'
        else:
            yratio = 'log_OIII_Hb'
        if single_OIII:
            yratio = 'log_OIII_Hb'
    return xratio, yratio, lineindex_cln

def plot_bpt(var_label, ax=None, color_code=False, line_ratio='NII', **kwargs):
    '''
    sdss.plot_bpt(True)
    SDSS data generated with astroML.fetch_corrected_sdss_spectra()
    '''
    assert line_ratio in ['NII','NIIb','SII','OI', 'OIa', 'OII', 'R23']
    if var_label:
        lab = kwargs.get('lab', 'SDSS')
    else:
        lab = '__nolegend__'
    
    data = load_spec()
    xratio, yratio, lind_cln = get_line_ratio(data, line_ratio, **kwargs)
    
    if ax is None:
        plt.figure()
        ax = plt.gca()
    if color_code:
        cs = kwargs.get('cs', None)
        if cs is None:
            color_by = lineindex_cln
        else:
            color_by = cs
        i, = np.where((data[lineindex_cln] == 4) | (data[lineindex_cln] == 5))
        ax.scatter(data[xratio][i], data[yratio][i],
                   c=data[color_by][i], s=9, lw=0,
                   label=lab)
    elif line_ratio == 'R23':
        ax.plot(data[xratio], yval, 'o', markersize=2.0, color='k', alpha=0.5)
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

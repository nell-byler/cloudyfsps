import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mpl_colors
import matplotlib.cm as cmx
import pkg_resources

c = 2.9979e10

def plot_bpt(logq_val=8.5, z_val=1.0, kappa_val=20, label='Dopita (2013)', line_ratio='NII',
             ax=None, color='k', tcolor='k', **kwargs):
    '''
    dopita.plot_bpt(logq_val='all', color='blue', use_doublet=True)
    '''
    linefile = pkg_resources.resource_filename(__name__, "data/dopita_lines.dat")
    data = np.genfromtxt(linefile, comments='#', delimiter=';', missing_values='  ', filling_values=np.inf, unpack=True, names='Z, kappa, logq, OIIa, OIIb, OIIIa, OIIIb, OI, NIIa, Ha, NIIb, SIIa, SIIb')
    if line_ratio in ['NII', 'SII']:
        rat_x = np.log10((data[line_ratio+'a']+data[line_ratio+'b'])/data['Ha'])
        rat_y = np.log10(data['OIIIa']+data['OIIIb'])
    if line_ratio in ['NIIb','OI']:
        rat_x = np.log10(data[line_ratio]/data['Ha'])
        rat_y = np.log10(data['OIIIb'])
    if line_ratio == 'OII':
        rat_x = np.log10((data['NIIa']+data['NIIb'])/(data['OIIa']+ data['OIIb']))
        rat_y = np.log10((data['OIIIa']+data['OIIIb'])/(data['OIIa']+ data['OIIb']))
    if ax is None:
        ax = plt.gca()
    if type(logq_val) is str:
        inds, = np.where(data['kappa'] == kappa_val)
    else:
        inds, = np.where((data['logq'] == logq_val) &
                         (data['Z'] == z_val) &
                         (data['kappa'] == kappa_val))
    do_grid = kwargs.get('do_grid', True)
    if do_grid:
        i=0
        for q in np.unique(data['logq']):
            inds, = np.where((data['logq'] == q) & (data['kappa'] == kappa_val))
            if i == 0:
                ax.plot(rat_x[inds], rat_y[inds], color=color, label=label)
            else:
                ax.plot(rat_x[inds], rat_y[inds], color=color, label='__nolegend__')
            ax.annotate('{0:.1f}'.format(np.log10((10.0**q)/c)),
                        xy=(rat_x[inds][-1], rat_y[inds][-1]), xycoords='data',
                        xytext=(-10,0), textcoords='offset points',
                        horizontalalignment='right',
                        verticalalignment='bottom',
                        size=18, color=tcolor)
            i+=1
        for z in np.unique(data['Z']):
            #print np.log10(z)
            inds, = np.where((data['Z'] == z) & (data['kappa'] == kappa_val))
            ax.plot(rat_x[inds], rat_y[inds], color=color)
            ax.annotate('{0:.1f}'.format(np.log10(z)),
                        xy=(rat_x[inds][-1], rat_y[inds][-1]), xycoords='data',
                        xytext=(0,-10), textcoords='offset points',
                        horizontalalignment='left',
                        verticalalignment='top',
                        size=18, color=tcolor)
    return


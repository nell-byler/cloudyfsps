import numpy as np
import matplotlib.pyplot as plt
import cubehelix
import matplotlib.colors as mpl_colors
import matplotlib.cm as cmx

this_dir = '/astro/users/ebyler/python/pro/astrodata/'
c = 2.9979e10
def plot_bpt(logq_val=8.5, z_val=1.0, label='Dopita (2013)', 
             ax=None, color='k', **kwargs):
    '''
    dopita.plot_bpt(logq_val='all', color='blue', auto_corr=True)
    '''
    auto_corr = kwargs.get('auto_corr', False)
    data = np.genfromtxt(this_dir+'dopita_lines.dat',
                         comments='#', delimiter='\t',
                         names='z,k,logq,o3a,o3b,o1,n2a,ha,n2b,s2a,s2b')
    if auto_corr:
        rat_x = np.log10((data['n2a']+data['n2b'])/data['ha'])
    else:
        rat_x = np.log10(data['n2b']/data['ha'])
    rat_y = np.log10(data['o3b'])
    
    if ax is None:
        ax = plt.gca()
    if type(logq_val) is str:
        inds, = np.where(data['k'] == 20)
    else:
        inds, = np.where((data['logq'] == logq_val) &
                         (data['z'] == z_val) &
                         (data['k'] == 20))
    do_grid = kwargs.get('do_grid', True)
    if do_grid:
        for q in np.unique(data['logq']):
            inds, = np.where((data['logq'] == q) & (data['k'] == 20))
            plt.plot(rat_x[inds], rat_y[inds], color=color)
            ax.annotate('{0:.1f}'.format(np.log10((10.0**q)/c)),
                        xy=(rat_x[inds][-1], rat_y[inds][-1]), xycoords='data',
                        xytext=(-10,0), textcoords='offset points',
                        horizontalalignment='right',
                        verticalalignment='bottom',
                        size=18, color='green')
        for z in np.unique(data['z']):
            print np.log10(z)
            inds, = np.where((data['z'] == z) & (data['k'] == 20))
            plt.plot(rat_x[inds], rat_y[inds], color=color)
            ax.annotate('{0:.1f}'.format(np.log10(z)),
                        xy=(rat_x[inds][-1], rat_y[inds][-1]), xycoords='data',
                        xytext=(0,-10), textcoords='offset points',
                        horizontalalignment='left',
                        verticalalignment='top',
                        size=18, color='green')
    #ax.plot(rat_x[inds], rat_y[inds], 'o', color=color, label=label)
    return


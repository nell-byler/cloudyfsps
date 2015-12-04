import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mpl_colors
import matplotlib.cm as cmx
import pkg_resources

def plot_bpt(var_label, ax=None, **kwargs):
    '''
    vanzee.plot_bpt(True, auto_corr=True)
    '''
    auto_corr =  kwargs.get('auto_corr', True)
    if var_label:
        lab = 'Van Zee (1998)'
    else:
        lab = '__nolegend__'
    linefile = pkg_resources.resource_filename(__name__, "data/vanzee_lines.dat")
    data = np.genfromtxt(linefile, comments='#',
                         names='o2, o2_e, o3, o3_e, ha, ha_e, n2, n2_e')
    if auto_corr:
        #removing contribution from doublet lines I_b = 2.88*I_a
        x = np.log10((data['n2'])/data['ha']) + np.log10(3.0/4.0)
        y = np.log10(data['o3']) + np.log10(3.0/4.0)
    else:
        x = np.log10(data['n2']/data['ha'])
        y = np.log10(data['o3'])
    xerr = ((data['n2_e']/(data['n2']*np.log(10)))**2.0 +\
                (data['ha_e']/(data['ha']*np.log(10)))**2.0)**0.5
    yerr = data['o3_e']/(data['o3']*np.log(10))
    if ax is None:
        ax = plt.gca()
    ax.errorbar(x,y,xerr=xerr, yerr=yerr,
                capsize=0, fmt='s', color='white', ecolor='k', 
                label=lab)
    return


def get_abunds():
    '''
    returns data, with column names
          temp, logO, logOerr, logNO, logNOerr
          T(O++), log(O/H), log(N/O)
    '''
    linefile = pkg_resources.resource_filename(__name__, "data/vanzee_abund.dat")
    data = np.genfromtxt(linefile, delimiter='\t',
                         names='temp, logO, logOerr, logNO, logNOerr')
    return data

def plot_NO():
    
    data = get_abunds()
    plt.errorbar(data['logO'], data['logNO'],
                 xerr=data['logOerr'], yerr=data['logNOerr'],
                 marker='o', color='grey', alpha=0.8, linestyle='None',
                 markersize=8)
    
    return

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as pltclrs
from matplotlib import cm
from matplotlib import rc

rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

def name_to_sym(val=None):
    elem_keys = dict(helium='He',
                     carbon='C',
                     nitrogen='N',
                     oxygen='O',
                     neon='Ne',
                     magnesium='Mg',
                     silicon='Si',
                     sulphur='S',
                     argon='Ar',
                     calcium='Ca',
                     iron='Fe',
                     sodium='Na',
                     aluminum='Al',
                     chlorine='Cl',
                     nickel='Ni')
    if val is None:
        return elem_keys
    else:
        try:
            return elem_keys[val.lower()]
        except KeyError:
            print 'key must be in ', elem_keys.keys()

def sym_to_name(val=None):
    elem_keys = dict(He='helium',
                     C='carbon',
                     N='nitrogen',
                     O='oxygen',
                     Ne='neon',
                     Mg='magnesium',
                     Si='silicon',
                     S='sulphur',
                     Ar='argon',
                     Ca='calcium',
                     Fe='iron',
                     Na='sodium',
                     Al='aluminum',
                     Cl='chlorine',
                     Ni='nickel')
    if val is None:
        return elem_keys
    else:
        try:
            return elem_keys[val.title()]
        except KeyError:
            print 'element not in ', elem_keys.keys()
        
def air_to_vac(inpt, no_uv_conv=True):
    '''
    from morton 1991
    preserves order of input array
    '''
    if type(inpt) is float:
        wl = np.array([inpt])
    else:
        wl = np.asarray(inpt)
    to_vac = lambda lam: (6.4328e-5 + (2.94981e-2/(146.0-(1.0e4/lam)**2.0)) + (2.554e-4/(41.0-(1.0e4/lam)**2.0)))*lam + lam
    if no_uv_conv:
        outpt = np.array([to_vac(lam) if lam > 2000.0 else lam for lam in wl])
    else:
        outpt = to_vac(wl)
    return outpt
    
def get_colors(vals, cname='jet'):
    cmap = plt.get_cmap(cname)
    cNorm = pltclrs.Normalize(vmin=vals.min(), vmax=vals.max())
    scalarMap = cm.ScalarMappable(norm=cNorm, cmap=cmap)
    colorVals = [scalarMap.to_rgba(val) for val in vals]
    scalarMap.set_array(vals)
    return scalarMap

def BPT_diagram(n2, o3, hb, ha, ax=None, color='k', label='__nolabel__', xlims=(-2.0, 0.5), ylims=(-1.5, 1.5), bounds=True, **kwargs):
    '''
    N2, O3, HB, HA
    '''
    if ax is None:
        ax = plt.gca()
    xax = np.log10(n2/ha)
    yax = np.log10(o3/hb)
    xlabel = r'log [N II] $\lambda 6584$ / H$\alpha$'
    ylabel = r'log [O III]$\lambda 5007$ / H$\beta$'
    ax.plot(xax, yax, color=color, marker='.', linestyle='None', label=label)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim(xlims[0], xlims[1])
    ax.set_ylim(ylims[0], ylims[1])
    if bounds:
        xlims = [-2.0, 1.0]
        ylims = [-1.5, 1.5]
        xarr = np.linspace(xlims[0], xlims[1], 500)
        yarr = 0.61 / (xarr - 0.05) + 1.3
        inds, = np.nonzero((yarr > ylims[0]) & (yarr<ylims[1]) & (xarr>xlims[0]) & (xarr<xlims[1]))
        ax.plot(xarr[inds], yarr[inds], lw=2, color='blue')
        ax.vlines(xlims, ylims[0], ylims[1], linestyle='dashed')
        ax.hlines(ylims, xlims[0], xlims[1], linestyle='dashed')
        
    return ax

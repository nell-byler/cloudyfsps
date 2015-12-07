import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mpl_colors
import matplotlib.cm as cmx
import cloudyfsps.cloudytools as ct
import fsps
from astrodata import dopita, sdss, vanzee, kewley
from cloudyfsps.astrotools import get_colors

c = 2.9979e18
lsun = 3.846e33
planck = 6.626e-27

def sextract(text, par1=None, par2=None):
    
    if np.size(text) == 1:
        if type(par1) is int:
            str1 = text[par1::]
        elif type(par1) is str:
            str1 = text.split(par1)
            if len(str1) == 1:
                return ''
            else:
                str1 = str1[-1]
        else:
            str1 = text
        if type(par2) is int:
            str2 = str1[0:par2]
        elif type(par2) is str:
            str2 = str1.split(par2)
            if len(str2) == 1:
                return ''
            else:
                str2 = str2[0]
        else:
            str2 = str1
        return str2
    else:
        res = []
        for subtext in text:
            res1 = sextract(subtext, par1=par1, par2=par2)
            if res1 != '':
                res.append(res1)
        return res

class modObj(object):
    '''
    '''
    def __init__(self, dir_, prefix, parline, **kwargs):
        '''
        [0]modnum; [1]logZ; [2]age; [3]logU; [4]logR; [5]logQ  
        '''
        use_doublet = kwargs.get('use_doublet', False) # fix n2/o3 line ratios
        read_out = kwargs.get('read_out', False)
        read_cont = kwargs.get('read_cont', False)
        self.modnum = int(parline[0])
        self.logZ = parline[1]
        self.age = parline[2]
        self.logU = parline[3]
        self.logR = parline[4]
        self.logQ = parline[5]
        self.nH = parline[6]
        self.logq = np.log10((10.0**self.logQ)/(np.pi*4.0*self.nH*(10.0**self.logR)**2.0))
        self.fl = '{}{}{}'.format(dir_, prefix, self.modnum)
        self.load_lines(use_doublet=use_doublet)
        if read_out:
            self.read_out(dust_mod=dust_mod)
        if read_cont:
            self.load_cont()
        
    def load_lines(self, use_doublet=False, **kwargs):
        lines = {'ha':6562.50,
                 'hb':4861.36,
                 'o3':5007.00,
                 'n2':6584.00,
                 'an2':6548.00,
                 'ao3':4959.00,
                 'o2':3727.00,
                 's2a':6716.00,
                 's2b':6731.00,
                 'o1':6300.00}
        line_info = np.genfromtxt(self.fl+'.lineflux')
        lam, flu = line_info[:,0], line_info[:,1]
        for name, wav in lines.iteritems():
            matchind = np.argmin(np.abs(lam-wav))
            self.__setattr__(name, flu[matchind])
        self.alln2 = self.n2+self.an2
        self.allo3 = self.o3+self.ao3
        self.s2 = self.s2a+self.s2b
        self.bpt_x_s2 = np.log10(self.s2/self.ha)
        self.bpt_x_o1 = np.log10(self.o1/self.ha)
        self.bpt_x_all = np.log10(self.alln2/self.ha)
        self.bpt_y_all = np.log10(self.allo3/self.hb)
        self.bpt_x = np.log10(self.n2/self.ha)
        self.bpt_y = np.log10(self.o3/self.hb)
        self.o3o2 = np.log10(self.allo3/self.o2)
        self.n2o2 = np.log10(self.alln2/self.o2)
        return
    def load_cont(self, **kwargs):
        cont_info = np.genfromtxt(self.fl+'.out_cont', skip_header=1)
        self.lam, self.nebflu = cont_info[:,0], cont_info[:,3]
        self.incflu, self.attflu = cont_info[:,1], cont_info[:,2]
        self.spec_Q = ct.calcQ(self.lam, self.incflu*lsun, f_nu=True)
        return
    def get_fsps_spec(self, **kwargs):
        sp = fsps.StellarPopulation(zcontinuous=1)
        sp.params['logzsol'] = self.logZ
        lam, spec = sp.get_spectrum(tage=self.age*1.0e-9)
        self.__setattr__('fsps_spec', spec)
        self.__setattr__('fsps_Q', ct.calcQ(lam, spec*lsun, f_nu=True))
        return
    def read_out(self):
        filename = self.fl+'.out'
        self.out = {}
        file_ = open(filename, 'r')
        for line in file_:
            if line[0:8] == ' ####  1':
                self.out['###First'] = line
            elif line[0:5] == ' ###':
                self.out['###Last'] = line
            elif 'Hi-Con' in line:
                for i in range(7):
                    self.out['SED' + str(i+1)] = file_.next()
            elif line[0:15] == ' IONIZE PARMET:':
                self.out['INZ'] = line
            elif 'H :' in line:
                self.out['gascomp'] = line
            elif 'Dust to gas ratio' in line:
                self.out['dust'] = line
        file_.close()
        self.dist_fact = 4.0*np.pi*(10.0**self.logR)**2.0
        self.Phi0 = float(sextract(self.out['SED2'], 'Ion pht flx:'))
        self.cloudyQ = self.Phi0*self.dist_fact
        #self.logU_Rs = float(sextract(self.out['INZ'], 'U(sp):', 'Q(ion):'))
        #self.calc_Q = (10.0**(self.logU))*self.dist_fact*30.0*2.9979e10
        self.gasC = float(sextract(self.out['gascomp'], 'C :', 8))
        self.gasN = float(sextract(self.out['gascomp'], 'N :', 8))
        self.gasO = float(sextract(self.out['gascomp'], 'O :', 8))
        self.DGR = float(sextract(self.out['dust'], '(by mass):',',' ))
        self.Av_ex = float(sextract(self.out['dust'], 'AV(ext):', '(pnt)'))
        self.Av_pt = float(sextract(self.out['dust'], ' (pnt):'))
        return

class allmods(object):
    '''
    mods = outobj.allmods(dir, prefix, read_out=True)
    '''
    def __init__(self, dir_, prefix, **kwargs):
        self.modpars = np.genfromtxt('{}{}.pars'.format(dir_, prefix))
        self.load_mods(dir_, prefix, **kwargs)
        self.set_pars()
        self.set_arrs()
        read_out = kwargs.get('read_out', False)
        dust_mod = kwargs.get('dust_mod', False)
        if read_out:
            self.add_arrs('gasC', 'gasN', 'gasO')
            if dust_mod:
                self.add_arrs('DGR', 'Av_ex', 'Av_pt')
        
    def load_mods(self, dir_, prefix, **kwargs):
        mods = []
        for par in self.modpars:
            mod = modObj(dir_, prefix, par, **kwargs)
            mods.append(mod)
        self.__setattr__('mods', mods)
        self.__setattr__('nmods', len(mods))
        return
    def set_pars(self):
        self.logZ_vals = np.unique(self.modpars[:,1])
        self.age_vals = np.unique(self.modpars[:,2])
        self.logU_vals = np.unique(self.modpars[:,3])
        self.logR_vals = np.unique(self.modpars[:,4])
        self.logQ_vals = np.unique(self.modpars[:,5])
        self.nH_vals = np.unique(self.modpars[:,6])
    def set_arrs(self):
        iterstrings = ['logZ', 'age', 'logU', 'logR', 'logQ', 'nH',
                       'n2', 'alln2', 'o3', 'allo3', 'hb', 'ha',
                       'bpt_x', 'bpt_y', 'o3o2', 'n2o2', 's2', 'o1',
                       'o2', 'bpt_x_all', 'bpt_y_all', 'bpt_x_s2',
                       'bpt_x_o1']
        for i in iterstrings:
            vals = np.array([mod.__getattribute__(i) for mod in self.mods])
            self.__setattr__(i, vals)
    def add_arrs(self, *args):
        for item in args:
            vals = np.array([mod.__getattribute__(item) for mod in self.mods])
            self.__setattr__(item, vals)
        return
    
    
    def makeBPT(self, ax=None, plot_data=True, line_ratio='NII', **kwargs):
        '''
        mo.makeBPT(ax=ax, const1='age', val1=0.5e6, const2=logR, val2=19.0,
                   const3='nH', val3=10.0)
        '''
        xlabel = r'log [N II] $\lambda 6548,6584$ / H$\alpha$'
        ylabel = r'log [O III] $\lambda 4959,5007$ / H$\beta$'
        bpt_inds = ['bpt_x_all', 'bpt_y_all']
        if line_ratio=='NIIb':
            bpt_inds = ['bpt_x', 'bpt_y']
            xlabel = r'log [N II] $\lambda 6584$ / H$\alpha$'
            ylabel = r'log [O III] $\lambda 5007$ / H$\beta$'
        if line_ratio == 'SII':
            bpt_inds[0] = 'bpt_x_s2'
            xlabel = r'log [S II] $\lambda 6716,6731$ / H$\alpha$'
        if line_ratio == 'OI':
            bpt_inds[0] = 'bpt_x_o1'
            xlabel = r'log [O I] $\lambda 6300$ / H$\alpha$'
        if line_ratio == 'OII':
            bpt_inds = ['n2o2', 'o3o2']
            ylabel = r'log [O III] $\lambda 4959,5007$ / [O II] $\lambda 3726,3727$'
            xlabel = r'log [N II] $\lambda 6548,6584$ / [O II] $\lambda 3726,3727$'
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111)
        pd = {'const1':'age',
              'val1':0.5e6,
              'const2':'logR',
              'val2':19.0,
              'const3':'nH',
              'val3':10.0}
        for key, val in kwargs.iteritems():
            pd[key] = val
        allvars = ['nH', 'logZ', 'logR', 'logU', 'age']
        [allvars.remove(x) for x in [pd['const1'], pd['const2'], pd['const3']]]
        x_name, y_name = allvars[0], allvars[1]
        grid_x = self.__getattribute__(x_name+'_vals')
        grid_y = self.__getattribute__(y_name+'_vals')
        
        use_mods = [mod for mod in self.mods
                    if (mod.__getattribute__(pd['const1']) == pd['val1'])
                    & (mod.__getattribute__(pd['const2']) == pd['val2'])
                    & (mod.__getattribute__(pd['const3']) == pd['val3'])]
        
        gshape = (len(grid_y), len(grid_x))
        X, Y = np.meshgrid(grid_x, grid_y, indexing='xy')
        Zx = np.zeros(gshape)
        Zy = np.zeros(gshape)
        nrows = gshape[0]
        ncols = gshape[1]
        for ind, val in np.ndenumerate(X):
            arr = [mod for mod in use_mods if (mod.__getattribute__(x_name) == val) & (mod.__getattribute__(y_name) == Y[ind])]
            Zx[ind] = arr[0].__getattribute__(bpt_inds[0])
            Zy[ind] = arr[0].__getattribute__(bpt_inds[1])
        if plot_data:
            sdss.plot_bpt(plot_data, line_ratio=line_ratio, ax=ax)
            vanzee.plot_bpt(plot_data, line_ratio=line_ratio, ax=ax)
        ax.set_xlabel(xlabel, fontsize=16)
        ax.set_ylabel(ylabel, fontsize=16)
        for i in range(nrows):
            if i == 0:
                par_label = kwargs.get('par_label', '__nolegend__')
                color = kwargs.get('color', 'k')
                ax.plot(Zx[i,:], Zy[i,:], color=color, label=par_label)
            else:
                ax.plot(Zx[i,:], Zy[i,:], color=color, label='__nolegend__')
        row_labs = [(Zx[i,0], Zy[i,0], '{0:.1f}'.format(float(np.unique(Y[i,:])))) for i in range(gshape[0])]
        for i in range(ncols):
            ax.plot(Zx[:,i], Zy[:,i], color=color, label='__nolegend__')
        col_labs = [(Zx[0, i], Zy[0, i], '{0:.1f}'.format(float(np.unique(X[:,i])))) for i in range(gshape[1])]
        
        var_label = kwargs.get('var_label', '__nolegend__')
        if var_label:
            for lab in col_labs:
                ax.annotate(lab[-1],
                            xy=(lab[0], lab[1]), xycoords='data',
                            xytext=(0, -10), textcoords='offset points',
                            size=22,
                            horizontalalignment='left',
                            verticalalignment='top')
            ax.annotate(r'log Z/Z$_{\odot}$',
                        xy=(col_labs[2][0], col_labs[2][1]),
                        xycoords='data', xytext=(0, -50),
                        textcoords='offset points', size=22,
                        horizontalalignment='left',
                        verticalalignment='top')
            for lab in row_labs:
                ax.annotate(lab[-1],
                            xy=(lab[0], lab[1]), xycoords='data',
                            xytext=(-10, 0), textcoords='offset points',
                            size=22,
                            horizontalalignment='right',
                            verticalalignment='bottom')
            ax.annotate(r'log U$_0$',
                        xy=(row_labs[1][0], row_labs[1][1]),
                        xycoords='data', xytext=(-50, 15),
                        textcoords='offset points', size=22,
                        horizontalalignment='right',
                        verticalalignment='bottom')
        plt.legend(numpoints=1)
        return

def nice_lines():
    lines = {'ha':[6562.50, r'H\alpha', r'\lambda6563'],
             'hb':[4861.36, r'H\beta', r'\lambda4861'],
             'o3':[5007.00, r'O III', r'\lambda5007'],
             'n2':[6584.00, r'N II', r'\lambda6584'],
             'an2':[6548.00, r'N II', r'\lambda6548'],
             'ao3':[4959.00, r'O III', r'\lambda4959'],
             'o2':[3727.00, r'O II', r'\lambdalambda3726,9'],
             's2a':[6716.00, r'S II', r'\lambda6716'],
             's2b':[6731.00, r'S II', r'\lambda6731'],
             'o1':[6300, r'O I', r'\lambda6300']}
    return lines
    
# uvals = [-3.0, -2.5, -2.0]
# uvals = [18.0, 19.0, 20.0]
# uvals = [0.5e6, 1.0e6, 2.0e6]
# cols = ['red', 'blue', 'green']
# fig = plt.figure()
# ax = fig.add_subplot(111)
# for i in range(3):
#     uval = uvals[i]
#     col = cols[i]
#     if i == 0:
#         pd = True
#     else:
#         pd = False
        
#     mo.makeBPT(const1='age', val1=uval, const2='logR', val2=19.0,
#                const3='nH', val3=10.0, color=col, var_label=True,
#                par_label='{0:.1f} Myr'.format(uval*1.0e-6), plot_data=pd, ax=ax)

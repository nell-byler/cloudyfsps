import numpy as np
from abund_sets import load_abund, load_depl
from .astrotools import sym_to_name
from scipy.interpolate import InterpolatedUnivariateSpline as InterpUS

def _get_abunds(set_name, logZ, dust=True, re_z=False):
    allowed_names = ['dopita', 'newdopita', 'cl01', 'yeh']
    if set_name in allowed_names:
        return eval('{}({}, dust={}, re_z={})'.format(set_name, logZ, dust, re_z))
    else:
        raise IOError(allowed_names)

class Element:
    def __init__(self, name, val):
        self.name=name.title()
        self.fullname = sym_to_name(name)
        self.val=val
    def __str__(self):
        return 'element abundance {0} {1:.1f}'.format(self.name, self.val)
    #def __repr__(self):
    #    return 'element abundance {0} {1:.1f}'.format(self.name, self.val)



class abundSet(object):
    abunds = {}
    def __init__(self, set_name, logZ):
        self.logZ = logZ
        self._abund_dict = load_abund(set_name)
    
    def deplete(self, val):
        return self._abunds
    @property
    def abunds(self):
        return self._abunds
    @abunds.setter
    def abunds(self):
        self._abunds = {}
        [self._abunds.__setitem__(k, Element(k,v)) for k,v in self._abund_dict]
        
        return     
        
    def calcSpecial(self):
        return
    def calcFinal(self):
        return
    def inputStrings(self):
        self.solarstr = 'abundances {} {}'.format(self.solar, self.grains)
        elem_strs = []
        names = sym_to_name()
        for key in self.abund_0.iterkeys():
            elm = names[key]
            abund = self.__getattribute__(key)
            if hasattr(self, 're_z'):
                if key != 'He':
                    abund -= self.re_z
            outstr = 'element abundance {0} {1:.2f} log'.format(elm, abund)
            elem_strs.append(outstr)
        self.__setattr__('elem_strs', elem_strs)
        return

class dopita(abundSet):
    def __init__(self, logZ, dust=True, re_z=False):
        self.solar = 'old solar 84'
        if dust:
            self.grains = 'no grains\ngrains ISM'
        else:
            self.grains = 'no grains'
        if re_z:
            self.re_z = logZ
        else:
            self.re_z = 0.0
        abundSet.__init__(self, 'dopita', logZ)
        
    def calcSpecial(self):
        '''
        piece-wise function for nitrogen abund
        functional form for helium
        '''
        def calc_N(logZ):
            if logZ <= -0.63:
                return -4.57 + logZ
            else:
                return -3.94 + (2.0*logZ)
        def calc_He(logZ):
            return np.log10(0.08096 + (0.02618*(10.0**logZ)))
        
        self.__setattr__('He', calc_He(self.logZ))
        self.__setattr__('N', calc_N(self.logZ)+self.depl['N'])
        return
    def calcFinal(self):
        '''
        apply depletions and scale with logZ
        '''
        [self.__setattr__(key, val+self.logZ+self.depl[key])
         for key, val in self.abund_0.iteritems() if not hasattr(self, key)]
        return

class newdopita(abundSet):
    def __init__(self, logZ, dust=True, re_z=False):
        self.solar = 'GASS10'
        if dust:
            self.grains = 'no grains\ngrains ISM'
        else:
            self.grains = 'no grains'
        self.re_z=re_z
        abundSet.__init__(self, 'newdopita', logZ)
        
    def calcSpecial(self):
        def calc_He(logZ):
            return np.log10(0.0737 + (0.024*(10.0**logZ)))
        def calc_CNO(logZ):
            oxy = np.array([7.39, 7.50, 7.69, 7.99, 8.17,
                    8.39, 8.69, 8.80, 8.99, 9.17, 9.39])
            nit = np.array([-6.61, -6.47, -6.23, -5.79, -5.51,
                    -5.14, -4.60, -4.40, -4.04, -3.67, -3.17])
            car = np.array([-5.58, -5.44, -5.20, -4.76, -4.48,
                    -4.11, -3.57, -3.37, -3.01, -2.64, -2.14])
            O = self.abund_0['O'] + logZ
            C = float(InterpUS(oxy, car, k=1)(O + 12.0))
            N = float(InterpUS(oxy, nit, k=1)(O + 12.0))
            return C, N, O
        self.__setattr__('He', calc_He(self.logZ))
        C, N, O = calc_CNO(self.logZ)
        [self.__setattr__(key, val + self.depl[key])
         for key, val in zip(['C', 'N', 'O'], [C, N, O])]
        return
    def calcFinal(self):
        [self.__setattr__(key, val+self.logZ+self.depl[key])
         for key, val in self.abund_0.iteritems() if not hasattr(self, key)]
        return















import numpy as np

#dicto={'c':13}
#my_abunds = abundSet(logZ=0.0, **dicto)

class abundSet(object):
    
    abunds = ['He', 'N']
    
    def __init__(self, logZ):
        self._abunds = kwargs
        self.iteritems = self._abunds.iteritems
    
    def do_depletion(self):
        return self.abunds + 40.0
    
    @property
    def abunds(self):
        return self._abunds
    
    @abunds.setter
    def abunds(self, value):
        self._abunds = value


class Element:
    def __init__(self, name, val):
        self.name=name.title()
        self.fullname = sym_to_name(name)
        self.val=val
    def __str__(self):
        return 'element abundance {0} {1:.1f}'.format(self.name, self.val)
    def __repr__(self):
        return 'element abundance {0} {1:.1f}'.format(self.name, self.val)


from abund_sets import load_set

def _get_abunds(set_name):
    allowed_names = ['dopita', 'newdopita', 'cl01', 'yeh']
    if set_name in allowed_names:
        return load_set(set_name)
    else:
        raise IOError('Set name must be in ', allowed_names)




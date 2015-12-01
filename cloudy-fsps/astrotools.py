import numpy as np

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

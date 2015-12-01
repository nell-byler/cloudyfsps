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
        

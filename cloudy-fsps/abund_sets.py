def load_abund(set_name):
    if set_name == 'dopita':
        adict = dict(He = -1.01,
                     C = -3.44,
                     N = -3.95,
                     O = -3.07,
                     Ne = -3.91,
                     Mg = -4.42,
                     Si = -4.45,
                     S = -4.79,
                     Ar = -5.44,
                     Ca = -5.64,
                     Fe = -4.33)
    elif set_name == 'newdopita':
        adict = dict(He = -1.01,	
                     C = -3.57,
                     N = -4.60,
                     O = -3.31,
                     Ne = -4.07,
                     Na = -5.75,
                     Mg = -4.40,
                     Al = -5.55,
                     Si = -4.49,
                     S = -4.86,
                     Cl = -6.63,
                     Ar = -5.60,
                     Ca = -5.66,
                     Fe = -4.50,
                     Ni = -5.78)
    return adict
	

def load_depl(set_name):
    if set_name == 'dopita':
        ddict = dict(C = -0.30,
                     N = -0.22,
                     O = -0.22,
                     Ne = 0.0,
                     Mg = -0.70,
                     Si = -1.0,
                     S = 0.0,
                     Ar = 0.0,
                     Ca = -2.52,
                     Fe = -2.0)
    elif set_name == 'newdopita':
        ddict = dict(He =0.00,	
                     C = -0.30,	
                     N = -0.05,	
                     O = -0.07,	
                     Ne = 0.00,	
                     Na = -1.00,	
                     Mg = -1.08,	
                     Al = -1.39,	
                     Si = -0.81,	
                     S = 0.00,	
                     Cl = -1.00,	
                     Ar = 0.00,	
                     Ca = -2.52,	
                     Fe = -1.31,	
                     Ni = -2.00)
    return ddict

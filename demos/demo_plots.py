from cloudyfsps import outobj as ob

dir_ = './output_csfh/' #r18, n100...lots of U and Z
mod_prefix='ZAU'
csf = ob.allmods(dir_, mod_prefix, read_out=True)

Dir_ = './output3ND/' #r18, n100...lots of U and Z
mod_prefix='ZAU'
nd = ob.allmods(dir_, mod_prefix, read_out=True)
ages = [0.5e6, 1.0e6, 1.5e6]
cols = ['red', 'orange', 'green']
ages = [2.0e6, 3.0e6, 5.0e6, 10.0e6]
cols = ['red', 'orange', 'green', 'blue']
fig = plt.figure()
ax = fig.add_subplot(111)
for age, col in zip(ages, cols):
    pd=False
    var_label=False
    if age == 0.5e6:
        pd=True
    if age == 1.0e6:
        var_label=True
    nh.makeBPT(ax=ax, val1=age, color=col,
               par_label='{0:.1f} Myr'.format(age*1.0e-6),
               plot_data=pd, var_label=var_label)


dir_='./output3/'
mod_prefix = 'ZAU'
wd = ob.allmods(dir_, mod_prefix, read_out=True)

ages = [0.5e6, 1.0e6, 2.0e6, 3.0e6]
cols = ['red', 'orange', 'green', 'blue']
fig = plt.figure()
ax = fig.add_subplot(111)
for age, col in zip(ages, cols):
    pd=False
    var_label=False
    if age == 0.5e6:
        pd=True
    if age == 3.0e6:
        var_label=True
    wd.makeBPT(ax=ax, const1='age', val1=age,
               const2='logR', val2=19.0,
               const3='nH', val3=10.0,
               par_label='{0:.1f} Myr'.format(age*1.0e-6),
               var_label=var_label, plot_data=pd, color=col)

ages = [0.5e6, 1.0e6, 2.0e6, 3.0e6]
cols = ['red', 'orange', 'green', 'blue']
fig = plt.figure()
ax = fig.add_subplot(111)
for age, col in zip(ages, cols):
    pd=False
    var_label=False
    if age == 0.5e6:
        pd=True
    if age == 3.0e6:
        var_label=True
    nd.makeBPT(ax=ax, const1='age', val1=age,
               const2='logR', val2=19.0,
               const3='nH', val3=10.0,
               par_label='{0:.1f} Myr'.format(age*1.0e-6),
               var_label=var_label, plot_data=pd, color=col)
fig = plt.figure()
ax = fig.add_subplot(111)
sM = ob.get_colors(np.unique(np.horizontalstack([no.logQ, mo.logQ])))

for q in no.logQ_vals:
    inds = np.where((no.logQ == q) & (no.age == 0.5e6))
    color = sM.to_rgba(q)
    plt.plot(no.bpt_x[inds], no.bpt_y[inds], color=color, lw=3)

for z in no.logZ_vals:
    inds = np.where((no.logZ == z) & (no.age == 0.5e6))
    plt.plot(no.bpt_x[inds], no.bpt_y[inds], '--', color='k', lw=2, alpha=0.5)

for q in mo.logQ_vals:
    inds = np.where((mo.logQ == q) & (mo.age == 0.5e6) & (mo.logZ >= -1.0))
    color = sM.to_rgba(q)
    plt.plot(mo.bpt_x[inds], mo.bpt_y[inds], color=color, lw=3)

for z in mo.logZ_vals:
    if z >= -1.0:
        inds = np.where((mo.logZ == z) & (mo.age == 0.5e6))
        plt.plot(mo.bpt_x[inds], mo.bpt_y[inds], '--', color='k', lw=2, alpha=0.5)


nd.makeBPT(ax=ax, const1='age', val1=0.5e6,
               const2='logR', val2=19.0,
               const3='nH', val3=100.0,
               par_label='Cloudy',
               var_label=True, plot_data=True, color='k')
wd.makeBPT(ax=ax, const1='age', val1=0.5e6,
               const2='logR', val2=19.0,
               const3='nH', val3=10.0,
               par_label='Cloudy',
               var_label=False, plot_data=False, color='k')
sM = get_colors(np.unique(np.horizontalstack([no.logQ, mo.logQ])))



fsps_Q / cloudyQ

sM = ob.get_colors(mo.logZ)

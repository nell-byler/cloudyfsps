from cloudyfsps import outobj as ob

# this code assumes you have run "csfh.py"
# to produce a grid of cloudy models and now
# want to look at the data

dir_ = './output_csfh/'
mod_prefix='ZAU'
# Read in output
csf = ob.allmods(dir_, mod_prefix, auto_corr=True)
# this is a python object with lots of model info.
# Line strengths, gas properties and ionizing properties, etc.

ages = [1.0e6, 2.0e6, 3.0e6, 5.0e6, 10.0e6]
cols = ['red', 'orange', 'green', 'blue', 'purple']
fig = plt.figure()
ax = fig.add_subplot(111)
for age, col in zip(ages, cols):
    pd=False
    var_label=False
    if age == 1.0e6: #only plot the observed data once
        pd=True
    if age == 2.0e6: #only plot the labels once
        var_label=True
    csf.makeBPT(ax=ax, val1=age, color=col,
                par_label='{0:.1f} Myr'.format(age*1.0e-6),
                plot_data=pd, var_label=var_label)



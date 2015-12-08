from setuptools import setup

setup(name='cloudyfsps',
      version='0.1',
      description='nebular emission for FSPS',
      url='http://github.com/nell-byler/cloudyfsps',
      author='Nell Byler',
      author_email='nell.byler@gmail.com',
      license='BSD new',
      packages=['cloudyfsps', 'astrodata'],
      package_dir={'cloudyfsps':'cloudyfsps',
                   'astrodata':'astrodata'},
      package_data={'cloudyfsps':['data/*.dat','*.sh'],
                    'astrodata':['data/*.dat', 'data/*.npz']}, 
      zip_safe=False)

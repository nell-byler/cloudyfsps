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
                    'astrodata':['data/*.dat']}, 
      install_requires=['fsps==0.2.0', 'numpy==1.9.3',
                        'astroML', 'scipy'],
      zip_safe=False)

from setuptools import setup

setup(name='cloudy-fsps',
      version='0.1',
      description='nebular emission for FSPS',
      url='http://github.com/nell-byler/cloudy-fsps',
      author='Nell Byler',
      author_email='nell.byler@gmail.com',
      license='BSD new',
      packages=['cloudy-fsps'],
      install_requires=['fsps'],
      zip_safe=False)

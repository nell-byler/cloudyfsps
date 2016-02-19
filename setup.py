#!/usr/bin/env python

import os
import sys
import glob

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import cloudyfsps
VERSION = cloudyfsps.__version__

setup(name="cloudyfsps",
      version="0.1",
      description="nebular emission for FSPS",
      url="http://github.com/nell-byler/cloudyfsps",
      author="Nell Byler",
      author_email="nell.byler@gmail.com",
      license="BSD new",
      packages=["cloudyfsps",
                "cloudyfsps.astrodata"],
      package_dir={"cloudyfsps":"cloudyfsps",
                   "astrodata":"cloudyfsps/astrodata"},
      package_data={
        "": ["README.rst", "LICENSE.rst", "AUTHORS.rst"],
        "cloudyfsps":["data/*.dat"],
        "astrodata":["data/*.dat", "data/*.npz"]
      },
      include_package_data=True,
      scripts=glob.glob("scripts/*.py"),
      classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python"],
      zip_safe=True)

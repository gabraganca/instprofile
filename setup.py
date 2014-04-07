# -*- coding: utf-8 -*-
"""setup.py: setuptools control."""

import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('instprofile/__init__.py').read(),
    re.M
    ).group(1)

with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(name='instprofile',
      version=version,
      description='Instrumental profile from lamp spectrum.',
      long_description = long_descr,
      url='https://github.com/gabraganca/norm_dif',
      author='Gustavo Bragança',
      author_email='ga.braganca@gmail.com',
      license='3-clause BSD',
      packages=['instprofile'],
      install_requires=['numpy'])

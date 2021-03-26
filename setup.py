#!/usr/bin/env python

from setuptools import setup

setup(name='tdf_innovation',

      description='Python package needed for data quality',
      author='Marylin Pemodjo',
      author_email='marylin.pemodjo@octo.com',
      url='git@gitlab.com:asaboni/tdf_innovation.git',
      packages=['notebooks'],
      install_requires=['recordlinkage', 'mlxtend', 'pandas', 'numpy', 'codecarbon', 'lightgbm']
     )


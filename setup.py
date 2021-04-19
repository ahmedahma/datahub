#!/usr/bin/env python

from setuptools import setup

setup(name='deduplicate',
      description='',
      author='Marylin Pemodjo',
      author_email='amine.saboni@octo.com, marylin.pemodjo@octo.com',
      url='git@gitlab.com:asaboni/tdf_innovation.git',
      packages=['deduplicate'],
      install_requires=[
          'codecarbon',
          'lightgbm',
          'mlxtend',
          'numpy',
          'pandas',
          'recordlinkage',
          'shapash',
          'sklearn',
          'tox'
      ])

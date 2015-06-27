# Copyright 2015 Massachusetts Institute of Technology.

"""
setup.py for installing projector.
"""

from distutils.core import setup
import os

DATADIR = 'templates'
DATAFILES = [(root, [os.path.join(root, f) for f in files])
             for root, dirs, files in os.walk(DATADIR)]

setup(name="projector",
      version="0.1.0",
      description="A convenience tool for creating projects.",
      author="W. Nicholas Greene",
      author_email="wng@csail.mit.edu",
      url="https://github.mit.edu/rrg/projector",
      data_files=DATAFILES,
      scripts=['projector.py'])

# Copyright 2015 Massachusetts Institute of Technology.

"""
setup.py for installing metaproject.
"""

from distutils.core import setup

setup(name="metaproject",
      version="0.1.0",
      description="A convenience tool for creating metaprojects.",
      author="W. Nicholas Greene",
      author_email="wng@csail.mit.edu",
      url="https://github.mit.edu/rrg/metaproject",
      package_data={'': ['template/*']},
      scripts=['metaproject.py'])

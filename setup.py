#!/usr/bin/env python
from setuptools import setup, find_packages
 
setup (
  name = "Nark",
  version = "0.1",
  description="Various python utilities",
  author="Douglas Linder",
  author_email="", # Removed to limit spam harvesting.
  url="",
  package_dir = {'': 'src'},
  packages = find_packages("src", exclude="tests"),
  zip_safe = True
)

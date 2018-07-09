#!/usr/bin/env python
import setuptools  # noqa: F401
from numpy.distutils.core import setup, Extension

setup(ext_modules=[Extension(name='gtd7',
                             sources=['fortran/nrlmsise00_sub.for'],
                             f2py_options=['--quiet'])])

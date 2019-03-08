#!/usr/bin/env python
import setuptools  # noqa: F401
setuptools.setup()
# from numpy.distutils.core import setup, Extension
# import os
# from pathlib import Path


# if os.name == 'nt':
#    sfn = Path(__file__).parent / 'setup.cfg'
#    stxt = sfn.read_text()
#    if '[build_ext]' not in stxt:
#        with sfn.open('a') as f:
#            f.write("[build_ext]\ncompiler = mingw32")


# setup(ext_modules=[Extension(name='gtd7',
#                             sources=['src/nrlmsise00_sub.for'])])

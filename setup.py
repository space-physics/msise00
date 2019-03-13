#!/usr/bin/env python
import setuptools  # noqa: F401
from pathlib import Path
import subprocess
import os

setuptools.setup()
# from numpy.distutils.core import setup, Extension


# if os.name == 'nt':
#    sfn = Path(__file__).parent / 'setup.cfg'
#    stxt = sfn.read_text()
#    if '[build_ext]' not in stxt:
#        with sfn.open('a') as f:
#            f.write("[build_ext]\ncompiler = mingw32")


# setup(ext_modules=[Extension(name='gtd7',
#                             sources=['src/nrlmsise00_sub.for'])])

R = Path(__file__).resolve().parent
BINDIR = R / 'build'
SRCDIR = R / 'src'


def cmake_setup():
    if os.name == 'nt':
        subprocess.check_call(['cmake', '-G', 'MinGW Makefiles',
                               '-DCMAKE_SH="CMAKE_SH-NOTFOUND', str(SRCDIR)],
                              cwd=BINDIR)
    else:
        subprocess.check_call(['cmake', str(SRCDIR)],
                              cwd=BINDIR)

    subprocess.check_call(['cmake', '--build', str(BINDIR), '-j'])


def meson_setup():
    subprocess.check_call(['meson', str(SRCDIR)], cwd=BINDIR)
    subprocess.check_call(['ninja'], cwd=BINDIR)


try:
    meson_setup()
except Exception:
    cmake_setup()

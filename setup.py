#!/usr/bin/env python3
import setuptools #enables develop
import subprocess


with open('README.rst','r') as f:
	  long_description = f.read()

try:
    subprocess.run(['conda','install','--yes','--quiet','--file','requirements.txt'])
except Exception as e:
    print('you will need to install packages in requirements.txt  {}'.format(e))

#%%
from numpy.distutils.core import setup,Extension

#%% install
setup(name='msise00',
      version='0.1',
	  description='Python wrapper for MSIS-E00 atmosphere model',
	  long_description=long_description,
	  author='Michael Hirsch',
	  url='https://github.com/scienceopen/msise00',
	  install_requires=['pymap3d','histutils'],
      packages=['msise00'],
      dependency_links = ['https://github.com/scienceopen/pymap3d/tarball/master#egg=pymap3d',
                          'https://github.com/scienceopen/histutils/tarball/master#egg=histutils'
                            ],
      ext_modules=[Extension(name='gtd7',
                    sources=['fortrancode/nrlmsise00_sub.for'],
                    f2py_options=['--quiet'])]
	  )


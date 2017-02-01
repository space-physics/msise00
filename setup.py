#!/usr/bin/env python
import setuptools #enables develop
try:
    import conda.cli
    conda.cli.main('install','--file','requirements.txt')
except Exception as e:
    print(e)

#%%
from numpy.distutils.core import setup,Extension

ext = Extension(name='gtd7',
                sources=['fortrancode/nrlmsise00_sub.for'],
                f2py_options=['--quiet'])

#%% install
setup(name='msise00',
	  install_requires=['pymap3d','histutils'],
      dependency_links = ['https://github.com/scienceopen/pymap3d/tarball/master#egg=pymap3d',
                          'https://github.com/scienceopen/histutils/tarball/master#egg=histutils'
                            ],
      ext_modules=[ext],
      packages=['msise00']
	  )


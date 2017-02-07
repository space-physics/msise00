#!/usr/bin/env python
import setuptools #enables develop
try:
    import conda.cli
    conda.cli.main('install','--file','requirements.txt')
except Exception as e:
    print(e)
    import pip
    pip.main(['install','-r','requirements.txt'])

#%%
from numpy.distutils.core import setup,Extension

ext = Extension(name='gtd7',
                sources=['fortrancode/nrlmsise00_sub.for'],
                f2py_options=['--quiet'])

#%% install
setup(name='msise00',
      description='Python API for Fortran MSISE-00 neutral atmosphere model.',
      author = 'Michael Hirsch',
      url='https://github.com/scienceopen/msise00',
      classifiers=[
      'Intended Audience :: Science/Research',
      'Development Status :: 4 - Beta',
      'License :: OSI Approved :: MIT License',
      'Topic :: Scientific/Engineering :: Atmospheric Science',
      'Programming Language :: Python :: 3.6',
      ],
	  install_requires=['pymap3d',
                        'histutils','gridaurora'],
      dependency_links = [
        'https://github.com/scienceopen/histutils/tarball/master#egg=histutils',
        'https://github.com/scienceopen/gridaurora/tarball/master#egg=gridaurora'
                            ],
      ext_modules=[ext],
      packages=['msise00']
	  )


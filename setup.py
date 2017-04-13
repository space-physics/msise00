#!/usr/bin/env python
import setuptools #enables develop
from numpy.distutils.core import setup,Extension

req = ['nose','python-dateutil','pytz','numpy','scipy','pandas','xarray','h5py','astropy','matplotlib','seaborn',
    'pymap3d','sciencedates','gridaurora']

ext = Extension(name='gtd7',
                sources=['fortran/nrlmsise00_sub.for'],
                f2py_options=['--quiet'])

#%% install
setup(name='msise00',
      description='Python API for Fortran MSISE-00 neutral atmosphere model.',
      author = 'Michael Hirsch',
      version = '0.9',
      url='https://github.com/scivision/msise00',
      classifiers=[
      'Intended Audience :: Science/Research',
      'Development Status :: 4 - Beta',
      'License :: OSI Approved :: MIT License',
      'Topic :: Scientific/Engineering :: Atmospheric Science',
      'Programming Language :: Python :: 3.6',
      ],
	  install_requires=req,
      ext_modules=[ext],
      packages=['msise00']
	  )


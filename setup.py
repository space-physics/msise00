#!/usr/bin/env python
req = ['nose','python-dateutil','pytz','numpy','scipy','pandas','xarray','h5py','astropy','matplotlib','seaborn','pathlib2']
pipreq=['pymap3d','sciencedates','gridaurora']
# %%
import pip
try:
    import conda.cli
    conda.cli.main('install',*req)
except Exception as e:
    pip.main(['install']+req)
pip.main(['install']+pipreq)
# %%
import setuptools #enables develop
from numpy.distutils.core import setup,Extension

setup(name='msise00',
      packages=['msise00'],
      description='Python API for Fortran MSISE-00 neutral atmosphere model.',
      author='Michael Hirsch, Ph.D.',
      version='1.0.0',
      url='https://github.com/scivision/msise00',
      classifiers=[
      'Intended Audience :: Science/Research',
      'Development Status :: 4 - Beta',
      'License :: OSI Approved :: MIT License',
      'Topic :: Scientific/Engineering :: Atmospheric Science',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3.6',
      ],
      ext_modules=[Extension(name='gtd7',
                sources=['fortran/nrlmsise00_sub.for'],
                f2py_options=['--quiet'])],
	  )


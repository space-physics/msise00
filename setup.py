#!/usr/bin/env python
from setuptools import find_packages
from numpy.distutils.core import setup, Extension

install_requires = ['python-dateutil', 'pytz', 'numpy', 'xarray',
                    'sciencedates', 'gridaurora']
tests_require = ['pytest', 'coveralls', 'flake8', 'mypy']


setup(name='msise00',
      packages=find_packages(),
      description='Python API for Fortran MSISE-00 neutral atmosphere model.',
      author='Michael Hirsch, Ph.D.',
      version='1.1.2',
      long_description=open('README.md').read(),
      long_description_content_type="text/markdown",
      url='https://github.com/scivision/msise00',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: Scientific/Engineering :: Atmospheric Science',
      ],
      ext_modules=[Extension(name='gtd7',
                             sources=['fortran/nrlmsise00_sub.for'],
                             f2py_options=['--quiet'])],
      install_requires=install_requires,
      tests_require=tests_require,
      python_requires='>=3.6',
      extras_require={'plot': ['matplotlib', 'seaborn'],
                      'io': ['astropy', 'pymap3d'],
                      'tests': tests_require},
      script=['RunMSIS.py'],
      include_package_data=True,
      )

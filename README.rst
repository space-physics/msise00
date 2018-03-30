.. image:: https://zenodo.org/badge/32971905.svg
   :target: https://zenodo.org/badge/latestdoi/32971905

.. image:: https://travis-ci.org/scivision/msise00.svg
    :target: https://travis-ci.org/scivision/msise00

.. image:: https://coveralls.io/repos/scivision/msise00/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/scivision/msise00?branch=master

.. image:: https://img.shields.io/pypi/pyversions/msise00.svg
  :target: https://pypi.python.org/pypi/msise00
  :alt: Python versions (PyPI)

.. image::  https://img.shields.io/pypi/format/msise00.svg
  :target: https://pypi.python.org/pypi/msise00
  :alt: Distribution format (PyPI)

.. image:: https://api.codeclimate.com/v1/badges/f6f206d6f6605bcf435d/maintainability
   :target: https://codeclimate.com/github/scivision/msise00/maintainability
   :alt: Maintainability


==========
msise-00
==========
NRL MSISE-00 atmospheric model.
Valid from altitude z = 0 - 1000 km.

The plot immediately below shows a slice at 200km on a world-wide grid.
The yellow ball represents the sun footprint on Earth.

.. image:: tests/msise00_demo.gif

Install
=======
If you don't already have Numpy::

    pip install numpy

* Mac: ``brew install gcc``
* Linux: ``apt install gfortran``
* `Windows <https://www.scivision.co/windows-gcc-gfortran-cmake-make-install/>`_ or use `Windows Subsystem for Linux <https://www.scivision.co/install-windows-subsystem-for-linux/>`_.

And then::

  pip install -e .

Examples
========

Write NetCDF4 output (HDF5 compatible) with command line argument `-w filename.nc`

Altitude Profile
~~~~~~~~~~~~~~~~
::

    python RunMSIS.py 2017-08-21 -c 40 -90


Grid: time,lat,lon
~~~~~~~~~~~~~~~~~~
This example takes several minutes, and generates the plots in the README::

    python RunMSIS.py

Reference
=========
`Original fortran code <http://nssdcftp.gsfc.nasa.gov/models/atmospheric/msis/nrlmsise00/>`_

`1200+ citations 2002 paper <http://onlinelibrary.wiley.com/doi/10.1029/2002JA009430/pdf>`_

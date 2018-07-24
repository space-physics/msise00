[![Zenodo DOI](https://zenodo.org/badge/32971905.svg)](https://zenodo.org/badge/latestdoi/32971905)
[![Travis-CI](https://travis-ci.org/scivision/msise00.svg)](https://travis-ci.org/scivision/msise00)
[![Coverage](https://coveralls.io/repos/scivision/msise00/badge.svg?branch=master&service=github)](https://coveralls.io/github/scivision/msise00?branch=master)
[![Build status](https://ci.appveyor.com/api/projects/status/g58w79defiiiu6j6?svg=true)](https://ci.appveyor.com/project/scivision/msise00)
[![Python versions (PyPI)](https://img.shields.io/pypi/pyversions/msise00.svg)](https://pypi.python.org/pypi/msise00)
[![Distribution format (PyPI)](https://img.shields.io/pypi/format/msise00.svg)](https://pypi.python.org/pypi/msise00)
[![Maintainability](https://api.codeclimate.com/v1/badges/f6f206d6f6605bcf435d/maintainability)](https://codeclimate.com/github/scivision/msise00/maintainability)
[![PyPi Download stats](http://pepy.tech/badge/msise00)](http://pepy.tech/project/msise00)

# MSISE-00 in Python

NRL MSISE-00 atmospheric model for Python &ge; 3.6, also accessible via Matlab.
Valid from altitude z = 0..1000 km.

The plot immediately below shows a slice at 200km on a world-wide grid.
The yellow ball represents the sun footprint on Earth.

![MSIS global time animation](tests/msise00_demo.gif)

This plot is from [Matlab](tests/test_msise00_matlab.m) calling the Python MSISE00:

![MSISE00 Matlab](tests/msis_matlab.png)

## Install

-   Mac: `brew install gcc`
-   Linux: `apt install gfortran`
-   [Windows](https://www.scivision.co/windows-gcc-gfortran-cmake-make-install/)
    or use [Windows Subsystem for Linux](https://www.scivision.co/install-windows-subsystem-for-linux/).

And then:

    pip install -e .

## Examples

MSISE00 can be used from the command line, as an imported module, and even from Matlab.

### import module

```python
import msise00
from datetime import datetime

atmos = msise00.rungtd1d(time=datetime(2013, 3, 31, 12), altkm=150., glat=65., glon=-148.)
```

atmos is an [xarray.Dataset](http://xarray.pydata.org/en/stable/generated/xarray.Dataset.html) containing all the simulation output values.
`atmos` is 4-D: (time, altitude, lat, lon), and indexed like `atmos['N2']`


### Command Line

Write NetCDF4 output (HDF5 compatible) with command line argument `-w filename.nc`.


#### Altitude Profile

at a single time:

    msis00 -t 2017-08-21T20:48 -c 40 -90

#### Alt. profile time-range

with hourly time step:

    msis00 -t 2017-08-21 2017-08-22 -c 40 -90

#### Grid: time,lat,lon

This example takes several minutes, and generates the plots in the README:

    msis00 -t 2016-09-20 2016-09-21

A single time lat/lon can be plotted:

    msise00 -t 2017-01-02T12

### Matlab
Matlab &ge; R2014b can interface directly with most Python modules, for example:

```matlab
atmos = py.msise00.run(time,altkm,glat,glon)
```

## Reference

* Original fortran [code](https://ccmc.gsfc.nasa.gov/pub/modelweb/atmospheric/msis/)
* 1200+ citations 2002 [paper](http://onlinelibrary.wiley.com/doi/10.1029/2002JA009430/pdf)

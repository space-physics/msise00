#!/usr/bin/env python
from pathlib import Path
import tempfile
import subprocess
import pytest
import xarray
import xarray.tests

R = Path(__file__).parent


def test_one_alt_one_time():
    """
    Regenerate ref3.nc by:
        ./msis00.py -q -w ref3.nc -a 200 -t 2017-03-01T12
    """
    pytest.importorskip('netCDF4')

    with tempfile.TemporaryDirectory() as d:
        fn = Path(d) / 'test.nc'
        subprocess.check_call(['msis00', '-q', '-w', str(fn), '-a', '200', '-t', '2017-03-01T12'])

        dat = xarray.open_dataset(fn)
        ref = xarray.open_dataset(R/'ref3.nc')
        xarray.tests.assert_allclose(ref, dat)


def test_time_range():
    """
    Regenerate ref4.nc by:
        ./msis00.py -q -w ref4.nc -gs 90 90 -t 2017-03-01T12 2017-03-01T14
    """
    pytest.importorskip('netCDF4')

    with tempfile.TemporaryDirectory() as d:
        fn = Path(d) / 'test.nc'
        subprocess.check_call(['msis00', '-q', '-w', str(fn),
                               '-gs', '90', '90', '-a', '200',
                               '-t', '2017-03-01T12', '2017-03-01T14'])

        dat = xarray.open_dataset(fn)
        ref = xarray.open_dataset(R/'ref4.nc')
        xarray.tests.assert_allclose(ref, dat)


def test_one_loc_one_time():
    """
    regenererate ref6.nc by:
        ./msis00.py -q -w ref6.nc -t 2017-03-01T12 -c 65 -148
    """
    pytest.importorskip('netCDF4')

    with tempfile.TemporaryDirectory() as d:
        fn = Path(d) / 'test.nc'
        subprocess.check_call(['msis00', '-q', '-w', str(fn), '-a', '200',
                               '-t', '2017-03-01T12', '-c', '65', '-148'])

        dat = xarray.open_dataset(fn)
        ref = xarray.open_dataset(R/'ref6.nc')
        xarray.tests.assert_allclose(ref, dat)


def test_one_alt_one_time_one_loc():
    """
    regenerate ref5.nc by:
        ./msis00.py -q -w ref5.nc -a 100 -t 2017-03-01T12 -c 65 -148
    """
    pytest.importorskip('netCDF4')

    with tempfile.TemporaryDirectory() as d:
        fn = Path(d) / 'test.nc'
        subprocess.check_call(['msis00', '-q', '-w', str(fn),
                               '-a', '100', '-t', '2017-03-01T12', '-c', '65', '-148'])

        dat = xarray.open_dataset(fn)
        ref = xarray.open_dataset(R/'ref5.nc')
        xarray.tests.assert_allclose(ref, dat)


if __name__ == '__main__':
    pytest.main(['-x', __file__])

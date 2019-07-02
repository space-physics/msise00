#!/usr/bin/env python
"""
Regenerate test data:

./MSISE00.py -q -w tests/ref3.nc -a 200 -t 2017-03-01T12
./MSISE00.py -q -w tests/ref4.nc -a 200 -gs 90 90 -t 2017-03-01T12 2017-03-01T14
./MSISE00.py -q -w tests/ref6.nc -a 200 -t 2017-03-01T12 -c 65 -148
./MSISE00.py -q -w tests/ref5.nc -a 100 -t 2017-03-01T12 -c 65 -148
"""
from pathlib import Path
import subprocess
import pytest
import xarray
import xarray.tests

R = Path(__file__).parent


def test_one_alt_one_time(tmp_path):
    pytest.importorskip('netCDF4')

    fn = tmp_path / 'test.nc'
    cmd = ['MSISE00', '-q', '-w', str(fn), '-a', '200', '-t', '2017-03-01T12']
    print(' '.join(cmd))
    subprocess.check_call(cmd)

    dat = xarray.open_dataset(fn)
    ref = xarray.open_dataset(R/'ref3.nc')
    xarray.tests.assert_allclose(ref, dat)


def test_time_range(tmp_path):
    pytest.importorskip('netCDF4')

    fn = tmp_path / 'test.nc'
    subprocess.check_call(['MSISE00', '-q', '-w', str(fn),
                           '-gs', '90', '90', '-a', '200',
                           '-t', '2017-03-01T12', '2017-03-01T14'])

    dat = xarray.open_dataset(fn)
    ref = xarray.open_dataset(R/'ref4.nc')
    xarray.tests.assert_allclose(ref, dat)


def test_one_loc_one_time(tmp_path):
    pytest.importorskip('netCDF4')

    fn = tmp_path / 'test.nc'
    subprocess.check_call(['MSISE00', '-q', '-w', str(fn), '-a', '200',
                           '-t', '2017-03-01T12', '-c', '65', '-148'])

    dat = xarray.open_dataset(fn)
    ref = xarray.open_dataset(R/'ref6.nc')
    xarray.tests.assert_allclose(ref, dat)


def test_one_alt_one_time_one_loc(tmp_path):
    pytest.importorskip('netCDF4')

    fn = tmp_path / 'test.nc'
    subprocess.check_call(['MSISE00', '-q', '-w', str(fn),
                           '-a', '100', '-t', '2017-03-01T12', '-c', '65', '-148'])

    dat = xarray.open_dataset(fn)
    ref = xarray.open_dataset(R/'ref5.nc')
    xarray.tests.assert_allclose(ref, dat)


if __name__ == '__main__':
    pytest.main(['-xv', __file__])

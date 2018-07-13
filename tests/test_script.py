#!/usr/bin/env python
from pathlib import Path
import tempfile
import subprocess
import pytest
import xarray

R = Path(__file__).parent

def test_blank():
    """current time, gridded over world, one altitude
       specified -gs 90 90 just to speed up on CI
    """
    with tempfile.TemporaryDirectory() as d:
        fn = Path(d) / 'test.nc'
        subprocess.check_call(['msis00', '-q', '-w', str(fn), '-gs', '90', '90'])

        dat = xarray.open_dataset(fn)
        ref = xarray.open_dataset(R/'ref1.nc')
        assert ref.species == dat.species
        assert ref.alt_km == dat.alt_km
        assert ref.lat.equals(dat.lat)
        assert ref.lon.equals(dat.lon)


def test_one_time():
    """ same as test_blank """
    with tempfile.TemporaryDirectory() as d:
        fn = Path(d) / 'test.nc'
        subprocess.check_call(['msis00', '-q', '-w', str(fn), '-gs', '90', '90',
                               '-t', '2017-03-21T12'])

        dat = xarray.open_dataset(fn)
        ref = xarray.open_dataset(R/'ref2.nc')
        assert ref.equals(dat)


def test_one_alt():
    """ same as test_blank """
    with tempfile.TemporaryDirectory() as d:
        fn = Path(d) / 'test.nc'
        subprocess.check_call(['msis00', '-q', '-w', str(fn), '-gs', '90', '90',
                               '-a', '200'])

        dat = xarray.open_dataset(fn)
        ref = xarray.open_dataset(R/'ref1.nc')
        assert ref.species == dat.species
        assert ref.alt_km == dat.alt_km
        assert ref.lat.equals(dat.lat)
        assert ref.lon.equals(dat.lon)


def test_one_alt_one_time():
    """ same as test_blank """
    with tempfile.TemporaryDirectory() as d:
        fn = Path(d) / 'test.nc'
        subprocess.check_call(['msis00', '-q', '-w', str(fn), '-a', '200', '-t', '2017-03-01T12'])

        dat = xarray.open_dataset(fn)
        ref = xarray.open_dataset(R/'ref3.nc')
        assert ref.equals(dat)


def test_time_range():
    with tempfile.TemporaryDirectory() as d:
        fn = Path(d) / 'test.nc'
        subprocess.check_call(['msis00', '-q', '-w', str(fn), '-gs', '90', '90',
                               '-t', '2017-03-01T12', '2017-03-01T14'])

        dat = xarray.open_dataset(fn)
        ref = xarray.open_dataset(R/'ref4.nc')
        assert ref.equals(dat)


def test_one_loc():
    with tempfile.TemporaryDirectory() as d:
        fn = Path(d) / 'test.nc'
        subprocess.check_call(['msis00', '-q', '-w', str(fn),
                               '-c', '65', '-148'])

        dat = xarray.open_dataset(fn)
        ref = xarray.open_dataset(R/'ref6.nc')
        assert ref.species == dat.species
        assert ref.alt_km == dat.alt_km
        assert ref.lat.equals(dat.lat)
        assert ref.lon.equals(dat.lon)


def test_one_loc_one_time():
    with tempfile.TemporaryDirectory() as d:
        fn = Path(d) / 'test.nc'
        subprocess.check_call(['msis00', '-q', '-w', str(fn),
                               '-t', '2017-03-01T12', '-c', '65', '-148'])

        dat = xarray.open_dataset(fn)
        ref = xarray.open_dataset(R/'ref6.nc')
        assert ref.equals(dat)


def test_one_alt_one_time_one_loc():
    with tempfile.TemporaryDirectory() as d:
        fn = Path(d) / 'test.nc'
        subprocess.check_call(['msis00', '-q', '-w', str(fn),
                               '-a', '100', '-t', '2017-03-01T12', '-c', '65', '-148'])

        dat = xarray.open_dataset(fn)
        ref = xarray.open_dataset(R/'ref5.nc')
        assert ref.equals(dat)


if __name__ == '__main__':
    pytest.main()

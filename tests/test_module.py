#!/usr/bin/env python
from datetime import datetime
import pytest
from pytest import approx
import msise00.base as mb


def test_gtd1d():
    t = datetime(2013, 3, 31, 12)
    altkm = 150.
    glat = 65.
    glon = -148.

    atmos = mb.rungtd1d(t, altkm, glat, glon)

    assert atmos['He'].ndim == 4
    assert atmos['He'].size == 1
    dims = list(atmos.dims)
    assert ['alt_km', 'lat', 'lon', 'time'] == dims

    assert atmos['He'].item() == approx(11932380700000.0)
    assert atmos['O'].item() == approx(1.3053125e+16)
    assert atmos['N2'].item() == approx(3.05005836e+16)
    assert atmos['O2'].item() == approx(2662636520000000.0)
    assert atmos['Ar'].item() == approx(67714152400000.0)
    assert atmos['Total'].item() == approx(1.91058636e-09)
    assert atmos['N'].item() == approx(9148033930000.0)
    assert atmos['AnomalousO'].item() == approx(5.3806201e-15)

    assert atmos.species == ['He', 'O', 'N2', 'O2', 'Ar', 'Total', 'H', 'N', 'AnomalousO']

    assert atmos['Tn'].item() == approx(680.611206)
    assert atmos['Texo'].item() == approx(936.991211)


def test_forecast():
    t = datetime(2023, 3, 31, 12)
    altkm = 150.
    glat = 65.
    glon = -148.

    atmos = mb.rungtd1d(t, altkm, glat, glon)

    assert atmos['He'].ndim == 4
    assert atmos['He'].size == 1
    dims = list(atmos.dims)
    assert ['alt_km', 'lat', 'lon', 'time'] == dims

    assert atmos['He'].item() == approx(4392053900000.0)
    assert atmos['O'].item() == approx(4572071070000000.0)
    assert atmos['N2'].item() == approx(3.69985706e+16)
    assert atmos['O2'].item() == approx(8123153790000000.0)
    assert atmos['Ar'].item() == approx(335924592000000.0)
    assert atmos['Total'].item() == approx(2.2950164e-09)
    assert atmos['N'].item() == approx(2154703490000.0)
    assert atmos['AnomalousO'].item() == approx(8.75042368e-16)

    assert atmos.species == ['He', 'O', 'N2', 'O2', 'Ar', 'Total', 'H', 'N', 'AnomalousO']

    assert atmos['Tn'].item() == approx(666.979004)
    assert atmos['Texo'].item() == approx(922.03186)


if __name__ == '__main__':
    pytest.main(['-xv', __file__])

#!/usr/bin/env python
from numpy.testing import assert_allclose
from datetime import datetime
import pytest
import msise00


def test_gtd1d():
    t = datetime(2013, 3, 31, 12)
    altkm = 150.
    glat = 65.
    glon = -148.

    atmos = msise00.rungtd1d(t, altkm, glat, glon)

    assert atmos['He'].ndim == 4
    assert atmos['He'].size == 1
    dims = list(atmos.dims)
    assert ['alt_km', 'lat', 'lon', 'time'] == dims

    assert_allclose(atmos['He'], 11908118740992.0)
    assert_allclose(atmos['O'],  1.306165589835776e+16)
    assert_allclose(atmos['N2'], 3.051389580214272e+16)
    assert_allclose(atmos['O2'],  2664322295660544.0)
    assert_allclose(atmos['Ar'],  67772830711808.0)
    assert_allclose(atmos['Total'], 1.9115256044699436e-09)
    assert_allclose(atmos['N'],  9171036536832.0)
    assert_allclose(atmos['AnomalousO'], 5.380620096337701e-15)

    assert atmos.species == ['He', 'O', 'N2', 'O2', 'Ar', 'Total', 'H', 'N', 'AnomalousO']

    assert_allclose(atmos['Tn'],   681.584167)
    assert_allclose(atmos['Texo'], 941.289246)


def test_forecast():
    t = datetime(2023, 3, 31, 12)
    altkm = 150.
    glat = 65.
    glon = -148.

    atmos = msise00.rungtd1d(t, altkm, glat, glon)

    assert atmos['He'].ndim == 4
    assert atmos['He'].size == 1
    dims = list(atmos.dims)
    assert ['alt_km', 'lat', 'lon', 'time'] == dims

    assert_allclose(atmos['He'], 4391892942848.0)
    assert_allclose(atmos['O'],  4572213877407744.0)
    assert_allclose(atmos['N2'], 3.699869941864858e+16)
    assert_allclose(atmos['O2'],  8123202106556416.0)
    assert_allclose(atmos['Ar'],  335927545167872.0)
    assert_allclose(atmos['Total'], 2.2950290556877917e-09)
    assert_allclose(atmos['N'],  2154773479424.0)
    assert_allclose(atmos['AnomalousO'], 8.750423680563095e-16)

    assert atmos.species == ['He', 'O', 'N2', 'O2', 'Ar', 'Total', 'H', 'N', 'AnomalousO']

    assert_allclose(atmos['Tn'],   666.9913330078125)
    assert_allclose(atmos['Texo'], 922.104736328125)


if __name__ == '__main__':
    pytest.main()

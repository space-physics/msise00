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

    assert_allclose(atmos['He'], 1.05781626142e+13)
    assert_allclose(atmos['O'],  1.184932e+16)
    assert_allclose(atmos['N2'], 3.13963956173e+16)
    assert_allclose(atmos['O2'],  2.9984524976e+15)
    assert_allclose(atmos['Ar'],  7.899407869e+13)
    assert_allclose(atmos['Total'], 1.938796678757e-09)
    assert_allclose(atmos['N'],  7.743147081728e+12)
    assert_allclose(atmos['AnomalousO'], 5.001278932e-15)

    assert atmos.species == ['He', 'O', 'N2', 'O2', 'Ar', 'Total', 'H', 'N', 'AnomalousO']

    assert_allclose(atmos['Tn'],  687.578613)
    assert_allclose(atmos['Texo'], 958.463623)


if __name__ == '__main__':
    pytest.main()

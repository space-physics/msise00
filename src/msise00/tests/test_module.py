from datetime import datetime
import pytest
from pytest import approx

import msise00


def test_past():
    t = datetime(2013, 3, 31, 12)
    altkm = 150.0
    glat = 65.0
    glon = -148.0

    try:
        atmos = msise00.run(t, altkm, glat, glon)
    except ConnectionError:
        pytest.skip("unable to download RecentIndices.txt")

    assert atmos["He"].ndim == 4
    assert atmos["He"].size == 1
    dims = list(atmos.dims)
    assert ["alt_km", "lat", "lon", "time"] == dims

    try:  # daily resolution
        assert atmos["He"].item() == approx(4365665440000.0)
        assert atmos["O"].item() == approx(9612878760000000.0)
        assert atmos["N2"].item() == approx(3.15052301e16)
        assert atmos["O2"].item() == approx(2312921490000000.0)
        assert atmos["Ar"].item() == approx(71974164400000.0)
        assert atmos["Total"].item() == approx(1.84757176e-09)
        assert atmos["N"].item() == approx(9424203680000.0)
        assert atmos["AnomalousO"].item() == approx(1.17317104e-14)

        assert atmos["Tn"].item() == approx(682.538, abs=0.01)
        assert atmos["Texo"].item() == approx(948.350, abs=0.01)
    except AssertionError:  # monthly resolution
        assert atmos["He"].item() == approx(4200180480000.0)
        assert atmos["O"].item() == approx(9338048100000000.0)
        assert atmos["N2"].item() == approx(3.23984781e16)
        assert atmos["O2"].item() == approx(2413811350000000.0)
        assert atmos["Ar"].item() == approx(81071685200000.0)
        assert atmos["Total"].item() == approx(1.88774951e-09)
        assert atmos["N"].item() == approx(9310465690000.0)
        assert atmos["AnomalousO"].item() == approx(5.3806201e-15)

        assert atmos["Tn"].item() == approx(699.021, abs=0.01)
        assert atmos["Texo"].item() == approx(1000.513, abs=0.01)

    assert atmos.species == ["He", "O", "N2", "O2", "Ar", "Total", "H", "N", "AnomalousO"]


def test_forecast():
    t = datetime(2023, 3, 31, 12)
    altkm = 150.0
    glat = 65.0
    glon = -148.0

    atmos = msise00.run(t, altkm, glat, glon)

    assert atmos["He"].ndim == 4
    assert atmos["He"].size == 1
    dims = list(atmos.dims)
    assert ["alt_km", "lat", "lon", "time"] == dims

    assert atmos["He"].item() == approx(1240641440000.0)
    assert atmos["O"].item() == approx(3047968100000000.0)
    assert atmos["N2"].item() == approx(3.597249e16)
    assert atmos["O2"].item() == approx(7343665540000000.0)
    assert atmos["Ar"].item() == approx(334703983000000.0)
    assert atmos["Total"].item() == approx(2.16534546e-09)
    assert atmos["N"].item() == approx(2576280450000.0)
    assert atmos["AnomalousO"].item() == approx(8.75042368e-16)

    assert atmos.species == ["He", "O", "N2", "O2", "Ar", "Total", "H", "N", "AnomalousO"]

    assert atmos["Tn"].item() == approx(671.513, abs=0.01)
    assert atmos["Texo"].item() == approx(883.342, abs=0.01)

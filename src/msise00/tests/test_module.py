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
    assert ["time", "alt_km", "lat", "lon"] == dims

    # daily resolution
    assert atmos["He"].item() == approx(1.2523275e13)
    assert atmos["O"].item() == approx(1.3222577e16)
    assert atmos["N2"].item() == approx(2.9318694e16)
    assert atmos["O2"].item() == approx(2.6164412e15)
    assert atmos["Ar"].item() == approx(5.9933693e13)
    assert atmos["Total"].item() == approx(1.8571854e-9)
    assert atmos["N"].item() == approx(9.1038102e12)
    assert atmos["AnomalousO"].item() == approx(4.503e-14)

    assert atmos["Tn"].item() == approx(655.79, abs=0.01)
    assert atmos["Texo"].item() == approx(875.18, abs=0.01)

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
    assert ["time", "alt_km", "lat", "lon"] == dims

    assert atmos["He"].item() == approx(4.3926901e12)
    assert atmos["O"].item() == approx(4.5728936e15)
    assert atmos["N2"].item() == approx(3.7001117e16)
    assert atmos["O2"].item() == approx(8.1215314e15)
    assert atmos["Ar"].item() == approx(3.3594181e14)
    assert atmos["Total"].item() == approx(2.2950717e-09)
    assert atmos["N"].item() == approx(2.155302e12)
    assert atmos["AnomalousO"].item() == approx(8.7590428e-16)

    assert atmos.species == ["He", "O", "N2", "O2", "Ar", "Total", "H", "N", "AnomalousO"]

    assert atmos["Tn"].item() == approx(667.06, abs=0.01)
    assert atmos["Texo"].item() == approx(922.28, abs=0.01)

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
import msise00
import msise00.worldgrid

R = Path(__file__).parent


def test_one_alt_one_time(tmp_path):
    pytest.importorskip("netCDF4")
    ref = xarray.open_dataset(R / "ref3.nc")

    lat, lon = msise00.worldgrid.latlonworldgrid(30, 60)
    time = "2017-03-01T12"
    altkm = 200.0
    indices = {"f107": 79.3, "f107s": 76.6802469, "Ap": 39}
    try:
        dat_mod = msise00.run(time, altkm, lat, lon, indices).squeeze()
    except ConnectionError:
        pytest.xfail("unable to download RecentIndices.txt")
    xarray.tests.assert_allclose(ref, dat_mod)

    fn = tmp_path / "test.nc"
    cmd = ["MSISE00", "-q", "-w", str(fn), "-a", str(altkm), "-t", time, "-gs", "30", "60"]
    print(" ".join(cmd))
    subprocess.check_call(cmd)

    dat = xarray.open_dataset(fn)
    xarray.tests.assert_allclose(ref, dat)


def test_multiple_time(tmp_path):
    pytest.importorskip("netCDF4")
    ref = xarray.open_dataset(R / "ref4.nc")

    lat, lon = msise00.worldgrid.latlonworldgrid(90, 90)
    time = ["2017-03-01T12", "2017-03-01T13"]
    altkm = 200.0

    try:
        dat_mod = msise00.run(time, altkm, lat, lon).squeeze()
    except ConnectionError:
        pytest.xfail("unable to download RecentIndices.txt")
    xarray.tests.assert_allclose(ref, dat_mod)

    fn = tmp_path / "test.nc"
    cmd = [
        "MSISE00",
        "-q",
        "-w",
        str(fn),
        "-gs",
        "90",
        "90",
        "-a",
        str(altkm),
        "-t",
        "2017-03-01T12",
        "2017-03-01T13",
    ]
    print(" ".join(cmd))
    subprocess.check_call(cmd)

    dat = xarray.open_dataset(fn)
    xarray.tests.assert_allclose(ref, dat)


@pytest.mark.parametrize("altkm,reffn", [(100.0, "ref5.nc"), (200.0, "ref6.nc")])
def test_one_loc_one_time(altkm, reffn, tmp_path):
    pytest.importorskip("netCDF4")
    ref = xarray.open_dataset(R / reffn)

    lat = 65
    lon = -148
    time = "2017-03-01T12"

    try:
        dat_mod = msise00.run(time, altkm, lat, lon).squeeze()
    except ConnectionError:
        pytest.xfail("unable to download RecentIndices.txt")
    xarray.tests.assert_allclose(ref, dat_mod)

    fn = tmp_path / "test.nc"
    cmd = ["MSISE00", "-q", "-w", str(fn), "-a", str(altkm), "-t", time, "-c", str(lat), str(lon)]
    print(" ".join(cmd))
    subprocess.check_call(cmd)

    dat = xarray.open_dataset(fn)
    xarray.tests.assert_allclose(ref, dat)


if __name__ == "__main__":
    pytest.main(["-xv", __file__])

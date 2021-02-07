"""
regenerate data:

python -m msise00 -w src/msise00/tests/ref3.nc -a 200 -gs 30 60 -t 2017-03-01T12
"""

import subprocess
import pytest
import xarray
import xarray.tests
import importlib.resources

import msise00
import msise00.worldgrid

altkm = 200.0
time = "2017-03-01T12"


def test_one_alt_one_time():
    pytest.importorskip("netCDF4")

    with importlib.resources.path(__package__, "ref3.nc") as fn:
        ref = xarray.open_dataset(fn)

    lat, lon = msise00.worldgrid.latlonworldgrid(30, 60)

    try:
        dat_mod = msise00.run(time, altkm, lat, lon).squeeze()
    except ConnectionError:
        pytest.skip("unable to download RecentIndices.txt")
    xarray.tests.assert_allclose(ref, dat_mod)


def test_script(tmp_path):
    pytest.importorskip("netCDF4")

    with importlib.resources.path(__package__, "ref3.nc") as fn:
        ref = xarray.open_dataset(fn)

    fn = tmp_path / "test.nc"
    cmd = ["msise00", "-q", "-w", str(fn), "-a", str(altkm), "-t", time, "-gs", "30", "60"]
    print(" ".join(cmd))
    subprocess.check_call(cmd)

    dat = xarray.open_dataset(fn)
    xarray.tests.assert_allclose(ref, dat)

"""
generate the reference data:

python -m msise00 -w src/msise00/tests/ref4.nc -a 200 -gs 90 90 -t 2017-03-01T12 2017-03-01T13
"""

import importlib.resources
import subprocess
import pytest
import xarray
import xarray.tests
import msise00
import msise00.worldgrid

time = ["2017-03-01T12", "2017-03-01T13"]
altkm = 200.0


def test_multiple_time():
    pytest.importorskip("netCDF4")

    with importlib.resources.path(__package__, "ref4.nc") as fn:
        ref = xarray.open_dataset(fn)

    lat, lon = msise00.worldgrid.latlonworldgrid(90, 90)

    try:
        dat_mod = msise00.run(time, altkm, lat, lon).squeeze()
    except ConnectionError:
        pytest.skip("unable to download RecentIndices.txt")
    xarray.tests.assert_allclose(ref, dat_mod)


def test_script(tmp_path):
    pytest.importorskip("netCDF4")

    with importlib.resources.path(__package__, "ref4.nc") as fn:
        ref = xarray.open_dataset(fn)

    fn = tmp_path / "test.nc"
    cmd = ["msise00", "-q", "-w", str(fn), "-gs", "90", "90", "-a", str(altkm), "-t"] + time
    print(" ".join(cmd))
    subprocess.check_call(cmd)

    dat = xarray.open_dataset(fn)
    xarray.tests.assert_allclose(ref, dat)

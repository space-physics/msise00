"""
Regenerate test data:

python -m msise00 -w src/msise00/tests/ref6.nc -a 200 -t 2017-03-01T12 -c 65 -148
python -m msise00 -w src/msise00/tests/ref5.nc -a 100 -t 2017-03-01T12 -c 65 -148
"""

import importlib.resources
import subprocess
import pytest
import xarray
import xarray.tests
import msise00
import msise00.worldgrid

lat = 65
lon = -148
time = "2017-03-01T12"


@pytest.mark.parametrize("altkm,reffn", [(100.0, "ref5.nc"), (200.0, "ref6.nc")])
def test_one_loc_one_time(altkm, reffn):
    pytest.importorskip("netCDF4")

    with importlib.resources.path(__package__, reffn) as fn:
        ref = xarray.open_dataset(fn)

    try:
        dat_mod = msise00.run(time, altkm, lat, lon).squeeze()
    except ConnectionError:
        pytest.skip("unable to download RecentIndices.txt")
    xarray.tests.assert_allclose(ref, dat_mod)


@pytest.mark.parametrize("altkm,reffn", [(100.0, "ref5.nc"), (200.0, "ref6.nc")])
def test_script(altkm, reffn, tmp_path):
    pytest.importorskip("netCDF4")

    with importlib.resources.path(__package__, reffn) as fn:
        ref = xarray.open_dataset(fn)

    fn = tmp_path / "test.nc"
    cmd = ["msise00", "-q", "-w", str(fn), "-a", str(altkm), "-t", time, "-c", str(lat), str(lon)]
    print(" ".join(cmd))
    subprocess.check_call(cmd)

    dat = xarray.open_dataset(fn)
    xarray.tests.assert_allclose(ref, dat)

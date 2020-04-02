#!/usr/bin/env python3
"""
Regenerate test data:

./MSISE00.py -q -w tests/ref6.nc -a 200 -t 2017-03-01T12 -c 65 -148
./MSISE00.py -q -w tests/ref5.nc -a 100 -t 2017-03-01T12 -c 65 -148
"""
from pathlib import Path
import subprocess
import sys
import pytest
import xarray
import xarray.tests
import msise00
import msise00.worldgrid

R = Path(__file__).resolve().parent
lat = 65
lon = -148
time = "2017-03-01T12"
script = R.parents[1] / "MSISE00.py"


@pytest.mark.parametrize("altkm,reffn", [(100.0, "ref5.nc"), (200.0, "ref6.nc")])
def test_one_loc_one_time(altkm, reffn):
    pytest.importorskip("netCDF4")
    ref = xarray.open_dataset(R / reffn)

    try:
        dat_mod = msise00.run(time, altkm, lat, lon).squeeze()
    except ConnectionError:
        pytest.skip("unable to download RecentIndices.txt")
    xarray.tests.assert_allclose(ref, dat_mod)


@pytest.mark.skipif(not script.is_file(), reason="demo script not available")
@pytest.mark.parametrize("altkm,reffn", [(100.0, "ref5.nc"), (200.0, "ref6.nc")])
def test_script(altkm, reffn, tmp_path):
    pytest.importorskip("netCDF4")
    ref = xarray.open_dataset(R / reffn)

    fn = tmp_path / "test.nc"
    cmd = [sys.executable, str(script), "-q", "-w", str(fn), "-a", str(altkm), "-t", time, "-c", str(lat), str(lon)]
    print(" ".join(cmd))
    subprocess.check_call(cmd)

    dat = xarray.open_dataset(fn)
    xarray.tests.assert_allclose(ref, dat)


if __name__ == "__main__":
    pytest.main([__file__])

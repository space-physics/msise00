#!/usr/bin/env python3
"""
python MSISE00.py -q -w tests/ref4.nc -a 200 -gs 90 90 -t 2017-03-01T12 2017-03-01T14
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
time = ["2017-03-01T12", "2017-03-01T13"]
altkm = 200.0
script = R.parent / "MSISE00.py"


def test_multiple_time():
    pytest.importorskip("netCDF4")
    ref = xarray.open_dataset(R / "ref4.nc")

    lat, lon = msise00.worldgrid.latlonworldgrid(90, 90)

    try:
        dat_mod = msise00.run(time, altkm, lat, lon).squeeze()
    except ConnectionError:
        pytest.skip("unable to download RecentIndices.txt")
    xarray.tests.assert_allclose(ref, dat_mod)


@pytest.mark.skipif(not script.is_file(), reason="demo script not available")
def test_script(tmp_path):
    pytest.importorskip("netCDF4")
    ref = xarray.open_dataset(R / "ref4.nc")

    fn = tmp_path / "test.nc"
    cmd = [sys.executable, str(script), "-q", "-w", str(fn), "-gs", "90", "90", "-a", str(altkm), "-t"] + time
    print(" ".join(cmd))
    subprocess.check_call(cmd, cwd=R.parent)

    dat = xarray.open_dataset(fn)
    xarray.tests.assert_allclose(ref, dat)


if __name__ == "__main__":
    pytest.main([__file__])

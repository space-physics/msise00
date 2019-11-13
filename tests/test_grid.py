#!/usr/bin/env python3
"""
python MSISE00.py -q -w tests/ref3.nc -a 200 -t 2017-03-01T12
"""
from pathlib import Path
import sys
import subprocess
import pytest
import xarray
import xarray.tests
import msise00
import msise00.worldgrid

R = Path(__file__).resolve().parent
altkm = 200.0
time = "2017-03-01T12"
script = R.parent / "MSISE00.py"


def test_one_alt_one_time():
    pytest.importorskip("netCDF4")
    ref = xarray.open_dataset(R / "ref3.nc")

    lat, lon = msise00.worldgrid.latlonworldgrid(30, 60)

    indices = {"f107": 79.3, "f107s": 76.6802469, "Ap": 39}
    try:
        dat_mod = msise00.run(time, altkm, lat, lon, indices).squeeze()
    except ConnectionError:
        pytest.skip("unable to download RecentIndices.txt")
    xarray.tests.assert_allclose(ref, dat_mod)


@pytest.mark.skipif(not script.is_file(), reason="demo script not available")
def test_script(tmp_path):
    pytest.importorskip("netCDF4")
    ref = xarray.open_dataset(R / "ref3.nc")

    fn = tmp_path / "test.nc"
    cmd = [sys.executable, str(script), "-q", "-w", str(fn), "-a", str(altkm), "-t", time, "-gs", "30", "60"]
    print(" ".join(cmd))
    subprocess.check_call(cmd)

    dat = xarray.open_dataset(fn)
    xarray.tests.assert_allclose(ref, dat)


if __name__ == "__main__":
    pytest.main([__file__])

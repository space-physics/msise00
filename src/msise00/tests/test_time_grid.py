"""
generate the reference data:

python -m msise00 -w src/msise00/tests/ref4.nc -a 200 -gs 90 90 -t 2017-03-01T12 2017-03-01T13
"""

import importlib.resources
import subprocess
import pytest
import sys
import xarray
import xarray.testing
from datetime import datetime

import msise00
import msise00.worldgrid

time = [datetime(2017, 3, 1, 12), datetime(2017, 3, 1, 13)]
altkm = 200.0


def test_multiple_time():
    with importlib.resources.as_file(importlib.resources.files(__package__) / "ref4.nc") as fn:
        ref = xarray.open_dataset(fn)

    lat, lon = msise00.worldgrid.latlonworldgrid(90, 90)

    try:
        dat_mod = msise00.run(time, altkm, lat, lon).squeeze()
    except ConnectionError:
        pytest.skip("unable to download RecentIndices.txt")
    xarray.testing.assert_allclose(ref, dat_mod)


def test_script(tmp_path):
    with importlib.resources.as_file(importlib.resources.files(__package__) / "ref4.nc") as fn:
        ref = xarray.open_dataset(fn)

    fn = tmp_path / "test.nc"
    cmd = [
        sys.executable,
        "-m",
        "msise00",
        "-q",
        "-w",
        str(fn),
        "-gs",
        "90",
        "90",
        "-a",
        str(altkm),
        "-t",
    ] + list(map(str, time))
    print(" ".join(cmd))
    subprocess.check_call(cmd)

    dat = xarray.open_dataset(fn)
    xarray.testing.assert_allclose(ref, dat)

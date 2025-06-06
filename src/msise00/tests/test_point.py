"""
Regenerate test data:

python -m msise00 -w src/msise00/tests/ref6.nc -a 200 -t 2017-03-01T12 -c 65.0 -148.0
python -m msise00 -w src/msise00/tests/ref5.nc -a 100 -t 2017-03-01T12 -c 65.0 -148.0
"""

import importlib.resources
import subprocess
import pytest
import sys
import xarray
import xarray.testing
import msise00

lat = 65.0
lon = -148.0
time = "2017-03-01T12"


@pytest.mark.parametrize("altkm,reffn", [(100.0, "ref5.nc"), (200.0, "ref6.nc")])
def test_one_loc_one_time(altkm, reffn):
    with importlib.resources.as_file(importlib.resources.files(__package__) / reffn) as fn:
        ref = xarray.open_dataset(fn)

    try:
        dat = msise00.run(time, altkm, lat, lon).squeeze()
    except ConnectionError:
        pytest.skip("unable to download RecentIndices.txt")

    assert dat.lat == ref.lat == lat
    assert dat.lon == ref.lon == lon
    assert dat.time == ref.time
    xarray.testing.assert_allclose(ref, dat, rtol=0.001)


@pytest.mark.parametrize("altkm,reffn", [(100.0, "ref5.nc"), (200.0, "ref6.nc")])
def test_script(altkm, reffn, tmp_path):
    with importlib.resources.as_file(importlib.resources.files(__package__) / reffn) as fn:
        ref = xarray.open_dataset(fn)

    fn = tmp_path / "test.nc"
    cmd = [
        sys.executable,
        "-m",
        "msise00",
        "-q",
        "-w",
        str(fn),
        "-a",
        str(altkm),
        "-t",
        time,
        "-c",
        str(lat),
        str(lon),
    ]
    print(" ".join(cmd))
    subprocess.check_call(cmd)

    dat = xarray.open_dataset(fn)
    xarray.testing.assert_allclose(ref, dat, rtol=0.001)

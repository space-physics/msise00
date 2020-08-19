"""
Call NRL MSISE-00 using f2py from Python
Michael Hirsch, Ph.D.

Original fortran code from
http://nssdcftp.gsfc.nasa.gov/models/atmospheric/msis/nrlmsise00/
"""

import os
import importlib.resources
from datetime import datetime, date
import xarray
import numpy as np
import subprocess
import typing
import shutil
from pathlib import Path

from .timeutils import todatetime

import geomagindices as gi

species = ["He", "O", "N2", "O2", "Ar", "Total", "H", "N", "AnomalousO"]
ttypes = ["Texo", "Tn"]
first = True


def cmake(setup_file: Path):
    """
    attempt to build using CMake
    """
    exe = shutil.which("ctest")
    if not exe:
        raise FileNotFoundError("CMake not available")

    subprocess.check_call([exe, "-S", str(setup_file), "-VV"])


def run(
    time: datetime,
    altkm: float,
    glat: typing.Union[float, np.ndarray],
    glon: typing.Union[float, np.ndarray],
    indices: typing.Dict[str, typing.Any] = None,
) -> xarray.Dataset:
    """
    loops the rungtd1d function below. Figure it's easier to troubleshoot in Python than Fortran.
    """
    glat = np.atleast_2d(glat)
    glon = np.atleast_2d(glon)  # has to be here
    # %% altitude 1-D
    if glat.size == 1 and glon.size == 1 and isinstance(time, (str, date, datetime, np.datetime64)):
        atmos = rungtd1d(time, altkm, glat.squeeze()[()], glon.squeeze()[()], indices)
    # %% lat/lon grid at 1 altitude
    else:
        atmos = loopalt_gtd(time, glat, glon, altkm, indices)

    return atmos


def loopalt_gtd(
    time: datetime,
    glat: typing.Union[float, np.ndarray],
    glon: typing.Union[float, np.ndarray],
    altkm: typing.Union[float, typing.Sequence[float], np.ndarray],
    indices: typing.Dict[str, typing.Any] = None,
) -> xarray.Dataset:
    """
    loop over location and time

    time: datetime or numpy.datetime64 or list of datetime or np.ndarray of datetime
    glat: float or 2-D np.ndarray
    glon: float or 2-D np.ndarray
    altkm: float or list or 1-D np.ndarray
    """
    glat = np.atleast_2d(glat)
    glon = np.atleast_2d(glon)
    assert glat.ndim == glon.ndim == 2

    times = np.atleast_1d(time)
    assert times.ndim == 1

    atmos = xarray.Dataset()

    for t in times:
        print("computing", t)
        for i in range(glat.shape[0]):
            for j in range(glat.shape[1]):
                # atmos = xarray.concat((atmos, rungtd1d(t, altkm, glat[i,j], glon[i,j])),
                #                      data_vars='minimal',coords='minimal',dim='lon')
                atm = rungtd1d(t, altkm, glat[i, j], glon[i, j], indices)
                atmos = xarray.merge((atmos, atm))

    atmos.attrs = atm.attrs

    return atmos


def rungtd1d(
    time: datetime, altkm: np.ndarray, glat: float, glon: float, indices: typing.Dict[str, typing.Any] = None
) -> xarray.Dataset:
    """
    This is the "atomic" function looped by other functions
    """
    time = todatetime(time)
    # %% get solar parameters for date
    if not indices:
        indices = gi.getApF107(time, smoothdays=81).squeeze()
    # %% dimensions
    altkm = np.atleast_1d(altkm)
    if altkm.ndim != 1:
        raise ValueError("altitude read incorrectly")
    if not isinstance(glon, (int, float, np.int32, np.int64)):
        raise TypeError("single longitude only")
    if not isinstance(glat, (int, float, np.int32, np.int64)):
        raise TypeError("single latitude only")

    # %%
    iyd = time.strftime("%y%j")
    altkm = np.atleast_1d(altkm)
    # %%
    dens = np.empty((altkm.size, len(species)))
    temp = np.empty((altkm.size, len(ttypes)))
    # %% build on run
    exe_name = "msise00_driver"
    if os.name == "nt":
        exe_name += ".exe"
    if not importlib.resources.is_resource(__package__, exe_name):
        with importlib.resources.path(__package__, "setup.cmake") as setup_file:
            cmake(setup_file)
    if not importlib.resources.is_resource(__package__, exe_name):
        raise ModuleNotFoundError("could not build MSISE00 Fortran driver")

    with importlib.resources.path(__package__, exe_name) as exe:
        for i, a in enumerate(altkm):
            cmd = [
                str(exe),
                iyd,
                str(time.hour),
                str(time.minute),
                str(time.second),
                str(glat),
                str(glon),
                str(indices["f107s"]),
                str(indices["f107"]),
                str(indices["Ap"]),
                str(a),
            ]

            ret = subprocess.run(cmd, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if ret.returncode != 0:
                raise RuntimeError(f"MSISE00 error code {ret.returncode}\n{ret.stderr}")
            # different compilers throw in extra \n
            raw = list(map(float, ret.stdout.split()))
            if not len(raw) == 9 + 2:
                raise ValueError(ret)
            dens[i, :] = raw[:9]
            temp[i, :] = raw[9:]

    dsf = {k: (("time", "alt_km", "lat", "lon"), v[None, :, None, None]) for (k, v) in zip(species, dens.T)}
    dsf.update(
        {
            "Tn": (("time", "alt_km", "lat", "lon"), temp[:, 1][None, :, None, None]),
            "Texo": (("time", "alt_km", "lat", "lon"), temp[:, 0][None, :, None, None]),
        }
    )

    atmos = xarray.Dataset(
        dsf,
        coords={"time": [time], "alt_km": altkm, "lat": [glat], "lon": [glon]},
        attrs={"species": species, "f107s": indices["f107s"], "f107": indices["f107"], "Ap": indices["Ap"]},
    )

    return atmos

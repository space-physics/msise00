"""
Call NRL MSISE-00 using f2py from Python
Michael Hirsch, Ph.D.

Original fortran code from
http://nssdcftp.gsfc.nasa.gov/models/atmospheric/msis/nrlmsise00/
"""

from __future__ import annotations
import typing as T
import os
import logging
import importlib.resources
from datetime import datetime, date
import xarray
import numpy as np
import subprocess
import shutil

from .timeutils import todatetime

import geomagindices as gi


species = ["He", "O", "N2", "O2", "Ar", "Total", "H", "N", "AnomalousO"]
ttypes = ["Texo", "Tn"]
first = True


def build():
    """
    attempt to build using CMake
    """
    cmake = shutil.which("cmake")
    if not cmake:
        raise FileNotFoundError("CMake not available")

    with importlib.resources.path(__package__, "CMakeLists.txt") as f:
        s = f.parent
        b = s / "build"
        g = []

        if os.name == "nt" and not os.environ.get("CMAKE_GENERATOR"):
            g = ["-G", "MinGW Makefiles"]

        subprocess.check_call([cmake, f"-S{s}", f"-B{b}"] + g)
        subprocess.check_call([cmake, "--build", str(b), "--parallel"])


def run(
    time: datetime,
    altkm: float,
    glat: float,
    glon: float,
    indices: dict[str, T.Any] = None,
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
    glat: float | np.ndarray,
    glon: float | np.ndarray,
    altkm: float,
    indices: dict[str, T.Any] = None,
) -> xarray.Dataset:
    """
    loop over location and time

    time: datetime or numpy.datetime64 or list of datetime or ndarray of datetime
    glat: float or 2-D ndarray
    glon: float or 2-D ndarray
    altkm: float or list or 1-D ndarray
    """
    glat = np.atleast_2d(glat)
    glon = np.atleast_2d(glon)
    assert glat.ndim == glon.ndim == 2

    times = np.atleast_1d(time)  # type: ignore
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
    time: datetime, altkm: float, glat: float, glon: float, indices: dict[str, T.Any] = None
) -> xarray.Dataset:
    """
    This is the "atomic" function looped by other functions
    """
    time = todatetime(time)
    # %% get solar parameters for date
    if not indices:
        indices = gi.get_indices(time, smoothdays=81).squeeze().to_dict()
    assert isinstance(indices, dict)
    # %% dimensions
    altkm = np.atleast_1d(altkm)
    if altkm.ndim != 1:
        raise ValueError("altitude read incorrectly")
    if not isinstance(glon, (int, float, np.int32, np.int64)):
        raise TypeError("single longitude only")
    if not isinstance(glat, (int, float, np.int32, np.int64)):
        raise TypeError("single latitude only")

    # %%
    doy = time.strftime("%j")
    altkm = np.atleast_1d(altkm)
    # %%
    dens = np.empty((altkm.size, len(species)))
    temp = np.empty((altkm.size, len(ttypes)))
    # %% build on run
    exe_name = "msise00_driver"
    if os.name == "nt":
        exe_name += ".exe"

    # check inputs for error, especially unavailable indices
    if not np.isfinite(glat).all():
        raise ValueError("glat is not finite.")

    if not np.isfinite(glon).all():
        raise ValueError("glon is not finite.")

    f107s = indices["f107s"]
    if not np.isfinite(f107s):
        raise ValueError("f107s is not finite.")

    f107s = indices["f107s"]
    if not np.isfinite(f107s):
        raise ValueError("f107s is not finite.")

    f107 = indices["f107"]
    if not np.isfinite(f107):
        raise ValueError("f107 is not finite.")

    Ap = indices["Ap"]
    if not np.isfinite(Ap):
        raise ValueError("Ap is not finite.")

    try:
        with importlib.resources.path(__package__, exe_name) as exe:
            pass
    except FileNotFoundError:
        build()

    with importlib.resources.path(__package__, exe_name) as exe:
        for i, a in enumerate(altkm):
            cmd = [
                str(exe),
                doy,
                str(time.hour),
                str(time.minute),
                str(time.second),
                str(glat),
                str(glon),
                str(f107s),
                str(f107),
                str(Ap),
                str(a),
            ]

            logging.info(" ".join(cmd))

            ret = subprocess.check_output(cmd, text=True)

            # different compilers throw in extra \n
            raw = list(map(float, ret.split()))
            if not len(raw) == 9 + 2:
                raise ValueError(ret)
            dens[i, :] = raw[:9]
            temp[i, :] = raw[9:]

    dsf = {
        k: (("time", "alt_km", "lat", "lon"), v[None, :, None, None])
        for (k, v) in zip(species, dens.T)
    }
    dsf.update(
        {
            "Tn": (("time", "alt_km", "lat", "lon"), temp[:, 1][None, :, None, None]),
            "Texo": (("time", "alt_km", "lat", "lon"), temp[:, 0][None, :, None, None]),
        }
    )

    atmos = xarray.Dataset(
        dsf,  # type: ignore
        coords={"time": [time], "alt_km": altkm, "lat": [glat], "lon": [glon]},
        attrs={
            "species": species,
            "f107s": indices["f107s"],
            "f107": indices["f107"],
            "Ap": indices["Ap"],
        },
    )

    return atmos

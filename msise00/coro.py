"""
coroutines and MSISE00
"""
import asyncio
from typing import Union, Sequence
from datetime import datetime, date
import numpy as np
import xarray
import io

from .base import todatetime, SPECIES, TTYPES, EXE, rungtd1d
import geomagindices as gi


def run(time: datetime, altkm: float,
        glat: Union[float, np.ndarray], glon: Union[float, np.ndarray], *,
        f107a: float = None, f107: float = None, Ap: int = None) -> xarray.Dataset:
    """
    loops the rungtd1d function below. Figure it's easier to troubleshoot in Python than Fortran.
    """
    glat = np.atleast_2d(glat)
    glon = np.atleast_2d(glon)  # has to be here
# %% altitude 1-D
    if glat.size == 1 and glon.size == 1 and isinstance(time, (str, date, datetime, np.datetime64)):
        atmos = rungtd1d(time, altkm, glat.squeeze()[()], glon.squeeze()[()],
                         f107a=f107a, f107=f107, Ap=Ap)
# %% lat/lon grid at 1 altitude
    else:
        atmos = loopalt_gtd(time, glat, glon, altkm,
                            f107a=f107a, f107=f107, Ap=Ap)

    return atmos


def loopalt_gtd(time: datetime,
                glat: Union[float, np.ndarray], glon: Union[float, np.ndarray],
                altkm: Union[float, Sequence[float], np.ndarray], *,
                f107a: float = None, f107: float = None, Ap: int = None) -> xarray.Dataset:
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

    for k, t in enumerate(times):
        print('computing', t)
        for i in range(glat.shape[0]):
            for j in range(glat.shape[1]):
                # atmos = xarray.concat((atmos, rungtd1d(t, altkm, glat[i,j], glon[i,j])),
                #                      data_vars='minimal',coords='minimal',dim='lon')
                atm = corogtd(t, altkm, glat[i, j], glon[i, j],
                              f107a=f107a, f107=f107, Ap=Ap)
                atmos = xarray.merge((atmos, atm))

    atmos.attrs = atm.attrs

    return atmos


async def corogtd(time: datetime,
                  altkm: np.ndarray,
                  glat: float, glon: float, *,
                  f107a: float = None, f107: float = None, Ap: int = None) -> xarray.Dataset:
    """
    This is the "atomic" connection to MSISE00 Fortran code via pipes
    """
    time = todatetime(time)
    # %% get solar parameters for date
    if f107a and f107a and Ap:
        pass
    else:
        f107Ap = gi.getApF107(time, smoothdays=81)
        f107a = f107Ap['f107s'].item()
        f107 = f107Ap['f107'].item()
        Ap = f107Ap['Ap'].item()
# %% dimensions
    altkm = np.atleast_1d(altkm)
    assert altkm.ndim == 1
    assert isinstance(glon, (int, float))
    assert isinstance(glat, (int, float))

# %%
    iyd = time.strftime('%y%j')
    altkm = np.atleast_1d(altkm)
# %%
    dens = np.empty((altkm.size, len(SPECIES)))
    temp = np.empty((altkm.size, len(TTYPES)))
    for i, a in enumerate(altkm):
        cmd = [str(EXE),
               iyd, str(time.hour), str(time.minute), str(time.second),
               str(glat), str(glon),
               str(f107a), str(f107), str(Ap), str(a)]

        proc = await asyncio.create_subprocess_exec(*cmd)

        ret = proc.wait()  # TODO

        f = io.StringIO(ret)
        dens[i, :] = np.genfromtxt(f, max_rows=1)
        temp[i, :] = np.genfromtxt(f, max_rows=1)

    dsf = {k: (('time', 'alt_km', 'lat', 'lon'), v[None, :, None, None]) for (k, v) in zip(SPECIES, dens.T)}
    dsf.update({'Tn':  (('time', 'alt_km', 'lat', 'lon'), temp[:, 1][None, :, None, None]),
                'Texo': (('time', 'alt_km', 'lat', 'lon'), temp[:, 0][None, :, None, None])})

    atmos = xarray.Dataset(dsf,
                           coords={'time': [time], 'alt_km': altkm, 'lat': [glat], 'lon': [glon], },
                           attrs={'Ap': Ap, 'f107': f107, 'f107a': f107a,
                                  'species': SPECIES})

    return atmos

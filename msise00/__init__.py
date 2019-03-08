"""
Call NRL MSISE-00 using f2py from Python
Michael Hirsch, Ph.D.

Original fortran code from
http://nssdcftp.gsfc.nasa.gov/models/atmospheric/msis/nrlmsise00/
"""
from datetime import datetime
import xarray
import numpy as np
from typing import Union, List
#
from sciencedates import datetime2gtd
import geomagindices as gi
#
import gtd7
#
MASS = 48  # compute all parameters
TSELECOPS = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], float)
species = ['He', 'O', 'N2', 'O2', 'Ar', 'Total', 'H', 'N', 'AnomalousO']
ttypes = ['Texo', 'Tn']
first = True


def run(time: Union[datetime, np.ndarray], altkm: float,
        glat: Union[float, np.ndarray], glon: Union[float, np.ndarray]) -> xarray.Dataset:
    """
    loops the rungtd1d function below. Figure it's easier to troubleshoot in Python than Fortran.
    """
    time = todt64(time)
    glat = np.atleast_2d(glat)
    glon = np.atleast_2d(glon)  # has to be here
# %% altitude 1-D
    if glat.size == 1 and glon.size == 1 and time.size == 1:
        atmos = rungtd1d(time, altkm, glat.squeeze()[()], glon.squeeze()[()])
# %% lat/lon grid at 1 altitude
    else:
        atmos = loopalt_gtd(time, glat, glon, altkm)

    return atmos


def loopalt_gtd(time: Union[datetime, np.ndarray],
                glat: Union[float, np.ndarray], glon: Union[float, np.ndarray],
                altkm: Union[float, List[float], np.ndarray]) -> xarray.Dataset:
    """
    loop over location and time

    time: datetime, numpy.datetime64, or list or 1-D np.ndarray thereof
    glat: float or 2-D np.ndarray
    glon: float or 2-D np.ndarray
    altkm: float or list or 1-D np.ndarray
    """
    time = todt64(time)
    glat = np.atleast_2d(glat)
    glon = np.atleast_2d(glon)

    assert glat.ndim == glon.ndim == 2
    assert time.ndim == 1

    atmos = xarray.Dataset()

    for k, t in enumerate(time):
        print('computing', t)
        for i in range(glat.shape[0]):
            for j in range(glat.shape[1]):
                # atmos = xarray.concat((atmos, rungtd1d(t, altkm, glat[i,j], glon[i,j])),
                #                      data_vars='minimal',coords='minimal',dim='lon')
                atm = rungtd1d(t, altkm, glat[i, j], glon[i, j])
                atmos = xarray.merge((atmos, atm))

    atmos.attrs = atm.attrs

    return atmos


def rungtd1d(time: Union[datetime, str, np.ndarray],
             altkm: np.ndarray,
             glat: float, glon: float) -> xarray.Dataset:
    """
    This is the "atomic" function looped by other functions
    """
    time = todt64(time)
    # %% get solar parameters for date
    f107Ap = gi.getApF107(time, smoothdays=81)
    f107a = f107Ap['f107s'].item()
    f107 = f107Ap['f107'].item()
    Ap = f107Ap['Ap'].item()
# %% dimensions
    altkm = np.atleast_1d(altkm)
    assert altkm.ndim == 1
    assert isinstance(glon, (int, float))
    assert isinstance(glat, (int, float))
    assert isinstance(time, np.datetime64) or (time.size == 1 and isinstance(
        time[0], np.datetime64)), 'if you have multiple times, for loop over them'

# don't check ap, too complicated
    assert isinstance(MASS, (float, int))
    assert len(TSELECOPS) == 25
# %%
    gtd7.tselec(TSELECOPS)  # like the msis_driver example

    iyd, utsec, stl = datetime2gtd(time, glon)
    altkm = np.atleast_1d(altkm)

    gtd7.meters(1)  # makes output in m^-3 and kg/m^-3
# %%
    if isinstance(Ap, (float, int)):
        Ap = [Ap]*7  # even if SW(9) == 1 due to f2py needs for array

    dens = np.empty((altkm.size, len(species)))
    temp = np.empty((altkm.size, len(ttypes)))
    for i, a in enumerate(altkm):
        dens[i, :], temp[i, :] = gtd7.gtd7(iyd, utsec, a, glat, glon, stl, f107a, f107, Ap, MASS)

    dsf = {k: (('time', 'alt_km', 'lat', 'lon'), v[None, :, None, None]) for (k, v) in zip(species, dens.T)}
    dsf.update({'Tn':  (('time', 'alt_km', 'lat', 'lon'), temp[:, 1][None, :, None, None]),
                'Texo': (('time', 'alt_km', 'lat', 'lon'), temp[:, 0][None, :, None, None])})

    atmos = xarray.Dataset(dsf,
                           coords={'time': time.astype(datetime), 'alt_km': altkm, 'lat': [glat], 'lon': [glon], },
                           attrs={'Ap': Ap, 'f107': f107, 'f107a': f107a,
                                  'species': species})

    return atmos


def todt64(time: Union[str, datetime, np.datetime64, list, np.ndarray]) -> np.ndarray:
    time = np.atleast_1d(time)

    if time.size == 1:
        time = np.atleast_1d(np.datetime64(time[0], dtype='datetime64[us]'))
    elif time.size == 2:
        time = np.arange(time[0], time[1], dtype='datetime64[h]')
    else:
        pass

    return time

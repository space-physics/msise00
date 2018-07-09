"""
Quick demo of calling NRL MSISE-00 using f2py from Python
Michael Hirsch, Ph.D.

Original fortran code from
http://nssdcftp.gsfc.nasa.gov/models/atmospheric/msis/nrlmsise00/
"""
from datetime import datetime
import xarray
import numpy as np
from typing import Union
#
from sciencedates import datetime2gtd
from gridaurora import readmonthlyApF107
#
import gtd7
#
MASS = 48  # compute all parameters
TSELECOPS = np.array([1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], float)
species = ['He', 'O', 'N2', 'O2', 'Ar', 'Total', 'H', 'N', 'AnomalousO']
ttypes = ['Texo', 'Tn']
first = True


def run(time: Union[datetime, np.ndarray], altkm: float,
        glat: Union[float, np.ndarray], glon: Union[float, np.ndarray]) -> xarray.Dataset:
    """
    loops the rungtd1d function below. Figure it's easier to troubleshoot in Python than Fortran.
    """
    time = np.atleast_1d(time)
    glat = np.atleast_2d(glat)
    glon = np.atleast_2d(glon)  # has to be here
# %% altitude 1-D
    if glat.size == 1 and glon.size == 1 and time.size == 1:
        atmos = rungtd1d(time, altkm, glat, glon)
# %% lat/lon grid at 1 altitude
    else:
        atmos = loopalt_gtd(time, glat, glon, altkm)

    return atmos


def loopalt_gtd(time: Union[datetime, np.ndarray],
                glat: np.ndarray, glon: np.ndarray, altkm: float) -> xarray.Dataset:
    time = np.atleast_1d(time)  # keep for code reuse

    atmos = xarray.Dataset()

    for k, t in enumerate(time):
        print(f'computing {t}')
        for i in range(glat.shape[0]):
            for j in range(glat.shape[1]):
                # atmos = xarray.concat((atmos, rungtd1d(t, altkm, glat[i,j], glon[i,j])),
                #                      data_vars='minimal',coords='minimal',dim='lon')
                atmos = xarray.merge((atmos, rungtd1d(t, altkm, glat[i, j], glon[i, j])))

    return atmos


def rungtd1d(time: datetime, altkm: np.ndarray,
             glat: np.ndarray, glon: np.ndarray) -> xarray.Dataset:
    """
    This is the "atomic" function looped by other functions
    """
    # %% get solar parameters for date
    f107Ap = readmonthlyApF107(time)
    f107a = f107Ap['f107s'].item()
    f107 = f107Ap['f107o'].item()
    Ap = np.atleast_1d((f107Ap['Apo'].item(),)*7)
# %%
    altkm = np.atleast_1d(altkm)
    glon = np.atleast_1d(glon).squeeze()
    glat = np.atleast_1d(glat).squeeze()

    assert isinstance(time, (np.datetime64, datetime, str)), 'if you have multiple times, for loop over them'

# don't check ap, too complicated
    assert isinstance(MASS, (float, int))
    assert len(TSELECOPS) == 25
# %%
    if Ap.size == 1:
        Ap = np.repeat(Ap, 7)

    gtd7.tselec(TSELECOPS)  # like the msis_driver example

    iyd, utsec, stl = datetime2gtd(time, glon)
    altkm = np.atleast_1d(altkm)

    gtd7.meters(1)  # makes output in m^-3 and kg/m^-3

    dens = np.empty((altkm.size, len(species)))
    temp = np.empty((altkm.size, len(ttypes)))
    for i, a in enumerate(altkm):
        dens[i, :], temp[i, :] = gtd7.gtd7(iyd, utsec, a, glat, glon, stl, f107a, f107, Ap, MASS)

    dsf = {k: (('time', 'alt_km', 'lat', 'lon'), v[None, :, None, None]) for (k, v) in zip(species, dens.T)}
    dsf.update({'Tn':  (('time', 'alt_km', 'lat', 'lon'), temp[:, 1][None, :, None, None]),
                'Texo': (('time', 'alt_km', 'lat', 'lon'), temp[:, 0][None, :, None, None])})

    atmos = xarray.Dataset(dsf,
                           coords={'time': [time], 'alt_km': altkm, 'lat': [glat], 'lon': [glon], },
                           attrs={'Ap': Ap, 'f107': f107, 'f107a': f107a,
                                  'species': species})

    return atmos

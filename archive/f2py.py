import numpy as np
import xarray


def rungtd1d(
    time: Union[datetime, str, np.ndarray], altkm: np.ndarray, glat: float, glon: float
) -> xarray.Dataset:
    """
    This is the "atomic" function looped by other functions
    """
    time = todt64(time)
    # %% get solar parameters for date
    f107Ap = gi.getApF107(time, smoothdays=81)
    f107a = f107Ap["f107s"].item()
    f107 = f107Ap["f107"].item()
    Ap = f107Ap["Ap"].item()
    # %% dimensions
    altkm = np.atleast_1d(altkm)
    assert altkm.ndim == 1
    assert isinstance(glon, (int, float))
    assert isinstance(glat, (int, float))
    assert isinstance(time, np.datetime64) or (
        time.size == 1 and isinstance(time[0], np.datetime64)
    ), "if you have multiple times, for loop over them"

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
        Ap = [Ap] * 7  # even if SW(9) == 1 due to f2py needs for array

    dens = np.empty((altkm.size, len(species)))
    temp = np.empty((altkm.size, len(ttypes)))
    for i, a in enumerate(altkm):
        dens[i, :], temp[i, :] = gtd7.gtd7(iyd, utsec, a, glat, glon, stl, f107a, f107, Ap, MASS)

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
        dsf,
        coords={"time": time.astype(datetime), "alt_km": altkm, "lat": [glat], "lon": [glon]},
        attrs={"Ap": Ap, "f107": f107, "f107a": f107a, "species": species},
    )

    return atmos

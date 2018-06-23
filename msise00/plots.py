from pathlib import Path
import xarray
import numpy as np
from astropy.time import Time
from astropy.coordinates import get_sun, EarthLocation, AltAz
from matplotlib.pyplot import figure, close
from matplotlib.ticker import ScalarFormatter
#
from pymap3d import aer2geodetic


def plotgtd(atmos: xarray.Dataset, rodir: Path=None):
    #
    if rodir:
        rodir = Path(rodir).expanduser()

    sfmt = ScalarFormatter(useMathText=True)  # for 10^3 instead of 1e3
    sfmt.set_powerlimits((-2, 2))
    sfmt.set_scientific(True)
    sfmt.set_useOffset(False)

    if atmos['N2'].squeeze().ndim == 1:  # altitude 1-D
        plot1d(atmos)
    elif atmos['N2'].squeeze().ndim == 4:  # lat/lon grid
        # %% sun lat/lon
        time = Time(str(atmos.time[0].values))
        obs = EarthLocation(0, 0)  # geodetic lat,lon = 0,0 arbitrary
        sun = get_sun(time=time)
        aaf = AltAz(obstime=time, location=obs)
        sloc = sun.transform_to(aaf)
        slat, slon = aer2geodetic(sloc.az.value, sloc.alt.value, sloc.distance.value, 0, 0, 0)[:2]
        slat = np.atleast_1d(slat)
        slon = np.atleast_1d(slon)
# %% tableau
        for i, t in enumerate(atmos.time):
            fg = figure(figsize=(8, 8))
            ax = fg.subplots(4, 2, sharex=True)
            fg.suptitle(str(t.values)[:-13] +
                        f' alt.(km) {atmos.alt_km[0]}\n'
                        f'Ap={atmos.Ap[0]}  F10.7={atmos.f107.item()}')
            ax = ax.ravel()

            j = 0
            for s in atmos.species:
                if s == 'Total':
                    continue

                a = ax[j]

                hi = a.imshow(atmos[s][i][0], aspect='auto',
                              interpolation='none', cmap='viridis',
                              extent=(atmos.lon[0], atmos.lon[-1], atmos.lat[0], atmos.lat[-1]))

                fg.colorbar(hi, ax=a, format=sfmt)
    # %% sun icon moving
                a.plot(slon[i], slat[i], linestyle='none',
                       marker='o', markersize=5, color='w')

                a.set_title(f'Density: {s}')
                a.set_xlim(-180, 180)
                a.set_ylim(-90, 90)
                a.autoscale(False)
                j += 1

            for k in range(0, 6+2, 2):
                ax[k].set_ylabel('latitude (deg)')
            for k in (6, 7):
                ax[k].set_xlabel('longitude (deg)')

            if rodir:
                ofn = rodir / f'{atmos.alt_km[0].item():.1f}_{i:03d}.png'
                print('writing', ofn)
                fg.savefig(ofn, dpi=100, bbox_inches='tight')
                close()

    else:
        print(atmos)


def plot1d(atmos: xarray.Dataset):

    footer = f'\n({atmos.lat.item()},{atmos.lon.item()})  Ap {atmos.Ap[0]}  F10.7 {atmos.f107}'

    z = atmos.alt_km.values
    ax = figure().gca()
    for s in atmos.species:
        if s == 'Total':
            continue
        ax.semilogx(atmos[s].squeeze(), z, label=s)
    ax.legend(loc='best')
    ax.set_xlim(left=1e3)
    ax.set_ylabel('altitude [km]')
    ax.set_xlabel('density [m$^{-3}$]')
    ax.grid(True)
    ax.set_title('Number Density from MSISE-00' + footer)

    ax = figure().gca()
    ax.semilogx(atmos['Total'].squeeze(), z)
    ax.set_xlabel('Total Mass Density [kg m$^{-3}$]')
    ax.set_ylabel('altitude [km]')
    ax.grid(True)
    ax.set_title('Total Mass Density from MSISE-00'+footer)

    ax = figure().gca()
    ax.plot(atmos['Tn'].squeeze(), z)
    ax.set_xlabel('Temperature')
    ax.set_ylabel('altitude [km]')
    ax.grid(True)
    ax.set_title('Temperature from MSISE-00' + footer)

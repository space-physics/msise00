from pathlib import Path
import xarray
from datetime import datetime
from matplotlib.pyplot import figure, close
from matplotlib.ticker import ScalarFormatter

try:
    from pymap3d import aer2geodetic
except ImportError:
    aer2geodetic = None
try:
    from astropy.time import Time
    from astropy.coordinates import get_sun, EarthLocation, AltAz
except ImportError:
    Time = None

sfmt = ScalarFormatter(useMathText=True)  # for 10^3 instead of 1e3
sfmt.set_powerlimits((-2, 2))
sfmt.set_scientific(True)
sfmt.set_useOffset(False)


def plotgtd(atmos: xarray.Dataset, rodir: Path = None):
    #
    if rodir:
        rodir = Path(rodir).expanduser()

    atmos = atmos.squeeze()
    tmp = atmos["N2"]

    if tmp.ndim == 1:
        if "alt_km" in tmp.dims:
            plot1dalt(atmos)
        elif "time" in tmp.dims:
            plot1dtime(atmos)
        else:
            raise NotImplementedError(
                "didnt handle this plotting case yet. Should be straightforward."
            )
    elif tmp.ndim == 2:
        if "lat" in tmp.dims and "lon" in tmp.dims:
            plot2dlatlon(atmos, rodir)
        elif "time" in tmp.dims:
            for t in atmos.time:
                plot1dalt(atmos.sel(time=t), rodir)
        else:
            raise NotImplementedError(
                "didnt handle this plotting case yet. Should be straightforward."
            )
    elif tmp.ndim in (3, 4):  # lat/lon grid vs. time
        plot4d(atmos, rodir)
    else:  # single point
        print(atmos)


def plot4d(atmos: xarray.Dataset, rodir: Path = None):

    for t in atmos.time:
        if Time is not None and aer2geodetic is not None:
            time = Time(str(t.values))
            obs = EarthLocation(0, 0)  # geodetic lat,lon = 0,0 arbitrary
            sun = get_sun(time=time)
            aaf = AltAz(obstime=time, location=obs)
            sloc = sun.transform_to(aaf)
            slat, slon = aer2geodetic(sloc.az.value, sloc.alt.value, sloc.distance.value, 0, 0, 0)[
                :2
            ]
            plot2dlatlon(atmos.sel(time=t), rodir, slat, slon)
        else:
            plot2dlatlon(atmos.sel(time=t), rodir)


def plot2dlatlon(atmos: xarray.Dataset, rodir: Path = None, slat: float = None, slon: float = None):

    fg = figure(figsize=(8, 8))
    ax = fg.subplots(4, 2, sharex=True).ravel()

    fg.suptitle(
        str(atmos.time.values.squeeze())[:-13] + f" alt.(km) {atmos.alt_km.item()}\n"
        f"Ap={atmos.Ap}  F10.7={atmos.f107}"
    )

    j = 0

    for s in atmos.species:
        if s == "Total":
            continue

        a = ax[j]

        hi = a.imshow(
            atmos[s].squeeze(),
            aspect="auto",
            interpolation="none",
            cmap="viridis",
            extent=(atmos.lon[0], atmos.lon[-1], atmos.lat[0], atmos.lat[-1]),
        )

        fg.colorbar(hi, ax=a, format=sfmt)
        # %% sun icon moving
        if slat is not None and slon is not None:
            a.plot(slon, slat, linestyle="none", marker="o", markersize=5, color="w")

        a.set_title(f"Density: {s}")
        a.set_xlim(-180, 180)
        a.set_ylim(-90, 90)
        a.autoscale(False)
        j += 1

    for k in range(0, 6 + 2, 2):
        ax[k].set_ylabel("latitude (deg)")
    for k in (6, 7):
        ax[k].set_xlabel("longitude (deg)")

    if rodir:
        ofn = rodir / (
            f"{atmos.alt_km.item():.1f}_" + str(atmos.time.values.squeeze())[:-13] + ".png"
        )
        writeplot(fg, ofn)


def plot1dalt(atmos: xarray.Dataset, odir: Path = None):

    footer = f"\n({atmos.lat.item()},{atmos.lon.item()})  Ap {atmos.Ap}  F10.7 {atmos.f107}"

    z = atmos.alt_km.values

    # %% number density
    fg = figure()
    ax = fg.gca()
    for s in atmos.species:
        if s == "Total":
            continue
        ax.semilogx(atmos[s].squeeze(), z, label=s)
    ax.legend(loc="best")
    ax.set_xlim(left=1e3)
    ax.set_ylabel("altitude [km]")
    ax.set_xlabel("density [m$^{-3}$]")
    ax.grid(True)
    ax.set_title("Number Density from MSISE-00" + footer)
    if odir:
        ofn = odir / ("number-density_" + str(atmos.time.values.squeeze())[:-13] + ".png")
        writeplot(fg, ofn)

    # %% total mass
    fg = figure()
    ax = fg.gca()
    ax.semilogx(atmos["Total"].squeeze(), z)
    ax.set_xlabel("Total Mass Density [kg m$^{-3}$]")
    ax.set_ylabel("altitude [km]")
    ax.grid(True)
    ax.set_title("Total Mass Density from MSISE-00" + footer)

    if odir:
        ofn = odir / ("total-density_" + str(atmos.time.values.squeeze())[:-13] + ".png")
        writeplot(fg, ofn)

    # %% temperature
    fg = figure()
    ax = fg.gca()
    ax.plot(atmos["Tn"].squeeze(), z)
    ax.set_xlabel("Temperature [K]")
    ax.set_ylabel("altitude [km]")
    ax.grid(True)
    ax.set_title("Temperature from MSISE-00" + footer)

    if odir:
        ofn = odir / ("temperature_" + str(atmos.time.values.squeeze())[:-13] + ".png")
        writeplot(fg, ofn)


def plot1dtime(atmos: xarray.Dataset, odir: Path = None):

    footer = f"\n({atmos.lat.item()},{atmos.lon.item()})  alt: {atmos.alt_km.item()} km,  Ap {atmos.Ap}  F10.7 {atmos.f107}"

    t = atmos.time.values.astype("datetime64[us]").astype(datetime)

    # %% number density
    fg = figure()
    ax = fg.gca()
    for s in atmos.species:
        if s == "Total":
            continue
        ax.plot(t, atmos[s].squeeze(), label=s)
    ax.legend(loc="best")
    ax.set_ylabel("density [m$^{-3}$]")
    ax.set_xlabel("time [UTC]")
    ax.grid(True)
    ax.set_title("Number Density from MSISE-00" + footer)
    if odir:
        ofn = odir / ("number-density_" + str(atmos.time.values.squeeze())[:-13] + ".png")
        writeplot(fg, ofn)

    # %% total mass
    fg = figure()
    ax = fg.gca()
    ax.plot(t, atmos["Total"].squeeze())
    ax.set_ylabel("Total Mass Density [kg m$^{-3}$]")
    ax.set_xlabel("time [UTC]")
    ax.grid(True)
    ax.set_title("Total Mass Density from MSISE-00" + footer)

    if odir:
        ofn = odir / ("total-density_" + str(atmos.time.values.squeeze())[:-13] + ".png")
        writeplot(fg, ofn)

    # %% temperature
    fg = figure()
    ax = fg.gca()
    ax.plot(t, atmos["Tn"].squeeze())
    ax.set_ylabel("Temperature [K]")
    ax.set_xlabel("time [UTC]")
    ax.grid(True)
    ax.set_title("Temperature from MSISE-00" + footer)

    if odir:
        ofn = odir / ("temperature_" + str(atmos.time.values.squeeze())[:-13] + ".png")
        writeplot(fg, ofn)


def writeplot(fg, ofn: Path):
    print("writing", ofn)
    fg.savefig(ofn, dpi=100, bbox_inches="tight")
    close(fg)

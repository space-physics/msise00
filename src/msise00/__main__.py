#!/usr/bin/env python
"""
Run MSISE00, save to NetCDF4 (HDF5) and/or plot.

Example:
Poker Flat Research Range altitude profile:

MSISE00.py -t 2018-01-01 -c 65 -148 -a 0.2
"""

from pathlib import Path
import numpy as np
from argparse import ArgumentParser

from .base import run
from .worldgrid import latlonworldgrid


def cli():
    p = ArgumentParser(description="calls MSISE-00 from Python, save to NetCDF4 and/or plot")
    p.add_argument("-t", "--time", help="time or times", nargs="+", required=True)
    p.add_argument(
        "-a",
        "--altkm",
        help="altitude (km). scalar, or (start,stop,step) or list of alts.",
        type=float,
        nargs="+",
        required=True,
    )
    p.add_argument(
        "-c",
        "--latlon",
        help="geodetic latitude/longitude (deg)",
        metavar=("lat", "lon"),
        type=float,
        nargs=2,
    )
    p.add_argument("-o", "--odir", help="directory to write plots to")
    p.add_argument("-w", help="NetCDF4 .nc filename to write")
    p.add_argument(
        "-gs", help="geographic grid spacing (lat, lon)", nargs=2, type=float, default=(10, 10)
    )
    p.add_argument("-q", "--quiet", help="disable plotting", action="store_true")
    P = p.parse_args()

    # %% altitude
    if len(P.altkm) == 1:
        altkm = P.altkm[0]
    elif len(P.altkm) == 3:
        altkm = np.arange(*P.altkm)
    else:
        altkm = P.altkm
    # %% latlon
    if P.latlon is not None:
        glat, glon = P.latlon
    else:
        glat, glon = latlonworldgrid(*P.gs)
    # %% run
    atmos = run(P.time, altkm, glat, glon)
    # %% save
    if P.w:
        ncfn = Path(P.w).expanduser()
        print("saving", ncfn)
        # NOTE: .squeeze() avoids ValueError: unsupported dtype for netCDF4 variable: datetime64[ns]
        atmos.squeeze().to_netcdf(ncfn)
    # %% plot
    if not P.quiet:
        try:
            from matplotlib.pyplot import show
            from .plots import plotgtd

            plotgtd(atmos, P.odir)
            show()
        except ImportError:
            print("skipped plotting")


if __name__ == "__main__":
    cli()

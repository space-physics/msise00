#!/usr/bin/env python
from tempfile import gettempdir
from pytz import UTC
from dateutil.parser import parse
from datetime import datetime
from numpy import arange, atleast_1d
from pandas import date_range
from matplotlib.pyplot import show
import seaborn as sns
sns.set_style('ticks')
#
from msise00 import rungtd7
from msise00.plots import plotgtd
#
from gridaurora.worldgrid import latlonworldgrid

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='calls MSISE-00 from Python, a basic demo')
    p.add_argument('-t','--simtime',help='yyyy-mm-ddTHH:MM:SSZ time of sim')
    p.add_argument('-a','--altkm',help='altitude (km) (start,stop,step)',type=float,nargs=3)
    p.add_argument('-c','--latlon',help='geodetic latitude/longitude (deg)',type=float,nargs=2)
    p.add_argument('--f107a',help=' 81 day AVERAGE OF F10.7 FLUX (centered on day DDD)',type=float,default=150)
    p.add_argument('--f107',help='DAILY F10.7 FLUX FOR PREVIOUS DAY',type=float,default=150)
    p.add_argument('--ap',help='daily ap, 0-3hr, 3-6hr, 6-9hr, 9-12hr,12-33hr, 36-57hr',type=float,nargs=7,default=[4,4,4,4,4,4,4])
    p.add_argument('-o','--odir',help='directory to write plots to',default=gettempdir())
    p = p.parse_args()

    if not p.simtime: #cycle through a few times for a demo
        dtime = date_range(datetime.now(),periods=24,freq='1H',tz=UTC,normalize=True).to_pydatetime()
    else:
        dtime = parse(p.simtime)
#%% altitude 1-D mode
    if p.latlon is not None:
        print('entering single location mode')
        if p.altkm is None:
            p.altkm = (60.,1000,5)
        altkm = arange(p.altkm[0],p.altkm[1],p.altkm[2])
        glat,glon=p.latlon
#%% lat/lon grid mode at constant altitude
    else:# len(p.altkm)==1:
        print('lat/lon not specified, entering auto whole-world grid mode at first altitude')
        if p.altkm is None:
            altkm = 200.
        else:
            altkm = p.altkm[0]
        glat,glon = latlonworldgrid()

    altkm = atleast_1d(altkm)
    print(f'using altitudes from {altkm[0]:.1f} to {altkm[-1]:.1f} km')

    dens,temp = rungtd7(dtime,altkm,glat,glon,p.f107a,p.f107,p.ap)

    plotgtd(dens,temp,dtime,altkm,p.ap,p.f107,glat,glon,p.odir)
    show()


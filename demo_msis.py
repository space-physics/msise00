#!/usr/bin/env python3
from pytz import UTC
from dateutil.parser import parse
from datetime import datetime
from numpy import arange, atleast_1d
from pandas import date_range
#
from msise00.runmsis import rungtd7
from msise00.plots import plotgtd

if __name__ == '__main__':
    from matplotlib.pyplot import show
    from gridaurora.worldgrid import latlonworldgrid

    from argparse import ArgumentParser
    p = ArgumentParser(description='calls MSISE-00 from Python, a basic demo')
    p.add_argument('simtime',help='yyyy-mm-ddTHH:MM:SSZ time of sim',type=str,nargs='?',default='2015-04-22T12:00:00Z')
    p.add_argument('-a','--altkm',help='altitude (km) (start,stop,step)',type=float,nargs=3)
    p.add_argument('-c','--latlon',help='geodetic latitude/longitude (deg)',type=float,nargs=2)
    p.add_argument('--f107a',help=' 81 day AVERAGE OF F10.7 FLUX (centered on day DDD)',type=float,default=150)
    p.add_argument('--f107',help='DAILY F10.7 FLUX FOR PREVIOUS DAY',type=float,default=150)
    p.add_argument('--ap',help='daily ap, 0-3hr, 3-6hr, 6-9hr, 9-12hr,12-33hr, 36-57hr',type=float,nargs=7,default=[4,4,4,4,4,4,4])
    p.add_argument('--mass',help=('MASS NUMBER (ONLY DENSITY FOR SELECTED GAS IS ' +
                       'CALCULATED.  MASS 0 IS TEMPERATURE.  MASS 48 FOR ALL. '+
                         'MASS 17 IS Anomalous O ONLY.'),type=float,default=48)
    p.add_argument('-o','--odir',help='directory to write plots to')
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
    print('using altitudes from {:.1f} to {:.1f} km'.format(altkm[0],altkm[-1]))

    dens,temp = rungtd7(dtime,altkm,glat,glon,p.f107a,p.f107,p.ap,p.mass)

    try:
        plotgtd(dens,temp,dtime,altkm,p.ap,p.f107,glat,glon,p.odir)
        show()
    except Exception as e:
        print('plotting was disabled. {}'.format(e))

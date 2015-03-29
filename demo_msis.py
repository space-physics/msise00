#!/usr/bin/env python3
"""
NOTE: The performance of this demo has not been checked at all.
Please do basic sanity checks of output.
Quick demo of calling NRL MSISE-00 using f2py3 from Python
Michael Hirsch
bostonmicrowave.com

Original fortran code from
http://nssdcftp.gsfc.nasa.gov/models/atmospheric/msis/nrlmsise00/
"""
from __future__ import division
from pandas import  DataFrame, Panel
from numpy import arange, meshgrid, empty, atleast_1d
from dateutil.parser import parse
from datetime import timedelta,datetime, time
from pytz import UTC
from matplotlib.pyplot import figure,show
#
import gtd7

def testgtd7(dtime,altkm,glat,glon,f107a,f107,ap,mass):
    iyd = int(dtime.strftime('%j'))
    #seconds since utc midnight
    utsec = timedelta.total_seconds(dtime-datetime.combine(dtime.date(),time(0,tzinfo=UTC)))

    stl = utsec/3600 + glon/15

#%% get ready for iteration
    species = ['He','O','N2','O2','Ar','Total','H','N','AnomalousO']
    ttypes = ['exotemp','heretemp']
    altkm = atleast_1d(altkm)
    glat = atleast_1d(glat); glon=atleast_1d(glon)
#%% altitude 1-D
    if glat.size==1 and glon.size==1:
        dens = empty((altkm.size,9)); temp=empty((altkm.size,2))
        for i,a in enumerate(altkm):
            dens[i,:],temp[i,:] = gtd7.gtd7(iyd,utsec,a,glat,glon,stl, f107a,f107, ap,mass)

        densd = DataFrame(dens, index=altkm, columns=species)
        tempd = DataFrame(temp, index=altkm, columns=ttypes)
#%% lat/lon grid at 1 altitude
    else: #I didn't use numpy.nditer just yet
        dens = empty((9,glat.shape[0],glat.shape[1])); temp = empty((2,glat.shape[0],glat.shape[1]))
        for i in range(glat.shape[0]):
            for j in range(glat.shape[1]):
                dens[:,i,j], temp[:,i,j] = gtd7.gtd7(iyd,utsec,altkm,glat[i,j],glon[i,j],stl,f107a,f107,ap,mass)

        densd = Panel(dens, items=species,major_axis=glat[:,0],minor_axis=glon[0,:])
        tempd = Panel(temp, items=ttypes, major_axis=glat[:,0],minor_axis=glon[0,:])

    return densd,tempd

def plotgtd(dens,temp,dtime,altkm):
    if dens.ndim==2: #altitude 1-D
        ax = figure().gca()
        for g in dens.columns:
            if g != 'Total':
                ax.semilogx(dens[g], dens.index, label=g)
        ax.legend(loc='best')
        ax.set_xlim(left=1e3)
        ax.set_ylabel('altitude [km]')
        ax.set_xlabel('density [cm$^{-3}$]')
        ax.grid(True)
        ax.set_title('Number Density from MSISE-00')

        ax = figure().gca()
        ax.semilogx(dens['Total'],dens.index)
        ax.set_xlabel('Total Mass Density [gm/cm^-3]')
        ax.set_ylabel('altitude [km]')
        ax.grid(True)
        ax.set_title('Total Mass Density from MSISE-00')

        ax = figure().gca()
        ax.plot(temp['heretemp'],temp.index)
        ax.set_xlabel('Temperature')
        ax.set_ylabel('altitude [km]')
        ax.grid(True)
        ax.set_title('Temperature from MSISE-00')
    elif dens.ndim==3: #lat/lon grid
        for g in dens.items:
            fg = figure()
            ax = fg.gca()
            hi = ax.imshow(dens[g].values,extent=(glon[0,0],glon[0,-1],glat[0,0],glat[-1,0]))
            fg.colorbar(hi)
            ax.set_xlabel('longitude (deg)')
            ax.set_ylabel('latitude (deg)')
            ax.set_title('Density: ' + g + '\n' + str(dtime) + ' at alt.(km) '+str(altkm))
    else:
        print('densities' + str(dens))
        print('temperatures ' + str(temp))

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='calls MSISE-00 from Python, a basic demo')
    p.add_argument('simtime',help='yyyy-mm-ddTHH:MM:SSZ time of sim',type=str,nargs='?',default='')
    p.add_argument('-a','--altkm',help='altitude (km) (start,stop,step)',type=float,nargs='+',default=[None])
    p.add_argument('-c','--latlon',help='geodetic latitude/longitude (deg)',type=float,nargs=2,default=(None,None))
    p.add_argument('--f107a',help=' 81 day AVERAGE OF F10.7 FLUX (centered on day DDD)',type=float,default=150)
    p.add_argument('--f107',help='DAILY F10.7 FLUX FOR PREVIOUS DAY',type=float,default=150)
    p.add_argument('--ap',help='daily ap, 0-3hr, 3-6hr, 6-9hr, 9-12hr,12-33hr, 36-57hr',type=float,nargs=7,default=[4,4,4,4,4,4,4])
    p.add_argument('--mass',help=('MASS NUMBER (ONLY DENSITY FOR SELECTED GAS IS ' +
                       'CALCULATED.  MASS 0 IS TEMPERATURE.  MASS 48 FOR ALL. '+
                         'MASS 17 IS Anomalous O ONLY.'),type=float,default=48)
    p = p.parse_args()

    dtime = parse(p.simtime)
    if dtime.tzinfo == None:
        dtime = dtime.replace(tzinfo = UTC)
    else:
        dtime = dtime.astimezone(UTC)
#%% altitude 1-D mode
    if p.latlon[0] and p.latlon[1]:
        if p.altkm[0] is None:
            amm = (60,1000,5)
        elif len(p.altkm) == 3:
            amm = p.altkm[0],p.altkm[1],p.altkm[2]
            if p.latlon[0] is None: #use pfisr coord
                glat = 65; glon=-148
        altkm = arange(amm[0],amm[1],amm[2])
        glat,glon=p.latlon
#%% lat/lon grid mode at constant altitude
    else:# len(p.altkm)==1:
        if p.altkm[0] is None:
            altkm = 100
        else:
            altkm = p.altkm[0]
        lat = arange(-90,90+5,5)
        lon = arange(-180,180+10,10)
        glon,glat = meshgrid(lon,lat)

    dens,temp = testgtd7(dtime,altkm,glat,glon,p.f107a,p.f107,p.ap,p.mass)

    plotgtd(dens,temp,dtime,altkm)
    show()
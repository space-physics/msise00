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
from __future__ import division, absolute_import
from six import integer_types,string_types
from datetime import datetime
import logging
from pandas import DataFrame, Panel4D
from numpy import empty, atleast_1d,atleast_2d,array,repeat,ndarray
from tempfile import gettempdir
from warnings import warn
from matplotlib.pyplot import figure,subplots, close
from matplotlib.ticker import ScalarFormatter
#
#import sys,os
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#
from pymap3d.coordconv3d import aer2geodetic
from histutils.fortrandates import datetime2gtd
#
import gtd7


def rungtd7(dtime,altkm,glat,glon,f107a,f107,ap,mass):
    glat = atleast_2d(glat); glon=atleast_2d(glon) #has to be here
#%% set / print msis globals
    tselecopts = array([1,1,1,1,1,1,1,1,-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],float)
#%% altitude 1-D
    if glat.size==1 and glon.size==1:
        densd,tempd = rungtd1d(dtime,altkm,glat,glon,f107a,f107,ap,mass,tselecopts)
#%% lat/lon grid at 1 altitude
    else: #I didn't use numpy.nditer just yet
        species = ['He','O','N2','O2','Ar','Total','H','N','AnomalousO']
        ttypes = ['exotemp','heretemp']
        dtime = atleast_1d(dtime) #keep for code reuse
        iyd,utsec,stl = datetime2gtd(dtime,glon)

        dens = empty((dtime.size,9,glat.shape[0],glat.shape[1]))
        temp = empty((dtime.size,2,glat.shape[0],glat.shape[1]))

        gtd7.meters(1) # makes output in m^-3 and kg/m^-3
        for k in range(dtime.size):
          for i in range(glat.shape[0]):
              for j in range(glat.shape[1]):
                dens[k,:,i,j], temp[k,:,i,j] = gtd7.gtd7(iyd[k],utsec[k],altkm,
                                       glat[i,j],glon[i,j],stl[k],f107a,f107,ap,mass)

        densd = Panel4D(dens, labels=dtime,items=species,major_axis=glat[:,0],minor_axis=glon[0,:])
        tempd = Panel4D(temp, labels=dtime,items=ttypes, major_axis=glat[:,0],minor_axis=glon[0,:])

    return densd,tempd

def rungtd1d(t,altkm,glat,glon,f107a,f107,ap,mass,tselecopts):
    assert isinstance(t,(datetime,string_types))
    assert isinstance(altkm,(tuple,list,ndarray))
    assert isinstance(glat,(float,integer_types))
    assert isinstance(glon,(float,integer_types))
    assert isinstance(f107a,(float,integer_types))
    assert isinstance(f107,(float,integer_types))
# don't check ap, too complicated
    assert isinstance(mass,(float,integer_types))
    assert len(tselecopts)==25
#%%
    ap = atleast_1d(ap)
    if ap.size==1: ap = repeat(ap,7)
    species = ['He','O','N2','O2','Ar','Total','H','N','AnomalousO']
    ttypes = ['exotemp','heretemp']

    gtd7.tselec(tselecopts) #like the msis_driver example
    logging.debug('tselec options used:   {}'.format(gtd7.csw.sw)) #don't use tretrv, it doesn't work


    iyd,utsec,stl = datetime2gtd(t,glon)

    altkm = atleast_1d(altkm)
    dens = empty((altkm.size,9)); temp=empty((altkm.size,2))

    gtd7.meters(1) # makes output in m^-3 and kg/m^-3
    for i,a in enumerate(altkm):
        dens[i,:],temp[i,:] = gtd7.gtd7(iyd,utsec,a,glat,glon,stl, f107a,f107, ap,mass)

    densd = DataFrame(dens, index=altkm, columns=species)
    tempd = DataFrame(temp, index=altkm, columns=ttypes)
    return densd,tempd

def plotgtd(dens,temp,dtime,altkm, ap, f107,glat,glon):
    try:
        from astropy.time import Time
        from astropy.coordinates import get_sun,EarthLocation, AltAz
    except ImportError as e:
        warn('you must have AstroPy>=1.0 to have full functionality, attempting to fail soft. ' + str(e))
        get_sun=None
#
    dtime = atleast_1d(dtime)
    rodir = gettempdir()
    sfmt = ScalarFormatter(useMathText=True) #for 10^3 instead of 1e3
    sfmt.set_powerlimits((-2, 2))
    sfmt.set_scientific(True)
    sfmt.set_useOffset(False)

    if dens.ndim==2: #altitude 1-D
        footer = '\nlat/lon {}/{}  Ap={}  F10.7={}'.format(glat,glon,ap[0],f107)
        ax = figure().gca()
        for g in dens.columns:
            if g != 'Total':
                ax.semilogx(dens[g], dens.index, label=g)
        ax.legend(loc='best')
        ax.set_xlim(left=1e3)
        ax.set_ylabel('altitude [km]')
        ax.set_xlabel('density [m$^{-3}$]')
        ax.grid(True)
        ax.set_title('Number Density from MSISE-00' + footer)

        ax = figure().gca()
        ax.semilogx(dens['Total'],dens.index)
        ax.set_xlabel('Total Mass Density [kg m$^{-3}$]')
        ax.set_ylabel('altitude [km]')
        ax.grid(True)
        ax.set_title('Total Mass Density from MSISE-00'+footer)

        ax = figure().gca()
        ax.plot(temp['heretemp'],temp.index)
        ax.set_xlabel('Temperature')
        ax.set_ylabel('altitude [km]')
        ax.grid(True)
        ax.set_title('Temperature from MSISE-00' + footer)
    elif dens.ndim==4: #lat/lon grid
        if dtime.size>8:
            print('silently outputting plots to ' + rodir)
#%%sun lat/lon #FIXME this is a seemingly arbitrary procedure
        if get_sun is not None:
            ttime = Time(dtime)
            obs = EarthLocation(0,0) # geodetic lat,lon = 0,0 arbitrary
            sun = get_sun(time=ttime)
            aaf = AltAz(obstime=ttime,location=obs)
            sloc = sun.transform_to(aaf)
            slat,slon = aer2geodetic(sloc.az.value, sloc.alt.value, sloc.distance.value,0,0,0)[:2]
#%%
        for k,t in enumerate(dens): #dens is a Panel4D
            fg,ax = subplots(4,2,sharex=True, figsize=(8,8))
            fg.suptitle(str(t) + ' at alt.(km) '+str(altkm) +
                        '\nAp='+str(ap[0]) + '  F10.7='+str(f107),
                         fontsize=14)
            ax=ax.ravel(); i = 0 #don't use enumerate b/c of skip
            for g in dens[t].items:
                if g != 'Total':
                    a = ax[i]
                    hi = a.imshow(dens.loc[t,g].values, aspect='auto',
                             extent=(glon[0,0],glon[0,-1],glat[0,0],glat[-1,0]))
                    fg.colorbar(hi,ax=a, format=sfmt)
                    if get_sun is not None:
                        a.plot(slon[k],slat[k],linestyle='none',
                                            marker='o',markersize=5,color='w')
                    a.set_title('Density: ' + g,fontsize=11)
                    a.set_xlim(-180,180)
                    a.set_ylim(-90,90)
                    a.autoscale(False)
                    i+=1
            for i in range(0,6+2,2):
                ax[i].set_ylabel('latitude (deg)')
            for i in (6,7):
                ax[i].set_xlabel('longitude (deg)')
            thisofn = rodir+'/{:.1f}_{:03d}'.format(altkm[0],k) + '.png'
            fg.savefig(thisofn,dpi=100,bbox_inches='tight')
            if dtime.size>8:
                print('wrote ' + thisofn)
                close()
    else:
        print('densities' + str(dens))
        print('temperatures ' + str(temp))

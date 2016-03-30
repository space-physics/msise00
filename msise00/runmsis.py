#!/usr/bin/env python3
"""
NOTE: The performance of this demo has not been checked at all.
Please do basic sanity checks of output.
Quick demo of calling NRL MSISE-00 using f2py3 from Python
Michael Hirsch

Original fortran code from
http://nssdcftp.gsfc.nasa.gov/models/atmospheric/msis/nrlmsise00/
"""
from datetime import datetime
import logging
from xarray import DataArray
from numpy import empty, atleast_1d,atleast_2d,array,repeat,ndarray
#
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
        ttypes = ['exoatm','atm']
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

        densd = DataArray(data=dens,
                          coords=[dtime,species,glat[:,0],glon[0,:]],
                          dims=['time','species','lat','lon'])
        tempd = DataArray(data=temp,
                          coords=[dtime,ttypes, glat[:,0],glon[0,:]],
                          dims=['time','temp','lat','lon'])

    return densd,tempd

def rungtd1d(t,altkm,glat,glon,f107a,f107,ap,mass,tselecopts):
    assert isinstance(t,(datetime,str))
    assert isinstance(altkm,(float,int,tuple,list,ndarray))
    assert isinstance(glat,(float,int))
    assert isinstance(glon,(float,int))
    assert isinstance(f107a,(float,int))
    assert isinstance(f107,(float,int))
# don't check ap, too complicated
    assert isinstance(mass,(float,int))
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

    densd = DataArray(data=dens, coords=[altkm, species],dims=['altkm','species'])
    tempd = DataArray(data=temp, coords=[altkm, ttypes],dims=['altkm','temp'])
    return densd,tempd
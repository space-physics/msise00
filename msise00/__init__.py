"""
Quick demo of calling NRL MSISE-00 using f2py from Python
Michael Hirsch, Ph.D.

Original fortran code from
http://nssdcftp.gsfc.nasa.gov/models/atmospheric/msis/nrlmsise00/
"""
from datetime import datetime
from xarray import DataArray
from numpy import empty, atleast_1d,atleast_2d,array,repeat
#
from sciencedates import datetime2gtd
#
import gtd7
#
MASS = 48 # compute all parameters
TSELECOPS = array([1,1,1,1,1,1,1,1,-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],float)
species = ['He','O','N2','O2','Ar','Total','H','N','AnomalousO']
ttypes = ['Texo','Tn']
first=True

def rungtd7(dtime,altkm,glat,glon,f107a,f107,ap):
    """
    loops the rungtd1d function below. Figure it's easier to troubleshoot in Python than Fortran.
    """
    glat = atleast_2d(glat); glon=atleast_2d(glon) #has to be here
#%% altitude 1-D
    if glat.size==1 and glon.size==1:
        dens,temp = rungtd1d(dtime,altkm,glat,glon,f107a,f107,ap)
#%% lat/lon grid at 1 altitude
    else:
       dens,temp = loopalt_gtd(dtime, glat,glon,altkm,f107a,f107,ap)

    return dens,temp

def loopalt_gtd(dtime, glat,glon,altkm,f107a,f107,ap):
    dtime = atleast_1d(dtime) #keep for code reuse

    dens = DataArray(data=empty((dtime.size,len(species),glat.shape[0],glat.shape[1])),
                     coords=[dtime,species,glat[:,0],glon[0,:]],
                     dims=['time','species','lat','lon'])
    temp = DataArray(data=empty((dtime.size,len(ttypes),glat.shape[0],glat.shape[1])),
                     coords=[dtime,ttypes, glat[:,0],glon[0,:]],
                     dims=['time','temp','lat','lon'])

    for k,t in enumerate(dtime):
        print('computing {}'.format(t))
        for i in range(glat.shape[0]):
            for j in range(glat.shape[1]):
                dens[k,:,i,j], temp[k,:,i,j] = rungtd1d(t,altkm,glat[i,j],glon[i,j],f107a,f107,ap)

    return dens,temp

def rungtd1d(t,altkm,glat,glon,f107a,f107,ap):
    """
    This is the "atomic" function looped by other functions
    """
#%%
    altkm= atleast_1d(altkm)
    glon = atleast_1d(glon).squeeze()
    glat = atleast_1d(glat).squeeze()

    assert isinstance(t,(datetime,str)),'if you have multiple times, for loop over them'

    assert isinstance(f107a,(float,int))
    assert isinstance(f107,(float,int))
# don't check ap, too complicated
    assert isinstance(MASS,(float,int))
    assert len(TSELECOPS)==25
#%%
    ap = atleast_1d(ap)
    if ap.size==1:
        ap = repeat(ap,7)

    gtd7.tselec(TSELECOPS) #like the msis_driver example

    iyd,utsec,stl = datetime2gtd(t,glon)
    altkm         = atleast_1d(altkm)

    dens = DataArray(data=empty((altkm.size, len(species))),
                     coords=[altkm, species],dims=['alt_km','species'])
    temp = DataArray(data=empty((altkm.size, len(ttypes))),
                      coords=[altkm, ttypes],dims=['alt_km','temp'])

    gtd7.meters(1) # makes output in m^-3 and kg/m^-3
    for i,a in enumerate(altkm):
        dens[i,:],temp[i,:] = gtd7.gtd7(iyd,utsec,a, glat,glon,stl, f107a,f107, ap,MASS)

    return dens,temp

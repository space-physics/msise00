#!/usr/bin/env python
"""
understanding sun apparent position over Earth in geodetic lat,lon
there must be a better way to do this!
"""
from astropy.time import Time
from astropy.coordinates import get_sun, AltAz,EarthLocation
import astropy.units as u
import numpy as np
from matplotlib.pyplot import figure,show
#
from pymap3d import aer2geodetic

midnight=Time('2014-12-21T00:00:00Z')
delta_midnight = np.linspace(0, 180,1000)*u.day
times = midnight + delta_midnight

obs = EarthLocation(0,0) #center of Earth
sun = get_sun(time=times)
aaf = AltAz(obstime=times,location=obs)
sloc = sun.transform_to(aaf)

ax = figure().gca()
ax.plot(sloc.alt,label='el')
ax.plot(sloc.az,label='az')
ax.legend()

lat,lon,alt = aer2geodetic(sloc.az.value, sloc.alt.value, sloc.distance.value,0,0,0)

ax = figure().gca()
ax.plot(lon,lat)

show()

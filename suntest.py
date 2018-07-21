#!/usr/bin/env python
"""
understanding sun apparent position over Earth in geodetic lat,lon
"""
from astropy.time import Time
from astropy.coordinates import get_sun, AltAz, EarthLocation
import astropy.units as u
import numpy as np
from matplotlib.pyplot import figure, show
from pymap3d import aer2geodetic

obslla = (0, 0, 0)

midnight = Time('2015-01-01T00:00')
delta_midnight = np.linspace(0, 365, 1000)*u.day
time = midnight + delta_midnight

obs = EarthLocation(lat=obslla[0], lon=obslla[1], height=obslla[2])
sun = get_sun(time=time)
aaf = AltAz(obstime=time, location=obs)
sloc = sun.transform_to(aaf)
# %%
time = time.to_datetime()

fg = figure()
ax = fg.subplots(2, 1, sharex=True)
ax[0].plot(time, sloc.alt)
ax[0].set_title('sun elevation')
ax[0].set_ylabel('elevation [deg]')

ax[1].plot(time, sloc.az)
ax[1].set_title('sun azimuth')
ax[1].set_ylabel('azimuth [deg]')
ax[1].set_xlabel('time')

fg.suptitle(f'sun over 1 year @ lat,lon,alt: {obslla}')

# %%

lat, lon, alt = aer2geodetic(sloc.az.value, sloc.alt.value, sloc.distance.value, *obslla)

ax = figure().gca()
ax.plot(time, lat)
ax.set_title('subsolar latitude vs. time')
ax.set_ylabel('latitude [deg]')
ax.set_xlabel('time')

show()

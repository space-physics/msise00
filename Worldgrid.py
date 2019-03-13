#!/usr/bin/env python
"""
Example:

lat / lon grid at altitude example
"""
from datetime import datetime
from matplotlib.pyplot import show

import msise00.plots as msplots
import msise00
from msise00.worldgrid import latlonworldgrid

glat, glon = latlonworldgrid(10., 20.)
alt_km = 200.
time = datetime(2015, 12, 13, 10, 0, 0)

atmos = msise00.run(time, alt_km, glat, glon)

msplots.plotgtd(atmos)

show()

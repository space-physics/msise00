#!/usr/bin/env python
"""
Example:
Poker Flat Research Range altitude profile
"""
import numpy as np
from datetime import datetime
from matplotlib.pyplot import show

import msise00.plots as msplots
import msise00

glat = 65.1
glon = -147.5
alt_km = np.arange(50, 1000, 20.0)
time = datetime(2015, 12, 13, 10, 0, 0)

atmos = msise00.run(time, alt_km, glat, glon)

msplots.plotgtd(atmos)

show()

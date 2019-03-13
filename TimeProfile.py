#!/usr/bin/env python
"""
Time profile example
"""
import numpy as np
from datetime import datetime, timedelta
from matplotlib.pyplot import show

import msise00.plots as msplots
import msise00

glat = 65.1
glon = -147.5
alt_km = 200
t0 = datetime(2015, 12, 13, 10, 0, 0)
t1 = datetime(2015, 12, 14, 10, 0, 0)

times = np.arange(t0, t1, timedelta(hours=1))

atmos = msise00.run(times, alt_km, glat, glon)

msplots.plotgtd(atmos)

show()

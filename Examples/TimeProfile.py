#!/usr/bin/env python3
"""
Time profile example
"""

from datetime import datetime, timedelta
from matplotlib.pyplot import show

import msise00.plots as msplots
import msise00

glat = 65.1
glon = -147.5
alt_km = 200
t0 = datetime(2015, 12, 13, 10, 0, 0)
t1 = datetime(2015, 12, 14, 10, 0, 0)

times = [t0 + timedelta(hours=i) for i in range(int((t1 - t0).total_seconds() // 3600))]

atmos = msise00.run(times, alt_km, glat, glon)

msplots.plotgtd(atmos)

show()

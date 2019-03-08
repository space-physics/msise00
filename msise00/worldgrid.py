import numpy as np
from typing import Tuple


def latlonworldgrid(latstep: int = 5, lonstep: int = 5) -> Tuple[np.ndarray, np.ndarray]:
    lat = np.arange(-90., 90+latstep, latstep)
    lon = np.arange(-180., 180+lonstep, lonstep)
    glon, glat = np.meshgrid(lon, lat)

    return glat, glon

import numpy as np
from typing import Tuple, Union


def latlonworldgrid(
    latstep: Union[float, int] = 5, lonstep: Union[float, int] = 5
) -> Tuple[np.ndarray, np.ndarray]:
    lat = np.arange(-90.0, 90 + latstep, latstep)
    lon = np.arange(-180.0, 180 + lonstep, lonstep)
    glon, glat = np.meshgrid(lon, lat)

    return glat, glon

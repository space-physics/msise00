from dateutil.parser import parse
import numpy as np
from datetime import datetime, date
from typing import Union


def todt64(time: Union[str, datetime, np.datetime64, list, np.ndarray]) -> np.ndarray:
    time = np.atleast_1d(time)

    if time.size == 1:
        time = np.atleast_1d(np.datetime64(time[0], dtype='datetime64[us]'))
    elif time.size == 2:
        time = np.arange(time[0], time[1], dtype='datetime64[h]')
    else:
        pass

    return time


def todatetime(time) -> datetime:

    if isinstance(time, str):
        dtime = parse(time)
    elif isinstance(time, datetime):
        dtime = time
    elif isinstance(time, np.datetime64):
        dtime = time.astype(datetime)
    elif isinstance(time, (tuple, list, np.ndarray)):
        if len(time) == 1:
            dtime = todatetime(time[0])
        else:
            dtime = [todatetime(t) for t in time]
    else:
        raise TypeError(f'{type(time)} not allowed')

    if not isinstance(dtime, datetime) and isinstance(dtime, date):
        dtime = datetime.combine(dtime, datetime.min.time())

    return dtime

from dateutil.parser import parse
import numpy as np
from datetime import datetime, date
import typing

TIME_FMTS = typing.Union[str, datetime, np.datetime64]


def todt64(time: TIME_FMTS) -> np.ndarray:
    time = np.atleast_1d(time)

    if time.size == 1:
        time = np.atleast_1d(np.datetime64(time[0], dtype="datetime64[us]"))
    elif time.size == 2:
        time = np.arange(time[0], time[1], dtype="datetime64[h]")
    else:
        pass

    return time


def todatetime(time: TIME_FMTS) -> datetime:

    if isinstance(time, str):
        dtime = parse(time)
    elif isinstance(time, datetime):
        dtime = time
    elif isinstance(time, np.datetime64):
        dtime = time.astype(datetime)
    else:
        raise TypeError(f"{type(time)} not allowed")

    if not isinstance(dtime, datetime) and isinstance(dtime, date):
        dtime = datetime.combine(dtime, datetime.min.time())

    return dtime

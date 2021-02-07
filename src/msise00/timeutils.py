from __future__ import annotations

from dateutil.parser import parse
import numpy as np
from datetime import datetime, date


def todt64(time: str | datetime | np.datetime64) -> np.ndarray:
    dtime = np.atleast_1d(todatetime(time))  # type: ignore

    if dtime.size == 1:
        dtime = np.atleast_1d(np.datetime64(dtime[0], dtype="datetime64[us]"))  # type: ignore
        # mypy bug
    elif dtime.size == 2:
        dtime = np.arange(dtime[0], dtime[1], dtype="datetime64[h]")
    else:
        pass

    return dtime


def todatetime(time: str | datetime | np.datetime64) -> datetime:

    if isinstance(time, str):
        dtime: datetime = parse(time)
    elif isinstance(time, datetime):
        dtime = time
    elif isinstance(time, np.datetime64):
        dtime = time.astype(datetime)  # type: ignore
        # mypy bug
    else:
        raise TypeError(f"{type(time)} not allowed")

    if not isinstance(dtime, datetime) and isinstance(dtime, date):
        dtime = datetime.combine(dtime, datetime.min.time())

    return dtime

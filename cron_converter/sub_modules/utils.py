import datetime
from typing import List, Union


def to_parts(d: Union[datetime.datetime, datetime.date]) -> List[Union[int, None]]:
    minute = None
    hour = None
    day = d.day
    month = d.month
    dayofweek = d.weekday()

    if isinstance(d, datetime.datetime):
        minute = d.minute
        hour = d.hour
    return [minute, hour, day, month, dayofweek]

import datetime
from typing import List, Union


def to_parts(d: Union[datetime.datetime, datetime.date]) -> List[Union[int, None]]:
    minute = None
    hour = None
    day = d.day
    month = d.month
    dayofweek = iso_to_cron_weekday(d.isoweekday())

    if isinstance(d, datetime.datetime):
        minute = d.minute
        hour = d.hour
    return [minute, hour, day, month, dayofweek]


def iso_to_cron_weekday(iso_weekday: int) -> int:
    """Converts ISO weekday numbers to cron weekday numbers.
        ISO weekday numbers are Monday (1) to Sunday (7)
        Cron weekday numbers are Sunday (0) to Saturday (6).
    """
    return iso_weekday % 7

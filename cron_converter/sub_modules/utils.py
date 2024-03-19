import datetime


def to_parts(d: datetime.datetime | datetime.date) -> list[int | None]:
    minute = None
    hour = None
    day = d.day
    month = d.month
    dayofweek = d.weekday()

    if isinstance(d, datetime.datetime):
        minute = d.minute
        hour = d.hour
    return [minute, hour, day, month, dayofweek]

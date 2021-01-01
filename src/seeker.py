from datetime import datetime, tzinfo, timezone, timedelta
import calendar
import copy
from collections import namedtuple
from typing import Optional

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from cron import Cron
    from part import Part

weekdays = {'Sun': 0, 'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6}  # en_US weekdays


def _add_months(date: 'datetime', months):
    month = date.month - 1 + months
    year = date.year + month // 12
    month = month % 12 + 1
    # day = min(self.date.day, calendar.monthrange(year, month)[1])
    return date.replace(year=year, month=month, day=1)  # day=1 if next(), day=lastOfMonth if prev()


class Seeker:
    """Create an instance of Seeker. Seeker objects search for execution times of a cron schedule.
    Args:
        cron (object): Cron object
        start_time (datetime): The start time for the schedule iterator
    """
    def __init__(self, cron: 'Cron', start_time: Optional[datetime] = None) -> None:
        if not cron.parts:
            raise LookupError('No schedule found')

        if start_time and isinstance(start_time, datetime):
            self.tz_info = start_time.tzinfo
            self.date = start_time
        else:
            self.date = datetime.now(timezone.utc)

        if self.date.second > 0:
            # Add a minute to the date to prevent returning dates in the past
            self.date = self.date + timedelta(minutes=+1)

        self.start_time = self.date
        self.cron = cron
        self.date = self.start_time
        self.pristine = True

    """Resets the iterator
    """
    def reset(self) -> None:
        self.pristine = True
        self.date = self.start_time

    """Returns the time the schedule would run next.
    """
    def next(self):
        if self.pristine:
            self.pristine = False
        else:
            one_minute = timedelta(minutes=1)
            self.date = self.date + one_minute  # so that next is never now

        return self.find_date(self.cron.parts)

    """Returns the time the schedule would have last run at.
    """
    def prev(self):
        self.pristine = False
        return self.find_date(self.cron.parts, True)

    """Returns the time the schedule would run next. # TODO refactor description 
    
    Args:
    
    Returns:
    
    """
    def find_date(self, cron_parts: List['Part'], reverse: bool = False):
        # operation = 'add'
        # reset = 'start_of'
        # if reverse:
        #     operation = 'subtract'
        #     reset = 'end_of'
        #     # self.date.subtract(1, 'minute'); // Ensure prev and next cannot be same time
        retry = 24
        for i in range(retry, 0, -1):
            self._shift_month(cron_parts[3])
            month_changed = self._shift_day(cron_parts[2], cron_parts[4])
            if not month_changed:
                day_changed = self._shift_hour(cron_parts[1])
                if not day_changed:
                    hour_changed = self._shift_minute(cron_parts[0])
                    if not hour_changed:
                        break
        if not retry:
            raise Exception('Unable to find execution time for schedule')

        return copy.deepcopy(self.date.replace(second=0, microsecond=0))

    def _shift_month(self, cron_month_part: 'Part'):
        while self.date.month not in cron_month_part.to_list():
            self.date = _add_months(self.date, 1)
            self.date = self.date.replace(day=1, hour=00, minute=00)

    def _shift_day(self, cron_day_part: 'Part', cron_weekday_part: 'Part'):
        current_month = self.date.month
        while self.date.day not in cron_day_part.to_list() or weekdays.get(self.date.strftime("%a")) not in cron_weekday_part.to_list():
            self.date = self.date + timedelta(days=+1)
            if current_month != self.date.month:
                self.date = self.date.replace(day=1, hour=00, minute=00)
                return True
        return False

    def _shift_hour(self, cron_hour_part: 'Part'):
        current_day = self.date.day
        while self.date.hour not in cron_hour_part.to_list():
            self.date = self.date + timedelta(hours=+1)
            if current_day != self.date.day:
                self.date = self.date.replace(hour=00, minute=00)
                return True
        return False

    def _shift_minute(self, cron_minute_part: 'Part'):
        current_hour = self.date.hour
        while self.date.minute not in cron_minute_part.to_list():
            self.date = self.date + timedelta(minutes=+1)
            if current_hour != self.date.hour:
                self.date = self.date.replace(minute=00) # se cambia ora e quindi vado una avanti o una indietro, allora devo resettare i minuti
                return True
        return False

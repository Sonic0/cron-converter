from datetime import datetime, timedelta, timezone
from dateutil import tz
import calendar
import copy
from typing import Optional

from typing import TYPE_CHECKING, List, Literal

if TYPE_CHECKING:
    from cron import Cron
    from sub_modules.part import Part

weekdays = {'Sun': 0, 'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6}  # en_US weekdays


class Seeker:
    """Create an instance of Seeker. Seeker objects search for execution times of a cron schedule.
    Args:
        cron (object): Cron object
        start_date (datetime): The start date for the schedule iterator, with or without timezone.
        timezone_str (str): The timezone to make an timezone aware datetime as response.
    """
    def __init__(self, cron: 'Cron', start_date: Optional[datetime] = None, timezone_str: Optional[str] = None) -> None:
        if not cron.parts:
            raise LookupError('No schedule found')

        if start_date is not None and timezone_str is not None:
            raise ValueError('should have location_num or location_path, but not both')
        if start_date:
            # Construct the Seeker object from a past or a future date
            try:
                isinstance(start_date, datetime)
                self.tz_info = start_date.tzinfo
                self.date = start_date
            except Exception as exc:
                raise ValueError(f'Input schedule start time is not a valid datetime object. Error -> {exc}')
        elif timezone_str:
            if tz.gettz(timezone_str):
                self.tz_info = tz.gettz(timezone_str)
                self.date = datetime.now(self.tz_info)
            else:
                raise ValueError(f'Provided not a valid Timezone --> {timezone_str}')
        else:
            self.date = datetime.now(tz.tzutc())

        if self.date.second > 0:
            # Add a minute to the date to prevent returning dates in the past
            self.date = self.date + timedelta(minutes=+1)

        self.start_time = self.date
        self.cron = cron
        self.pristine = True

    """Resets the iterator."""
    def reset(self) -> None:
        self.pristine = True
        self.date = self.start_time

    """Returns the time the schedule would run next.
    
     Returns:
        (datetime): The time the schedule would run next.
    """
    def next(self) -> datetime:
        if self.pristine:
            self.pristine = False
        else:
            one_minute = timedelta(minutes=+1)
            # Ensure next is never now
            self.date = self.date + one_minute

        return self.find_date(getattr(self.cron, 'parts'))

    """Returns the time the schedule would have last run at.
    
    Returns:
        (datetime): The time the schedule would have last run at.
    """
    def prev(self) -> datetime:
        self.pristine = False
        # Ensure prev and next cannot be same time
        self.date = self.date + timedelta(minutes=-1)
        return self.find_date(getattr(self.cron, 'parts'), True)

    """Returns the time the schedule would run next. # TODO refactor description.
    
    Args:
        cron_parts (List): List of all cron 'Part'.
        reverse(boolean): Whether to find the previous value instead of next.
    Returns:
        (datetime): A new datetime object. The date the schedule would have executed at.
    """
    def find_date(self, cron_parts: List['Part'], reverse: bool = False) -> datetime:
        operation: Literal['add', 'subtract'] = 'add'
        if reverse:
            operation = 'subtract'
        retry = 24
        while retry:
            retry -= 1
            self._shift_month(cron_parts[3], operation)
            month_changed = self._shift_day(cron_parts[2], cron_parts[4], operation)
            if not month_changed:
                day_changed = self._shift_hour(cron_parts[1], operation)
                if not day_changed:
                    hour_changed = self._shift_minute(cron_parts[0], operation)
                    if not hour_changed:
                        break
        else:
            raise Exception('Unable to find execution time for schedule')

        return copy.deepcopy(self.date.replace(second=0, microsecond=0))

    """Increments/decrements the month value of a date, until a month that matches the schedule is found.
    
    Args:
        cron_month_part (Part): The month 'Part' object.
        operation (Literal['add', 'subtract']): The function to call on date: 'add' or 'subtract'.
    """
    def _shift_month(self, cron_month_part: 'Part', operation: Literal['add', 'subtract']) -> None:
        while self.date.month not in cron_month_part.to_list():
            self.date = self._calc_months(self.date, 1, operation)

    """Increments/decrements the day value of a date, until a day that matches the schedule is found.

    Args:
        cron_day_part (Part): The days 'Part' object.
        operation (Literal['add', 'subtract']): The function to call on date: 'add' or 'subtract'.
    Returns:
        (boolean): Whether the month of the date was changed.
    """
    def _shift_day(self, cron_day_part: 'Part', cron_weekday_part: 'Part', operation: Literal['add', 'subtract']) -> bool:
        current_month = self.date.month
        while self.date.day not in cron_day_part.to_list() or \
                weekdays.get(self.date.strftime("%a")) not in cron_weekday_part.to_list():
            if operation == 'add':
                self.date = self.date + timedelta(days=+1)
                self.date = self.date.replace(hour=0, minute=0, second=0)
            else:
                self.date = self.date + timedelta(days=-1)
                self.date = self.date.replace(hour=23, minute=59, second=59)
            if current_month != self.date.month:
                return True
        return False

    """Increments/decrements the hour value of a date, until an hour that matches the schedule is found.

    Args:
        cron_hour_part (Part): The hours 'Part' object
        operation (Literal['add', 'subtract']): The function to call on date: 'add' or 'subtract'.
    Returns:
        (boolean): Whether the day of the date was changed
    """
    def _shift_hour(self, cron_hour_part: 'Part', operation: Literal['add', 'subtract']) -> bool:
        current_day = self.date.day
        while self.date.hour not in cron_hour_part.to_list():
            if operation == 'add':
                self.date = self.date + timedelta(hours=+1)
                self.date = self.date.replace(minute=00, second=0)
            else:
                self.date = self.date + timedelta(hours=-1)
                self.date = self.date.replace(minute=59, second=59)
            if current_day != self.date.day:
                return True
        return False

    """Increments/decrements the minute value of a date, until a minute that matches the schedule is found.

    Args:
        cron_minute_part (Part): The minutes 'Part' object.
        operation (Literal['add', 'subtract']): The function to call on date: 'add' or 'subtract'.

    Returns:
        (boolean): Whether the hour of the date was changed.
    """
    def _shift_minute(self, cron_minute_part: 'Part', operation: Literal['add', 'subtract']) -> bool:
        current_hour = self.date.hour
        while self.date.minute not in cron_minute_part.to_list():
            if operation == 'add':
                self.date = self.date + timedelta(minutes=+1)
                self.date = self.date.replace(second=0)
            else:
                self.date = self.date + timedelta(minutes=-1)
                self.date = self.date.replace(second=59)
            if current_hour != self.date.hour:
                return True
        return False

    """Static method to increment/decrement the month value of a datetime Object.
    
    Args:
        date (datetime): Date Object it increments/decrements the month value to.
        months (int): Number of months to add at the provided input date Object
        operation (Literal['add', 'subtract']): The function to call on date: 'add' or 'subtract'.
    Returns:
        (datetime): The input datetime object incremented or decremented.
    """
    @staticmethod
    def _calc_months(date: 'datetime', months: int, operation: Literal['add', 'subtract']) -> datetime:
        if operation == 'add':
            month = date.month - 1 + months
        else:
            month = date.month - 1 - months
        year = date.year + month // 12
        month = month % 12 + 1
        if operation == 'add':
            return date.replace(year=year, month=month, day=1, hour=00, minute=00, second=00)
        else:
            # Get the last day of the month
            max_month_day = calendar.monthrange(year, month)[1]
            return date.replace(year=year, month=month, day=max_month_day, hour=23, minute=59, second=59)

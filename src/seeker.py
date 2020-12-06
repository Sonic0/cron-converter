from datetime import datetime, tzinfo, timezone
from typing import Optional

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from cron import Cron
    from part import Part  # Cron part


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

        self.date = self.date.replace(microsecond=0)
        self.cron = cron
        self.start_time = self.date
        self.pristine = True

    """Resets the iterator
    """
    def reset(self) -> None:
        self.pristine = True
        self.date = self.start_time

    """Returns the time the schedule would run next.
    """
    def next(self):
        pass

    """Returns the time the schedule would have last run at.
    """
    def prev(self):
        self.pristine = False
        return self.find_date(self.cron.parts, self.date, True)

    """Returns the time the schedule would run next. # TODO refactor description 
    
    Args:
    
    Returns:
    
    """
    def find_date(self, cron_parts: List['Part'], reverse: bool):
        operation = 'add'
        reset = 'start_of'
        if reverse:
            operation = 'subtract'
            reset = 'end_of'
            # date.subtract(1, 'minute'); // Ensure prev and next cannot be same time
        retry = 24
        for i in range(retry, 0):
            self.shift_month(cron_parts[4], operation, reset)
        pass

    def shift_month(self, cron_part: 'Part', operation, reset):
        month = self.date.month
        print(cron_part.to_list())
        pass

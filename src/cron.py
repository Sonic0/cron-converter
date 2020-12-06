from part import Part
from units import units
# from seeker import Seeker
# from datetime import datetime

# from typing import Optional


class Cron:
    """Creates an instance of Cron.

    Cron objects each represent a cron schedule.

    Attributes:
        options (dict): The options to use
    """
    def __init__(self, options=None):
        self.options = options if bool(options) else dict()
        self.parts = None

    """Parses a cron string.
    
    Args:
        cron_string (str): The cron string to parse.    
    """
    def from_string(self, cron_string: str) -> None:
        if type(cron_string) != str:
            raise TypeError('Invalid cron string')
        self.parts = cron_string.strip().split()
        if len(self.parts) != 5:
            raise ValueError("Invalid cron string format")
        new_parts = []
        for item, unit in zip(self.parts, units):
            part = Part(unit, self.options)
            part.from_string(item)
            new_parts.append(part)

        self.parts = new_parts

    """Return the cron schedule as a string.
    
    Returns:
        cron string (str): The cron schedule as a string.
    """
    def to_string(self) -> str:
        if not self.parts:
            raise LookupError('No schedule found')
        return ' '.join(str(part) for part in self.parts)

    """Returns the cron schedule as a 2-dimentional list of integers
    
    Returns:
        schedule_list (list of lists): The cron schedule as a list. 
    """
    def to_list(self):
        if not self.parts:
            raise LookupError('No schedule found')
        schedule_list = []
        for part in self.parts:
            schedule_list.append(part.to_list())
        return schedule_list

    """Returns the time the schedule would run next.
    
    Args:
        start_date Optional(datetime): A datetime object. If not provided, time now in utc
    
    Returns:
        Seeker (Object): A schedule iterator.
    """
    # def schedule(self, start_time: Optional[datetime] = None):
    #     return Seeker(self, start_time)

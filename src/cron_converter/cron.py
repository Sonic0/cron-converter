from .sub_modules.part import Part
from .sub_modules.units import units
from .sub_modules.seeker import Seeker

from datetime import datetime

from typing import Optional


class Cron:
    """Creates an instance of Cron.

    Cron objects each represent a cron schedule.

    Attributes:
        options (dict): The options to use
    """
    def __init__(self, cron_string: str = None, options=None):
        self.options = options if bool(options) else dict()
        self.parts = None
        if cron_string:
            self.from_string(cron_string)

    """Print directly the Cron Object"""
    def __str__(self):
        return self.to_string()

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
        cron_parts = []
        for item, unit in zip(self.parts, units):
            part = Part(unit, self.options)
            part.from_string(item)
            cron_parts.append(part)

        self.parts = cron_parts

    """Return the cron schedule as a string.
    
    Returns:
        cron string (str): The cron schedule as a string.
    """
    def to_string(self) -> str:
        if not self.parts:
            raise LookupError('No schedule found')
        return ' '.join(str(part) for part in self.parts)

    """Parses a 2-dimentional array of integers as a cron schedule.
    
    Args:
        cron_list (list of list): The 2-dimensional list to parse
    """
    def from_list(self, cron_list):
        cron_parts = []
        if len(cron_list) != 5:
            raise ValueError(f'Invalid cron list')

        for cron_part_list, unit in zip(cron_list, units):
            part = Part(unit, self.options)
            part.from_list(cron_part_list)
            cron_parts.append(part)

        self.parts = cron_parts

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
    def schedule(self, start_time: Optional[datetime] = None):
        return Seeker(self, start_time)

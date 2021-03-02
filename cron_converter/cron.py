from .sub_modules.part import Part
from .sub_modules.units import units
from .sub_modules.seeker import Seeker

from datetime import datetime

from typing import Optional, List, Union


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

    def __str__(self) -> str:
        """Print directly the Cron Object"""
        return self.to_string()

    def from_string(self, cron_string: str) -> None:
        """Parses a cron string (minutes - hours - days - months - weekday)

        :param cron_string: (str) The cron string to parse. It has to be made up 5 parts.
        :raises ValueError: Incorrect length of the cron string.
        """
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

    def to_string(self) -> str:
        """Return the cron schedule as a string.

        :return: cron string (str) -> The cron schedule as a string.
        """
        if not self.parts:
            raise LookupError('No schedule found')
        return ' '.join(str(part) for part in self.parts)

    def from_list(self, cron_list: List[List[Union[str, int]]]):
        """Parses a 2-dimentional array of integers as a cron schedule.

        :param cron_list: (list of list) The 2-dimensional list to parse.
        :raises ValueError: Incorrect length of the cron list.
        """
        cron_parts = []
        if len(cron_list) != 5:
            raise ValueError(f'Invalid cron list')

        for cron_part_list, unit in zip(cron_list, units):
            part = Part(unit, self.options)
            part.from_list(cron_part_list)
            cron_parts.append(part)

        self.parts = cron_parts

    def to_list(self) -> List[Part]:
        """Returns the cron schedule as a 2-dimentional list of integers

        :return: schedule_list -> The cron schedule as a list.
        :raises LookupError: Empty Cron object.
        """
        if not self.parts:
            raise LookupError('No schedule found')
        schedule_list = []
        for part in self.parts:
            schedule_list.append(part.to_list())
        return schedule_list

    def schedule(self, start_time: Optional[datetime] = None) -> Seeker:
        """Returns the time the schedule would run next.

        :param start_time: A datetime object. If not provided, it will be now in utc.
        :return: A schedule iterator.
        """
        return Seeker(self, start_time)

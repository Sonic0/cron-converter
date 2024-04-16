from datetime import date, datetime
from functools import total_ordering
from typing import List, Optional, Union

from .sub_modules.part import Part
from .sub_modules.seeker import Seeker
from .sub_modules.units import units
from .sub_modules.utils import to_parts


@total_ordering
class Cron:
    """Creates an instance of Cron.

    Cron objects each represent a cron schedule.

    Attributes:
        options (dict): The options to use
    """
    def __init__(self, cron_string: Optional[str] = None, options=None):
        self.options = options if bool(options) else dict()
        self.parts: List[Part] = []
        if cron_string:
            self.from_string(cron_string)

    def __str__(self) -> str:
        """Print directly the Cron Object"""
        return self.to_string()

    def __lt__(self, other) -> bool:
        """ This Cron object is lower than the other Cron.
        The comparison is made by 'total_ordering' comparing the number of Cron schedule times.
        """
        reordered_parts = self.parts[:3] + [self.parts[4], self.parts[3]]
        reordered_parts_other = other.parts[:3] + [other.parts[4], other.parts[3]]
        for part, other_part in zip(reversed(reordered_parts), reversed(reordered_parts_other)):
            if part < other_part:
                return True
        return False

    def __eq__(self, other) -> bool:
        """ This Cron object is equal to the other Cron.
        The comparison is made by 'total_ordering' comparing the number of Cron schedule times.
        """
        return all(part == other_part for part, other_part in zip(self.parts, other.parts))

    def __contains__(self, item: Union[datetime, date]) -> bool:
        return self.validate(item)

    def from_string(self, cron_string: str) -> None:
        """Parses a cron string (minutes - hours - days - months - weekday)

        :param cron_string: (str) The cron string to parse. It has to be made up 5 parts.
        :raises ValueError: Incorrect length of the cron string.
        """
        if type(cron_string) is not str:
            raise TypeError('Invalid cron string')
        raw_cron_parts = cron_string.strip().split()
        if len(raw_cron_parts) != 5:
            raise ValueError("Invalid cron string format")
        for item, unit in zip(raw_cron_parts, units):
            part = Part(unit, self.options)
            part.from_string(item)
            self.parts.append(part)

    def to_string(self) -> str:
        """Return the cron schedule as a string.

        :return: cron string (str) -> The cron schedule as a string.
        """
        if not self.parts:
            raise LookupError('No schedule found')
        return ' '.join(str(part) for part in self.parts)

    def from_list(self, cron_list: List[List[Union[str, int]]]):
        """Parses a 2-dimensional array of integers as a cron schedule.

        :param cron_list: (list of list) The 2-dimensional list to parse.
        :raises ValueError: Incorrect length of the cron list.
        """
        if len(cron_list) != 5:
            raise ValueError('Invalid cron list')

        for cron_part_list, unit in zip(cron_list, units):
            part = Part(unit, self.options)
            part.from_list(cron_part_list)
            self.parts.append(part)

    def to_list(self) -> List[List[int]]:
        """Returns the cron schedule as a 2-dimensional list of integers

        :return: schedule_list -> The cron schedule as a list.
        :raises LookupError: Empty Cron object.
        """
        if not self.parts:
            raise LookupError('No schedule found')
        schedule_list = []
        for part in self.parts:
            schedule_list.append(part.to_list())
        return schedule_list

    def schedule(self, start_date: Optional[datetime] = None, timezone_str: Optional[str] = None) -> Seeker:
        """Returns the time the schedule would run next.

        :param start_date: Optional. A datetime object. If not provided, date will be now in UTC.
                                     This param exclude 'timezone_str'.
        :param timezone_str: Optional. A timezone str('Europe/Rome', 'America/New_York', ...).
                                       Date will be now, but localized.
                                       If not provided, date will be now in UTC. This param exclude 'start_date'.
        :return: A schedule iterator.
        """
        return Seeker(self, start_date, timezone_str)

    def validate(self, date_time_obj: Union[datetime, date]) -> bool:
        """Returns True if the object passed is within the Cron rule.

        :param date_time_obj: A datetime or date object

        :return: True if the object passed is within the Cron Rule.
        """

        valid = []
        for cron_part, d_par in zip(self.parts, to_parts(date_time_obj)):
            if d_par is not None:
                valid.append(d_par in cron_part.to_list())
            else:
                valid.append(True)

        return all(valid)

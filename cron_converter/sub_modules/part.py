from functools import total_ordering
from typing import List, Union


@total_ordering
class Part:
    """Creates an instance of Part.

    Part objects represent a collection of positive integers.

    Attributes:
        unit (dict): The unit of measurement of time (see units.py).
        options (dict): The options to use: output_weekday_names and output_month_names
    """
    def __init__(self, unit, options):
        self.options = options if bool(options) else dict()
        self.unit = unit
        self.values = None

    def __str__(self) -> str:
        """Print directly the Part Object"""
        return self.to_string()

    def __repr__(self):
        return f'{self.__class__.__name__} - (values:{self.values!r}, unit:{self.unit.get("name")!r})'

    def __len__(self):
        return len(self.to_list())

    def __lt__(self, other) -> bool:
        """ This Part object is lower than the other Part.
        The comparison is made by 'total_ordering', comparing self.values list.
        """
        return len(self) < len(other)

    def __eq__(self, other) -> bool:
        """ This Part object is equal to the other Part.
        The comparison is made by 'total_ordering', comparing self.values list.
        """
        return len(self) == len(other)

    def from_list(self, part_list: List[Union[str, int]]) -> None:
        """Validates a range of positive integers.

        :param part_list: An array of positive integers.
        :raises ValueError: An error occurred in case of invalid value or out of range value
        """
        values = []
        for part_value in part_list:
            try:
                parsed_value = int(part_value)
            except ValueError:
                raise ValueError(f'Invalid list value {part_value}')
            if parsed_value is None:
                raise ValueError(f'Invalid list value {part_value}')
            values.append(parsed_value)

        if not values:
            raise ValueError('Empty interval value')

        sunday_fixed_values = self._fix_sunday(values)
        unique_values = list(dict.fromkeys(sunday_fixed_values))  # Remove eventual duplicates
        unique_values.sort()
        part_value = self.out_of_range(unique_values)
        if part_value is not None:
            raise ValueError(f'Value {part_value!r} out of range for {self.unit.get("name")!r}')

        self.values = unique_values

    def from_string(self, cron_part: str) -> None:
        """Parses a string as a range of positive integers.

        :param cron_part: The string that represent a Part. It will be converted as a range.
        :raises ValueError: Invalid value.
        :raises ValueError: An error occurred in case of invalid value or out of range value.
        """
        intervals_values_list = []  # Final list of list. Every sub-list will be a unit range
        # Split in the case of multiple unit ranges and replace months 'alt' with corresponding 'int' numbers
        string_parts = self._replace_alternatives(cron_part).split(',')
        for string_part in string_parts:
            # Split in the case of step parameter
            range_step_string_parts = string_part.split('/')
            if len(range_step_string_parts) > 2:
                raise ValueError(f'Invalid value {string_part!r} in cron part {cron_part!r}')
            range_string = range_step_string_parts[0]
            if not range_string:
                raise ValueError(f'Invalid value {range_string}')
            elif range_string == '*':
                range_list = self.possible_values()
            else:
                range_list = self._parse_range(range_string)
                range_list = self._fix_sunday(range_list)
                value = self.out_of_range(range_list)
                if value is not None:
                    raise ValueError(f'Value {value!r} out of range for {self.unit.get("name")!r}')
            step = self._get_step(range_step_string_parts)

            interval_values = self._apply_interval(range_list, step)  # filter by step
            if not len(interval_values):
                raise ValueError(f'Empty intervals value {cron_part}')
            intervals_values_list.append(interval_values)

        flattened_ranges_list = [item for sublist in intervals_values_list for item in sublist]
        flattened_ranges_list = list(dict.fromkeys(flattened_ranges_list))  # Remove eventual duplicates
        flattened_ranges_list.sort()
        self.values = flattened_ranges_list

    def _fix_sunday(self, values: List[int]) -> List[int]:
        """Replaces all 7 with 0 as Sunday can be represented by both.

         :param values: The values to process.
         :returns: values -> The resulting array.
         """
        if self.unit.get('name') == 'weekday':
            values = [0 if value == 7 else value for value in values]
        return values

    @staticmethod
    def _parse_range(unit_range: str) -> List[int]:
        """Parses a range string. Example: input="15-19" output=[15, 16, 17, 18, 19]

        :param unit_range: The range string.
        :return: The resulting array.
        :raise ValueError: Impossible to convert the Part unit as int.
        :raise ValueError: Invalid min or max value for the Part unit.
        :raise ValueError: Not valid Range, max range is less than min range
        """
        sub_parts = unit_range.split('-')
        if len(sub_parts) == 1:
            try:
                value = int(sub_parts[0])
            except ValueError as exc:
                raise ValueError(f'Invalid value {unit_range!r} --> {exc}')
            return [value]
        elif len(sub_parts) == 2:
            try:
                min_value = int(sub_parts[0])
                max_value = int(sub_parts[1])
            except ValueError as exc:
                raise ValueError(f'Invalid min or max value from: {unit_range!r} --> {exc}')
            if max_value < min_value:
                raise ValueError(f'Max range is less than min range in {unit_range}')
            return [int_value for int_value in range(min_value, max_value + 1)]
        else:
            raise ValueError(f'Invalid value {unit_range}')

    def _get_step(self, range_string_parts: List[str]) -> Union[None, int]:
        """Get the step part of the part string.

        :param range_string_parts: the part string of the current range.
        :return step: parsed step.
        :raise IndexError: The second index of the list does not exist. The step is not present.
        """
        try:
            step = range_string_parts[1]
        except IndexError:
            step = None

        if step or step == '':
            step = self._parse_step(step)

        return step

    def _parse_step(self, step: str) -> int:
        """Parses the step from a part string.

        :param step: The step string.
        :return: The step value.
        :raise ValueError: Invalid interval step value.
        """
        try:
            parsed_step = int(step)
        except (ValueError, TypeError):
            raise ValueError(f'Invalid interval step value {step!r} for {self.unit.get("name")!r}')
        if not parsed_step or parsed_step < 1:
            raise ValueError(f'Invalid interval step value {step!r} for {self.unit.get("name")!r}')
        return parsed_step

    @staticmethod
    def _apply_interval(values: List[int], step: int) -> List[int]:
        """Applies an interval step to a collection of values.

        :param values: A collection of numbers.
        :param step: The step value.
        :returns: The resulting collection.
        """
        if step:
            min_value = values[0]
            values = [value for value in values if value % step == min_value % step or value == min_value]
        return values

    def _replace_alternatives(self, string: str) -> str:
        """Replaces the alternative representations of numbers in a string.
        Example -> month 'dec' will be '12'

        :param string: The string to process.
        :return: The processed string.
        """
        if 'alt' in self.unit:
            string = string.upper()
            for idx, alt in enumerate(self.unit.get('alt')):
                string = string.replace(alt, str(self.unit.get("min") + idx))
        return string

    def out_of_range(self, values: List[int]) -> Union[int, None]:
        """Finds an element from values that is outside of the range of self.unit

        :param values: The values to test.
        :return: An integer is a value out of range was found, otherwise None.
        """
        first = values[0]
        last = values[-1]
        if first < self.unit.get('min'):
            return first
        elif last > self.unit.get('max'):
            return last
        else:
            return None

    def possible_values(self) -> List[int]:
        """Creates a list of Part Unit possible values from 'min' to 'max'

        :return: A List of Part Unit values
        """
        return list(range(self.unit.get('min'), self.unit.get('max') + 1))

    def min(self) -> int:
        """Returns the smallest value in the range.
        Example -> month Part: 1

        :return: The smallest Part value.
        """
        return self.values[0]

    def max(self) -> int:
        """Returns the largest value in the range.
        Example -> month Part: 12

        :return: The largest Part value.
        """
        return self.values[-1]

    def is_full(self) -> bool:
        """Returns true if range has all the values of the unit.
        """
        return len(self.values) == self.unit.get('max') - self.unit.get('min') + 1

    def get_step(self) -> Union[int, None]:
        """Returns the difference between first and second elements in the range.

        :return: step between numbers in the interval whether array interval > 2.
        """
        if self.values and len(self.values) > 2:
            step = self.values[1] - self.values[0]
            if step > 1:
                return step
        else:
            return None

    def is_interval(self, step: int) -> bool:
        """Returns true if the range can be represented as an interval.

        :param step: The difference between numbers in the interval.
        """
        for idx, value in enumerate(self.values):
            if self.values[0] == value:
                continue
            prev_value = self.values[idx - 1]
            current_value = value
            if current_value - prev_value != step:
                return False
        return True

    def is_full_interval(self, step: int) -> bool:
        """Returns true if the range contains all the interval values.

        :param step: The difference between numbers in the interval.
        """
        have_all_values = len(self.values) == round((self.max() - self.min()) / step) + 1
        if self.min() == self.unit.get('min') and self.max() + step > self.unit.get('max') and have_all_values:
            return True
        return False

    def has(self, value: int) -> bool:
        """Checks if the range contains the specified value.

        :param value: The value to look for.
        :return: Whether the value is present in the range or not.
        """
        try:
            self.values.index(value)
            return True
        except ValueError:
            return False

    def to_list(self) -> List[int]:
        """Returns the range as an array of positive integers.

        :return: The range as an array.
        """
        return self.values

    def to_ranges(self) -> List[List[Union[str, int]]]:
        """Returns the range as an array of ranges defined as arrays of positive integers.

        :return: multi_dim_values (list of list): The range as a multi-dimensional array.
        """
        multi_dim_values = list()
        start_number = None
        for idx, value in enumerate(self.values):
            try:
                next_value = self.values[idx + 1]
            except IndexError:
                next_value = -1  # No next item in the self.values list

            if value != next_value - 1:  # next_value is not the subsequent number
                if start_number is not None:
                    multi_dim_values.append([start_number, value])
                    start_number = None
                else:  # The last number of the list "self.values" is not in a range
                    multi_dim_values.append(value)
            elif start_number is None:
                start_number = value

        return multi_dim_values

    def to_string(self) -> str:
        """Returns the range as a string.

        :return: The range as a string.
        """
        cron_range_strings = []
        if self.is_full():
            if 'output_hashes' in self.options:
                cron_part_str = 'H'
            else:
                cron_part_str = '*'
        else:
            step = self.get_step()
            if step and self.is_interval(step):
                if self.is_full_interval(step):
                    if 'output_hashes' in self.options:
                        cron_part_str = f'H/{step}'
                    else:
                        cron_part_str = f'*/{step}'
                else:
                    if 'output_hashes' in self.options:
                        cron_part_str = f'H({self.format_value(self.min())}-{self.format_value(self.max())})/{step}'
                    else:
                        cron_part_str = f'{self.format_value(self.min())}-{self.format_value(self.max())}/{step}'
            else:
                cron_ranges = self.to_ranges()
                for cron_range in cron_ranges:
                    if isinstance(cron_range, list):
                        cron_range_strings.append(
                            f'{self.format_value(cron_range[0])}-{self.format_value(cron_range[1])}')
                    else:
                        cron_range_strings.append(f'{self.format_value(cron_range)}')

                if isinstance(cron_range_strings, list) and cron_range_strings:
                    cron_part_str = ','.join(cron_range_strings)
                else:
                    cron_part_str = cron_range_strings[0]

        return cron_part_str

    def format_value(self, value: int) -> Union[int, str]:
        """Formats weekday and month names as string when the relevant options are set.

        :param value: The value to process.
        :return: The formatted string or number.
        """
        if 'output_weekday_names' in self.options and self.options.get('output_weekday_names') and \
                self.unit.get('name') == 'weekday' or 'output_month_names' in self.options and \
                self.options.get('output_month_names') and self.unit.get('name') == 'month':
            return_value = self.unit.get("alt")[value - self.unit.get('min')]
        else:
            return_value = value
        return return_value

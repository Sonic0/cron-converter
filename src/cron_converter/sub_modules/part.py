from typing import List, Union


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

    """Print directly the Part Object"""
    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return f'{self.__class__.__name__} - (values:{self.values!r}, unit:{self.unit.get("name")!r})'

    """Validates a range of positive integers. 
    
    Args:
        range (list): An array of positive integers.
        
    Raises:
        ValueError: An error occurred in case of invalid value or out of range value
    """
    def from_list(self, arr: List[Union[str, int]]) -> None:
        values = []
        for value in arr:
            try:
                parsed_value = int(value)
            except ValueError:
                raise ValueError(f'Invalid list value {value}')
            if parsed_value is None:
                raise ValueError(f'Invalid list value {value}')
            values.append(parsed_value)

        if not values:
            raise ValueError('Empty interval value')

        sunday_fixed_values = self.fix_sunday(values)
        unique_values = list(dict.fromkeys(sunday_fixed_values))  # Remove eventual duplicates
        unique_values.sort()
        value = self.out_of_range(unique_values)
        if value is not None:
            raise ValueError(f'Value {value!r} out of range for {self.unit.get("name")!r}')

        self.values = unique_values

    """Parses a string as a range of positive integers.
     
    Args:
        cron_part (str): The string to be parsed as a range.
    
    Raises:
        ValueError: An error occurred in case of invalid value or out of range value
    """
    def from_string(self, cron_part: str) -> None:
        string_parts = cron_part.split('/')
        if len(string_parts) > 2:
            raise ValueError(f'Invalid value {cron_part}')

        range_string = self.replace_alternatives(string_parts[0])
        if not range_string:
            raise ValueError(f'Invalid value {range_string}')
        elif range_string == '*':
            unit_range = list(range(self.unit.get('min'), self.unit.get('max') + 1))
            parsed_values = [num for num in unit_range]
        else:
            ranges_lists = []
            for hour_range in range_string.split(','):
                ranges_lists.append(self.parse_range(hour_range))
            flattened_ranges_list = [item for sublist in ranges_lists for item in sublist]
            flattened_ranges_list = self.fix_sunday(flattened_ranges_list)
            parsed_values = list(dict.fromkeys(flattened_ranges_list))  # Remove eventual duplicates
            parsed_values.sort()
            value = self.out_of_range(parsed_values)
            if value is not None:
                raise ValueError(f'Value {value!r} out of range for {self.unit.get("name")!r}')

        step = self._get_step(string_parts)

        interval_values = self.apply_interval(parsed_values, step)  # filter by step
        if not len(interval_values):
            raise ValueError(f'Empty intervals value {cron_part}')

        self.values = interval_values

    """Replaces all 7 with 0 as Sunday can be represented by both.

     Args:
        values (list): The values to process.
     
     Returns:
        values (list) The resulting array.
     """
    def fix_sunday(self, values: List[int]) -> List[int]:
        if self.unit.get('name') == 'weekday':
            values = [0 if value == 7 else value for value in values]
        return values

    """Parses a range string.
    
    Args:
        unit_range (string): The range string.
        context (str): The operation context string.
    
    Returns:
        return (list): The resulting array.
    """
    def parse_range(self, unit_range: str):
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
            if max_value <= min_value:
                raise ValueError(f'Max range is less than min range in {unit_range}')
            return [int_value for int_value in range(min_value, max_value + 1)]
        else:
            raise ValueError(f'Invalid value {unit_range}')

    """Get the step part of the part string.
    
    Args:
        string_parts (str): the part string.

    Returns:
        step (int): parsed step.
    """
    def _get_step(self, string_parts) -> Union[None, int]:
        try:
            step = string_parts[1]
        except IndexError:
            step = None

        if step or step == '':
            step = self._parse_step(step)

        return step

    """Parses the step from a part string.
    
    Args:
        step (str): The step string.
    
    Returns:
        return (int) The step value.
    """
    def _parse_step(self, step: str) -> int:
        try:
            parsed_step = int(step)
        except (ValueError, TypeError):
            raise ValueError(f'Invalid interval step value {step!r} for {self.unit.get("name")!r}')
        if not parsed_step or parsed_step < 1:
            raise ValueError(f'Invalid interval step value {step!r} for {self.unit.get("name")!r}')
        return parsed_step

    """Applies an interval step to a collection of values.
    
    Args:
        values (list of ints): A collection of numbers.
        step (int): The step value.
    
    Returns:
        result (list): The resulting collection.
    """
    def apply_interval(self, values: List[int], step: int) -> List[int]:
        if step:
            min_value = values[0]
            values = [value for value in values if value % step == min_value % step or value == min_value]
        return values

    """Replaces the alternative representations of numbers in a string.
    
    Args:
        string (str): The string to process.
    
    Returns:
        return (str): The processed string.
    """
    def replace_alternatives(self, string: str) -> str:
        if 'alt' in self.unit:
            string = string.upper()
            for alt in self.unit.get('alt'):
                string = string.replace(alt,
                                        str(self.unit.get("min") + self.unit.get("alt").index(alt)))
        return string

    """Finds an element from values that is outside of the range of self.unit
    
    Args:
        values (list of int): The values to test.
    
    Returns:
        return (int or None): An integer is a value out of range was found, otherwise None.
    """
    def out_of_range(self, values: List[int]) -> Union[int, None]:
        first = values[0]
        last = values[-1]
        if first < self.unit.get('min'):
            return first
        elif last > self.unit.get('max'):
            return last
        else:
            return None

    """Returns the smallest value in the range.
    
    Returns:
        return (int): The smallest value.
    """
    def min(self) -> int:
        return self.values[0]

    """Returns the largest value in the range.
    
    Returns:
        return (int): The largest value.
    """
    def max(self) -> int:
        return self.values[-1]

    """Returns true if range has all the values of the unit.
    
    Returns:
        (boolean).
    """
    def is_full(self) -> bool:
        return len(self.values) == self.unit.get('max') - self.unit.get('min') + 1

    """Returns the difference between first and second elements in the range.
    
    Returns:
        return (int or None): step between numbers in the interval whether array interval > 2.
    """
    def get_step(self) -> Union[int, None]:
        if self.values and len(self.values) > 2:
            step = self.values[1] - self.values[0]
            if step > 1:
                return step
        else:
            return None

    """Returns true if the range can be represented as an interval.
    
    Args:
        step (int): The difference between numbers in the interval.
    
    Returns:
        return (bool): true/false.
    """
    def is_interval(self, step: int) -> bool:
        for value in self.values:
            if self.values[0] == value:
                continue
            prev_value = self.values[self.values.index(value) - 1]
            current_value = value
            if current_value - prev_value != step:
                return False
        return True

    """Returns true if the range contains all the interval values.
    
    Args:
        step (int): The difference between numbers in the interval.

    Returns:
        return (bool): true/false.
    """
    def is_full_interval(self, step: int) -> bool:
        have_all_values = len(self.values) == round((self.max() - self.min()) / step) + 1
        if self.min() == self.unit.get('min') and self.max() + step > self.unit.get('max') and have_all_values:
            return True
        return False

    """Checks if the range contains the specified value.
    
    Args:
        value (int): The value to look for.

    Returns:
        return (bool): Whether the value is present in the range.
    """
    def has(self, value: int) -> bool:
        try:
            self.values.index(value)
            return True
        except ValueError:
            return False

    """Returns the range as an array of positive integers.
    
    Returns:
        (self)values (list): The range as an array.
    """
    def to_list(self) -> List[int]:
        return self.values

    """Returns the range as an array of ranges defined as arrays of positive integers.

    Returns:
        multi_dim_values (list of list): The range as a multi-dimensional array.
    """
    def to_ranges(self):
        multi_dim_values = list()
        start_number = None
        for value in self.values:
            index = self.values.index(value)
            try:
                next_value = self.values[index + 1]
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

    """Returns the range as a string.

    Returns:
        return_value (string):The range as a string.
    """
    def to_string(self):
        cron_part_str = ''
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
                    # if 'output_hashes' in self.options:
                    #     cron_part_str = f'H/{step}'
                    # else:
                    cron_part_str = f'*/{step}'
                else:
                    # if 'output_hashes' in self.options:
                    #     cron_part_str = f'H({self.format_value(self.min())}-{self.format_value(self.max())})/{step}'
                    # else:
                    cron_part_str = f'{self.format_value(self.min())}-{self.format_value(self.max())}/{step}'
            else:
                cron_ranges = self.to_ranges()
                for cron_range in cron_ranges:
                    if isinstance(cron_range, list):
                        cron_range_strings.append(
                            f'{self.format_value(cron_range[0])}-{self.format_value(cron_range[1])}')
                    else:
                        cron_range_strings.append(f'{self.format_value(cron_range)}')

                if cron_range_strings and len(cron_range_strings) > 1:
                    cron_part_str = ','.join(cron_range_strings)
                else:
                    cron_part_str = cron_range_strings[0]

        return cron_part_str

    """Formats weekday and month names as string when the relevant options are set.
    
    Args:
        value (int): The value to process.
    
    Returns:
        return_value: (int or string): The formatted string or number.
    """
    def format_value(self, value: int) -> Union[int, str]:
        if 'output_weekday_names' in self.options and self.options.get('output_weekday_names') and \
                self.unit.get('name') == 'weekday' or 'output_month_names' in self.options and \
                self.options.get('output_month_names') and self.unit.get('name') == 'month':
            return_value = self.unit.get("alt")[value - self.unit.get('min')]
        else:
            return_value = value
        return return_value

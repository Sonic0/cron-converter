import unittest

from fixtures.invalid_ranges import invalid_ranges

from cron_converter.sub_modules.part import Part
from cron_converter.sub_modules.units import units


class PartTestInvalid(unittest.TestCase):

    def test_from_string_invalid_0(self):
        for invalid_range in invalid_ranges:
            with self.subTest(range=invalid_range):
                part = Part(units[invalid_range['unit']], {})
                with self.assertRaises(ValueError, msg=invalid_range['error']):
                    part.from_string(invalid_range['input'])

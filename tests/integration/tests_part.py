import unittest

from fixtures.valid_ranges import valid_ranges

from cron_converter.sub_modules.part import Part
from cron_converter.sub_modules.units import units


class PartTest(unittest.TestCase):

    def test_from_string_to_list(self):
        for valid_range in valid_ranges:
            with self.subTest(range=valid_range):
                part = Part(units[valid_range['unit']], {})
                part.from_string(valid_range['input'])
                self.assertEqual(part.to_list(), valid_range['arr'], 'Failed converting Part to list')

    def test_from_string_to_string(self):
        for valid_range in valid_ranges:
            with self.subTest(range=valid_range):
                part = Part(units[valid_range['unit']], {})
                part.from_string(valid_range['input'])
                self.assertEqual(part.to_string(), valid_range['output'], 'Failed converting Part to string')

    def test_from_list_to_list(self):
        for valid_range in valid_ranges:
            with self.subTest(range=valid_range):
                part = Part(units[valid_range['unit']], {})
                part.from_list(valid_range['arr'])
                self.assertEqual(part.to_list(), valid_range['arr'], 'Failed converting Part to list')

    def test_from_list_to_string(self):
        for valid_range in valid_ranges:
            with self.subTest(range=valid_range):
                part = Part(units[valid_range['unit']], {})
                part.from_list(valid_range['arr'])
                self.assertEqual(part.to_string(), valid_range['output'], 'Failed converting Part to string')

import unittest
from part import Part
from units import units

from tests.statics.valid_ranges import valid_ranges


class PartTest(unittest.TestCase):

    def test_min(self):
        part = Part(units[0], {})
        part.values = [1, 12]
        self.assertEqual(part.min(), 1)
        part = Part(units[1], {})
        part.values = [12, 23]
        self.assertEqual(part.min(), 12)

    def test_get_step(self):
        part = Part(units[0], {})
        part.values = [2, 5, 8, 11]
        self.assertEqual(part.get_step(), 3, "The result has to be 3")
        part.values = [1, 6, 11]
        self.assertEqual(part.get_step(), 5, "The result has to be 5")

    def test_is_interval(self):
        part = Part(units[0], {})
        part.values = [2, 5, 8, 11]
        self.assertTrue(part.is_interval(3), "The interval does not contain a stepped range of minutes")

    def test_has(self):
        part = Part(units[0], {})
        part.values = [2, 5, 8, 11]
        self.assertTrue(part.has(5), "The interval does not contain the specified value")

    def test_to_ranges(self):
        part = Part(units[0], {})
        part.values = [0]
        self.assertEqual(part.to_ranges(), [0], "Wrong multi-dimensional list as return")
        part.values = [0, 1, 2, 3, 4]
        self.assertEqual(part.to_ranges(), [[0, 4]], "Wrong multi-dimensional list as return")
        part.values = [2, 3, 4, 6, 7]
        self.assertEqual(part.to_ranges(), [[2, 4], [6, 7]], "Wrong multi-dimensional list as return")
        part.values = [2, 3, 4, 6, 7, 59]
        self.assertEqual(part.to_ranges(), [[2, 4], [6, 7], 59], "Wrong multi-dimensional list as return")
        part.values = [20, 21, 22, 28, 29, 31, 41, 59]
        self.assertEqual(part.to_ranges(), [[20, 22], [28, 29], 31, 41, 59], "Wrong multi-dimensional list as return")

    def test_format_value(self):
        part = Part(units[3], {'output_weekday_names': True, 'output_month_names': True})
        self.assertEqual(part.format_value(5), "MAY")
        part = Part(units[4], {'output_weekday_names': True, 'output_month_names': True})
        self.assertEqual(part.format_value(5), 'FRI')

    def test_is_full_interval(self):
        part = Part(units[3], {})
        part.values = [1, 3, 6, 9, 12]  # JAN, MAR, JUN, SEP, DEC
        self.assertTrue(part.is_full_interval(3), 'The interval does not contain all stepped months of the year')
        part = Part(units[4], {})
        part.values = [0, 2, 4, 6]  # SUN, TUE, THU, SAT
        self.assertTrue(part.is_full_interval(2), 'The interval does not contain all stepped days of the week')

    def test_fix_sunday(self):
        part = Part(units[4], {})
        result = part.fix_sunday([7])
        self.assertEqual(result, [0], 'Fail!')

    def test_parse_range(self):
        part = Part(units[4], {})
        result = part.parse_range('0')
        self.assertEqual(result, [0], 'Fail parsing a non range string')
        # test SUN to FRI
        result = part.parse_range('0-5')
        self.assertEqual(result, [0, 1, 2, 3, 4, 5], 'Fail parsing range')

    def test_parse_step(self):
        part = Part(units[4], {})
        self.assertEqual(part.parse_step('5'), 5, 'Fail parsing step')

    def test_apply_interval(self):
        part = Part(units[4], {})
        result = part.apply_interval([2, 3, 4, 5, 6], 3)
        self.assertEqual(result, [2, 5])

    def test_replace_alternatives(self):
        part = Part(units[3], {})
        self.assertEqual(part.replace_alternatives('sep'), '9', 'The correspondent number of month does not match')

    def test_from_string(self):
        for valid_range in valid_ranges:
            with self.subTest(range=valid_range):
                part = Part(units[valid_range['unit']], {})
                part.from_string(valid_range['input'])
                self.assertEqual(part.to_list(), valid_range['arr'], 'Failed converting Part to list')

            with self.subTest(range=valid_range):
                part = Part(units[valid_range['unit']], {})
                part.from_string(valid_range['input'])
                self.assertEqual(part.to_string(), valid_range['output'], 'Failed converting Part to string')


if __name__ == "__main__":
    unittest.main()

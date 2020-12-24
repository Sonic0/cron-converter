import unittest
from part import Part
from units import units

from tests.statics.invalid_ranges import invalid_ranges


class PartTestInvalid(unittest.TestCase):
    @unittest.expectedFailure
    def test_from_string_invalid_0(self):
        part = Part(units[invalid_ranges[0]['unit']], {})
        self.assertRaises(ValueError, part.from_string(invalid_ranges[0]['input']))

    @unittest.expectedFailure
    def test_from_string_invalid_1(self):
        part = Part(units[invalid_ranges[1]['unit']], {})
        self.assertRaises(ValueError, part.from_string(invalid_ranges[1]['input']))

    @unittest.expectedFailure
    def test_from_string_invalid_2(self):
        part = Part(units[invalid_ranges[2]['unit']], {})
        self.assertRaises(ValueError, part.from_string(invalid_ranges[2]['input']))

    @unittest.expectedFailure
    def test_from_string_invalid_3(self):
        part = Part(units[invalid_ranges[3]['unit']], {})
        self.assertRaises(ValueError, part.from_string(invalid_ranges[3]['input']))

    @unittest.expectedFailure
    def test_from_string_invalid_4(self):
        part = Part(units[invalid_ranges[4]['unit']], {})
        self.assertRaises(ValueError, part.from_string(invalid_ranges[4]['input']))

    @unittest.expectedFailure
    def test_from_string_invalid_5(self):
        part = Part(units[invalid_ranges[5]['unit']], {})
        self.assertRaises(ValueError, part.from_string(invalid_ranges[5]['input']))


if __name__ == "__main__":
    unittest.main()

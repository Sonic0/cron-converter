import unittest
from datetime import date, datetime

import cron_converter.sub_modules.utils as utils


class UtilsTest(unittest.TestCase):

    def test_to_parts(self):
        today_d = date(day=20, month=5, year=2024)
        self.assertEqual(utils.to_parts(today_d), [None, None, 20, 5, 1], "The result has to be True")
        today_dt = datetime(minute=20, hour=23, day=20, month=5, year=2024)
        self.assertEqual(utils.to_parts(today_dt), [20, 23, 20, 5, 1], "The result has to be True")

    def test_iso_to_cron_weekday(self):
        iso_weekdays = range(1, 7+1, 1)
        cron_weekdays = []
        for iso_weekday in iso_weekdays:
            cron_weekdays.append(utils.iso_to_cron_weekday(iso_weekday))
        self.assertListEqual(cron_weekdays, [1, 2, 3, 4, 5, 6, 0], "The result has to be a range from 0 to 6")

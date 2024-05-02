import unittest
from datetime import date, datetime

from cron_converter.cron import Cron, Seeker


class SeekerTest(unittest.TestCase):

    def test_input_datetime_not_changed(self):
        cron = Cron('* * * * *')
        seeker = Seeker(cron, datetime(2023, 1, 3, 15, 17, 0))
        self.assertEqual(datetime(2023, 1, 3, 15, 17), seeker.start_time)
        seeker = Seeker(cron, datetime(2023, 1, 3, 15, 17, 0, 900))
        self.assertEqual(datetime(2023, 1, 3, 15, 17, 0, 900), seeker.start_time)

    def test_reset(self):
        cron = Cron('* * * * *')
        seeker = Seeker(cron, datetime(2023, 1, 3, 15, 17, 0))
        self.assertEqual(datetime(2023, 1, 3, 15, 17, ), seeker.next())
        self.assertEqual(datetime(2023, 1, 3, 15, 18, ), seeker.next())
        self.assertEqual(datetime(2023, 1, 3, 15, 19,), seeker.next())
        seeker.reset()
        self.assertEqual(datetime(2023, 1, 3, 15, 17), seeker.start_time)
        self.assertEqual(datetime(2023, 1, 3, 15, 17), seeker.next())

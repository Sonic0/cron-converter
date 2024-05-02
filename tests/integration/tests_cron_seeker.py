import logging
import sys
import unittest
from datetime import datetime

from dateutil import tz
from fixtures.valid_schedule_date import valid_schedules, valid_schedules_timezone

from cron_converter.cron import Cron

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger("TestLog")


class SeekerTest(unittest.TestCase):

    def test_prev(self):
        for valid_schedule in valid_schedules:
            with self.subTest(range=valid_schedule):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))
                self.assertEqual(schedule.prev().isoformat(), valid_schedule['prev'],
                                 'Failed seeking the previous schedule date')

    def test_prev_of_prev(self):
        for valid_schedule in valid_schedules:
            with self.subTest(range=valid_schedule):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))
                schedule.prev()
                self.assertEqual(schedule.prev().isoformat(), valid_schedule['prev_prev'],
                                 'Failed seeking the prev prev schedule date')

    def test_next(self):
        for valid_schedule in valid_schedules:
            with self.subTest(range=valid_schedule):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))
                self.assertEqual(schedule.next().isoformat(), valid_schedule['next'],
                                 'Failed seeking the next schedule date')

    def test_next_of_next(self):
        for valid_schedule in valid_schedules:
            with self.subTest(range=valid_schedule):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))
                schedule.next()
                self.assertEqual(schedule.next().isoformat(), valid_schedule['next_next'],
                                 'Failed seeking the next next schedule date')

    def test_timezone(self):
        for valid_schedule in valid_schedules_timezone:
            with self.subTest(range=valid_schedule):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(timezone_str=valid_schedule['timezone'])
                self.assertTrue(schedule.next().utcoffset().seconds ==
                                datetime.now(tz=tz.gettz(valid_schedule['timezone'])).utcoffset().seconds,
                                'Timezones does not match')

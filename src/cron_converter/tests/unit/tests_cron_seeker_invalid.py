import unittest
from datetime import datetime

from src.cron_converter.cron import Cron

from tests.data.invalid_schedule_date import invalid_schedules


class SeekerTestInvalid(unittest.TestCase):
    def test_invalid_cron_date(self):
        with self.assertRaises(invalid_schedules[0]['error'], msg=invalid_schedules[0]['message']):
            cron = Cron()
            cron.from_string(invalid_schedules[0]['schedule'])
            schedule = cron.schedule(datetime.fromisoformat(invalid_schedules[0]['now']))
            schedule.next()

    def test_invalid_schedule(self):
        with self.assertRaises(invalid_schedules[1]['error'], msg=invalid_schedules[1]['message']):
            cron = Cron()
            cron.from_string(invalid_schedules[1]['schedule'])
            schedule = cron.schedule(invalid_schedules[1]['now'])
            schedule.next()

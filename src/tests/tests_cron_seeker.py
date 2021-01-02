import unittest
from datetime import datetime

from cron import Cron

from tests.statics.valid_schedule_date import valid_schedules


class SeekerTest(unittest.TestCase):

    def test_prev(self):
        for valid_schedule in valid_schedules:
            with self.subTest(range=valid_schedule):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))
                self.assertEqual(schedule.prev().isoformat(), valid_schedule['prev'], 'Failed seeking the previous schedule date')

    def test_next(self):
        for valid_schedule in valid_schedules:
            with self.subTest(range=valid_schedule):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))
                self.assertEqual(schedule.next().isoformat(), valid_schedule['next'], 'Failed seeking the next schedule date')
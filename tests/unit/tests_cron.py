import unittest

from cron_converter.cron import Cron


class CronTest(unittest.TestCase):

    def test_to_string(self):
        cron = Cron('*/5 9-17/2 * 1-3 1-5')
        self.assertEqual('*/5 9-17/2 * 1-3 1-5', cron.to_string())

    def test_to_string_output_weekday_names(self):
        cron = Cron('*/5 9-17/2 * 1-3 1-5', {'output_weekday_names': True})
        self.assertEqual('*/5 9-17/2 * 1-3 MON-FRI', cron.to_string())

    def test_to_string_output_month_names(self):
        cron = Cron('*/5 9-17/2 * 1-3 1-5', {'output_month_names': True})
        self.assertEqual('*/5 9-17/2 * JAN-MAR 1-5', cron.to_string())

    def test_to_string_hashes(self):
        cron = Cron('*/5 9-17/2 * 1-3 1-5', {'output_hashes': True})
        self.assertEqual('H/5 H(9-17)/2 H 1-3 1-5', cron.to_string())

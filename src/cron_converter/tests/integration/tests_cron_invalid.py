import unittest

from src.cron_converter.cron import Cron

from fixtures.invalid_crons import invalid_crons


class CronTestInvalid(unittest.TestCase):

    def test_from_string(self):
        for invalid_cron in invalid_crons:
            with self.subTest(range=invalid_cron):
                with self.assertRaises(invalid_cron['error'], msg=invalid_cron['message']):
                    cron = Cron()
                    cron.from_string(invalid_cron['string'])

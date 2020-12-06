import unittest

from cron import Cron

from tests.statics.valid_crons import valid_crons_string, valid_crons_to_list


class CronTest(unittest.TestCase):

    def test_to_string(self):
        for valid_cron in valid_crons_string:
            with self.subTest(range=valid_cron):
                cron = Cron()
                cron.from_string(valid_cron['in'])
                self.assertEqual(cron.to_string(), valid_cron['out'], 'Failed parsing cron string')

    def test_to_list(self):
        for valid_cron in valid_crons_to_list:
            with self.subTest(range=valid_cron):
                cron = Cron()
                cron.from_string(valid_cron['in'])
                self.assertEqual(cron.to_list(), valid_cron['out'], 'Failed parsing cron string')

import unittest

from src.cron_converter.cron import Cron

from tests.data.valid_crons import valid_crons_string, valid_crons_to_list, valid_crons_list


class CronTest(unittest.TestCase):

    def test_from_string_to_string(self):
        for valid_cron in valid_crons_string:
            with self.subTest(range=valid_cron):
                cron = Cron()
                cron.from_string(valid_cron['in'])
                self.assertEqual(cron.to_string(), valid_cron['out'], 'Failed parsing cron string')

    def test_from_string_to_list(self):
        for valid_cron in valid_crons_to_list:
            with self.subTest(range=valid_cron):
                cron = Cron()
                cron.from_string(valid_cron['in'])
                self.assertEqual(cron.to_list(), valid_cron['out'], 'Failed parsing cron string')

    def test_from_list_to_string(self):
        for valid_cron in valid_crons_list:
            with self.subTest(range=valid_cron):
                cron = Cron()
                cron.from_list(valid_cron['in'])
                self.assertEqual(cron.to_string(), valid_cron['out'], 'Failed parsing cron list')

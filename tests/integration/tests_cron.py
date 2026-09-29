import unittest
from datetime import datetime

from cron_converter.cron import Cron
from tests.integration.fixtures.valid_crons import (
    valid_crons_list,
    valid_crons_string,
    valid_crons_to_list,
)


class CronTest(unittest.TestCase):

    def test_replacing_schedule(self):
        original = Cron('0 12 * * *')
        replacement = Cron('30 8 * * *')
        for initial_method in ('from_string', 'from_list'):
            for replacement_method in ('from_string', 'from_list'):
                with self.subTest(initial=initial_method, replacement=replacement_method):
                    cron = Cron()
                    initial_value = original.to_string() if initial_method == 'from_string' else original.to_list()
                    getattr(cron, initial_method)(initial_value)
                    replacement_value = (
                        replacement.to_string() if replacement_method == 'from_string' else replacement.to_list()
                    )
                    getattr(cron, replacement_method)(replacement_value)

                    self.assertEqual(cron.to_string(), '30 8 * * *')
                    self.assertEqual(cron.to_list(), replacement.to_list())
                    self.assertTrue(cron.validate(datetime(2026, 9, 29, 8, 30)))
                    self.assertFalse(cron.validate(datetime(2026, 9, 29, 12)))
                    self.assertEqual(
                        cron.schedule(datetime(2026, 9, 29)).next(),
                        datetime(2026, 9, 29, 8, 30),
                    )

    def test_rejected_replacement_preserves_schedule(self):
        for method, value in (('from_string', '15 24 * * *'), ('from_list', [[15], [24], [1], [1], [0]])):
            with self.subTest(method=method):
                cron = Cron('0 12 * * *')
                with self.assertRaises(ValueError):
                    getattr(cron, method)(value)

                self.assertEqual(cron.to_string(), '0 12 * * *')
                self.assertEqual(
                    cron.schedule(datetime(2026, 9, 29)).next(),
                    datetime(2026, 9, 29, 12),
                )

    def test_rejected_import_keeps_empty_schedule(self):
        for method, value in (('from_string', '15 24 * * *'), ('from_list', [[15], [24], [1], [1], [0]])):
            with self.subTest(method=method):
                cron = Cron()
                with self.assertRaises(ValueError):
                    getattr(cron, method)(value)

                with self.assertRaises(LookupError):
                    cron.to_list()
                with self.assertRaises(LookupError):
                    cron.schedule(datetime(2026, 9, 29))
                cron.from_string('0 12 * * *')
                self.assertEqual(cron.to_string(), '0 12 * * *')

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

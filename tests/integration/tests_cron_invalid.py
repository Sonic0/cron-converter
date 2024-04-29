import unittest

from fixtures.invalid_crons import invalid_crons

from cron_converter.cron import Cron


class CronTestInvalid(unittest.TestCase):

    def test_from_string(self):
        for invalid_cron in invalid_crons:
            with self.subTest(range=invalid_cron):
                with self.assertRaises(invalid_cron['error']) as error:
                    cron = Cron()
                    cron.from_string(invalid_cron['string'])
                self.assertEqual(str(error.exception), invalid_cron['message'])

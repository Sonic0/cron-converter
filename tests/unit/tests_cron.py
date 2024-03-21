import unittest
from datetime import datetime, date

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

    def test_to_string_equal_min_max_range(self):
        cron = Cron('* * * * 1-1', {'output_weekday_names': True})
        self.assertEqual('* * * * MON', cron.to_string())

    def test_eq_hour(self):
        self.assertEqual(Cron('0 1 * * 1-5'), Cron('0 2 * * 1-5'))

    def test_gt_hour(self):
        self.assertTrue(Cron('0 1,15 * * 1-5') > Cron('0 2 * * 1-5'))
        self.assertTrue(Cron('0 1-15 * * 1-5') > Cron('0 1-14 * * 1-5'))
        self.assertTrue(Cron('0 1,2,3 * * 1-5') > Cron('0 1,23 * * 1-5'))

    def test_eq_minute(self):
        self.assertEqual(Cron('* 1 * * 1-5'), Cron('0-59 1 * * 1-5'))
        self.assertEqual(Cron('* 1 * * 1-5'), Cron('* 1 * * 1-5'))
        self.assertEqual(Cron('23 1 * * 1-5'), Cron('32 1 * * 1-5'))

    def test_gt_minute(self):
        self.assertTrue(Cron('1-30 1 * * 1-5') > Cron('1-29 1 * * 1-5'))
        self.assertTrue(Cron('* 1 * * 1-5') > Cron('0-58 1 * * 1-5'))

    def test_eq_day(self):
        self.assertEqual(Cron('* 1 1 * 1-5'), Cron('0-59 1 2 * 1-5'))

    def test_gt_day(self):
        self.assertTrue(Cron('* 1 1,2 * 1-5') > Cron('* 1 6 * 1-5'))

    def test_eq_month(self):
        self.assertEqual(Cron('* 1 1 11 1-5'), Cron('* 1 1 1 1-5'))

    def test_gt_month(self):
        self.assertTrue(Cron('* 1 6 * 1-5') > Cron('* 1 6 1 1-5'))
        self.assertTrue(Cron('* 1 6 1-2 1-5') > Cron('* 1 6 1 1-5'))

    def test_eq_weekday(self):
        self.assertEqual(Cron('* 1 1 11 *'), Cron('* 1 1 11 0-6'))
        self.assertEqual(Cron('* 1 1 11 1'), Cron('* 1 1 11 5'))

    def test_gt_weekday(self):
        self.assertTrue(Cron('* 1 6 * 1-5') > Cron('* 1 6 * 1-4'))
        self.assertTrue(Cron('* 1 6 1 *') > Cron('* 1 6 1 1-5'))

    def test_datetime_is_valid_cron(self):
        self.assertTrue(Cron('* * * * *').validate(datetime.now()))
        self.assertTrue(Cron('10 * * * *').validate(datetime(2022, 1, 1, 9, 10)))
        self.assertTrue(Cron('* 10 * * *').validate(datetime(2022, 1, 1, 10, 9)))
        self.assertTrue(Cron('* * 10 * *').validate(datetime(2022, 1, 10, 1, 9)))
        self.assertTrue(Cron('* * * 10 *').validate(datetime(2022, 10, 1, 1, 9)))
        # 2024-03-19 is a Tuesday
        self.assertTrue(Cron('* * * * 1').validate(datetime(2024, 3, 19, 1, 9)))
        self.assertTrue(Cron('9 1 19 3 1').validate(datetime(2024, 3, 19, 1, 9)))
        self.assertTrue(Cron('* 1 19 3 1').validate(datetime(2024, 3, 19, 1, 55)))
        self.assertTrue(
            Cron('*/5 9-17/2 * 1-3 1-5').validate(datetime(2024, 3, 19, 15, 55)))

    def test_date_object_in_cron(self):
        self.assertTrue((date.today()) in Cron('* * * * *'))
        self.assertTrue((datetime(2022, 1, 1, 1, 10)) in Cron('10 * * * *'))
        self.assertFalse((datetime(2022, 1, 1)) in Cron('10 * * * *'))
        self.assertTrue(date(2022, 1, 1) in (Cron('* 10 * * *')))
        # 2024-03-19 is a Tuesday
        self.assertTrue((date(2024, 3, 19)) in Cron('* * * * 1'))
        self.assertTrue((date(2024, 3, 19)) in Cron('9 1 19 3 1'))
        self.assertTrue((datetime(2024, 3, 19, 1, 55)) in Cron('* 1 19 3 1'))
        self.assertFalse((datetime(2024, 4, 19, 1, 55)) in Cron('* 1 19 3 1'))
        self.assertTrue((datetime(2024, 3, 19, 15, 55) in Cron('*/5 9-17/2 * 1-3 1-5')))

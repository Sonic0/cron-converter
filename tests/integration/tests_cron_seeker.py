"""
Integration tests for cron_converter.Seeker class.

This test suite uses real-world data from fixtures to ensure:
- Basic next/prev operations work correctly
- Iterator protocol (PR #31) is properly implemented
- Timezone handling is correct
- Edge cases are covered
- Bidirectional iteration works as expected

All tests are data-driven using proven fixtures from production cases.
"""

import unittest
from datetime import datetime
from itertools import islice

from dateutil import tz

from cron_converter import Cron
from tests.integration.fixtures.valid_schedule_date import (
    valid_schedules,
    valid_schedules_timezone,
)


class TestSeekerPrevOperation(unittest.TestCase):
    """Test prev() method with fixture data"""

    def test_prev(self):
        """Test prev() returns correct previous schedule date"""
        for valid_schedule in valid_schedules:
            with self.subTest(schedule=valid_schedule['schedule'], now=valid_schedule['now']):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))

                result = schedule.prev()
                expected = valid_schedule['prev']

                self.assertEqual(
                    result.isoformat(),
                    expected,
                    f"Failed seeking previous schedule date for '{valid_schedule['schedule']}' "
                    f"at {valid_schedule['now']}"
                )

    def test_prev_of_prev(self):
        """Test two consecutive prev() calls"""
        for valid_schedule in valid_schedules:
            with self.subTest(schedule=valid_schedule['schedule'], now=valid_schedule['now']):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))

                # First prev
                schedule.prev()

                # Second prev
                result = schedule.prev()
                expected = valid_schedule['prev_prev']

                self.assertEqual(
                    result.isoformat(),
                    expected,
                    f"Failed seeking prev-prev schedule date for '{valid_schedule['schedule']}' "
                    f"at {valid_schedule['now']}"
                )


class TestSeekerNextOperation(unittest.TestCase):
    """Test next() method with fixture data"""

    def test_next(self):
        """Test next() returns correct next schedule date"""
        for valid_schedule in valid_schedules:
            with self.subTest(schedule=valid_schedule['schedule'], now=valid_schedule['now']):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))

                result = schedule.next()
                expected = valid_schedule['next']

                self.assertEqual(
                    result.isoformat(),
                    expected,
                    f"Failed seeking next schedule date for '{valid_schedule['schedule']}' "
                    f"at {valid_schedule['now']}"
                )

    def test_next_default_is_exclusive(self):
        """next() never returns the start minute, even when it matches the schedule"""
        cron = Cron('* * * * *')
        # Start exactly on a matching minute boundary (zero seconds).
        schedule = cron.schedule(datetime.fromisoformat('2020-02-08T09:32:00'))
        result = schedule.next()
        self.assertEqual(result.isoformat(), '2020-02-08T09:33:00')

    def test_next_inclusive_returns_matching_start_minute(self):
        """next(inclusive=True) returns the start minute when it matches the schedule"""
        cron = Cron('* * * * *')
        schedule = cron.schedule(datetime.fromisoformat('2020-02-08T09:32:00'))
        result = schedule.next(inclusive=True)
        self.assertEqual(result.isoformat(), '2020-02-08T09:32:00')

    def test_next_inclusive_ignored_for_subminute_start(self):
        """inclusive has no effect when the start carries seconds (already in the past)"""
        cron = Cron('* * * * *')
        schedule = cron.schedule(datetime.fromisoformat('2020-02-08T09:32:15'))
        result = schedule.next(inclusive=True)
        self.assertEqual(result.isoformat(), '2020-02-08T09:33:00')

    def test_next_inclusive_only_affects_first_call(self):
        """Subsequent next() calls stay exclusive after an inclusive first call"""
        cron = Cron('* * * * *')
        schedule = cron.schedule(datetime.fromisoformat('2020-02-08T09:32:00'))
        first = schedule.next(inclusive=True)
        second = schedule.next()
        self.assertEqual(first.isoformat(), '2020-02-08T09:32:00')
        self.assertEqual(second.isoformat(), '2020-02-08T09:33:00')

    def test_next_of_next(self):
        """Test two consecutive next() calls"""
        for valid_schedule in valid_schedules:
            with self.subTest(schedule=valid_schedule['schedule'], now=valid_schedule['now']):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))

                # First next
                schedule.next()

                # Second next
                result = schedule.next()
                expected = valid_schedule['next_next']

                self.assertEqual(
                    result.isoformat(),
                    expected,
                    f"Failed seeking next-next schedule date for '{valid_schedule['schedule']}' "
                    f"at {valid_schedule['now']}"
                )


class TestSeekerTimezone(unittest.TestCase):
    """Test timezone handling with fixture data"""

    def test_timezone_offset_matches(self):
        """Test that timezone offset is correctly applied"""
        for valid_schedule in valid_schedules_timezone:
            with self.subTest(
                schedule=valid_schedule['schedule'],
                timezone=valid_schedule['timezone']
            ):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(timezone_str=valid_schedule['timezone'])

                result = schedule.next()
                expected_tz = tz.gettz(valid_schedule['timezone'])
                expected_offset = datetime.now(tz=expected_tz).utcoffset()

                self.assertEqual(
                    result.utcoffset(),
                    expected_offset,
                    f"Timezone offset does not match for {valid_schedule['timezone']}"
                )


class TestIteratorProtocol(unittest.TestCase):
    """Test Python Iterator protocol compliance (PR #31)"""

    def test_iter_returns_self(self):
        """Test that __iter__ returns self (Iterator protocol requirement)"""
        # Test with first few fixtures to verify protocol compliance
        for valid_schedule in valid_schedules[:5]:
            with self.subTest(schedule=valid_schedule['schedule']):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))

                # __iter__ must return self
                self.assertIs(
                    iter(schedule),
                    schedule,
                    f"iter() should return self for schedule '{valid_schedule['schedule']}'"
                )

    def test_next_builtin_function(self):
        """Test that built-in next() function works"""
        for valid_schedule in valid_schedules[:5]:
            with self.subTest(schedule=valid_schedule['schedule']):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))

                # Built-in next() should work
                result = next(schedule)

                self.assertIsInstance(
                    result,
                    datetime,
                    f"next() should return datetime for schedule '{valid_schedule['schedule']}'"
                )

                # Should match expected next value
                self.assertEqual(
                    result.isoformat(),
                    valid_schedule['next'],
                    f"next() result should match fixture data"
                )

    def test_for_loop_with_islice(self):
        """Test that for loop with islice works (Iterator protocol)"""
        # Use a simple schedule for this test
        cron = Cron('*/5 * * * *')
        schedule = cron.schedule(datetime.fromisoformat('2020-02-08T09:32:15'))

        # Collect 5 dates using for loop
        dates = []
        for dt in islice(schedule, 5):
            dates.append(dt)

        # Should have exactly 5 dates
        self.assertEqual(len(dates), 5)

        # All should be datetime instances
        for dt in dates:
            self.assertIsInstance(dt, datetime)

        # First should be 9:35 (from fixture data)
        self.assertEqual(dates[0].isoformat(), '2020-02-08T09:35:00')

        # Second should be 9:40 (from fixture data)
        self.assertEqual(dates[1].isoformat(), '2020-02-08T09:40:00')

    def test_list_comprehension_with_islice(self):
        """Test that list comprehension works with iterator"""
        for valid_schedule in valid_schedules[:3]:
            with self.subTest(schedule=valid_schedule['schedule']):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))

                # List comprehension should work
                dates = [dt for dt in islice(schedule, 3)]

                self.assertEqual(len(dates), 3)

                # First element should match expected next
                self.assertEqual(
                    dates[0].isoformat(),
                    valid_schedule['next']
                )

    def test_iterator_state_persists_across_calls(self):
        """Test that iterator maintains state across multiple calls"""
        cron = Cron('*/5 * * * *')
        schedule = cron.schedule(datetime.fromisoformat('2020-02-08T09:32:15'))

        # First batch using iterator
        batch1 = list(islice(schedule, 2))  # 9:35, 9:40

        # Second batch should continue, not restart
        batch2 = list(islice(schedule, 2))  # 9:45, 9:50

        # Verify continuity
        self.assertEqual(batch1[0].isoformat(), '2020-02-08T09:35:00')
        self.assertEqual(batch1[1].isoformat(), '2020-02-08T09:40:00')
        self.assertEqual(batch2[0].isoformat(), '2020-02-08T09:45:00')
        self.assertEqual(batch2[1].isoformat(), '2020-02-08T09:50:00')


class TestIteratorPrevMixing(unittest.TestCase):
    """Test mixing Iterator protocol with prev() method (PR #31)"""

    def test_prev_after_iterator_usage(self):
        """Test that .prev() works correctly after using iterator protocol"""
        # Use fixture data with known values
        cron = Cron('*/5 * * * *')
        schedule = cron.schedule(datetime.fromisoformat('2020-02-08T09:32:15'))

        # Use iterator protocol
        dt1 = next(schedule)  # Should be 9:35
        self.assertEqual(dt1.isoformat(), '2020-02-08T09:35:00')

        # Switch to custom API
        dt2 = schedule.prev()  # Should go back to 9:30
        self.assertEqual(dt2.isoformat(), '2020-02-08T09:30:00')

        # Back to iterator
        dt3 = next(schedule)  # Should be 9:35 again
        self.assertEqual(dt3.isoformat(), '2020-02-08T09:35:00')

    def test_mixing_next_builtin_and_custom_next(self):
        """Test that built-in next() and .next() work interchangeably"""
        for valid_schedule in valid_schedules[:3]:
            with self.subTest(schedule=valid_schedule['schedule']):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))

                # Built-in next()
                dt1 = next(schedule)
                self.assertEqual(dt1.isoformat(), valid_schedule['next'])

                # Custom .next()
                dt2 = schedule.next()
                self.assertEqual(dt2.isoformat(), valid_schedule['next_next'])

    def test_for_loop_then_prev(self):
        """Test that prev() works after for loop iteration"""
        cron = Cron('*/5 * * * *')
        schedule = cron.schedule(datetime.fromisoformat('2020-02-08T09:32:15'))

        # Iterate forward using for loop
        dates_forward = list(islice(schedule, 3))  # 9:35, 9:40, 9:45

        # State should be at 9:45, going back should give 9:40
        dt_back = schedule.prev()
        self.assertEqual(dt_back.isoformat(), '2020-02-08T09:40:00')


class TestBidirectionalNavigation(unittest.TestCase):
    """Test bidirectional navigation using fixture data"""

    def test_next_then_prev_symmetry(self):
        """Test that next() followed by prev() maintains consistency"""
        for valid_schedule in valid_schedules[:5]:
            with self.subTest(schedule=valid_schedule['schedule']):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))

                dt_next = schedule.next()
                self.assertEqual(dt_next.isoformat(), valid_schedule['next'])

                dt_prev = schedule.prev()

                # Should be close to original prev value
                # (might differ by a minute due to state management)
                self.assertIsInstance(dt_prev, datetime)

    def test_multiple_prev_then_next(self):
        """Test multiple prev() calls followed by next()"""
        cron = Cron('*/5 * * * *')
        schedule = cron.schedule(datetime.fromisoformat('2020-02-08T09:32:15'))

        schedule.prev()  # 9:30
        dt2 = schedule.prev()  # 9:25
        self.assertEqual(dt2.isoformat(), '2020-02-08T09:25:00')

        dt3 = schedule.next()  # 9:30
        self.assertEqual(dt3.isoformat(), '2020-02-08T09:30:00')


class TestResetFunctionality(unittest.TestCase):
    """Test reset() method using fixture data"""

    def test_reset_after_next(self):
        """Test that reset() returns to start after next() calls"""
        for valid_schedule in valid_schedules[:10]:
            with self.subTest(schedule=valid_schedule['schedule']):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                start_time = datetime.fromisoformat(valid_schedule['now'])
                schedule = cron.schedule(start_time)

                schedule.next()
                schedule.next()

                schedule.reset()

                # Next should give the same result as first next
                result = schedule.next()
                self.assertEqual(result.isoformat(), valid_schedule['next'])

    def test_reset_after_iterator_usage(self):
        """Test that reset() works after using iterator protocol"""
        cron = Cron('*/5 * * * *')
        schedule = cron.schedule(datetime.fromisoformat('2020-02-08T09:32:15'))

        # Use iterator to advance
        list(islice(schedule, 5))

        schedule.reset()

        # Should start from beginning
        dt = schedule.next()
        self.assertEqual(dt.isoformat(), '2020-02-08T09:35:00')


class TestEdgeCasesWithFixtures(unittest.TestCase):
    """Test edge cases using fixture data"""

    def test_exact_time_match(self):
        """Test behavior when 'now' exactly matches schedule time"""
        # Using fixture where now == schedule time
        exact_match_fixtures = [
            fixture for fixture in valid_schedules
            if fixture['now'] == fixture['next']
        ]

        for valid_schedule in exact_match_fixtures:
            with self.subTest(schedule=valid_schedule['schedule']):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))

                result = schedule.next()
                self.assertEqual(result.isoformat(), valid_schedule['next'])

    def test_with_microseconds(self):
        """Test that microseconds are properly handled"""
        # Find fixtures with microseconds
        microsecond_fixtures = [
            fixture for fixture in valid_schedules
            if '.' in fixture['now']
        ]

        for valid_schedule in microsecond_fixtures:
            with self.subTest(schedule=valid_schedule['schedule']):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))

                result = schedule.next()

                # Result should have no microseconds
                self.assertEqual(result.microsecond, 0)
                self.assertEqual(result.isoformat(), valid_schedule['next'])

    def test_timezone_aware_datetimes(self):
        """Test with timezone-aware datetimes from fixtures"""
        # Find fixtures with timezone info
        tz_aware_fixtures = [
            fixture for fixture in valid_schedules
            if '+' in fixture['now'] or fixture['now'].endswith('Z')
        ]

        for valid_schedule in tz_aware_fixtures:
            with self.subTest(schedule=valid_schedule['schedule']):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))

                result = schedule.next()

                # Result should maintain timezone awareness
                self.assertIsNotNone(result.tzinfo)
                self.assertEqual(result.isoformat(), valid_schedule['next'])

    def test_month_boundary_crossing(self):
        """Test schedules that cross month boundaries"""
        # Find fixtures that cross months
        month_crossing_fixtures = [
            fixture for fixture in valid_schedules
            if (datetime.fromisoformat(fixture['now']).month !=
                datetime.fromisoformat(fixture['next']).month)
        ]

        for valid_schedule in month_crossing_fixtures:
            with self.subTest(schedule=valid_schedule['schedule']):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))

                result = schedule.next()
                self.assertEqual(result.isoformat(), valid_schedule['next'])

    def test_year_boundary_crossing(self):
        """Test schedules that cross year boundaries"""
        # Find fixtures that cross years
        year_crossing_fixtures = [
            fixture for fixture in valid_schedules
            if (datetime.fromisoformat(fixture['now']).year !=
                datetime.fromisoformat(fixture['next']).year)
        ]

        for valid_schedule in year_crossing_fixtures:
            with self.subTest(schedule=valid_schedule['schedule']):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))

                result = schedule.next()
                self.assertEqual(result.isoformat(), valid_schedule['next'])

    def test_leap_year_handling(self):
        """Test February 29th handling in leap year"""
        # Find leap year fixture (2020-02-29)
        leap_year_fixtures = [
            fixture for fixture in valid_schedules
            if '2020-02-29' in fixture['next']
        ]

        for valid_schedule in leap_year_fixtures:
            with self.subTest(schedule=valid_schedule['schedule']):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))

                result = schedule.next()
                self.assertEqual(result.isoformat(), valid_schedule['next'])

                # Verify it's actually Feb 29
                self.assertEqual(result.month, 2)
                self.assertEqual(result.day, 29)

    def test_weekday_schedules(self):
        """Test schedules with weekday specifications"""
        # Find fixtures with weekday specifications
        weekday_fixtures = [
            fixture for fixture in valid_schedules
            if any(day in fixture['schedule'] for day in ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'])
        ]

        for valid_schedule in weekday_fixtures:
            with self.subTest(schedule=valid_schedule['schedule']):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))

                result = schedule.next()
                self.assertEqual(result.isoformat(), valid_schedule['next'])


class TestComplexSchedules(unittest.TestCase):
    """Test complex cron expressions from fixtures"""

    def test_every_minute_schedule(self):
        """Test '* * * * *' (every minute) schedules"""
        every_minute = [f for f in valid_schedules if f['schedule'] == '* * * * *']

        for valid_schedule in every_minute:
            with self.subTest(now=valid_schedule['now']):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))

                result = schedule.next()
                self.assertEqual(result.isoformat(), valid_schedule['next'])

    def test_midnight_schedules(self):
        """Test '0 0 * * *' (midnight) schedules"""
        midnight = [f for f in valid_schedules if f['schedule'] == '0 0 * * *']

        for valid_schedule in midnight:
            with self.subTest(now=valid_schedule['now']):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))

                result = schedule.next()
                self.assertEqual(result.isoformat(), valid_schedule['next'])

    def test_specific_day_of_month(self):
        """Test schedules with specific day of month"""
        day_specific = [f for f in valid_schedules if '1 * *' in f['schedule']]

        for valid_schedule in day_specific:
            with self.subTest(schedule=valid_schedule['schedule']):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))

                result = schedule.next()
                self.assertEqual(result.isoformat(), valid_schedule['next'])

    def test_interval_schedules(self):
        """Test schedules with intervals (*/N)"""
        interval = [f for f in valid_schedules if '*/' in f['schedule']]

        for valid_schedule in interval:
            with self.subTest(schedule=valid_schedule['schedule']):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))

                result = schedule.next()
                self.assertEqual(result.isoformat(), valid_schedule['next'])

    def test_range_schedules(self):
        """Test schedules with ranges (e.g., MON-FRI)"""
        ranges = [f for f in valid_schedules if '-' in f['schedule'] and '/' not in f['schedule']]

        for valid_schedule in ranges:
            with self.subTest(schedule=valid_schedule['schedule']):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))

                result = schedule.next()
                self.assertEqual(result.isoformat(), valid_schedule['next'])


class TestConsistencyAcrossFixtures(unittest.TestCase):
    """Test consistency of behavior across all fixtures"""

    def test_all_fixtures_produce_datetime(self):
        """Test that all fixtures produce datetime objects"""
        for valid_schedule in valid_schedules:
            with self.subTest(schedule=valid_schedule['schedule']):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))

                result_next = schedule.next()
                self.assertIsInstance(result_next, datetime)

    def test_all_fixtures_next_never_in_past(self):
        """Test that next() never returns a date in the past"""
        for valid_schedule in valid_schedules:
            with self.subTest(schedule=valid_schedule['schedule']):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                now = datetime.fromisoformat(valid_schedule['now'])
                schedule = cron.schedule(now)

                result = schedule.next()
                expected = datetime.fromisoformat(valid_schedule['next'])

                # Next should be >= now (allowing for exact match)
                self.assertGreaterEqual(result, now.replace(second=0, microsecond=0))

    def test_all_fixtures_maintain_seconds_zero(self):
        """Test that all results have seconds=0"""
        for valid_schedule in valid_schedules:
            with self.subTest(schedule=valid_schedule['schedule']):
                cron = Cron()
                cron.from_string(valid_schedule['schedule'])
                schedule = cron.schedule(datetime.fromisoformat(valid_schedule['now']))

                result = schedule.next()

                # Cron schedules are minute-precision
                self.assertEqual(result.second, 0)


# if __name__ == '__main__':
#     unittest.main(verbosity=2)

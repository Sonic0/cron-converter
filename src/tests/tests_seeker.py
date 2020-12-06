import unittest
from datetime import datetime, timezone

from cron import Cron
from seeker import Seeker


class SeekerTest(unittest.TestCase):

    def test_create_seeker(self):
        cron = Cron()
        cron.from_string('0-59 0-23 1-31 JAN-DEC SUN-SAT')
        now = datetime.now(timezone.utc)
        seeker = Seeker(cron, now)
        print(seeker.date)
        self.assertEqual(0, 1, 'NP')

import unittest
from datetime import datetime, timezone

from cron import Cron
from seeker import Seeker


class SeekerTest(unittest.TestCase):

    def test_create_seeker(self):
        cron = Cron()
        cron.from_string('*/5 * * * *')
        seeker = cron.schedule()

        print("###")
        print(seeker.next())
        print("-------")
        print(seeker.next())
        self.assertTrue(True)

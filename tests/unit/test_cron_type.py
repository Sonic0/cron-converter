import unittest

from pydantic import BaseModel

from cron_converter import Cron, CronType


class PartTestInvalid(unittest.TestCase):
    def test_valid_class(self):
        class Model(BaseModel):
            cron: CronType

        m = Model(cron='* * * * *')
        self.assertEqual(m.cron, Cron('* * * * *'))

    def test_invalid_class(self):
        from pydantic import BaseModel

        class Model(BaseModel):
            cron: CronType

        with self.assertRaises(ValueError):
            Model(cron='* * * * * *')

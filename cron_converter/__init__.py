import sys

from .cron import Cron

if sys.modules.get('pydantic', None):
    from .cron import CronType

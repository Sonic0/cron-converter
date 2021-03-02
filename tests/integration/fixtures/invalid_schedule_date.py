invalid_schedules = [
  {
    'schedule': '* * 30 FEB *',
    'now': '2020-02-08T09:32:00',
    'error': Exception,
    'message': 'Unable to find execution time for schedule'
  },
  {
    'schedule': '* * * * *',
    'now': None,
    'error': ValueError,
    'message': 'Input schedule start time is not a valid datetime object'
  },
]

invalid_crons = [
  {
    'string': None,
    'error': TypeError,
    'message': 'Invalid cron string'
  },
  {
    'string': '',
    'error': ValueError,
    'message': 'Invalid cron string format'
  },
  {
    'string': '0',
    'error': ValueError,
    'message': 'Invalid cron string format'
  },
  {
    'string': '0 0 0 0 0',
    'error': ValueError,
    'message': 'Value "0" out of range for day'
  },
  {
    'string': '0 0 0 1 0',
    'error': ValueError,
    'message': 'Value "0" out of range for day'
  },
  {
    'string': '0 0 1 0 0',
    'error': ValueError,
    'message': 'Value "0" out of range for month'
  },
  {
    'string': '/ / / / /',
    'error': ValueError,
    'message': 'Invalid value "/" for minute'
  },
  {
    'string': '60 5 5 5 5',
    'error': ValueError,
    'message': 'Value "60" out of range for minute'
  },
  {
    'string': '/5 5 5 5 5',
    'error': ValueError,
    'message': 'Invalid value "/5" for minute'
  },
  {
    'string': '10-5/5 5 5 5 5',
    'error': ValueError,
    'message': 'Max range is less than min range in "10-5" for minute'
  },
  {
    'string': '* * 0 * *',
    'error': ValueError,
    'message': 'Value "0" out of range for day'
  },
  {
    'string': '* * * 0 *',
    'error': ValueError,
    'message': 'Value "0" out of range for month'
  },
  {
    'string': '0/5/5 * * 0 *',
    'error': ValueError,
    'message': 'Invalid value "0/5/5" for minute'
  },
  {
    'string': '5/a * * * *',
    'error': ValueError,
    'message': 'Invalid interval step value "a" for minute'
  },
  {
    'string': '5/ * * * *',
    'error': ValueError,
    'message': 'Invalid interval step value "" for minute'
  }
]

units = [
  {
    "name": "minute",
    "min": 0,
    "max": 59
  },
  {
    "name": "hour",
    "min": 0,
    "max": 23
  },
  {
    "name": "day",
    "min": 1,
    "max": 31
  },
  {
    "name": "month",
    "min": 1,
    "max": 12,
    "alt": [
      'JAN', 'FEB', 'MAR', 'APR',
      'MAY', 'JUN', 'JUL', 'AUG',
      'SEP', 'OCT', 'NOV', 'DEC'
    ]
    # TODO implement max last day of month ( 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 )
  },
  {
    "name": 'weekday',
    "min": 0,
    "max": 6,
    "alt": ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
  }
]

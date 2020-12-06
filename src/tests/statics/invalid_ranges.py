invalid_ranges = [
  {
    'input': '',
    'unit': 1,
    'error': 'Invalid value "" for sample unit',
  },
  {
    'input': '3-1',
    'unit': 1,
    'error': 'Max range is less than min range in "3-1" for sample unit',
  },
  {
    'input': '1-2-3',
    'unit': 1,
    'error': 'Invalid value "1-2-3" for sample unit',
  },
  {
    'input': '5-15',
    'unit': 4,
    'error': 'Value "5" out of range for sample unit',
  },
  {
    'input': '**',
    'unit': 1,
    'error': 'Invalid value "**" for sample unit',
  },
  {
    'input': '0-',
    'unit': 1,
    'error': 'Empty interval value "0-" for sample unit',
  }
]

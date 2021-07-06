valid_ranges = [
    {
        'input': '0-4',
        'arr': [0, 1, 2, 3, 4],
        'output': '0-4',
        'unit': 1
    },
    {
        'input': 'SUN',
        'arr': [0],
        'output': '0',
        'unit': 4
    },
    {
        'input': 'SUN,MON,TUE',
        'arr': [0, 1, 2],
        'output': '0-2',
        'unit': 4
    },
    {
        'input': 'mon-fri',
        'arr': [1, 2, 3, 4, 5],
        'output': '1-5',
        'unit': 4
    },
    {
        'input': '1,2,3',
        'arr': [1, 2, 3],
        'output': '1-3',
        'unit': 0
    },
    {
        'input': '0,1,3,2,4,6,5',
        'arr': [0, 1, 2, 3, 4, 5, 6],
        'output': '*',
        'unit': 4
      },
    {
        'input': '1-10/5',
        'arr': [1, 6],
        'output': '1,6',
        'unit': 0
    },
    {
        'input': '5,5,6,6,7,7',
        'arr': [5, 6, 7],
        'output': '5-7',
        'unit': 1
    },
    {
        'input': '*',
        'arr': [0, 1, 2, 3, 4, 5, 6],
        'output': '*',
        'unit': 4
    },
    {
        'input': '0,5',
        'arr': [0, 5],
        'output': '0,5',
        'unit': 1
    },
    {
        'input': '0,5-6',
        'arr': [0, 5, 6],
        'output': '0,5-6',
        'unit': 4
    },
    {
        'input': '1-1',
        'arr': [1],
        'output': '1',
        'unit': 4
    },
]

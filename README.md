# cron-converter

Cron string parser for Python. This project is a transposition in Python of JS [cron-converter](https://github.com/roccivic/cron-converter) by [roccivic](https://github.com/roccivic). 

[![MIT License Badge](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Sonic0/cron-converter/blob/master/LICENCE)

__This project is WIP__.

## Install

#### Pip
```bash
pip install cron-converter
```

## Use
```python
from cron-converter import Cron
```

### Create a new instance
```python
cron_instance = Cron()
```

### Parse a cron string
```python
# Every 10 mins between 9am and 5pm on the 1st of every month
cron_instance.from_string('*/10 9-17 1 * *')

# Prints: '*/10 9-17 1 * *'
print(cron_instance.to_string())

# Prints:
# [
#   [ 0, 10, 20, 30, 40, 50 ],
#   [ 9, 10, 11, 12, 13, 14, 15, 16, 17 ],
#   [ 1 ],
#   [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 ],
#   [ 0, 1, 2, 3, 4, 5, 6 ]
# ]
print(cron_instance.to_list())
```

### Parse an Array
```python
cron_instance.from_array([[0], [1], [1], [5], [0,2,4,6]])

# Prints: '0 1 1 5 */2'
print(cron_instance.to_string())
```


### Constructor options

#### outputWeekdayNames and outputMonthNames
Default: false
```python
cron_instance = Cron({
  'outputWeekdayNames': True,
  'outputMonthNames': True
})
cron_instance.fromString('*/5 9-17/2 * 1-3 1-5')
# Prints: '*/5 *(10-16)/2 * JAN-MAR MON-FRI'
print(cron_instance)
```

## Test and build

```bash
git clone https://github.com/Sonic0/cron-converter
cd cron-converter

```

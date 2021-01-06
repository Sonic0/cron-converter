<p align="center">
  <img src="https://raw.githubusercontent.com/Sonic0/cron-converter/main/logo.png" title="Cron-converter">
</p>

Cron-converter provides a Cron string parser ( from string/lists to string/lists ) and iteration for the datetime object with a cron like format.<br>
This project would be a transposition in Python of JS [cron-converter](https://github.com/roccivic/cron-converter) by [roccivic](https://github.com/roccivic). 

[![MIT License Badge](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Sonic0/cron-converter/blob/master/LICENCE)
![Unit and Integration tests](https://github.com/Sonic0/cron-converter/workflows/Unit%20and%20Integration%20tests/badge.svg)
[![codebeat badge](https://codebeat.co/badges/33cfdde8-34ce-4fcc-85b6-2031d919639f)](https://codebeat.co/projects/github-com-sonic0-cron-converter-main)

## Install

#### Pip
```bash
pip install cron-converter
```

## Use
```python
from cron_converter import Cron
```

### Create a new instance
```python
cron_instance = Cron()
```
or
```python
cron_instance = Cron('*/10 9-17 1 * *')
```
or (with constructor options)
```python
cron_instance = Cron('*/10 9-17 1 * *', {
  'output_weekday_names': True,
  'output_month_names': True
})
```

### Parse a cron string
```python
# Every 10 mins between 9am and 5pm on the 1st of every month
# In the case of the second or third creation method this step is not required
cron_instance.from_string('*/10 9-17 1 * *')

# Prints: '*/10 9-17 1 * *'
print(cron_instance.to_string())
# Alternatively, you could print directly the object obtaining the same result:
# print(cron_instance) # Prints: '*/10 9-17 1 * *'

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
cron_instance.from_list([[0], [1], [1], [5], [0,2,4,6]])

# Prints: '0 1 1 5 */2'
print(cron_instance.to_string())
```

### Constructor options
Possible options:
- output_weekday_names: false (default)
- output_month_mames: false (default)
- output_hashes: false (default)

#### output_weekday_names and output_month_mames
```python
cron_instance = Cron(None, {
  'output_weekday_names': True,
  'output_month_names': True
})
cron_instance.from_string('*/5 9-17/2 * 1-3 1-5')
# Prints: '*/5 9-17/2 * JAN-MAR MON-FRI'
print(cron_instance)
```
or
```python
cron_instance = Cron('*/5 9-17/2 * 1-3 1-5', {
  'output_weekday_names': True,
  'output_month_names': True
})
# Prints: '*/5 9-17/2 * JAN-MAR MON-FRI'
print(cron_instance)
```

#### output_hashes
```python
cron_instance = Cron('*/5 9-17/2 * 1-3 1-5', {
  'output_hashes': True
})
# Prints: 'H/5 H(9-17)/2 H 1-3 1-5'
print(cron_instance.to_string())
```

### Get the schedule execution times. Example with raw Datetime
```python
# Parse a string to init a schedule
cron_instance.from_string('*/5 * * * *')

# Raw datetime without timezone info (not aware)
reference = datetime.now()
# Get the iterator, initialised to now
schedule = cron_instance.schedule(reference)

# Calls to .next() and .prev()
# return a Datetime object

# Examples with time now: '2021-01-01T09:32:00
# Prints: '2021-01-01T09:35:00'
print(schedule.next().isoformat())
# Prints: '2021-01-01T09:40:00'
print(schedule.next().isoformat())

# Reset
schedule.reset()

# Prints: '2021-01-01T09:30:00'
print(schedule.prev().isoformat())
# Prints: '2021-01-01T09:25:00'
print(schedule.prev().isoformat())
```

## About DST
Be sure to init your cron-converter instance with a TZ aware datetime for this to work!

Example using pytz:
```python
from pytz import timezone
from datetime import datetime
from cron_converter import Cron

tz = timezone("Europe/Rome")
local_date = tz.localize(datetime(2021, 1, 1))
cron = Cron('0 0 * * *')
schedule = cron.schedule(local_date)
next_schedule = schedule.next()
next_next_schedule = schedule.next()
# Prints: '2021-01-01T00:00:00+01:00'
print(next_schedule.isoformat())
# Prints: '2021-01-02T00:00:00+01:00'
print(next_next_schedule.isoformat())
```
Example using python_dateutil:
```python
import dateutil.tz
from datetime import datetime
from cron_converter import Cron

tz = dateutil.tz.gettz('Asia/Tokyo')
local_date = datetime(2021, 1, 1, tzinfo=tz)
cron = Cron('0 0 * * *')
schedule = cron.schedule(local_date)
next_schedule = schedule.next()
next_next_schedule = schedule.next()
# Prints: '2021-01-01T00:00:00+09:00'
print(next_schedule.isoformat())
# Prints: '2021-01-02T00:00:00+09:00'
print(next_next_schedule.isoformat())
```

## About seconds repeats
Cron-converter is NOT able to do second repetition crontabs form.

## Develop & Tests
```bash
git clone https://github.com/Sonic0/cron-converter
cd cron-converter
python -m unittest discover -s src/cron_converter/tests/unit
python -m unittest discover -s src/cron_converter/tests/integration
```

### TODO
```
Cron day part string output in the form: 
'*(10-16)/2' 
instead of: 
'9-17/2'
```

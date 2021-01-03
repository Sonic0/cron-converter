# cron-converter
<p align="center">
  <img src="https://cdn.webservertalk.com/wp-content/uploads/cron-jobs-656x410.png" width="450" title="Cron Syntax">
</p>
Cron-converter provides a Cron string parser ( from string/list to string/lists ) and iteration for the datetime object with a cron like format. <br>
This project is a transposition in Python of JS [cron-converter](https://github.com/roccivic/cron-converter) by [roccivic](https://github.com/roccivic). 

[![MIT License Badge](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Sonic0/cron-converter/blob/master/LICENCE)

__This project is WIP__.

## Install

#### Pip
```bash
pip install cron-converter
```

## Use
```python
from cron_converter import cron
```

### Create a new instance
```python
cron_instance = cron.Cron()
```
or
```python
cron_instance = cron.Cron('*/10 9-17 1 * *')
```
or (with constructor options)
```python
cron_instance = cron.Cron('*/10 9-17 1 * *', {
  'outputWeekdayNames': True,
  'outputMonthNames': True
})
```

### Parse a cron string
```python
# Every 10 mins between 9am and 5pm on the 1st of every month
# In case of the second or third creation method this step is not required
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
cron_instance.from_list([[0], [1], [1], [5], [0,2,4,6]])

# Prints: '0 1 1 5 */2'
print(cron_instance.to_string())
```

### Constructor options

##### outputWeekdayNames and outputMonthNames --> Default: false

```python
cron_instance = Cron(None, {
  'outputWeekdayNames': True,
  'outputMonthNames': True
})
cron_instance.from_string('*/5 9-17/2 * 1-3 1-5')
# Prints: '*/5 *(10-16)/2 * JAN-MAR MON-FRI'
print(cron_instance)
```
or
```python
cron_instance = Cron('*/5 9-17/2 * 1-3 1-5', {
  'outputWeekdayNames': True,
  'outputMonthNames': True
})
# Prints: '*/5 *(10-16)/2 * JAN-MAR MON-FRI'
print(cron_instance)
```

### Get the schedule execution times. Example with raw Datetime
```python
# Parse a string to init a schedule
cron_instance.from_string('*/5 * * * *')

# Optionally, use a reference Date or moment object
reference = datetime.now()  # Raw datetime without timezone info (not aware)
# Get the iterator, initialised to now
schedule = cron_instance.schedule(reference)

# Calls to .next() and .prev()
# return a Datetime object

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
    from datetime import datetime
    import pytz
    from datetime import datetime
    from cron_converter import cron

    tz = pytz.timezone("Europe/Rome")
    local_date = tz.localize(datetime(2021, 1, 1))
    cron = cron.Cron('0 0 * * *')
    next_schedule = cron.schedule(local_date).next()
    # Prints: '2021-01-01T09:25:00+01:00'
    print(next_schedule.isoformat())
```
Example using python_dateutil:
```python
    import dateutil.tz
    from datetime import datetime
    from cron_converter import cron

    tz = dateutil.tz.gettz('Asia/Tokyo')
    local_date = datetime(2021, 1, 1, tzinfo=tz)
    cron = cron.Cron('0 0 * * *')
    next_schedule = cron.schedule(local_date).next()
    # Prints: '2021-01-01T17:25:00+09:00'
    print(next_schedule.isoformat())
```

## About seconds repeats
Cron-converter is NOT able to do second repetition crontabs form.

## Test and build

```bash
git clone https://github.com/Sonic0/cron-converter
cd cron-converter
# TODO this step
```

shut
=========
shut is short for "SHape Unix Time." It uses regular expressions to take piped data
and convert substrings that look like Unix time into human-readable timestamps.

This is for those of us who have Unix time logs and want to see when events occurred as lazily as possible.

## Installation

`git clone https://github.com/ajduberstein/shut.git`
`cd shut`
`python setup.py install`

## Usage

```
echo '{"ts": 1440999387, "level": "ERROR", "msg": "A mistake at some time"}' | shut
# {"ts": "2015-08-31 05:36:27", "level": "ERROR", "msg": "A mistake at some time"}
```

Since Unix time could in theory be between negative and positive infinity, you may choose to provide a reasonable range
for timestamps. The default is to parse a string for numbers greater than a year ago and less than a year from today.

```
echo '{"ts": 584928000, "level": "INFO", "msg": "Die Hard release date"}' | shut --min-date 1988-01-01
# {"ts": "1988-07-15 00:00:00", "level": "ERROR", "msg": "A mistake at some time"}
```

Feel free to feed Unix times as args as well:

```
echo '{"ts": 584928000, "level": "INFO", "msg": "Die Hard release date"}' | shut --min-date 567993600
# {"release_date": "1988-07-15 00:00:00", "msg": "Die Hard release date"}
```

I can't think of why a max range would be useful, but perhaps you can:

```
echo '{"ts": 584928000, "level": "INFO", "msg": "Die Hard release date"}' | shut --min-date 1988-01-01
# {"release_date": "1988-07-15 00:00:00", "msg": "The Die Hard franchise has grossed $2015-06-23 19:06:02.00 globally"}
echo '{"ts": 584928000, "level": "INFO", "msg": "Die Hard release date"}' | shut --min-date 1988-01-01 --max-date 2013-02-14
# {"release_date": "1988-07-15 00:00:00", "msg": "The Die Hard franchise has grossed $1435086362.00 globally"}
```

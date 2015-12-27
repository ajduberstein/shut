#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from optparse import OptionParser
from pytz import timezone, utc
import re
import sys

DATE_FORMAT = '%Y-%m-%d'

now, year_delta = datetime.utcnow(), timedelta(days=365)
DEFAULT_MIN_DATE = (now - year_delta).strftime(DATE_FORMAT)
DEFAULT_MAX_DATE = (now + year_delta).strftime(DATE_FORMAT)


def shape_unix_time(min_date, max_date, input_tz):
    min_ut, max_date = _convert_cutoffs_to_epoch(min_date, max_date, input_tz)
    lines = sys.stdin.read().split('\n')
    for line in lines:
        print _make_readable_ut(line, min_ut, max_date, input_tz)


def _convert_cutoffs_to_epoch(min_date, max_date, input_tz):
    """Parse max and min date strings into a Unix time. All timezones in UTC
    unless otherwise specified."""
    min_ut = min_date
    if type(min_date) != int:
        input_ts_with_tz = timezone(input_tz).localize(datetime.strptime(min_date, DATE_FORMAT))
        min_ut = int(input_ts_with_tz.astimezone(utc).strftime('%s'))
    max_ut = max_date
    if type(max_date) != int:
        input_ts_with_tz = timezone(input_tz).localize(datetime.strptime(max_date, DATE_FORMAT))
        max_ut = int(input_ts_with_tz.astimezone(utc).strftime('%s'))
    return min_ut, max_ut


def _make_readable_ut(input_str, lo, hi, input_tz):
    all_numbers = re.findall(r'\d+', input_str)
    in_range_numbers = [int(x) for x in all_numbers if lo <= int(x) and int(x) <= hi]
    for num in in_range_numbers:
        local_datetime = timezone(input_tz).localize(datetime.fromtimestamp(float(num)))
        utc_ts = local_datetime.astimezone(utc).strftime('%Y-%m-%d %H:%M:%S')
        input_str = input_str.replace(str(num), utc_ts)
    return input_str


def main():
    parser = OptionParser()
    parser.add_option('-m', '--min-date',
                      dest='min_date',
                      default=DEFAULT_MIN_DATE,
                      help='Lower bound for Unix time candidates, YYYY-MM-DD format or a Unix time number',
                      metavar='YYYY-MM-DD')

    parser.add_option('-M', '--max-date',
                      dest='max_date',
                      default=DEFAULT_MAX_DATE,
                      help='Upper bound for Unix time candidates, YYYY-MM-DD format or a Unix time number',
                      metavar='YYYY-MM-DD')

    parser.add_option('-t', '--input-tz',
                      dest='input_tz',
                      default='UTC',
                      help='Timezone of input dates (Default: UTC). All Unix time inputs are assumed to be UTC.',
                      metavar='TIMEZONE')

    (options, args) = parser.parse_args()
    shape_unix_time(options.min_date, options.max_date, options.input_tz)


if __name__ == '__main__':
    main()

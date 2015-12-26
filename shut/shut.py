#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from optparse import OptionParser
import re
import sys


now, year_delta = datetime.utcnow(), timedelta(days=365)
DEFAULT_MIN_DATE = (now - year_delta).strftime('%Y-%m-%d')
DEFAULT_MAX_DATE = (now + year_delta).strftime('%Y-%m-%d')


def shape_unix_time(min_date, max_date):
    min_ut, max_date = _handle_inputs(min_date, max_date)
    lines = sys.stdin.read().split('\n')
    for line in lines:
        print _make_readable_ut(line, min_ut, max_date)


def _handle_inputs(min_date='2015-01-01', max_date=None):
    # Make unix time
    min_ut = min_date
    if type(min_date) != int:
        min_ut = int(datetime.strptime(min_date, '%Y-%m-%d').strftime('%s'))
    max_ut = max_date
    if type(max_date) != int:
        max_ut = int(datetime.strptime(max_date, '%Y-%m-%d').strftime('%s'))
    return min_ut, max_ut


def _make_readable_ut(input_str, lo, hi):
    all_numbers = re.findall(r'\d+', input_str)
    in_range_numbers = [int(x) for x in all_numbers if lo <= int(x) and int(x) <= hi]
    for num in in_range_numbers:
        ut_as_date = datetime.fromtimestamp(float(num)).strftime('%Y-%m-%d %H:%M:%S')
        input_str = input_str.replace(str(num), ut_as_date)
    return input_str


def main():
    parser = OptionParser()
    parser.add_option('-m', '--min-date',
                      dest='min_date',
                      default=DEFAULT_MIN_DATE,
                      help='Lower bound for Unix time candidates, YYYY-MM-DD format',
                      metavar='YYYY-MM-DD')

    parser.add_option('-M', '--max-date',
                      dest='max_date',
                      default=DEFAULT_MAX_DATE,
                      help='Upper bound for Unix time candidates, YYYY-MM-DD format',
                      metavar='YYYY-MM-DD')

    (options, args) = parser.parse_args()
    shape_unix_time(options.min_date, options.max_date)


if __name__ == '__main__':
    main()

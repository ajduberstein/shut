# -*- coding: utf-8 -*-
import sys
import re
from datetime import datetime
import click


@click.command()
@click.option('--min-date',
              default='2015-01-01',
              help='Lower bound for Unix time candidates.'
              )
@click.option('--max-date',
              default='2999-01-01',
              help='Upper bound for Unix time candidates.'
              )
def shape_unix_time(min_date, max_date):
    min_ut, max_date = handle_defaults(min_date, max_date)
    lines = sys.stdin.read().split('\n')
    for line in lines:
        print _make_readable_ut(line, min_ut, max_date)


def handle_defaults(min_date='2015-01-01', max_date=None):
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


if __name__ == '__main__':
    shape_unix_time()

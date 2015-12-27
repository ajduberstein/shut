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


class UnixTimeParser:

    def __init__(self, min_date, max_date, input_tz):
        self.input_tz = input_tz
        self.min_ut, self.max_ut = self._convert_cutoffs_to_epoch(min_date, max_date, input_tz)

    @staticmethod
    def _convert_cutoffs_to_epoch(min_date, max_date, input_tz):
        """Parse max and min date strings into a Unix time. All timezones in UTC
        unless otherwise specified.
        """
        min_ut = min_date
        if type(min_date) != int:
            input_ts_with_tz = timezone(input_tz).localize(datetime.strptime(min_date, DATE_FORMAT))
            min_ut = int(input_ts_with_tz.astimezone(utc).strftime('%s'))
        max_ut = max_date
        if type(max_date) != int:
            input_ts_with_tz = timezone(input_tz).localize(datetime.strptime(max_date, DATE_FORMAT))
            max_ut = int(input_ts_with_tz.astimezone(utc).strftime('%s'))
        return min_ut, max_ut

    def _make_readable_ut(self, input_str):
        """Given a line, convert all digits within a specified range to a readable time in the user-specified tz
        """
        lo, hi = self.min_ut, self.max_ut
        all_numbers = re.findall(r'\d+', input_str)
        in_range_numbers = [int(x) for x in all_numbers if lo <= int(x) and int(x) <= hi]
        for num in in_range_numbers:
            # input is assumed to be a Unix timestamp, which are by default in UTC
            unix_ts = datetime.fromtimestamp(float(num), tz=utc)
            # Convert to specificed user timezone
            ts = unix_ts.astimezone(timezone(self.input_tz)).strftime('%Y-%m-%d %H:%M:%S')
            input_str = input_str.replace(str(num), ts)
        return input_str

    def shape_unix_time(self):
        """Read from stdin and apply unix time conversion"""
        lines = sys.stdin.read().split('\n')
        for line in lines:
            print self._make_readable_ut(line)


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
    t = UnixTimeParser(options.min_date, options.max_date, options.input_tz)
    t.shape_unix_time()


if __name__ == '__main__':
    main()

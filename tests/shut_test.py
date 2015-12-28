#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_shut
----------------------------------

Tests for `shut` module.
"""

import subprocess
import sys
import unittest
import StringIO

from mock import patch

from shut import UnixTimeParser


class TestShut(unittest.TestCase):

    def setUp(self):
        self.utp = UnixTimeParser('2015-01-01', '2015-10-01', 'UTC')
        self.utp_pacific = UnixTimeParser('2015-01-01', '2015-10-01', 'US/Pacific')

    def test_shape_unix_time_unchanged_input(self):
        with patch('sys.stdout', new=StringIO.StringIO()) as fakeOutput:
            sys.stdin = StringIO.StringIO('asdlkj')
            self.utp.shape_unix_time()
            assert fakeOutput.getvalue().strip() == 'asdlkj'

    def test_shape_unix_time_converted(self):
        with patch('sys.stdout', new=StringIO.StringIO()) as fakeOutput:
            sys.stdin = StringIO.StringIO('asdlkj,1443304641,more_text,1443304642')
            self.utp_pacific.shape_unix_time()
            assert fakeOutput.getvalue().strip() == 'asdlkj,2015-09-26 14:57:21,more_text,2015-09-26 14:57:22'

    def test_shape_unix_time_converted_utc(self):
        with patch('sys.stdout', new=StringIO.StringIO()) as fakeOutput:
            sys.stdin = StringIO.StringIO('asdlkj,1443304641,more_text,1443304642')
            self.utp.shape_unix_time()
            assert fakeOutput.getvalue().strip() == 'asdlkj,2015-09-26 21:57:21,more_text,2015-09-26 21:57:22'

    def test_command_line_execution(self):
        proc = subprocess.check_output(
            'echo \'{"ts": 1440999387, "msg": ""}\' | ./shut/shut.py',
            shell=True)
        assert '2015-08-31 05:36:27' in proc

    def test_command_line_execution_min(self):
        proc = subprocess.check_output(
            'echo \'{"ts": 584928000, "msg": ""}\' | ./shut/shut.py -m 1988-01-01',
            shell=True)
        assert '1988-07-15 00:00:00' in proc

    def test_command_line_execution_min_max(self):
        proc = subprocess.check_output(
            'echo \'{"ts": 584928000, "msg": "$1435086362.00"}\' | ./shut/shut.py -m 1988-01-01 -M 2013-02-14',
            shell=True)
        assert '1988-07-15 00:00:00' in proc and '$1435086362.00' in proc

    def test_command_line_execution_min_tz(self):
        proc = subprocess.check_output(
            'echo \'{"ts": 584928000, "msg": "$1435086362.00"}\' | ./shut/shut.py -m 1988-01-01 -t US\/Pacific',
            shell=True)
        print proc
        assert '1988-07-14 17:00:00' in proc

if __name__ == '__main__':
    TestShut()

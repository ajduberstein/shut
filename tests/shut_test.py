#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_shut
----------------------------------

Tests for `shut` module.
"""

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

if __name__ == '__main__':
    TestShut()

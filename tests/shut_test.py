#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_shut
----------------------------------

Tests for `shut` module.
"""

import sys
import unittest

from shut import shape_unix_time


class TestShut(unittest.TestCase):

    def setUp(self):
        pass

    def test_shape_unix_time(self):
        raw_input = lambda _: ''  # noqa
        shape_unix_time('2015-01-01', '2015-10-01')
        output = sys.stdout.getvalue().strip()
        assert output == ''

    def tearDown(self):
        pass

if __name__ == '__main__':
    TestShut()

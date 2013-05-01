#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2013 by Łukasz Langa
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

try:
    import unittest2 as unittest
except ImportError:
    import unittest


import requests
from requests_testadapter import TestAdapter, TestSession


class TestRequestsTestAdapter(unittest.TestCase):
    def setUp(self):
        pass

    def testBasic(self):
        s = requests.Session()
        mocked_content = b'Test basic!'
        s.mount('http://', TestAdapter(mocked_content))
        r = s.get('http://testbasic.com/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.content, mocked_content)

    def testSession(self):
        s = TestSession()
        self.assertEqual([], list(s.adapters))
        s.mount('http://git', TestAdapter(b'git'))
        s.mount('http://github', TestAdapter(b'github'))
        s.mount('http://github.com', TestAdapter(b'github.com'))
        s.mount('http://github.com/about/', TestAdapter(b'github.com/about'))
        order = [
            'http://github.com/about/',
            'http://github.com',
            'http://github',
            'http://git',
        ]
        self.assertEqual(order, list(s.adapters))
        s.mount('http://gittip', TestAdapter(b'gittip'))
        s.mount('http://gittip.com', TestAdapter(b'gittip.com'))
        s.mount('http://gittip.com/about/', TestAdapter(b'gittip.com/about'))
        order = [
            'http://github.com/about/',
            'http://gittip.com/about/',
            'http://github.com',
            'http://gittip.com',
            'http://github',
            'http://gittip',
            'http://git',
        ]
        self.assertEqual(order, list(s.adapters))
        s2 = requests.Session()
        s2.adapters = {'http://': TestAdapter(b'http')}
        s2.mount('https://', TestAdapter(b'https'))
        self.assertTrue('http://' in s2.adapters)
        self.assertTrue('https://' in s2.adapters)


if __name__ == '__main__':
    unittest.main()

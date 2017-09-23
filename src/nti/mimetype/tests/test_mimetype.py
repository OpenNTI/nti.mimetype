#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import is_not
from hamcrest import assert_that
does_not = is_not

import unittest

from nti.mimetype.mimetype import parse_mime_type
from nti.mimetype.mimetype import rfc2047MimeTypeConstraint

from nti.mimetype.tests import SharedConfiguringTestLayer


class TestMimeType(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_parse_mime_type(self):
        s = "application/xhtml;q=0.5"
        parsed = parse_mime_type(s)
        assert_that(parsed, is_(("application", "xhtml", {"q": "0.5"})))

    def test_rfc2047_mime_type_constraint(self):
        for s in ("application/xhtml;q=0.5",
                  "application/*",
                  "application/xhtml;",
                  'text/plain',
                  str('text/plain;charset=US-ASCII')):
            value = rfc2047MimeTypeConstraint(s)
            assert_that(value, is_(True))

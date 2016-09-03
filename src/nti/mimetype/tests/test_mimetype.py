#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import assert_that
does_not = is_not

import unittest

from nti.mimetype.mimetype import parse_mime_type
from nti.mimetype.mimetype import mime_type_constraint

from nti.mimetype.tests import SharedConfiguringTestLayer

class TestMimeType(unittest.TestCase):

	layer = SharedConfiguringTestLayer

	def test_parse_mime_type(self):
		s = "application/xhtml;q=0.5"
		parsed = parse_mime_type(s)
		assert_that(parsed, is_(("application", "xhtml", { "q" : "0.5" })))
		
	def test_mime_type_constraint(self):
		for s in ("application/xhtml;q=0.5","application/*", "application/xhtml;"):
			obj = mime_type_constraint(s)
			assert_that(obj, is_not(none()))

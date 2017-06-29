#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that

import unittest

from nti.mimetype import guess_type


class TestMimeTypes(unittest.TestCase):

    def test_guess_type(self):
        t = guess_type('foo.xml')
        assert_that(t[0], is_('application/xml'))
        t = guess_type('foo.mml')
        assert_that(t[0], is_('text/mathml'))
        assert_that(guess_type(None), is_((None, None)))

    def test_image_types(self):
        assert_that(guess_type('foo.png')[0], is_('image/png'))
        assert_that(guess_type('foo.jpg')[0], is_('image/jpeg'))
        assert_that(guess_type('foo.jpeg')[0], is_('image/jpeg'))
        assert_that(guess_type('foo.bmp')[0], is_('image/bmp'))
        assert_that(guess_type('foo.gif')[0], is_('image/gif'))
        assert_that(guess_type('foo.tif')[0], is_('image/tiff'))
        assert_that(guess_type('foo.tiff')[0], is_('image/tiff'))
        assert_that(guess_type('foo.jp2')[0], is_('image/jp2'))
        assert_that(guess_type('foo.rst')[0], is_('text/x-rst'))

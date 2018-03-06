#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import has_property
does_not = is_not

import six
import unittest

from zope import interface

from zope.mimetype.interfaces import IContentTypeAware

from nti.externalization.interfaces import IMimeObjectFactory

from nti.mimetype.interfaces import IContentTypeMarker

from nti.mimetype.mimetype import ModeledContentTypeAwareRegistryMetaclass

from nti.mimetype.mimetype import safe_by
from nti.mimetype.mimetype import is_nti_mimetype
from nti.mimetype.mimetype import parse_mime_type
from nti.mimetype.mimetype import nti_mimetype_class
from nti.mimetype.mimetype import nti_mimetype_with_class
from nti.mimetype.mimetype import nti_mimetype_from_object
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

    def test_is_nti_mimetype(self):
        assert_that(is_nti_mimetype('application/vnd.nextthought.bleach'),
                    is_(True))
        assert_that(is_nti_mimetype(None),
                    is_(False))

    def test_nti_mimetype_class(self):
        assert_that(nti_mimetype_class('application/vnd.nextthought.bleach'),
                    is_('bleach'))
        assert_that(nti_mimetype_class('text/plain'),
                    is_(none()))

    def test_nti_mimetype_with_class(self):
        assert_that(nti_mimetype_with_class(None),
                    is_(none()))

        class Bleach(object):
            pass
        assert_that(nti_mimetype_with_class(Bleach),
                    is_('application/vnd.nextthought.bleach'))
        assert_that(nti_mimetype_with_class('Bleach'),
                    is_('application/vnd.nextthought.bleach'))

    def test_content_type_marker(self):
        @interface.implementer(IContentTypeMarker)
        class Bleach(object):
            pass

        aware = IContentTypeAware(Bleach(), None)
        assert_that(aware, is_not(none()))
        assert_that(aware,
                    has_property('mimeType', is_('application/vnd.nextthought.bleach')))
        assert_that(aware,
                    has_property('parameters', is_(none())))

    def test_metaclass(self):

        @six.add_metaclass(ModeledContentTypeAwareRegistryMetaclass)
        class Ichigo(object):
            pass

        assert_that(Ichigo,
                    has_property('mimeType', is_('application/vnd.nextthought.ichigo')))

        @six.add_metaclass(ModeledContentTypeAwareRegistryMetaclass)
        class Aizen(object):
            mime_type = 'application/vnd.nextthought.aizen'
            __external_can_create__ = True

        assert_that(Aizen,
                    has_property('mimeType', is_('application/vnd.nextthought.aizen')))

        factory = IMimeObjectFactory(
            {'MimeType': 'application/vnd.nextthought.aizen'}, None)
        assert_that(factory, is_not(none()))
        assert_that(factory(), is_(Aizen))

        assert_that(ModeledContentTypeAwareRegistryMetaclass.mime_types,
                    has_length(2))

        assert_that(ModeledContentTypeAwareRegistryMetaclass.external_mime_types,
                    has_length(1))

    def test_nti_mimetype_from_object(self):

        class Ichigo(object):
            pass
        assert_that(nti_mimetype_from_object(Ichigo),
                    is_('application/vnd.nextthought.ichigo'))

        @interface.implementer(IContentTypeAware)
        class Aizen(object):
            mimeType = 'application/vnd.nextthought.aizen'
        assert_that(nti_mimetype_from_object(Aizen),
                    is_('application/vnd.nextthought.aizen'))

        class Suigetsu(object):

            def __conform__(self, iface):
                if IContentTypeAware.isOrExtends(iface):
                    return Aizen()

        assert_that(nti_mimetype_from_object(Suigetsu()),
                    is_('application/vnd.nextthought.aizen'))

        class ICaptain(IContentTypeMarker):
            pass

        @interface.implementer(ICaptain)
        class Zaraki(object):
            pass

        assert_that(nti_mimetype_from_object(Zaraki),
                    is_('application/vnd.nextthought.captain'))

        assert_that(nti_mimetype_from_object('application/vnd.nextthought.captain'),
                    is_('application/vnd.nextthought.captain'))

        assert_that(nti_mimetype_from_object('invalid'),
                    is_(none()))

        assert_that(nti_mimetype_from_object(None),
                    is_(none()))


class TestCoverage(unittest.TestCase):

    def test_safe_by(self):
        safe_by(IContentTypeAware, object())

    def test_nti_mimetype_from_object(self):
        class ICaptain(IContentTypeMarker):
            pass

        @interface.implementer(ICaptain)
        class Toshiro(object):
            pass
        obj = Toshiro()
        interface.alsoProvides(obj, IContentTypeMarker)
        assert_that(nti_mimetype_from_object(obj),
                    is_('application/vnd.nextthought.captain'))

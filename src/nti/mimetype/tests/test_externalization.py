#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import has_entry
from hamcrest import assert_that

import unittest

from zope import interface

from nti.externalization.interfaces import StandardExternalFields
from nti.externalization.interfaces import IInternalObjectExternalizer

from nti.externalization.externalization import to_external_object
from nti.externalization.externalization import decorate_external_mapping

from nti.mimetype.tests import SharedConfiguringTestLayer

CLASS = StandardExternalFields.CLASS
MIMETYPE = StandardExternalFields.MIMETYPE


@interface.implementer(IInternalObjectExternalizer)
class Bleach(object):

    mimeType = mime_type = 'application/vnd.nextthought.bleach'

    def toExternalObject(self, **unused_kwargs):
        return {CLASS: 'Bleach'}


class TestExternalization(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_decorator(self):
        b = Bleach()
        ext_obj = to_external_object(b)
        decorate_external_mapping(b, ext_obj)
        assert_that(ext_obj,
                    has_entry(MIMETYPE, is_('application/vnd.nextthought.bleach')))

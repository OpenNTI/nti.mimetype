#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

__all__ = ['MimeTypeDecorator']

from zope import component
from zope import interface

from nti.externalization.interfaces import StandardExternalFields
from nti.externalization.interfaces import IExternalMappingDecorator

from nti.externalization.singleton import SingletonDecorator

from nti.mimetype.mimetype import nti_mimetype_from_object

CLASS = StandardExternalFields.CLASS
MIMETYPE = StandardExternalFields.MIMETYPE


def decorateMimeType(orig, result):
    if CLASS in result and MIMETYPE not in result:
        mime_type = nti_mimetype_from_object(orig, 0)
        if mime_type:
            result[MIMETYPE] = mime_type
            return mime_type
    return None


@component.adapter(object)
@interface.implementer(IExternalMappingDecorator)
class MimeTypeDecorator(object):

    __metaclass__ = SingletonDecorator

    def decorateExternalMapping(self, orig, result):
        decorateMimeType(orig, result)

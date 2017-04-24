#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import unicode_literals, print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
import csv
import codecs
import mimetypes as p_mimetypes

from zope.mimetype.interfaces import IContentTypeAware

from nti.mimetype.mimetype import rfc2047MimeTypeConstraint


def _add_local_types():
    path = os.path.join(os.path.dirname(__file__), "mimetypes.csv")
    with codecs.open(path, "r", encoding="utf-8") as fp:
        reader = csv.reader(fp)
        for row in reader:
            mimeType = row[0]
            for ext in [e.strip().lower() for e in row[2].split(',')]:
                ext = '.' + ext if not ext.startswith('.') else ext
                p_mimetypes.add_type(mimeType, ext)

_add_local_types()
del _add_local_types


def _patch():
    # TODO: This is wrong for interface
    mimeType = IContentTypeAware[u'mimeType']
    mimeType.constraint = rfc2047MimeTypeConstraint

_patch()
del _patch


def patch():
    pass

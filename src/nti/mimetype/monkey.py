#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import csv
import codecs
import mimetypes as p_mimetypes

from zope.mimetype.interfaces import IContentTypeAware

from nti.base.deprecation import moved

from nti.mimetype.mimetype import rfc2047MimeTypeConstraint

logger = __import__('logging').getLogger(__name__)


def _add_local_types():
    logger.debug('Loading additional mimetypes')
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
    mimeType = IContentTypeAware['mimeType']
    mimeType.constraint = rfc2047MimeTypeConstraint

    moved('nti.mimetype.interfaces', 'nti.base.interfaces')


_patch()
del _patch


def patch():
    pass

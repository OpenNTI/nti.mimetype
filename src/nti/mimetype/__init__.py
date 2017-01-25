#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
import csv

import mimetypes as p_mimetypes

from nti.mimetype.externalization import decorateMimeType

from nti.mimetype.mimetype import nti_mimetype_from_object

from nti.mimetype.monkey import patch
patch()
del patch


def _add_local_types():
    path = os.path.join(os.path.dirname(__file__), "mimetypes.csv")
    with open(path, "rU") as fp:
        reader = csv.reader(fp)
        for row in reader:
            mimeType = row[0]
            for ext in [e.strip().lower() for e in row[2].split(',')]:
                ext = '.' + ext if not ext.startswith('.') else ext
                p_mimetypes.add_type(mimeType, ext)

_add_local_types()
del _add_local_types


def guess_type(url, strict=True):
    return p_mimetypes.guess_type(url, strict) if url else (None, None)


def guess_extension(name, strict=True):
    return p_mimetypes.guess_extension(name, strict)

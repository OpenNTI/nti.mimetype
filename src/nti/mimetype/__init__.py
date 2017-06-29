#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import mimetypes as p_mimetypes

from nti.mimetype.externalization import decorateMimeType

from nti.mimetype.mimetype import nti_mimetype_from_object

from nti.mimetype.monkey import patch
patch()
del patch


def guess_type(url, strict=True):
    return p_mimetypes.guess_type(url, strict) if url else (None, None)


def guess_extension(name, strict=True):
    return p_mimetypes.guess_extension(name, strict)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import mimetypes as p_mimetypes

logger = __import__('logging').getLogger(__name__)


def guess_type(url, strict=True):
    return p_mimetypes.guess_type(url, strict) if url else (None, None)


def guess_extension(name, strict=True):
    return p_mimetypes.guess_extension(name, strict)


from nti.mimetype.monkey import patch
patch()
del patch

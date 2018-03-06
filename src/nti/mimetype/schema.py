#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import re

token_re = r"[!#$%&'*+\-.\d^_`a-z{|}~]+"
mime_type_rx = re.compile("%s/%s(;.*)*" % (token_re, token_re))

logger = __import__('logging').getLogger(__name__)


def rfc2047MimeTypeConstraint(value):
    """
    Return `True` iff `value` is a syntactically legal MIME type.
    """
    return bool(mime_type_rx.match(value) is not None)
mime_type_constraint = mimeTypeConstraint = rfc2047MimeTypeConstraint

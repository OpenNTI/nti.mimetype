#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import six

logger = __import__('logging').getLogger(__name__)

if six.PY3:  # pragma: no cover
    def native_(s, encoding='latin-1', errors='strict'):
        """ 
        If ``s`` is an instance of ``text_type``, return
        ``s``, otherwise return ``str(s, encoding, errors)``
        """
        if isinstance(s, six.text_type):
            return s
        return str(s, encoding, errors)
else:  # pragma: no cover
    def native_(s, encoding='latin-1', errors='strict'):
        """ 
        If ``s`` is an instance of ``text_type``, return
        ``s.encode(encoding, errors)``, otherwise return ``str(s)``
        """
        if isinstance(s, six.text_type):
            return s.encode(encoding, errors)
        return str(s)

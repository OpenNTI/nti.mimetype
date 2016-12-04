#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import unicode_literals, print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope.mimetype.interfaces import IContentTypeAware

from nti.mimetype.mimetype import mimeTypeConstraint

def _patch():
	# use a proper mime-type validation
	mimeType = IContentTypeAware['mimeType']
	mimeType.constraint = mimeTypeConstraint

def patch():
	pass

_patch()
del _patch

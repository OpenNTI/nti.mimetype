#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

try:
	from nti.coremetadata.interfaces import IContentTypeMarker
except ImportError:
	class IContentTypeMarker(interface.Interface):
		pass
IContentTypeMarker = IContentTypeMarker

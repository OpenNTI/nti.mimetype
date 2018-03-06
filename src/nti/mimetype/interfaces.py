#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=inherit-non-class,expression-not-assigned

from zope import interface


class IContentTypeMarker(interface.Interface):
    """
    Marker interface for deriving mimetypes from class names.
    """


class IDict(interface.Interface):
    """
    Marker interface for dicts
    """
interface.classImplements(dict, IDict)

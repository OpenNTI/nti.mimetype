#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Having to do with mime types.

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import re
import weakref
import warnings

from zope import component
from zope import interface

from zope.mimetype.interfaces import IContentTypeAware

from nti.base.interfaces import IContentTypeMarker

from nti.property.property import alias

#: The base mimetype for items in this package.
#: NOTE: Mimetypes should be bytes, not unicode
MIME_BASE = b'application/vnd.nextthought'

#: The extension on the base mimetype explicitly requesting
#: JSON format data
MIME_EXT_JSON = b'+json'

#: The extension on the base mimetype explicitly requesting
#: plist format data
MIME_EXT_PLIST = b'+plist'

#: The base mimetype with json
MIME_BASE_JSON = MIME_BASE + MIME_EXT_JSON

#: The base mimetype with plist
MIME_BASE_PLIST = MIME_BASE + MIME_EXT_PLIST

_token_re = r"[!#$%&'*+\-.\d^_`a-z{|}~]+"
_mime_type_rx = re.compile("%s/%s(;.*)*" % (_token_re, _token_re))


def mimeTypeConstraint(value):
    """
    Return `True` iff `value` is a syntactically legal MIME type.
    """
    return bool(_mime_type_rx.match(value) is not None)
mime_type_constraint = mimeTypeConstraint


@interface.implementer(IContentTypeAware)
@component.adapter(IContentTypeMarker)
class ContentTypeMarkerTypeAwareAdapter(object):
    """
    Makes any :class:IResource into an :class:IContentTypeAware
    object by using its class name.
    """

    def __init__(self, obj):
        # Not type(obj) to work with proxies
        self.mime_type = nti_mimetype_with_class(obj.__class__)
        self.parameters = None

    mimeType = alias('mime_type')

ContentTypeMarkeTypeAwareAdapter = ContentTypeMarkerTypeAwareAdapter  # BBB

_mm_types = weakref.WeakSet()


class _ClassProperty(property):

    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class ModeledContentTypeAwareRegistryMetaclass(type):
    """
    A metaclass for classes whose mimetype derives from their class.

    This class declares one property, `mime_types`, which is an
    iterable of the string values of all known modeled
    content types (those that use this metaclass).

    A second property, `external_mime_types`, is an iterable
    across the string values of all known modeled content
    types which can be directly created given external input.

    .. warning::

            If you are going to implement other interfaces, the metaclass
            definition *must* be the first statement in the class, above
            the :func:`zope.interface.implements` statement. (But using
             :func:`zope.interface.implementer` avoids this problem altogether.)

    """
    # A metaclass might be overkill for this??

    @_ClassProperty
    @classmethod
    def mime_types(mcs):
        return {x.mimeType for x in _mm_types}

    @_ClassProperty
    @classmethod
    def external_mime_types(mcs):
        return {x.mimeType for x in _mm_types if getattr(x, '__external_can_create__', False)}

    def __new__(cls, name, bases, cls_dict):
        if '__eq__' in cls_dict and '__hash__' not in cls_dict:
            # This is a deprecated scenario; but the built-in DeprecationWarning includes
            # no useful information (it points to the metaclass)
            # (Because we are almost always used in a class that is being decorated by
            # zope.interface or zope.component, we issue a warning for stacklevel two and
            # three to get the expected behaviour)
            warnings.warn("Overriding __eq__ blocks inheritance of __hash__ in 3.x",
                          DeprecationWarning, stacklevel=2)
            warnings.warn("Overriding __eq__ blocks inheritance of __hash__ in 3.x",
                          DeprecationWarning, stacklevel=3)

        new_type = type.__new__(cls, name, bases, cls_dict)
        # elide internal classes. (In the future, we may want
        # finer control with a class dictionary attribute.)
        # Also don't overwrite an existing value
        if not name.startswith('_'):
            if 'mime_type' not in cls_dict:  # legacy
                mimeType = nti_mimetype_with_class(new_type)
                new_type.mimeType = new_type.mime_type = mimeType
            elif 'mimeType' not in cls_dict:
                new_type.mimeType = new_type.mime_type
            new_type.parameters = None
            interface.classImplements(new_type, IContentTypeAware)
            _mm_types.add(new_type)
        return new_type

from dolmen.builtins import IDict

from nti.externalization.interfaces import IMimeObjectFactory


@interface.implementer(IMimeObjectFactory)
@component.adapter(IDict)
def ModeledContentTypeMimeFactory(externalized_object):
    """
    A generic adapter factory to find specific factories (types)
    based on the mimetype of an object.
    """
    # TODO: An optimization might be to register a specific factory
    # each time a class is created?
    mime_name = externalized_object.get('MimeType')
    for x in _mm_types:
        if x.mime_type == mime_name and getattr(x, '__external_can_create__', False):
            return x


def is_nti_mimetype(obj):
    """
    :return: Whether `obj` is a string representing an NTI mimetype.
    """
    try:
        return mimeTypeConstraint(obj.lower()) and obj.lower().startswith(MIME_BASE)
    except (TypeError, AttributeError):
        return False


def nti_mimetype_class(content_type):
    """
    :return: The `class` portion of the NTI mimetype given. Undefined
            if not an NTI mimetype. Note that this will be all lowercase.

    EOD
    """
    if is_nti_mimetype(content_type):
        # The last dotted section
        cname = content_type.split('.')[-1]
        # Minus anything with +
        cname = cname.split('+')[0]
        # Which must not be empty, and must not be 'nextthought'
        return cname.lower() if (cname and cname != 'nextthought') else None


def nti_mimetype_with_class(clazz):
    """
    Returns a ASCII string.
    """

    name = b''
    if isinstance(clazz, type):
        name = b'.' + clazz.__name__
    elif isinstance(clazz, basestring):
        name = b'.' + clazz.encode('ascii')

    return MIME_BASE + name.lower()


def _safe_by(meth, obj):
    # These tend to use hashing, which tends
    # to blow up on builtin objects like dicts
    try:
        return meth(obj)
    except TypeError:
        return False


def nti_mimetype_from_object(obj, use_class=True):
    """
    Return the mimetype for the object, or None.

    If the object is :class:`.IContentTypeAware`, that value will be
    returned. If it is :class:`interfaces.IModeledContent`, then
    a value will be derived from that. Otherwise, if it is a recognized
    class, a value will be derived from that. Finally, if it
    is a string that fits the :meth:`mimeTypeConstraint`, that will
    be returned.

    :param bool use_class: If true (the default), then the class of the object
            will be a candidate if nothing else matches.
    """
    # IContentTypeAware uses mimeType; much of our legacy code has a mime_type
    for an in 'mimeType', 'mime_type':
        mimeType = getattr(obj, an, None)
        if mimeType:
            return mimeType

    content_type_aware = IContentTypeAware(obj, None)
    if content_type_aware:
        return content_type_aware.mimeType

    if _safe_by(IContentTypeMarker.providedBy, obj):
        # Find the IModeledContent subtype that it implements.
        # The most derived will be in the list providedBy.
        for iface in interface.providedBy(obj):
            if iface.extends(IContentTypeMarker):
                return nti_mimetype_with_class(iface.__name__[1:])

    # A class that can become IModeledContent
    # NOTE: It is critically important to only call this on class objects.
    # If we call it on an instance that happens to be callable, zope.interface
    # will happily assign to the instance's __dict__ and then we won't be able to
    # unpickle it if the instance ever becomes non-callable:
    #   zope.interface-4.0.1-py2.7-macosx-10.7-x86_64.egg/zope/interface/declarations.py",
    #     line 189, in implementedByFallback
    #         raise TypeError("ImplementedBy called for non-factory", cls)
    obj_is_type = isinstance(obj, type)
    if obj_is_type and _safe_by(IContentTypeMarker.implementedBy, obj):
        for iface in interface.implementedBy(obj):
            if iface.extends(IContentTypeMarker):
                return nti_mimetype_with_class(iface.__name__[1:])

    # NOT type(obj), to play well with proxies
    clazz = obj if obj_is_type else obj.__class__
    if use_class and clazz.__module__.startswith('nti.'):
        # NOTE: Must be very careful not to try to print the object in this
        # function. Printing some objects tries to get their external
        # representation, which wants the mimetype, which gets to this function.
        # Infinite recursion.
        # But do log the __class__ value in case the type has been proxied
        logger.debug("Falling back to class to get MIME for %s/%s",
                     clazz, getattr(obj, '__class__', clazz))
        return nti_mimetype_with_class(clazz.__name__)

    if isinstance(obj, basestring) and mimeTypeConstraint(obj):
        return obj


def parse_mime_type(mime_type):
    params = {}
    parts = mime_type.split(';')
    for part in parts or ():
        p = part.split('=')
        if len(p) == 2:
            params[p[0].strip()] = p[1].strip()
    fullType = parts[0].replace('/^\s+/', '').replace('/\s+$/', '')
    if fullType == '*':
        fullType = '*/*'
    typeParts = fullType.split('/')
    return (typeParts[0], typeParts[1], params)

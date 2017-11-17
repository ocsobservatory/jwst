# -*- coding: utf-8 -*-

"""
Defines a ``JWSTTransformType`` used by jwst pipeine transform types.
All types are added automatically to ``_jwst_types`` and the JWSTExtension.

"""
import six

from asdf.asdftypes import ExtensionTypeMeta
from astropy.io.misc.asdf.tags.transform.basic import TransformType
from astropy.io.misc.asdf.types import AstropyTypeMeta

__all__ = ['JWSTTransformType']


_jwst_types = set()


class JWSTTypeMeta(AstropyTypeMeta):
    """
    Keeps track of `JWSTType` subclasses that are created so that they can
    be stored automatically by astropy extensions for ASDF.
    """
    def __new__(mcls, name, bases, attrs):
        cls = super(JWSTTypeMeta, mcls).__new__(mcls, name, bases, attrs)
        # Classes using this metaclass are automatically added to the list of
        # astropy extensions
        if cls.organization == 'stsci.edu' and cls.standard == 'jwst_pipeline':
            _jwst_types.add(cls)

        return cls


@six.add_metaclass(JWSTTypeMeta)
class JWSTTransformType(TransformType):
    """
    This class represents types that have schemas and tags implemented within
    the jwst pipeline.
    """
    organization = 'stsci.edu'
    standard = 'jwst_pipeline'

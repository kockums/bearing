# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Kockums Bearing - Exceptions
============================

The exception hierarchy shared across bearing. These are pure stdlib
(subclasses of the builtins), so importing them never pulls a dependency.

``External*`` errors flag bad *external input* — a malformed request
parameter, an unparseable CRS URI, a bounding box with the wrong arity —
as distinct from internal programming errors. A host (e.g. a WFS/WMS
service in ``ortha``) can map them straight to a client-facing 400.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations


# =============================================================================
# Base
# =============================================================================

class BearingError(Exception):
    """Root of every bearing-specific exception."""


# =============================================================================
# External-input errors
# =============================================================================

class ExternalError(BearingError):
    """Base for errors caused by bad external input (not a bearing bug)."""


class ExternalParsingError(ExternalError, ValueError):
    """External input could not be parsed (wrong shape, arity, or syntax)."""


class ExternalValueError(ExternalError, ValueError):
    """External input parsed but carried an invalid or unsupported value."""

# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Kockums Bearing - IO Package
============================

Interchange codecs over GeoJSON-style geometry dictionaries. WKT today; WKB
and GeoJSON (RFC 7946) are the next additions (see TODO).

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Local Modules
from bearing.io import wkt
from bearing.io.wkt import WKTError


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "WKTError",
    "wkt",
]

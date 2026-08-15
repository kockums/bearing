# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Kockums Bearing - Geospatial Module
===================================

Geographic identity and extent types: the :class:`CRS` reference-system
parser, the :class:`BoundingBox`, and the WGS84 constants. These are the
dependency-free members of the package; ``area``, ``grid``, and
``coordinate`` still carry third-party imports (numpy / geojson / pyproj) and
are on the DEPENDENCIES.md ledger for rewrite or relocation — they are not
re-exported here so that ``import bearing.geospatial`` stays clean.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Local Modules
from bearing.geospatial.bounding_box import BoundingBox
from bearing.geospatial.crs import CRS
from bearing.geospatial.wgs84 import WGS84, WGS84_A, WGS84_B, WGS84_F


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "CRS",
    "BoundingBox",
    "WGS84",
    "WGS84_A",
    "WGS84_B",
    "WGS84_F",
]


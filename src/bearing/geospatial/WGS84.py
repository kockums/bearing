# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Kockums Bearing - WGS84
=======================

The WGS84 geographic CRS (EPSG:4326) as a ready-made :class:`CRS` constant,
and the WGS84 ellipsoid parameters used across the geodesy and projection
modules.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Local Modules
from bearing.geospatial.crs import CRS


# =============================================================================
# Ellipsoid parameters
# =============================================================================

#: WGS84 semi-major (equatorial) axis, metres.
WGS84_A: float = 6378137.0

#: WGS84 flattening.
WGS84_F: float = 1.0 / 298.257223563

#: WGS84 semi-minor (polar) axis, metres.
WGS84_B: float = WGS84_A * (1.0 - WGS84_F)


# =============================================================================
# CRS constant
# =============================================================================

#: The WGS84 geographic CRS, EPSG:4326 (lat/long axis order).
WGS84: CRS = CRS.from_srid(4326)

# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Kockums Bearing - Projection Package
====================================

Map projections, dependency-free. Web Mercator (EPSG:3857) today; the
transverse-Mercator / UTM Krüger series is the next addition (see TODO).

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Local Modules
from bearing.projection.mercator import (
    EARTH_RADIUS,
    MAX_LATITUDE,
    ORIGIN_SHIFT,
    lonlat_to_meters,
    lonlat_to_pixels,
    lonlat_to_tile,
    meters_to_lonlat,
    pixels_to_lonlat,
    tile_bounds,
    tile_bounds_meters,
)


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "EARTH_RADIUS",
    "MAX_LATITUDE",
    "ORIGIN_SHIFT",
    "lonlat_to_meters",
    "lonlat_to_pixels",
    "lonlat_to_tile",
    "meters_to_lonlat",
    "pixels_to_lonlat",
    "tile_bounds",
    "tile_bounds_meters",
]

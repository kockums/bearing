# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Kockums Bearing - Geodesy Package
=================================

Dependency-free geodesy: great-circle (spherical) formulae and the
ellipsoidal geodesic (Karney's direct and inverse problems).

All angles are radians internally; the public helpers whose names end in
``_deg`` take and return degrees. Longitude is east-positive, latitude
north-positive. Distances are metres.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Local Modules
from bearing.geodesy.ellipsoidal import Geodesic, WGS84
from bearing.geodesy.spherical import (
    EARTH_MEAN_RADIUS,
    along_track_distance,
    cross_track_distance,
    destination,
    distance,
    final_bearing,
    initial_bearing,
    interpolate,
    midpoint,
)


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "EARTH_MEAN_RADIUS",
    "Geodesic",
    "WGS84",
    "along_track_distance",
    "cross_track_distance",
    "destination",
    "distance",
    "final_bearing",
    "initial_bearing",
    "interpolate",
    "midpoint",
]

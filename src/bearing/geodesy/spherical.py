# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Kockums Bearing - Spherical Geodesy
===================================

Great-circle geodesy on a sphere: the exact, closed-form formulae for
distance, bearing, destination, midpoint, interpolation, and cross/along
track distance.

These are correct for a spherical Earth and are the numerically-stable base
the ellipsoidal solver (``bearing.geodesy.ellipsoidal``) is validated
against. Every function takes and returns **degrees** at the API edge and
works in **radians** internally; distances are metres on a sphere of the
given ``radius`` (mean Earth radius by default).

References
----------
- Ed Williams, "Aviation Formulary" (great-circle navigation).
- The ``atan2``-based haversine variant, stable for both tiny and
  antipodal separations.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
import math


# =============================================================================
# Constants
# =============================================================================

# IUGG mean radius R1 = (2a + b) / 3 for WGS84, metres.
EARTH_MEAN_RADIUS: float = 6371008.771415059


# =============================================================================
# Functions
# =============================================================================

def distance(
    lat1_deg: float,
    lon1_deg: float,
    lat2_deg: float,
    lon2_deg: float,
    radius: float = EARTH_MEAN_RADIUS,
) -> float:
    """
    Great-circle distance between two points, metres.

    Uses the haversine formula evaluated through ``atan2``, which stays
    accurate for both very short and near-antipodal separations (the plain
    ``acos`` form loses precision at small angles).
    """
    phi1 = math.radians(lat1_deg)
    phi2 = math.radians(lat2_deg)
    dphi = math.radians(lat2_deg - lat1_deg)
    dlmb = math.radians(lon2_deg - lon1_deg)
    a = (
        math.sin(dphi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlmb / 2.0) ** 2
    )
    return radius * 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))


def initial_bearing(
    lat1_deg: float,
    lon1_deg: float,
    lat2_deg: float,
    lon2_deg: float,
) -> float:
    """
    Initial great-circle bearing from point 1 toward point 2, in degrees
    clockwise from true north, normalised to ``[0, 360)``.
    """
    phi1 = math.radians(lat1_deg)
    phi2 = math.radians(lat2_deg)
    dlmb = math.radians(lon2_deg - lon1_deg)
    y = math.sin(dlmb) * math.cos(phi2)
    x = (
        math.cos(phi1) * math.sin(phi2)
        - math.sin(phi1) * math.cos(phi2) * math.cos(dlmb)
    )
    return math.degrees(math.atan2(y, x)) % 360.0


def final_bearing(
    lat1_deg: float,
    lon1_deg: float,
    lat2_deg: float,
    lon2_deg: float,
) -> float:
    """
    Final bearing arriving at point 2 (degrees from north). The bearing of
    the reverse geodesic, flipped 180 degrees.
    """
    back = initial_bearing(lat2_deg, lon2_deg, lat1_deg, lon1_deg)
    return (back + 180.0) % 360.0


def destination(
    lat1_deg: float,
    lon1_deg: float,
    bearing_deg: float,
    dist: float,
    radius: float = EARTH_MEAN_RADIUS,
) -> tuple[float, float]:
    """
    The point reached by travelling ``dist`` metres from the start along the
    initial ``bearing_deg`` (the spherical direct problem). Returns
    ``(lat_deg, lon_deg)`` with longitude normalised to ``(-180, 180]``.
    """
    phi1 = math.radians(lat1_deg)
    lmb1 = math.radians(lon1_deg)
    theta = math.radians(bearing_deg)
    delta = dist / radius  # angular distance
    sin_phi2 = (
        math.sin(phi1) * math.cos(delta)
        + math.cos(phi1) * math.sin(delta) * math.cos(theta)
    )
    phi2 = math.asin(max(-1.0, min(1.0, sin_phi2)))
    y = math.sin(theta) * math.sin(delta) * math.cos(phi1)
    x = math.cos(delta) - math.sin(phi1) * sin_phi2
    lmb2 = lmb1 + math.atan2(y, x)
    return math.degrees(phi2), _wrap_lon(math.degrees(lmb2))


def midpoint(
    lat1_deg: float,
    lon1_deg: float,
    lat2_deg: float,
    lon2_deg: float,
) -> tuple[float, float]:
    """
    The half-way point along the great circle between the two points,
    ``(lat_deg, lon_deg)``.
    """
    return interpolate(lat1_deg, lon1_deg, lat2_deg, lon2_deg, 0.5)


def interpolate(
    lat1_deg: float,
    lon1_deg: float,
    lat2_deg: float,
    lon2_deg: float,
    fraction: float,
) -> tuple[float, float]:
    """
    The point a given ``fraction`` (0 at point 1, 1 at point 2) of the way
    along the great circle, via spherical linear interpolation of the two
    surface unit vectors. Handles the coincident-point case (returns point 1).
    """
    phi1 = math.radians(lat1_deg)
    lmb1 = math.radians(lon1_deg)
    phi2 = math.radians(lat2_deg)
    lmb2 = math.radians(lon2_deg)

    # Angular separation via haversine (stable at small angles).
    dphi = phi2 - phi1
    dlmb = lmb2 - lmb1
    hav = (
        math.sin(dphi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlmb / 2.0) ** 2
    )
    delta = 2.0 * math.atan2(math.sqrt(hav), math.sqrt(1.0 - hav))
    if delta == 0.0:
        return lat1_deg, lon1_deg

    a = math.sin((1.0 - fraction) * delta) / math.sin(delta)
    b = math.sin(fraction * delta) / math.sin(delta)
    x = a * math.cos(phi1) * math.cos(lmb1) + b * math.cos(phi2) * math.cos(lmb2)
    y = a * math.cos(phi1) * math.sin(lmb1) + b * math.cos(phi2) * math.sin(lmb2)
    z = a * math.sin(phi1) + b * math.sin(phi2)
    phi = math.atan2(z, math.hypot(x, y))
    lmb = math.atan2(y, x)
    return math.degrees(phi), _wrap_lon(math.degrees(lmb))


def cross_track_distance(
    lat_deg: float,
    lon_deg: float,
    lat1_deg: float,
    lon1_deg: float,
    lat2_deg: float,
    lon2_deg: float,
    radius: float = EARTH_MEAN_RADIUS,
) -> float:
    """
    Signed distance of a point from the great circle defined by points 1→2,
    metres. Positive left of the path, negative right (following the usual
    aviation convention).
    """
    d13 = distance(lat1_deg, lon1_deg, lat_deg, lon_deg, radius) / radius
    theta13 = math.radians(initial_bearing(lat1_deg, lon1_deg, lat_deg, lon_deg))
    theta12 = math.radians(initial_bearing(lat1_deg, lon1_deg, lat2_deg, lon2_deg))
    return math.asin(
        max(-1.0, min(1.0, math.sin(d13) * math.sin(theta13 - theta12)))
    ) * radius


def along_track_distance(
    lat_deg: float,
    lon_deg: float,
    lat1_deg: float,
    lon1_deg: float,
    lat2_deg: float,
    lon2_deg: float,
    radius: float = EARTH_MEAN_RADIUS,
) -> float:
    """
    Distance from point 1 to the point on the great circle 1→2 nearest the
    given point (the foot of the cross-track perpendicular), metres.
    """
    d13 = distance(lat1_deg, lon1_deg, lat_deg, lon_deg, radius) / radius
    xt = cross_track_distance(
        lat_deg, lon_deg, lat1_deg, lon1_deg, lat2_deg, lon2_deg, radius
    ) / radius
    # Guard the tiny domain slip when the point is essentially on the path.
    c = math.cos(d13) / math.cos(xt)
    return math.acos(max(-1.0, min(1.0, c))) * radius


# =============================================================================
# Helpers
# =============================================================================

def _wrap_lon(lon_deg: float) -> float:
    """Normalise a longitude to ``(-180, 180]``."""
    wrapped = math.fmod(lon_deg + 180.0, 360.0)
    if wrapped <= 0.0:
        wrapped += 360.0
    return wrapped - 180.0

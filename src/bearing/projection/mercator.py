# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Kockums Bearing - Web Mercator Projection
=========================================

The spherical (Web / "Pseudo") Mercator projection, EPSG:3857 — the
projection every slippy-map / XYZ tile pipeline is drawn in. It treats the
Earth as a sphere of radius equal to the WGS84 semi-major axis, so it is
*not* conformal to the true ellipsoid, but it is the ubiquitous web-tiling
standard.

This module provides three coordinate spaces and the exact transforms
between them:

- **geographic**  ``(lon_deg, lat_deg)``  (WGS84 degrees)
- **world metres** ``(x, y)``             (EPSG:3857, metres from origin)
- **tile pixels**  ``(px, py)`` at a zoom, and the enclosing ``(z, x, y)``
  XYZ tile (origin top-left, y increasing south — the slippy-map convention).

Latitude is clamped to the projection limit (~±85.0511°) where the Mercator
y diverges. Standard library only.

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

#: WGS84 semi-major axis, metres — the Web-Mercator sphere radius.
EARTH_RADIUS: float = 6378137.0

#: Half the equatorial circumference — the world half-extent in metres.
ORIGIN_SHIFT: float = math.pi * EARTH_RADIUS  # 20037508.342789244

#: The Mercator latitude limit, degrees (where y = ±ORIGIN_SHIFT).
MAX_LATITUDE: float = 85.05112877980659


# =============================================================================
# Geographic <-> world metres
# =============================================================================

def lonlat_to_meters(lon_deg: float, lat_deg: float) -> tuple[float, float]:
    """
    Project geographic ``(lon, lat)`` degrees to EPSG:3857 world metres.
    Latitude is clamped to :data:`MAX_LATITUDE`.
    """
    lat = max(-MAX_LATITUDE, min(MAX_LATITUDE, lat_deg))
    x = math.radians(lon_deg) * EARTH_RADIUS
    y = math.log(math.tan(math.pi / 4.0 + math.radians(lat) / 2.0)) * EARTH_RADIUS
    return x, y


def meters_to_lonlat(x: float, y: float) -> tuple[float, float]:
    """Inverse of :func:`lonlat_to_meters`: world metres to ``(lon, lat)``."""
    lon = math.degrees(x / EARTH_RADIUS)
    lat = math.degrees(2.0 * math.atan(math.exp(y / EARTH_RADIUS)) - math.pi / 2.0)
    return lon, lat


# =============================================================================
# Geographic <-> tile pixels / XYZ tiles
# =============================================================================

def lonlat_to_pixels(
    lon_deg: float,
    lat_deg: float,
    zoom: int,
    tile_size: int = 256,
) -> tuple[float, float]:
    """
    Project ``(lon, lat)`` to global pixel coordinates at ``zoom`` (origin
    top-left, x east, y south). The world is ``tile_size * 2**zoom`` pixels
    square.
    """
    lat = max(-MAX_LATITUDE, min(MAX_LATITUDE, lat_deg))
    world = float(tile_size) * (1 << zoom)
    px = (lon_deg + 180.0) / 360.0 * world
    sin_lat = math.sin(math.radians(lat))
    py = (
        0.5 - math.log((1.0 + sin_lat) / (1.0 - sin_lat)) / (4.0 * math.pi)
    ) * world
    return px, py


def pixels_to_lonlat(
    px: float,
    py: float,
    zoom: int,
    tile_size: int = 256,
) -> tuple[float, float]:
    """Inverse of :func:`lonlat_to_pixels`."""
    world = float(tile_size) * (1 << zoom)
    lon = px / world * 360.0 - 180.0
    n = math.pi - 2.0 * math.pi * py / world
    lat = math.degrees(math.atan(math.sinh(n)))
    return lon, lat


def lonlat_to_tile(
    lon_deg: float,
    lat_deg: float,
    zoom: int,
) -> tuple[int, int]:
    """
    The XYZ tile ``(x, y)`` at ``zoom`` containing ``(lon, lat)`` (origin
    top-left, y increasing south). Tile indices are clamped to
    ``[0, 2**zoom - 1]``.
    """
    lat = max(-MAX_LATITUDE, min(MAX_LATITUDE, lat_deg))
    n = 1 << zoom
    xt = int((lon_deg + 180.0) / 360.0 * n)
    lat_rad = math.radians(lat)
    yt = int(
        (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n
    )
    xt = max(0, min(n - 1, xt))
    yt = max(0, min(n - 1, yt))
    return xt, yt


def tile_bounds(x: int, y: int, zoom: int) -> tuple[float, float, float, float]:
    """
    The geographic bounds ``(west, south, east, north)`` in degrees of XYZ
    tile ``(x, y)`` at ``zoom``.
    """
    n = 1 << zoom
    west = x / n * 360.0 - 180.0
    east = (x + 1) / n * 360.0 - 180.0
    north = math.degrees(math.atan(math.sinh(math.pi * (1.0 - 2.0 * y / n))))
    south = math.degrees(
        math.atan(math.sinh(math.pi * (1.0 - 2.0 * (y + 1) / n)))
    )
    return west, south, east, north


def tile_bounds_meters(
    x: int, y: int, zoom: int
) -> tuple[float, float, float, float]:
    """
    The EPSG:3857 bounds ``(left, bottom, right, top)`` in metres of XYZ tile
    ``(x, y)`` at ``zoom`` — the world square is ``[-ORIGIN_SHIFT,
    ORIGIN_SHIFT]`` per axis, split into ``2**zoom`` tiles (origin top-left).

    The pure-arithmetic replacement for ``mercantile.xy_bounds`` — the tile
    grid in Web-Mercator metres is exact and needs no external library.
    """
    n = 1 << zoom
    tile_span = 2.0 * ORIGIN_SHIFT / n
    left = -ORIGIN_SHIFT + x * tile_span
    right = left + tile_span
    top = ORIGIN_SHIFT - y * tile_span
    bottom = top - tile_span
    return left, bottom, right, top

# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Kockums Bearing - Vector Tile Addressing
========================================

A :class:`VectorTile` — the **addressing** of one XYZ vector tile: its
``(x, y, z)`` index, its geographic bounds, and its EPSG:3857 bounds. Pure
arithmetic via :mod:`bearing.projection.mercator` (this replaces the former
``mercantile`` dependency).

Scope note (dependency doctrine): the *generation* of tile payloads — Mapbox
Vector Tile / protobuf encoding, feature querysets, clipping and buffering
against a spatial database — is a pipeline concern and belongs downstream in
``ortha``. What stays here is the geometry-only addressing every such
pipeline needs, dependency-free. The former Django ``VectorTile`` mixin
(``get_queryset`` / ``get_tile`` protobuf) is intentionally **not** carried
into the pure core.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from dataclasses import dataclass

# Import | Local Modules
from bearing.geospatial.bounding_box import BoundingBox
from bearing.projection import mercator


# =============================================================================
# Class
# =============================================================================

@dataclass(frozen=True)
class VectorTile:
    """
    An XYZ tile address ``(x, y, z)`` (origin top-left, y increasing south),
    with the standard tile-render extent/buffer parameters.

    Attributes
    ----------
    x, y, z : int
        Tile column, row, and zoom.
    extent : int
        Tile coordinate extent (MVT default 4096).
    buffer : int
        Buffer, in tile coordinates, drawn around the tile edge.
    """

    x: int
    y: int
    z: int
    extent: int = 4096
    buffer: int = 256

    def bounds(self) -> tuple[float, float, float, float]:
        """Geographic bounds ``(west, south, east, north)`` in degrees."""
        return mercator.tile_bounds(self.x, self.y, self.z)

    def bounds_meters(self) -> tuple[float, float, float, float]:
        """EPSG:3857 bounds ``(left, bottom, right, top)`` in metres."""
        return mercator.tile_bounds_meters(self.x, self.y, self.z)

    def bounding_box(self) -> BoundingBox:
        """The geographic extent as a :class:`BoundingBox` (WGS84)."""
        west, south, east, north = self.bounds()
        from bearing.geospatial.wgs84 import WGS84
        return BoundingBox(west, south, east, north, crs=WGS84)

    @classmethod
    def containing(cls, lon_deg: float, lat_deg: float, zoom: int) -> "VectorTile":
        """The tile at ``zoom`` containing the given ``(lon, lat)``."""
        x, y = mercator.lonlat_to_tile(lon_deg, lat_deg, zoom)
        return cls(x, y, zoom)

    def __repr__(self) -> str:
        return f"VectorTile(z={self.z}, x={self.x}, y={self.y})"

"""Helper classes to handle geometry data types.

This includes the CRS parsing, coordinate transforms and bounding box object.
The bounding box can be calculated within Python, or read from a database result.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from decimal import Decimal
from functools import lru_cache

from django.contrib.gis.gdal import AxisOrder, CoordTransform, SpatialReference
from django.contrib.gis.geos import GEOSGeometry, Polygon

from .crs import CRS

from ..exceptions import ExternalParsingError, ExternalValueError

CRS_URN_REGEX = re.compile(
    r"^urn:(?P<domain>[a-z]+)"
    r":def:crs:(?P<authority>[a-z]+)"
    r":(?P<version>[0-9]+\.[0-9]+(\.[0-9]+)?)?"
    r":(?P<id>[0-9]+|crs84)"
    r"$",
    re.IGNORECASE,
)

__all__ = [
    "BoundingBox",
]


@dataclass
class BoundingBox:
    """A bounding box that describes the extent of a map layer"""

    south: Decimal  # longitude
    west: Decimal  # latitude
    north: Decimal  # longitude
    east: Decimal  # latitude
    crs: CRS | None = None

    @classmethod
    def from_string(cls, bbox):
        """Parse the bounding box from an input string.

        It can either be 4 coordinates, or 4 coordinates with a special reference system.
        """
        bbox = bbox.split(",")
        if not (4 <= len(bbox) <= 5):
            raise ExternalParsingError(
                f"Input does not contain bounding box, "
                f"expected 4 or 5 values, not {bbox}."
            )
        return cls(
            Decimal(bbox[0]),
            Decimal(bbox[1]),
            Decimal(bbox[2]),
            Decimal(bbox[3]),
            CRS.from_string(bbox[4]) if len(bbox) == 5 else None,
        )

    @classmethod
    def from_geometry(cls, geometry: GEOSGeometry, crs: CRS | None = None):
        """Construct the bounding box for a geometry"""
        if crs is None:
            crs = CRS.from_srid(geometry.srid)
        elif geometry.srid != crs.srid:
            geometry = crs.apply_to(geometry, clone=True)

        return cls(*geometry.extent, crs=crs)

    @property
    def lower_corner(self):
        return [self.south, self.west]

    @property
    def upper_corner(self):
        return [self.north, self.east]

    def __repr__(self):
        return f"BoundingBox({self.south}, {self.west}, {self.north}, {self.east})"

    def extend_to(
        self, lower_lon: float, lower_lat: float, upper_lon: float, upper_lat: float
    ):
        """Expand the bounding box in-place"""
        self.south = min(self.south, lower_lon)
        self.west = min(self.west, lower_lat)
        self.north = max(self.north, upper_lon)
        self.east = max(self.east, upper_lat)

    def extend_to_geometry(self, geometry: GEOSGeometry):
        """Extend this bounding box with the coordinates of a given geometry."""
        if self.crs is not None and geometry.srid != self.crs.srid:
            geometry = self.crs.apply_to(geometry, clone=True)

        self.extend_to(*geometry.extent)

    def __add__(self, other):
        """Combine both extents into a larger box."""
        if isinstance(other, BoundingBox):
            if other.crs != self.crs:
                raise ValueError(
                    "Can't combine instances with different spatial reference systems"
                )
            return BoundingBox(
                min(self.south, other.south),
                min(self.west, other.west),
                max(self.north, other.north),
                max(self.east, other.east),
            )
        else:
            return NotImplemented

    def as_polygon(self) -> Polygon:
        """Convert the value into a GEOS polygon."""
        polygon = Polygon.from_bbox((self.south, self.west, self.north, self.east))
        if self.crs is not None:
            polygon.srid = self.crs.srid
        return polygon
# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Kockums Bearing - Bounding Box
==============================

A dependency-free axis-aligned geographic :class:`BoundingBox` — the extent
of a map layer, feature, or request, with an optional :class:`CRS`.

This merges and supersedes the former Django/GEOS-backed bounding box: the
core (parse a ``minx,miny,maxx,maxy[,crs]`` string, expand, union,
containment, intersection, centre) is pure arithmetic. The old
``from_geometry`` / ``as_polygon`` returned GEOS objects; the pure analogues
here take and return plain coordinate tuples / rings, so nothing pulls a
dependency. Reprojecting a box between CRSs is delegated (see
:mod:`bearing.geospatial.crs`).

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from dataclasses import dataclass

# Import | Local Modules
from bearing.exceptions import ExternalParsingError
from bearing.geospatial.crs import CRS


# =============================================================================
# Class
# =============================================================================

@dataclass
class BoundingBox:
    """
    An axis-aligned bounding box ``(min_x, min_y, max_x, max_y)`` with an
    optional coordinate reference system.

    The names ``min_x`` / ``max_x`` are axis-order-neutral (x is the first
    ordinate of the box's CRS — longitude for a long/lat CRS, latitude for a
    lat/long one). ``west``/``south``/``east``/``north`` are provided as
    aliases for the common geographic long/lat case.

    Attributes
    ----------
    min_x, min_y, max_x, max_y : float
        The lower and upper corners.
    crs : CRS | None
        The coordinate reference system, or ``None`` if unspecified.
    """

    min_x: float
    min_y: float
    max_x: float
    max_y: float
    crs: CRS | None = None

    # -- Geographic aliases (long/lat convention) --------------------------

    @property
    def west(self) -> float:
        return self.min_x

    @property
    def south(self) -> float:
        return self.min_y

    @property
    def east(self) -> float:
        return self.max_x

    @property
    def north(self) -> float:
        return self.max_y

    @property
    def lower_corner(self) -> list[float]:
        return [self.min_x, self.min_y]

    @property
    def upper_corner(self) -> list[float]:
        return [self.max_x, self.max_y]

    @property
    def width(self) -> float:
        return self.max_x - self.min_x

    @property
    def height(self) -> float:
        return self.max_y - self.min_y

    @property
    def center(self) -> tuple[float, float]:
        return (
            (self.min_x + self.max_x) / 2.0,
            (self.min_y + self.max_y) / 2.0,
        )

    # -- Constructors ------------------------------------------------------

    @classmethod
    def from_string(cls, bbox: str) -> "BoundingBox":
        """
        Parse ``"min_x,min_y,max_x,max_y"`` (4 values) or the same with a
        trailing CRS reference (5 values).

        Raises
        ------
        ExternalParsingError
            If the string does not contain 4 or 5 comma-separated values.
        """
        parts = bbox.split(",")
        if not (4 <= len(parts) <= 5):
            raise ExternalParsingError(
                f"Input does not contain a bounding box; expected 4 or 5 "
                f"values, not {parts!r}."
            )
        crs = CRS.from_string(parts[4]) if len(parts) == 5 else None
        return cls(
            float(parts[0]),
            float(parts[1]),
            float(parts[2]),
            float(parts[3]),
            crs,
        )

    @classmethod
    def from_points(
        cls,
        points,
        crs: CRS | None = None,
    ) -> "BoundingBox":
        """The tightest box enclosing an iterable of ``(x, y)`` points."""
        it = iter(points)
        try:
            x0, y0 = next(it)
        except StopIteration:
            raise ExternalParsingError("cannot build a bbox from no points") \
                from None
        min_x = max_x = float(x0)
        min_y = max_y = float(y0)
        for x, y in it:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        return cls(min_x, min_y, max_x, max_y, crs)

    # -- Mutation / combination -------------------------------------------

    def extend_to(
        self, min_x: float, min_y: float, max_x: float, max_y: float
    ) -> None:
        """Expand this box in place to also cover the given extent."""
        self.min_x = min(self.min_x, min_x)
        self.min_y = min(self.min_y, min_y)
        self.max_x = max(self.max_x, max_x)
        self.max_y = max(self.max_y, max_y)

    def __add__(self, other: object) -> "BoundingBox":
        """The union of two boxes (they must share a CRS)."""
        if isinstance(other, BoundingBox):
            if other.crs != self.crs:
                raise ValueError(
                    "cannot combine bounding boxes with different CRSs"
                )
            return BoundingBox(
                min(self.min_x, other.min_x),
                min(self.min_y, other.min_y),
                max(self.max_x, other.max_x),
                max(self.max_y, other.max_y),
                self.crs,
            )
        return NotImplemented

    # -- Predicates --------------------------------------------------------

    def contains(self, x: float, y: float) -> bool:
        """Whether point ``(x, y)`` lies within (or on) this box."""
        return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y

    def intersects(self, other: "BoundingBox") -> bool:
        """Whether this box overlaps ``other`` (touching counts)."""
        return not (
            other.min_x > self.max_x
            or other.max_x < self.min_x
            or other.min_y > self.max_y
            or other.max_y < self.min_y
        )

    # -- Conversion --------------------------------------------------------

    def as_tuple(self) -> tuple[float, float, float, float]:
        """The extent as ``(min_x, min_y, max_x, max_y)``."""
        return (self.min_x, self.min_y, self.max_x, self.max_y)

    def as_ring(self) -> list[tuple[float, float]]:
        """
        The box as a closed counter-clockwise polygon ring of ``(x, y)``
        corners — the pure-data replacement for the old GEOS ``as_polygon``.
        """
        return [
            (self.min_x, self.min_y),
            (self.max_x, self.min_y),
            (self.max_x, self.max_y),
            (self.min_x, self.max_y),
            (self.min_x, self.min_y),
        ]

    def __repr__(self) -> str:
        return (
            f"BoundingBox({self.min_x}, {self.min_y}, "
            f"{self.max_x}, {self.max_y})"
        )

# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Kockums Bearing - WKT Interchange
=================================

Read and write OGC Simple Features **Well-Known Text**. Geometries are
represented as GeoJSON-style dictionaries — ``{"type": ..., "coordinates":
...}`` (and ``{"type": "GeometryCollection", "geometries": [...]}``) — so
the same object model feeds a future GeoJSON and WKB codec (see TODO).

Supported geometry types (the OGC SF core):

    Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon,
    GeometryCollection

Both 2D (XY) and 3D (XYZ, the ``Z`` tag) are supported, plus the ``EMPTY``
forms. Measured coordinates (the ``M`` / ``ZM`` tags) are parsed to their
dimensionality but raise :class:`NotImplementedError` on emit until the
object model carries M explicitly (TODO phase 2). Standard library only.

References
----------
- OGC 06-103r4, "OpenGIS Simple Features Access - Part 1: Common
  Architecture", the normative WKT grammar.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from typing import Any


# =============================================================================
# Errors
# =============================================================================

class WKTError(ValueError):
    """Raised on malformed WKT input."""


# =============================================================================
# Public API
# =============================================================================

def loads(text: str) -> dict[str, Any]:
    """
    Parse a WKT string into a GeoJSON-style geometry dictionary.

    Raises
    ------
    WKTError
        If the text is not valid WKT.
    NotImplementedError
        For measured (``M`` / ``ZM``) geometries (parsed but not modelled).
    """
    parser = _Parser(text)
    geom = parser.parse_geometry()
    parser.expect_end()
    return geom


def dumps(geometry: dict[str, Any], precision: int | None = None) -> str:
    """
    Serialise a GeoJSON-style geometry dictionary to WKT.

    ``precision`` optionally rounds ordinates to that many decimal places
    (``None`` uses ``repr`` for a lossless round-trip).
    """
    return _dump_geometry(geometry, precision)


# =============================================================================
# Parser
# =============================================================================

_TYPES = {
    "POINT": "Point",
    "LINESTRING": "LineString",
    "POLYGON": "Polygon",
    "MULTIPOINT": "MultiPoint",
    "MULTILINESTRING": "MultiLineString",
    "MULTIPOLYGON": "MultiPolygon",
    "GEOMETRYCOLLECTION": "GeometryCollection",
}


class _Parser:
    """A small recursive-descent WKT parser."""

    def __init__(self, text: str) -> None:
        self._text = text
        self._pos = 0
        self._len = len(text)

    # -- Character-level helpers -------------------------------------------

    def _skip_ws(self) -> None:
        while self._pos < self._len and self._text[self._pos].isspace():
            self._pos += 1

    def _peek(self) -> str:
        self._skip_ws()
        return self._text[self._pos] if self._pos < self._len else ""

    def _word(self) -> str:
        self._skip_ws()
        start = self._pos
        while self._pos < self._len and (
            self._text[self._pos].isalpha()
        ):
            self._pos += 1
        return self._text[start:self._pos].upper()

    def _consume(self, char: str) -> None:
        self._skip_ws()
        if self._pos >= self._len or self._text[self._pos] != char:
            raise WKTError(
                f"expected {char!r} at position {self._pos} in {self._text!r}"
            )
        self._pos += 1

    def _number(self) -> float:
        self._skip_ws()
        start = self._pos
        while self._pos < self._len and (
            self._text[self._pos] in "+-.eE0123456789"
        ):
            self._pos += 1
        token = self._text[start:self._pos]
        if not token:
            raise WKTError(f"expected a number at position {self._pos}")
        try:
            return float(token)
        except ValueError as exc:  # pragma: no cover - defensive
            raise WKTError(f"invalid number {token!r}") from exc

    def expect_end(self) -> None:
        """Assert the whole string was consumed (only trailing whitespace)."""
        self._skip_ws()
        if self._pos != self._len:
            raise WKTError(f"trailing text at position {self._pos}")

    # -- Grammar -----------------------------------------------------------

    def parse_geometry(self) -> dict[str, Any]:
        tag = self._word()
        if tag not in _TYPES:
            raise WKTError(f"unknown geometry type {tag!r}")
        gtype = _TYPES[tag]
        dim = self._dimensionality()
        if self._peek_word_is_empty():
            self._word()  # consume EMPTY
            if gtype == "GeometryCollection":
                return {"type": gtype, "geometries": []}
            return {"type": gtype, "coordinates": []}

        coords: Any
        if gtype == "Point":
            coords = self._point_body(dim)
        elif gtype == "LineString":
            coords = self._point_list(dim)
        elif gtype == "Polygon":
            coords = self._ring_list(dim)
        elif gtype == "MultiPoint":
            coords = self._multipoint_body(dim)
        elif gtype == "MultiLineString":
            coords = self._ring_list(dim)
        elif gtype == "MultiPolygon":
            coords = self._polygon_list(dim)
        else:  # GeometryCollection
            return {"type": gtype, "geometries": self._geometry_list()}
        return {"type": gtype, "coordinates": coords}

    def _dimensionality(self) -> int:
        """Read an optional Z / M / ZM tag; return ordinate count (2 or 3)."""
        save = self._pos
        tag = self._word()
        if tag in ("Z", "M", "ZM"):
            if "M" in tag:
                raise NotImplementedError(
                    "measured (M/ZM) WKT geometries are not yet modelled"
                )
            return 3  # Z
        # Not a dimensionality tag: rewind.
        self._pos = save
        return 2

    def _peek_word_is_empty(self) -> bool:
        save = self._pos
        word = self._word()
        self._pos = save
        return word == "EMPTY"

    def _coord(self, dim: int) -> list[float]:
        vals = [self._number() for _ in range(dim)]
        return vals

    def _point_body(self, dim: int) -> list[float]:
        self._consume("(")
        c = self._coord(dim)
        self._consume(")")
        return c

    def _point_list(self, dim: int) -> list[list[float]]:
        self._consume("(")
        pts = [self._coord(dim)]
        while self._peek() == ",":
            self._consume(",")
            pts.append(self._coord(dim))
        self._consume(")")
        return pts

    def _multipoint_body(self, dim: int) -> list[list[float]]:
        # Two accepted forms: MULTIPOINT (1 2, 3 4) and
        # MULTIPOINT ((1 2), (3 4)).
        self._consume("(")
        pts: list[list[float]] = []
        while True:
            if self._peek() == "(":
                self._consume("(")
                pts.append(self._coord(dim))
                self._consume(")")
            else:
                pts.append(self._coord(dim))
            if self._peek() == ",":
                self._consume(",")
                continue
            break
        self._consume(")")
        return pts

    def _ring_list(self, dim: int) -> list[list[list[float]]]:
        # Polygon / MultiLineString: a list of point-lists.
        self._consume("(")
        rings = [self._point_list(dim)]
        while self._peek() == ",":
            self._consume(",")
            rings.append(self._point_list(dim))
        self._consume(")")
        return rings

    def _polygon_list(self, dim: int) -> list[list[list[list[float]]]]:
        self._consume("(")
        polys = [self._ring_list(dim)]
        while self._peek() == ",":
            self._consume(",")
            polys.append(self._ring_list(dim))
        self._consume(")")
        return polys

    def _geometry_list(self) -> list[dict[str, Any]]:
        self._consume("(")
        geoms = [self.parse_geometry()]
        while self._peek() == ",":
            self._consume(",")
            geoms.append(self.parse_geometry())
        self._consume(")")
        return geoms


# =============================================================================
# Writer
# =============================================================================

def _fmt(value: float, precision: int | None) -> str:
    if precision is not None:
        return f"{value:.{precision}f}"
    # Lossless, but drop the trailing ".0" on integral values so
    # "POINT (30 10)" round-trips to itself rather than "POINT (30.0 10.0)".
    f = float(value)
    if f.is_integer():
        return str(int(f))
    return repr(f)


def _fmt_coord(coord: list[float], precision: int | None) -> str:
    return " ".join(_fmt(v, precision) for v in coord)


def _fmt_point_list(points: list[list[float]], precision: int | None) -> str:
    return "(" + ", ".join(_fmt_coord(p, precision) for p in points) + ")"


def _fmt_ring_list(rings, precision: int | None) -> str:
    return "(" + ", ".join(_fmt_point_list(r, precision) for r in rings) + ")"


def _dim_tag(coords: list) -> str:
    """The ' Z' tag when the first ordinate tuple has three components."""
    first = coords
    while isinstance(first, list) and first and isinstance(first[0], list):
        first = first[0]
    if isinstance(first, list) and len(first) == 3:
        return " Z "
    return " "


def _dump_geometry(geom: dict[str, Any], precision: int | None) -> str:
    gtype = geom.get("type")
    if gtype == "GeometryCollection":
        geoms = geom.get("geometries", [])
        if not geoms:
            return "GEOMETRYCOLLECTION EMPTY"
        inner = ", ".join(_dump_geometry(g, precision) for g in geoms)
        return f"GEOMETRYCOLLECTION ({inner})"

    coords = geom.get("coordinates", [])
    tag = {
        "Point": "POINT",
        "LineString": "LINESTRING",
        "Polygon": "POLYGON",
        "MultiPoint": "MULTIPOINT",
        "MultiLineString": "MULTILINESTRING",
        "MultiPolygon": "MULTIPOLYGON",
    }.get(gtype)
    if tag is None:
        raise WKTError(f"cannot serialise geometry type {gtype!r}")
    if not coords:
        return f"{tag} EMPTY"

    z = _dim_tag(coords)  # " " or " Z "

    if gtype == "Point":
        body = "(" + _fmt_coord(coords, precision) + ")"
    elif gtype in ("LineString", "MultiPoint"):
        body = _fmt_point_list(coords, precision)
    elif gtype in ("Polygon", "MultiLineString"):
        body = _fmt_ring_list(coords, precision)
    else:  # MultiPolygon
        body = "(" + ", ".join(
            _fmt_ring_list(poly, precision) for poly in coords
        ) + ")"
    return f"{tag}{z}{body}".replace("  ", " ")

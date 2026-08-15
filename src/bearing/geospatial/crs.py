# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Kockums Bearing - Coordinate Reference System
=============================================

A dependency-free :class:`CRS` — a Coordinate Reference System *identity*
and parser. It recognises the OGC URN form
(``urn:ogc:def:crs:EPSG::4326``), the legacy forms (``EPSG:4326``,
``http://www.opengis.net/def/crs/EPSG/0/4326``), and a bare numeric SRID,
and exposes the canonical ``srid`` / ``authority`` / ``urn`` / ``legacy``
identity plus the CRS84-vs-EPSG:4326 axis-order distinction.

What it deliberately does **not** do is *reproject* coordinates: arbitrary
datum/projection transforms need a PROJ/EPSG database, which is not
stdlib-doable. That work is delegated — Web Mercator lives in
:mod:`bearing.projection`, geodesy in :mod:`bearing.geodesy`, and arbitrary
EPSG transforms belong downstream in ``ortha`` (per the dependency
doctrine). Merging the former Django/GDAL-backed ``CRS`` down to this pure
identity is what lets ``import bearing`` stay dependency-free.

References
----------
- OGC URN policy, http://www.opengeospatial.org/ogcUrnPolicy
- CRS-parsing logic after wglas85/django-wfs (Apache-2.0), re-authored pure.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
import re
from dataclasses import dataclass, field

# Import | Local Modules
from bearing.exceptions import ExternalValueError


# =============================================================================
# Grammar
# =============================================================================

CRS_URN_REGEX = re.compile(
    r"^urn:(?P<domain>[a-z]+)"
    r":def:crs:(?P<authority>[a-z]+)"
    r":(?P<version>[0-9]+\.[0-9]+(\.[0-9]+)?)?"
    r":(?P<id>[0-9]+|crs84)"
    r"$",
    re.IGNORECASE,
)

_LEGACY_HEADS = (
    "epsg:",
    "http://www.opengis.net/def/crs/epsg/0/",
    "http://www.opengis.net/gml/srs/epsg.xml#",
)


# =============================================================================
# Class
# =============================================================================

@dataclass(frozen=True)
class CRS:
    """
    A Coordinate Reference System identity, preferably in OGC URN form.

    Attributes
    ----------
    domain : str
        ``"ogc"`` (recommended) or ``"opengis"``.
    authority : str
        ``"EPSG"`` or ``"OGC"``.
    version : str
        The authority registry version — usually empty (e.g. WFS 2.0).
    crsid : str
        The reference id: ``"CRS84"`` for OGC, else the numeric SRID string.
    srid : int
        The numeric spatial reference id (EPSG code).
    origin : str
        The original input string that produced this CRS.
    """

    domain: str
    authority: str
    version: str
    crsid: str
    srid: int
    origin: str = field(default="", compare=False)

    # -- Constructors ------------------------------------------------------

    @classmethod
    def from_string(cls, uri: str | int) -> "CRS":
        """
        Parse a CRS from a URN, a legacy URI (``EPSG:<srid>`` / OpenGIS URL),
        or a bare numeric SRID.

        Raises
        ------
        ExternalValueError
            If the URI is not a recognised CRS reference.
        """
        if isinstance(uri, int) or (isinstance(uri, str) and uri.isdigit()):
            return cls.from_srid(int(uri))
        text = str(uri)
        if text.startswith("urn:"):
            return cls._from_urn(text)
        return cls._from_legacy(text)

    @classmethod
    def from_srid(cls, srid: int) -> "CRS":
        """
        Build a CRS from a numeric EPSG SRID — equivalent to
        ``from_string("urn:ogc:def:crs:EPSG::<srid>")``.
        """
        return cls(
            domain="ogc",
            authority="EPSG",
            version="",
            crsid=str(int(srid)),
            srid=int(srid),
            origin=str(srid),
        )

    @classmethod
    def _from_urn(cls, urn: str) -> "CRS":
        match = CRS_URN_REGEX.match(urn)
        if not match:
            raise ExternalValueError(
                f"Unknown CRS URN [{urn}] specified: {CRS_URN_REGEX.pattern}"
            )
        domain = match.group("domain").lower()
        authority = match.group("authority").upper()
        if domain not in ("ogc", "opengis"):
            raise ExternalValueError(
                f"CRS URI [{urn}] contains unknown domain [{domain}]"
            )
        if authority == "EPSG":
            crsid = match.group("id")
            try:
                srid = int(crsid)
            except ValueError:
                raise ExternalValueError(
                    f"CRS URI [{urn}] should contain a numeric SRID value."
                ) from None
        elif authority == "OGC":
            crsid = match.group("id").upper()
            if crsid != "CRS84":
                raise ExternalValueError(
                    f"OGC CRS URI [{urn}] contains unknown id [{crsid}]"
                )
            srid = 4326
        else:
            raise ExternalValueError(
                f"CRS URI [{urn}] contains unknown authority [{authority}]"
            )
        return cls(
            domain=domain,
            authority=authority,
            version=match.group("version") or "",
            crsid=crsid,
            srid=srid,
            origin=urn,
        )

    @classmethod
    def _from_legacy(cls, uri: str) -> "CRS":
        lowered = uri.lower()
        for head in _LEGACY_HEADS:
            if lowered.startswith(head):
                crsid = lowered[len(head):]
                try:
                    srid = int(crsid)
                except ValueError:
                    raise ExternalValueError(
                        f"CRS URI [{uri}] should contain a numeric SRID value."
                    ) from None
                return cls(
                    domain="ogc",
                    authority="EPSG",
                    version="",
                    crsid=crsid,
                    srid=srid,
                    origin=uri,
                )
        raise ExternalValueError(f"Unknown CRS URI [{uri}] specified")

    # -- Identity ----------------------------------------------------------

    @property
    def legacy(self) -> str:
        """The legacy ``"EPSG:<srid>"`` string."""
        return f"EPSG:{self.srid:d}"

    @property
    def urn(self) -> str:
        """The canonical OGC URN for this CRS."""
        return (
            f"urn:{self.domain}:def:crs:{self.authority}"
            f":{self.version or ''}:{self.crsid}"
        )

    @property
    def is_geographic(self) -> bool:
        """
        Whether this is a geographic (lon/lat degrees) CRS — WGS84 in either
        axis order (EPSG:4326 or OGC:CRS84).
        """
        return self.srid == 4326

    @property
    def is_yx_order(self) -> bool:
        """
        Whether the authority defines **lat, lon** (y, x) axis order.
        EPSG:4326 is lat/long; OGC CRS84 is long/lat. This is the distinction
        that makes ``EPSG:4326 != CRS84`` even though both are WGS84.
        """
        return self.authority == "EPSG" and self.srid == 4326

    def __str__(self) -> str:
        return self.urn

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CRS):
            # CRS84 is NOT equivalent to EPSG:4326: same datum, opposite axis
            # order, so the authority must match too.
            return self.authority == other.authority and self.srid == other.srid
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.authority, self.srid))

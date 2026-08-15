# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Kockums Bearing - Vector Layer
==============================

A :class:`VectorLayer` — the metadata of one named layer in a vector-tile
set: its id, description, and the zoom range over which it is visible. Pure
data, no dependencies.

The heavy machinery that *serves* vector tiles (querysets, Mapbox protobuf
encoding) is a pipeline concern and lives downstream in ``ortha``; this is
just the portable descriptor those pipelines carry.

References
----------
- The layer descriptor shape follows the Mapbox Vector Tile spec's
  ``layers`` metadata and django-vectortiles' layer definition.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations


# =============================================================================
# Class
# =============================================================================

class VectorLayer:
    """
    A vector-tile layer descriptor.

    Attributes
    ----------
    id : str
        Unique identifier for the layer.
    description : str
        Human-readable description.
    min_zoom : int
        Lowest zoom at which the layer is drawn.
    max_zoom : int
        Highest zoom at which the layer is drawn.
    """

    def __init__(
        self,
        id: str,
        description: str = "",
        min_zoom: int = 0,
        max_zoom: int = 22,
    ) -> None:
        """Initialise a vector layer descriptor."""
        self.id = id
        self.description = description
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom

    def as_dict(self) -> dict:
        """
        The descriptor as a plain dict — the ``layers`` entry a tile-set
        manifest or ``TileJSON`` document carries.
        """
        return {
            "id": self.id,
            "description": self.description,
            "fields": {},  # populated by the serving layer downstream
            "minzoom": self.min_zoom,
            "maxzoom": self.max_zoom,
        }

    def __repr__(self) -> str:
        return (
            f"VectorLayer(id={self.id!r}, "
            f"min_zoom={self.min_zoom}, max_zoom={self.max_zoom})"
        )

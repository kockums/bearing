# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Vector Tile Class
==========================

A class to handle vector tile generation for web mapping applications.

Links:
- https://github.com/submarcos/django-vectortiles/

"""


# =============================================================================
# Import
# =============================================================================

# Import | Standard Library
from typing import Tuple, Optional, Any

# Import | Libraries
import mercantile


# =============================================================================
# Classes
# =============================================================================

class VectorTile(object):
    """
    Vector Tile Class
    ==================

    Base Mixin class to handle vector tile generation. This class can be
    extended to generate vector tiles with specific data and styles.

    Attributes:
        vector_tile_content_type (str): The MIME type for vector tiles.
        vector_tile_queryset (QuerySet): The queryset to be used for
            generating tiles.
        vector_tile_queryset_limit (int): Limit for the number of features
            per tile.
        vector_tile_layer_name (str): Name for the data layer in the
            vector tile.
        vector_tile_geom_name (str): The geometry field name in the queryset.
        vector_tile_fields (list): Additional fields to include from the
            queryset.
        vector_tile_generation (callable): Function to generate vector tiles.
        vector_tile_extent (int): Tile extent.
        vector_tile_buffer (int): Buffer around tiles.
        vector_tile_clip_geom (bool): Whether to clip feature geometries in
            the tile.

    """

    vector_tile_content_type: str = "application/x-protobuf"
    vector_tile_queryset: Optional[Any] = None
    vector_tile_queryset_limit: Optional[int] = None
    # name for data layer in vector tile
    vector_tile_layer_name: Optional[str] = None
    # geom field to consider in qs
    vector_tile_geom_name: str = "geom"
    # other fields to include from qs
    vector_tile_fields: Optional[list] = None
    # use mapbox if you installed [mapbox] sub-dependencies
    vector_tile_generation: Optional[callable] = None
    # define tile extent
    vector_tile_extent: int = 4096
    # define buffer around tiles (intersected polygon display without borders)
    vector_tile_buffer: int = 256
    # define if feature geometries should be clipped in tile
    vector_tile_clip_geom: bool = True

    @classmethod
    def get_bounds(
        cls, x: int, y: int, z: int
    ) -> Tuple[float, float, float, float]:
        """
        Get extent from XYZ tile coordinates to EPSG:3857.

        Args:
            x (int): Tile X coordinate (longitude).
            y (int): Tile Y coordinate (latitude).
            z (int): Tile zoom level.

        Returns:
            Tuple[float, float, float, float]: The tile bounds (xmin, ymin,
            xmax, ymax) in EPSG:3857.
        """
        return mercantile.xy_bounds(x, y, z)

    def get_vector_tile_queryset(self) -> Any:
        """
        Get the feature queryset for the tile dynamically.

        Returns:
            QuerySet: The queryset used for generating the tile.
        """
        return self.vector_tile_queryset if self.vector_tile_queryset is not None else self.get_queryset()  # noqa E501

    def get_vector_tile_queryset_limit(self) -> Optional[int]:
        """
        Get the feature limit per tile dynamically.

        Returns:
            Optional[int]: The feature limit per tile.
        """
        return self.vector_tile_queryset_limit

    def get_vector_tile_layer_name(self) -> Optional[str]:
        """
        Get the layer name in the tile dynamically.

        Returns:
            Optional[str]: The layer name in the tile.
        """
        return self.vector_tile_layer_name

    def get_tile(self, x: int, y: int, z: int) -> bytearray:
        """
        Generate a mapbox vector tile as bytearray.

        Args:
            x (int): Tile X coordinate (longitude).
            y (int): Tile Y coordinate (latitude).
            z (int): Tile zoom level.

        Returns:
            bytearray: The generated mapbox vector tile.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError(
            "Subclasses must implement the get_tile method"
        )

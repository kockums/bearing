# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Vector Layer Class
=====================================

Class for representing vector layers in a map, typically used in web mapping
applications.

Todo:
- Implement additional methods or attributes as needed.
- Extend layer fields customization.

Links:
- https://github.com/submarcos/django-vectortiles/

"""


# =============================================================================
# Import
# =============================================================================

# Import | Standard Library

# Import | Libraries


# =============================================================================
# Classes
# =============================================================================

class VectorLayer(object):
    """
    Vector Layer Class
    ==================

    Represents a vector layer with its associated properties and metadata.

    Attributes:
        vector_tile_layer_id (str): Unique identifier for the vector layer.
        vector_tile_layer_description (str): Description of the vector layer.
        vector_tile_layer_min_zoom (int): Minimum zoom level at which the
            layer is visible.
        vector_tile_layer_max_zoom (int): Maximum zoom level at which
            the layer is visible.
    """

    # vector_tile_layer_id = ""
    # vector_tile_layer_description = ""
    # vector_tile_layer_min_zoom = 0
    # vector_tile_layer_max_zoom = 22

    def __init__(
        self,
        id_layer: str,
        description: str = "",
        min_zoom: int = 0,
        max_zoom: int = 22
    ):
        """
        Initializes a new instance of the VectorLayer class.

        Args:
            id_layer (str): Unique identifier for the vector layer.
            description (str): A brief description of the vector layer.
            min_zoom (int): Minimum zoom level at which the layer is visible.
            max_zoom (int): Maximum zoom level at which the layer is visible.
        """
        self.vector_tile_layer_id = id_layer
        self.vector_tile_layer_description = description
        self.vector_tile_layer_min_zoom = min_zoom
        self.vector_tile_layer_max_zoom = max_zoom

    def get_vector_tile_layer_id(self) -> str:
        """
        Retrieves the unique identifier of the vector layer.

        Returns:
            str: The unique identifier of the layer.
        """
        return self.vector_tile_layer_id

    def get_vector_tile_layer_description(self) -> str:
        """
        Retrieves the description of the vector layer.

        Returns:
            str: The description of the layer.
        """
        return self.vector_tile_layer_description

    def get_vector_tile_layer_min_zoom(self) -> int:
        """
        Retrieves the minimum zoom level at which the layer is visible.

        Returns:
            int: The minimum zoom level for the layer.
        """
        return self.vector_tile_layer_min_zoom

    def get_vector_tile_layer_max_zoom(self) -> int:
        """
        Retrieves the maximum zoom level at which the layer is visible.

        Returns:
            int: The maximum zoom level for the layer.
        """
        return self.vector_tile_layer_max_zoom

    def get_vector_layer(self) -> dict:
        """
        Constructs and returns a dictionary representing the vector layer.

        Returns:
            dict: A dictionary containing the layer's properties.
        """
        return {
            "id": self.get_vector_tile_layer_id(),
            "description": self.get_vector_tile_layer_description(),
            # Placeholder for layer fields, extend as needed.
            "fields": {},  # self.layer_fields(layer),
            "minzoom": self.get_vector_tile_layer_min_zoom(),
            "maxzoom": self.get_vector_tile_layer_max_zoom(),
        }

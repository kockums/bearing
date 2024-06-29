# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Grid Cell Class
========================


"""


# =============================================================================
# Import
# =============================================================================

# Import | Standard Library
from typing import Any, Iterator, List, Optional, Tuple
import copy

# Import | Libraries
import numpy as np


# Import | Local Modules
from .cell_base import Cell


# =============================================================================
# Classes
# =============================================================================

class GridCell(Cell):
    """
    Grid Cell Class
    ==========

    Represents a cell within a multi-dimensional grid, extending the generic
    Cell class with positional information.

    Each cell holds a data and optional meta. The cell's position is
    represented as a list of integers, allowing for flexibility in grid
    dimensions.

    The position of the cell is immutable once set, ensuring consistent
    referencing within the grid.
    The data and meta are mutable, allowing dynamic updates during
    the cell's lifecycle.


    Attributes
    ----------
    _position (List[int]): The cell's coordinates within the grid.

    Methods
    -------
    position: Property to get the cell's position.

    """

    # Constructor
    # =========================================================================

    def __init__(
        self,
        position: List[int],
        data: Any = None,
        meta: dict = None
    ):
        """
        Initializes a new GridCell instance with position, data, and meta.

        Parameters
        ----------
        position: A list of integers representing the cell's coordinates
            in the grid.
        data: Inherits the data attribute from the Cell class.
        meta: Inherits the meta attribute from the Cell class.

        """
        super().__init__(data, meta)
        self._position = position
        # Using a tuple to enforce immutability
        # self._position = tuple(position)

    # Properties
    # =========================================================================

    @property
    def position(self) -> Tuple[int]:
        """
        Returns the cell's immutable position.

        """
        return self._position

    @position.setter
    def position(self, new_position: List[int]) -> None:
        """
        Sets the cell's position. Ensure new_position is a list of integers.

        """
        if not all(isinstance(coord, int) for coord in new_position):
            raise ValueError("Position must be a list of integers.")
        self._position = new_position

    @position.deleter
    def position(self) -> None:
        """
        Resets the cell's position. Not typically used but included
        for completeness.

        """
        # Reset to origin based on the current dimensionality
        self._position = [0] * len(self._position)

    # Magic Methods
    # =========================================================================

    def __repr__(self) -> str:
        """
        Returns an official string representation of the GridCell.

        """
        return f"GridCell(position={self.position}, data={repr(self.data)}, meta={repr(self.meta)})"  # noqa E501

    # Public Methods
    # =========================================================================

    def get_neighbor_positions(
        self, include_diagonals=False
    ) -> List[Tuple[int]]:
        """
        Calculates the positions of adjacent neighbors in the grid.

        Parameters
        ----------
        include_diagonals: Determines whether diagonal neighbors should
            be included. Defaults to False.

        Returns
        -------
        A list of tuples representing the positions of adjacent neighbor cells.

        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if include_diagonals:
            directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        neighbors = [
            (
                self.position[0] + dx, self.position[1] + dy
            ) for dx, dy in directions
        ]
        return neighbors

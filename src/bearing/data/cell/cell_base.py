# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Cell Class
===================


"""


# =============================================================================
# Import
# =============================================================================

# Import | Standard Library
from typing import Any, Dict, List, Iterator, Optional, Tuple
import copy

# Import | Libraries
import numpy as np

# Import | Local Modules
from data import Data
from meta import Metadata


# =============================================================================
# Classes
# =============================================================================

class Cell:
    """
    Cell Class
    ==========

    Represents a cell that can store data and associated metadata, suitable
    for various applications.


    This class provides a structured way to encapsulate a piece of data along
    with its metadata within a cell-like structure, making it a versatile
    component for data grids, spreadsheets, simulations, and more complex
    data structures.


    The data and meta are mutable, allowing dynamic updates during
    the cell's lifecycle.

    Attributes:
    _data (Data): The primary content of the cell, encapsulated in a
        Data instance.
    _meta (Metadata): The metadata of the cell, encapsulated in a
        Metadata instance.

    Methods:
    data: Property to get, set, or delete the cell's primary content.
    meta: Property to get, set, or delete the cell's metadata.
    update_meta: Incorporates new key-value pairs into the cell's
        existing metadata.
    validate_meta: Placeholder for a method to validate the cell's
        metadata against a provided schema.

    """

    # Constructor
    # =========================================================================

    def __init__(self, data: Any = None, meta: Dict[str, Any] = None):
        """
        Initializes a new Cell instance with data and metadata.

        Parameters
        ----------
        data: The initial content of the cell.
        meta: A dictionary containing initial metadata key-value pairs.

        """
        self._data = Data(data)
        self._meta = Metadata(meta)

    # Properties
    # =========================================================================

    # Property | Data
    # -------------------------------------------------------------------------

    @property
    def data(self) -> Data:
        """
        Returns the cell's data.

        """
        return self._data

    def data(self, new_data: Any):
        """
        Updates the cell's data. Custom validation can be added here.

        """
        self._data.value = new_data

    @data.deleter
    def data(self) -> None:
        """
        Resets the cell's data to its default state (None).

        """
        self._data = None

    # Property | Meta
    # -------------------------------------------------------------------------

    @property
    def meta(self) -> Metadata:
        """
        Returns the cell's meta.

        """
        return self._meta

    @meta.setter
    def meta(self, new_meta: Dict[str, Any]):
        """
        Updates the cell's meta.

        """
        self._meta.value = new_meta

    @meta.deleter
    def meta(self) -> None:
        """
        Clears the cell's meta, resetting it to an empty dictionary.

        """
        self._meta = {}

    # Magic Methods
    # =========================================================================

    def __str__(self) -> str:
        """
        Returns a string representation of the Cell's data and metadata for
        easy display purposes.

        """
        return f"Cell(data={str(self._data)}, meta={str(self._meta)})"

    def __repr__(self) -> str:
        """
        Returns an official string representation of the Cell instance.

        """
        return f"Cell(data={repr(self._data)}, meta={repr(self._meta)})"

    # Public Methods
    # =========================================================================

    def copy(self, deep: bool = False) -> 'Cell':
        """
        Creates a copy of the cell, with an option for a deep copy.

        Parameters
        ----------
        deep: If True, performs a deep copy of the cell, including its
            data and metadata.

        Returns
        -------
        A new Cell instance that is a copy of this cell.

        """
        return Cell(
            data=self._data.clone(deep=deep).value,
            meta=self._meta.clone(deep=deep).value
        )
